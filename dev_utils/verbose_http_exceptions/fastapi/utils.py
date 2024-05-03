from typing import Any

from dev_utils.core.guards import all_elements_in_sequence_are_str
from dev_utils.verbose_http_exceptions.exc import RequestValidationVerboseHTTPException

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


def validation_error_from_error_dict(
    error: dict[str, Any],
) -> RequestValidationVerboseHTTPException:
    """Convert error dict to RequestValidationVerboseHTTPException instance."""
    location, attribute = resolve_error_location_and_attr(error)
    return RequestValidationVerboseHTTPException(
        type_=error.get("type") or "not_known_type",
        message=error.get("msg") or "not_known_message",
        location=location,
        attr_name=attribute,
    )
