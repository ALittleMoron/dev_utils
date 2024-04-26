"""Module with datetime core utils."""

import datetime


def get_utc_now() -> datetime.datetime:
    """Get current UTC datetime.

    Returns
    -------
        datetime: current datetime with UTC timezone.
    """
    return datetime.datetime.now(datetime.UTC)
