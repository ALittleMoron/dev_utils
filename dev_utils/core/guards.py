from typing import Any, TypeGuard


def all_dict_keys_are_str(value: dict[Any, Any]) -> TypeGuard[dict[str, Any]]:
    """TypeGuard for checking dict keys are all strings."""
    return all(isinstance(key, str) for key in value)
