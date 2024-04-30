"""Module with getenv functions.

Basically, I would prefer to use `pydantic.BaseSettings`, but there are some cases, which make
BaseSettings not needed, like situations, when you need to get one env var before BaseSettings
build.
"""

import os


def getenv_list(key: str, default: str = "", separator: str = ",") -> list[str]:
    """Get environment variable as list of strings."""
    value = os.getenv(key, default)
    if separator not in value and not value.isalnum():
        return []
    result_list = [x.strip() for x in value.strip().split(separator)]
    return list(filter(lambda x: x, result_list))


def getenv_bool(key: str, default: str = "") -> bool:  # noqa: FNE005
    """Get environment variable as boolean."""
    return os.getenv(key, default).lower() in ("1", "true", "yes", "t")


def getenv_int(key: str, default: int | None = None) -> int | None:
    """Get environment variable as integer."""
    value = os.getenv(key, "")
    try:
        return int(float(value))
    except ValueError:
        return default
