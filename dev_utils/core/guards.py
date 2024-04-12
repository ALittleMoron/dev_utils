from typing import TYPE_CHECKING, Any, TypeGuard

if TYPE_CHECKING:
    from collections.abc import Sequence


def all_dict_keys_are_str(value: dict[Any, Any]) -> TypeGuard[dict[str, Any]]:
    """TypeGuard for checking dict keys are all strings."""
    return all(isinstance(key, str) for key in value)


def all_elements_in_sequence_are_str(value: "Sequence[Any]") -> "TypeGuard[Sequence[str]]":
    """TypeGuard for checking sequence elements are all strings."""
    if isinstance(value, str):
        return True
    return all(isinstance(ele, str) for ele in value)
