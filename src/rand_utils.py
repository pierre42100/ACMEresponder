import string
import random

def get_random_string(length: int):
    """
    Generate a random string
    """
    return ''.join(random.choice(string.ascii_letters) for i in range(length))
