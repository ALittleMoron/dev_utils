from typing import Any

from dev_utils.core.guards import all_elements_in_sequence_are_str

Location = str | None
Attribute = str | None


def resolve_error_location_and_attr(error: dict[str, Any]) -> tuple[Location, Attribute]:
    """Resolve given fastapi error: get loc and attr fields info."""
    location = error.get("loc", [])
    loc, attr = None, None
    if (
        not isinstance(location, list | tuple)
        or not all_elements_in_sequence_are_str(location)  # type: ignore
        or len(location) == 0
    ):
        return loc, attr
    if len(location) == 1:
        loc = location[0]
        return loc, attr
    *loc, attr = location
    return " -> ".join(loc), attr
