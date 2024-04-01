"""TypeGuards module.

Contains functions-checkers of filter types.
"""

from typing import TYPE_CHECKING, Any, TypeGuard

from dev_utils.sqlalchemy.filters.types import AdvancedOperatorsSet, OperatorFilterDict

if TYPE_CHECKING:
    from dev_utils.sqlalchemy.filters.converters import AnyLookupMapping, LookupMappingWithNested


def is_dict_simple_filter_dict(value: dict[Any, Any]) -> TypeGuard['OperatorFilterDict']:
    """TypeGuard for checking dict is ``OperatorFilterDict`` (typed dict) instance.

    OperatorFilterDict should has ``field``, ``value``, and ``operator`` keys with validated values:

    ``field``: any string.
    ``value``: any value.
    ``operator``: any string of ``AdvancedOperatorsLiteral``.
    """
    if 'field' not in value or not isinstance(value['field'], str):
        return False
    if 'value' not in value:
        return False
    if 'operator' in value and value['operator'] not in AdvancedOperatorsSet:
        return False
    return True


def has_nested_lookups(mapping: 'AnyLookupMapping') -> TypeGuard['LookupMappingWithNested']:
    """TypeGuard for specify converter mapping type with nested lookups.

    By default, all mappings can has either operator function or tuple of operator function and
    available sub-lookups set.
    """
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
