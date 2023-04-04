"""
Time utilities
"""
import datetime


def parse_unix_time(t: int) -> datetime.datetime:
    """
    Parse a UNIX time into a datetime.

    The microsecond is set to 0

    :param t: Unix timestamp to parse
    """
    return datetime.datetime.fromtimestamp(t).replace(microsecond=0)


def fmt_time(t: int) -> str:
    """
    Format time in standard RFC format

    :param t: Unix timestamp to parse
    :return: A string that can be send in response to
        client requests.
    """
    return datetime.datetime.fromtimestamp(t).isoformat()
