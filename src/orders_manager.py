"""
Manages orders, challenges request
"""
import json
import time
from src.accounts_manager import Account
from src.base64_utils import safe_base64_decode, safe_base64_encode
from src.config import settings
from src.rand_utils import get_random_string
from hashlib import sha256
import requests

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

    def http_challenge_url(self) -> str:
        """
        Get the URL where a challenge must be checked
        """
        return f"http://{self.domain}:{settings.http_challenge_port}/.well-known/acme-challenge/{self.http_challenge_token}"

    def check_http_challenge(self, account_jwk) -> bool:
        """
        Attempt to validate the HTTP challenge
        """
        response = requests.get(self.http_challenge_url(), allow_redirects=True)

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
    def __init__(self, domains: list[str], account_id: str):
        """
        Contains orders information
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
        return all(x.full_filled for x in self.domains)

    def sign_csr(self, csr: str):
        """
        Sign the CSR of a client, if possible
        """
        if self.crt is not None:
            raise OrderException("A certificate has already been issued!")

        if not self.is_full_filled():
            raise OrderException("The client did not comply with all requirements!")

        decoded_csr = safe_base64_decode(csr)
        domains = list(map(lambda d: d.domain, self.domains))
        X509.check_csr(csrb=decoded_csr, domains=domains)

        with open(settings.ca_keyfile(), "rb") as f:
            ca_privkey = f.read()

        with open(settings.ca_certfile(), "rb") as f:
            ca_pubkey = f.read()

        self.crt = X509.sign_csr(
            ca_privkey=ca_privkey,
            ca_pubkey=ca_pubkey,
            csr=decoded_csr,
            domains=domains,
            not_before=self.not_before,
            not_after=self.not_after,
        )
        self.cert_id = get_random_string(10)

    def url(self):
        """
        Get order URL
        """
        return f"{settings.domain_uri}/acme/order/{self.id}"

    def status(self) -> str:
        """
        Get current order status, as text
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


# TODO : cleanup old orders
ORDERS: list[Order] = []


class OrdersManager:
    """
    Orders manager
    """

    @staticmethod
    def create(account_id: str, domains: list[str]) -> Order:
        """
        Create a new order
        """
        global ORDERS
        order = Order(domains=domains, account_id=account_id)
        ORDERS = list(filter(lambda o: not o.is_expired(), ORDERS))
        ORDERS.append(order)
        return order

    @staticmethod
    def find_order_by_id(account_id: str, order_id: str) -> Order:
        """
        Find an order by its id
        """
        global ORDERS

        return next(
            filter(lambda x: x.account_id == account_id and x.id == order_id, ORDERS)
        )

    @staticmethod
    def find_domain_by_authz_id(account_id: str, authz_id: str) -> OrderDomain:
        """
        Find an OrderDomain by its AuthzID
        """
        global ORDERS

        for order in ORDERS:
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
        """
        global ORDERS

        for order in ORDERS:
            if order.account_id != account_id:
                continue
            for domain in order.domains:
                if domain.http_challenge_id == chall_id:
                    return domain

        raise OrderException("Failed to find domain by its challenge id!")
