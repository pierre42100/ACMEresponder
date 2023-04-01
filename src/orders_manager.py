"""
Manages orders, challenges request
"""
import time
from src.config import settings
from src.rand_utils import get_random_string
import datetime

from src.time_utils import fmt_time


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

    def url(self):
        """
        Get order URL
        """
        return f"{settings.domain_uri}/acme/order/{self.id}"

    def status(self) -> str:
        """
        Get current order status, as text
        """
        if self.is_full_filled():
            return "ready"
        return "pending"

    def info(self):
        """
        Give output information returned to the client
        """
        return {
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
    def find_by_authz_id(account_id: str, authz_id: str) -> OrderDomain:
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
