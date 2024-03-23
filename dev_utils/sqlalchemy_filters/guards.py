from typing import TYPE_CHECKING, Any, TypeGuard

from dev_utils.sqlalchemy_filters.schemas import AdvancedOperatorsSet, OperatorFilterDict

if TYPE_CHECKING:
    from dev_utils.sqlalchemy_filters.converters import AnyLookupMapping, LookupMappingWithNested


def all_dict_keys_are_str(value: dict[Any, Any]) -> TypeGuard[dict[str, Any]]:
    return all(isinstance(key, str) for key in value)


def is_dict_simple_filter_dict(value: dict[Any, Any]) -> TypeGuard['OperatorFilterDict']:
    if 'field' not in value or not isinstance(value['field'], str):
        return False
    if 'value' not in value:
        return False
    if 'operator' in value and value['operator'] not in AdvancedOperatorsSet:
        return False
    return True


def has_nested_lookups(mapping: 'AnyLookupMapping') -> TypeGuard['LookupMappingWithNested']:
    if not mapping:
        return False
    for value in mapping.values():
        if (
            not isinstance(value, tuple)
            or len(value) != 2
            or not isinstance(value[1], set)  # type: ignore
        ):
            return False
    return True
