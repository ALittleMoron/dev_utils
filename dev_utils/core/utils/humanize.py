"""Module with functions, that make some data more human-friendly."""

SIZEOF_UNIT = ["", "K", "M", "G", "T", "P", "E", "Z"]


def sizeof_fmt(num: float, *, suffix: str = "b", force_float: bool = False) -> str:
    """Make sizeof value more human-friendly.

    Convert given number to string with size unit postfix, like: Mb, Gb, Kb.

    Number convert to smallest one too. If you pass 1024, it will be converted to 1.0.
    """
    for unit in SIZEOF_UNIT:
        if abs(num) < 1024.0:
            if force_float or int(num) != num:
                return f"{num:.1f}{unit}{suffix}"
            return f"{int(num)}{unit}{suffix}"
        num /= 1024.0
    if force_float or int(num) != num:
        return f"{num:.1f}Y{suffix}"
    return f"{int(num)}Y{suffix}"
