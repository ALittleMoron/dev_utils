from typing import Any

from dev_utils.sqlalchemy.mixins.base import BaseModelMixin
from dev_utils.sqlalchemy.utils import get_valid_field_names


class DictConverterMixin(BaseModelMixin):
    """Mixin for converting models to dict."""

    def _replace(
        self,
        item: dict[str, Any],
        **replace: str,
    ) -> None:
        """Add replace field for item.

        Uses like alias: rename existing fields
        """
        for original, replaced in replace.items():
            value_to_replace = self._get_instance_attr(original)
            item[replaced] = value_to_replace
            item.pop(original, None)

    def as_dict(
        self,
        exclude: set[str] | None = None,
        **replace: str,
    ) -> dict[str, Any]:
        """Convert model instance to dict."""
        valid_fields = get_valid_field_names(self._sa_model_class)
        exclude_fields: set[str] = (exclude or set()).union(
            self._sa_instance_state.unloaded,  # type: ignore
        )
        available_fields = valid_fields - exclude_fields
        item: dict[str, Any] = {field: self._get_instance_attr(field) for field in available_fields}
        replace = {key: value for key, value in replace.items() if key in item}
        self._replace(item, **replace)
        return item
