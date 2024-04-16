from typing import Any

from dev_utils.sqlalchemy.mixins.base import BaseModelMixin

class DictConverterMixin(BaseModelMixin):
    def _replace(
        self,
        item: dict[str, Any],
        **replace: str,
    ) -> None: ...
    def as_dict(
        self,
        exclude: set[str] | None = None,
        **replace: str,
    ) -> dict[str, Any]: ...
