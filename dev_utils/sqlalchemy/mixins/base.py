from functools import cached_property
from typing import TYPE_CHECKING, Any, TypeGuard

from sqlalchemy.orm.decl_api import declarative_mixin

from dev_utils.core.exc import NoDeclarativeModelError
from dev_utils.core.utils import get_object_class_absolute_name
from dev_utils.sqlalchemy.utils import is_declarative

if TYPE_CHECKING:
    from sqlalchemy.orm.decl_api import DeclarativeBase
    from sqlalchemy.orm.mapper import Mapper


@declarative_mixin
class BaseModelMixin:
    """Base model mixin."""

    @cached_property
    def _is_mixin_in_declarative_model(self) -> "TypeGuard[Mapper[Any]]":  # type: ignore
        return any(is_declarative(class_) for class_ in self.__class__.mro())

    @cached_property
    def _sa_model_class(self) -> "type[DeclarativeBase]":
        if not self._is_mixin_in_declarative_model:
            cls_path = get_object_class_absolute_name(self.__class__)
            msg = f"No declarative base attributes were found in {cls_path}"
            raise NoDeclarativeModelError(msg)
        return self.__mapper__.class_  # type: ignore

    def _get_instance_attr(self, field: str) -> Any:  # noqa: ANN401
        value = getattr(self, field)
        if callable(value):
            value = value()
        return value
