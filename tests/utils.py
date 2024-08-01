import datetime
from typing import Any


def generate_datetime_list(
    *,
    n: int = 10,
    tz: Any = None,  # noqa: ANN401
) -> list[datetime.datetime]:
    """Generate list of datetimes of given length with or without timezone."""
    now = datetime.datetime.now(tz=tz)
    res = [now]
    for i in range(1, n):
        delta = datetime.timedelta(days=i)
        res.append(now + delta)
    return res
