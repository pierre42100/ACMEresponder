"""
Random utilities
"""

import base64
import os


def get_random_bytes(length: int) -> bytes:
    """
    Generate random bytes

    :param length: The expected length of the output array
    :return: The generated bytes
    """
    return os.urandom(length)


def get_random_string(length: int) -> str:
    """
    Generate a random string

    :param length: The length of the generated string
    :return: The generated string
    """
    return base64.b32encode(os.urandom(length))[:length].decode("utf-8")
