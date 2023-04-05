"""
Random utilities
"""

import base64
import os


def get_random_string(length: int) -> str:
    """
    Generate a random string

    :param length: The length of the generated string
    :return: The generated string
    """
    return base64.b32encode(os.urandom(length))[:length].decode("utf-8")
