"""
Manages orders, challenges request
"""
import json
import time
from hashlib import sha256
import requests

from src.base64_utils import safe_base64_decode, safe_base64_encode
from src.config import settings
from src.rand_utils import get_random_string
from src.time_utils import fmt_time
from src.x509 import X509


class OrderException(Exception):
    """
    Exception that occurred during orders processing
    """


class OrderDomain:
    """
    Information about a single domain
    """

    def __init__(self, domain: str, expire: int):
        self.id = get_random_string(10)
        self.domain = domain
        self.expire = expire
        self.full_filled = False
        self.http_challenge_id = get_random_string(10)
        self.http_challenge_token = get_random_string(20)

    def is_expired(self) -> bool:
        """
        Check if the order is expired
        """
        return self.expire < time.time()

    def http_challenge_url(self) -> str:
        """
        Get the URL where a challenge must be checked
        """
        return f"http://{self.domain}:{settings.http_challenge_port}/.well-known/acme-challenge/{self.http_challenge_token}"

    def check_http_challenge(self, account_jwk) -> bool:
        """
        Attempt to validate the HTTP challenge

        :param account_jwk: The JWK of the account making the request
        :return: True if the JWK is valid, false otherwise
        """

        if self.is_expired():
            raise OrderException(
                "Can not check an HTTP challenge for an expired order!"
            )

        response = requests.get(
            self.http_challenge_url(), allow_redirects=True, timeout=10
        )

        if response.status_code != 200:
            return False

        acme_header_jwk_json = json.dumps(
            account_jwk, sort_keys=True, separators=(",", ":")
        )
        acme_thumbprint = safe_base64_encode(
            sha256(acme_header_jwk_json.encode("utf8")).digest()
        )
        acme_keyauthorization = f"{self.http_challenge_token}.{acme_thumbprint}"

        if acme_keyauthorization != response.text:
            return False

        self.full_filled = True
        return True

    def status(self) -> str:
        """
        Get domain status, as text
        """
        if self.full_filled:
            return "valid"
        return "pending"

    def info(self):
        """
        Give output information returned to the client
        """
        return {
            "status": self.status(),
            "expires": fmt_time(self.expire),
            "identifier": {"type": "dns", "value": self.domain},
            "challenges": [
                {
                    "type": "http-01",
                    "url": f"{settings.domain_uri}/acme/chall/{self.http_challenge_id}",
                    "token": self.http_challenge_token,
                }
            ],
        }


class Order:
    """
    Contains orders information
    """

    def __init__(self, domains: list[str], account_id: str):
        """
        Initialize a new order

        :param domains: The domains to include in the certificate
        :param account_id: The ID of the target account
        """
        self.id = get_random_string(10)
        self.account_id = account_id
        self.expire = time.time() + settings.order_lifetime
        self.not_before = time.time()
        self.not_after = time.time() + settings.certs_duration
        self.domains = list(map(lambda d: OrderDomain(d, expire=self.expire), domains))
        self.crt = None
        self.cert_id = None

    def is_expired(self) -> bool:
        """
        Check if the order is expired
        """
        return self.expire < time.time()

    def is_full_filled(self) -> bool:
        """
        Check if all requirements of the order were full_filled
        """
        return all(x.full_filled for x in self.domains) and not self.is_expired()

    def sign_csr(self, csr: str):
        """
        Sign the CSR of a client, if possible

        :param csr: The CSR to sign
        """
        if self.crt is not None:
            raise OrderException("A certificate has already been issued!")

        if not self.is_full_filled():
            raise OrderException("The client did not comply with all requirements!")

        decoded_csr = safe_base64_decode(csr)
        domains = list(map(lambda d: d.domain, self.domains))
        X509.check_csr(csrb=decoded_csr, domains=domains)

        self.crt = X509.sign_csr(
            ca_privkey=settings.ca_get_keyfile(),
            ca_pubkey=settings.ca_get_certfile(),
            csr=decoded_csr,
            domains=domains,
            not_before=self.not_before,
            not_after=self.not_after,
        )
        self.cert_id = get_random_string(10)

    def url(self) -> str:
        """
        Get order URL
        """
        return f"{settings.domain_uri}/acme/order/{self.id}"

    def status(self) -> str:
        """
        Get current order status, as text

        This method is used in the `info` method of this object
        """
        if self.crt is not None:
            return "valid"
        if self.is_full_filled():
            return "ready"
        return "pending"

    def info(self):
        """
        Give output information returned to the client
        """
        status = {
            "status": self.status(),
            "expires": fmt_time(self.expire),
            "notBefore": fmt_time(self.not_before),
            "notAfter": fmt_time(self.not_after),
            "identifiers": list(
                map(lambda d: {"type": "dns", "value": d.domain}, self.domains)
            ),
            "authorizations": list(
                map(lambda d: f"{settings.domain_uri}/acme/authz/{d.id}", self.domains)
            ),
            "finalize": f"{settings.domain_uri}/acme/order/{self.id}/finalize",
        }

        if self.cert_id is not None:
            status["certificate"] = f"{settings.domain_uri}/acme/cert/{self.cert_id}"

        return status


class OrdersManager:
    """
    Orders manager
    """

    ORDERS: list[Order] = []

    @staticmethod
    def cleanupOldOrders():
        """
        Remove outdated orders from the list
        """
        OrdersManager.ORDERS = list(
            filter(lambda x: not x.is_expired(), OrdersManager.ORDERS)
        )

    @staticmethod
    def create(account_id: str, domains: list[str]) -> Order:
        """
        Create a new order

        :param account_id: The ID of the target account
        :param domains: The domains included in the request
        :return: The created order
        """
        order = Order(domains=domains, account_id=account_id)
        OrdersManager.cleanupOldOrders()
        OrdersManager.ORDERS.append(order)
        return order

    @staticmethod
    def find_order_by_id(account_id: str, order_id: str) -> Order:
        """
        Find an order by its id

        :param account_id: The ID of the account making the request
        :param order_id: The ID of the target order
        :return: Information about the order
        """

        return next(
            filter(
                lambda x: x.account_id == account_id and x.id == order_id,
                OrdersManager.ORDERS,
            )
        )

    @staticmethod
    def find_order_by_cert_id(account_id: str, cert_id: str) -> Order:
        """
        Find an order by certificates id

        :param account_id: The ID of the account making the request
        :param cert_id: The ID of the certificate
        :return: Information about the order
        """

        return next(
            filter(
                lambda x: x.account_id == account_id and x.cert_id == cert_id,
                OrdersManager.ORDERS,
            )
        )

    @staticmethod
    def find_domain_by_authz_id(account_id: str, authz_id: str) -> OrderDomain:
        """
        Find an OrderDomain by its AuthzID

        :param account_id: The ID of the account making the request
        :param authz: The ID of the target authorization ID
        :return: Information about the domain order
        """

        for order in OrdersManager.ORDERS:
            if order.account_id != account_id:
                continue
            for domain in order.domains:
                if domain.id == authz_id:
                    return domain

        raise OrderException("Failed to find domain by its authz!")

    @staticmethod
    def find_domain_by_http_chall_id(account_id: str, chall_id: str) -> OrderDomain:
        """
        Find an OrderDomain by its HTTP Challenge ID

        :param account_id: The ID of the account making the request
        :param chall_id: The ID of the challenge
        :return: Information about the requested domain in the order
        """

        for order in OrdersManager.ORDERS:
            if order.account_id != account_id:
                continue
            for domain in order.domains:
                if domain.http_challenge_id == chall_id:
                    return domain

        raise OrderException("Failed to find domain by its challenge id!")
