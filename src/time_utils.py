"""
Time utilities
"""
import datetime


def fmt_time(t: int) -> str:
    """
    Format time in standard format
    """
    return datetime.datetime.fromtimestamp(t).isoformat()
