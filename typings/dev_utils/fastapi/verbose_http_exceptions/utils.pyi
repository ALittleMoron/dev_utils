from typing import Any, TypeAlias

Location: TypeAlias = str | None
Attribute: TypeAlias = str | None

def resolve_error_location_and_attr(error: dict[str, Any]) -> tuple[Location, Attribute]: ...
