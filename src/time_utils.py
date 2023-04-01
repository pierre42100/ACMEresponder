"""
Time utilities
"""
import datetime


def parse_unix_time(t: int) -> datetime.datetime:
    """
    Parse a UNIX time into a datetime
    """
    return datetime.datetime.fromtimestamp(t).replace(microsecond=0)

def fmt_time(t: int) -> str:
    """
    Format time in standard format
    """
    return datetime.datetime.fromtimestamp(t).isoformat()
