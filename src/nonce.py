"""
Nonces management
"""

import time
import threading
from src.rand_utils import get_random_string

lock = threading.Lock()


class Nonce:
    """
    This class hold a single nonce information
    """

    def __init__(self):
        """
        Generate a new Nonce

        Nonce are valid for 1 hour
        """
        self.expire = time.time() + 3600
        self.nonce = get_random_string(15)


class NoncesManager:
    """
    Helper class to manage nonces
    """

    NONCES: list[Nonce] = []

    @staticmethod
    def cleanupOldNonces():
        """
        Remove outdated nonces from the list
        """

        NoncesManager.NONCES = list(
            filter(lambda x: time.time() < x.expire, NoncesManager.NONCES)
        )

    @staticmethod
    def getNewNonce() -> str:
        """
        Generate & return a new nonce

        :return: The generated nonce
        """
        lock.acquire()
        NoncesManager.cleanupOldNonces()
        n = Nonce()
        NoncesManager.NONCES.append(n)
        lock.release()
        return n.nonce

    @staticmethod
    def consumeNonce(v: str):
        """
        Attempt to consume a nonce.

        If none are found, an error is thrown

        :param v: The nonce to consume
        """
        lock.acquire()
        for idx, n in enumerate(NoncesManager.NONCES):
            if v == n.nonce:
                NoncesManager.NONCES.pop(idx)
                lock.release()
                return True
        lock.release()
        return False
