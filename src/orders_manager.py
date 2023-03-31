"""
Manages orders, challenges request
"""
import time
from src.config import settings
from src.rand_utils import get_random_string
import datetime


class OrderDomain:
    """
    Information about a single domain
    """

    def __init__(self, domain: str):
        self.id = get_random_string(10)
        self.domain = domain
        self.full_filled = False


class Order:
    def __init__(self, domains: list[str]):
        """
        Contains orders information
        """
        self.id = get_random_string(10)
        self.expire = time.time() + settings.order_lifetime
        self.not_before = time.time()
        self.not_after = time.time() + settings.certs_duration
        self.domains = list(map(lambda d: OrderDomain(d), domains))

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

    def status(self):
        """
        Give output information returned to the client
        """
        return {
            "status": "ready" if self.is_full_filled() else "pending",
            "expires": datetime.datetime.fromtimestamp(self.expire).isoformat(),
            "notBefore": datetime.datetime.fromtimestamp(self.not_before).isoformat(),
            "notAfter": datetime.datetime.fromtimestamp(self.not_after).isoformat(),
            "identifiers": list(
                map(lambda d: {"type": "dns", "value": d.domain}, self.domains)
            ),
            "authorizations": list(
                map(lambda d: f"{settings.domain_uri}/acme/authz/{d.id}", self.domains)
            ),
            "finalize": f"{settings.domain_uri}/acme/order/{self.id}/finalize",
        }


ORDERS: list[Order] = []


class OrdersManager:
    """
    Orders manager
    """

    @staticmethod
    def create(domains: list[str]) -> Order:
        """
        Create a new order
        """
        global ORDERS
        order = Order(domains=domains)
        ORDERS = list(filter(lambda o: not o.is_expired(), ORDERS))
        ORDERS.append(order)
        return order
