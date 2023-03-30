import time
from src.rand_utils import get_random_string

class Nonce:
    def __init__(self):
        """
        Generate a new Nonce

        Nonce are valid for 1 hour
        """
        self.expire = time.time() + 3600
        self.nonce = get_random_string(15)

"""
The list of nonces
"""
NONCES: list[Nonce] = []


def cleanupOldNonces():
    """
    Remove outdated nonces from the list
    """
    global NONCES
    NONCES = list(filter(lambda x: time.time() < x.expire, NONCES))


def getNewNonce() -> str :
    """
    Generate & return a new nonce
    """
    cleanupOldNonces()
    n = Nonce()
    NONCES.append(n)
    return n.nonce


def consumeNonce(v: str):
    """
    Attempt to consume a nonce.

    If none are found, an error is thrown
    """
    for idx, n in enumerate(NONCES):
        if v == n.nonce:
            NONCES.pop(idx)
            return True
    return False
