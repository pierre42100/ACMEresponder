"""
Random utilities
"""

import string
import random


def get_random_string(length: int) -> str:
    """
    Generate a random string

    :param length: The length of the generated string
    :return: The generated string
    """
    return "".join(random.choice(string.ascii_letters) for i in range(length))
