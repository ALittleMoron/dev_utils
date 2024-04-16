from functools import cached_property
from typing import Any, TypeGuard

from sqlalchemy.orm import DeclarativeBase, Mapper

class BaseModelMixin:
    @cached_property
    def _is_mixin_in_declarative_model(self) -> TypeGuard[Mapper[Any]]:  # type: ignore
        ...

    @cached_property
    def _sa_model_class(self) -> type[DeclarativeBase]: ...
    def _get_instance_attr(self, field: str) -> Any:  # noqa: ANN401
        ...
