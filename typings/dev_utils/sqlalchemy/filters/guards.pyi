from typing import Any, TypeGuard

from dev_utils.sqlalchemy.filters.converters import AnyLookupMapping, LookupMappingWithNested
from dev_utils.sqlalchemy.filters.types import OperatorFilterDict

def is_dict_simple_filter_dict(value: dict[Any, Any]) -> TypeGuard[OperatorFilterDict]: ...
def has_nested_lookups(mapping: AnyLookupMapping) -> TypeGuard[LookupMappingWithNested]: ...
