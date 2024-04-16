import datetime
from collections.abc import Callable, Sequence
from typing import Any, TypeAlias, TypeGuard, TypeVar

from sqlalchemy import Delete, Insert, Select, Update
from sqlalchemy.orm import DeclarativeBase, Mapper, QueryableAttribute
from sqlalchemy.orm.base import InspectionAttr
from sqlalchemy.orm.clsregistry import _ClsRegistryType  # type: ignore
from sqlalchemy.orm.strategy_options import _AbstractLoad  # type: ignore

_T = TypeVar("_T", bound=Select[Any])
Statement: TypeAlias = (
    Select[tuple[DeclarativeBase]]
    | Update[DeclarativeBase]
    | Delete[DeclarativeBase]
    | Insert[DeclarativeBase]
)

def get_utc_now() -> datetime.datetime: ...
def is_declarative(model: Any) -> TypeGuard[Mapper[Any]]: ...  # noqa: ANN401
def get_sqlalchemy_attribute(
    model: type[DeclarativeBase],
    field_name: str,
) -> QueryableAttribute[Any]: ...
def get_model_classes_from_statement(stmt: Statement) -> Sequence[type[DeclarativeBase]]: ...
def get_registry_class(model: type[DeclarativeBase]) -> _ClsRegistryType: ...
def get_model_class_by_tablename(
    registry: _ClsRegistryType,
    tablename: str,
) -> type[DeclarativeBase] | None: ...
def get_model_class_by_name(
    registry: _ClsRegistryType,
    name: str,
) -> type[DeclarativeBase] | None: ...
def get_valid_model_class_names(registry: _ClsRegistryType) -> set[str]: ...
def get_valid_relationships_names(model: type[DeclarativeBase]) -> set[str]: ...
def get_valid_field_names(model: type[DeclarativeBase]) -> set[str]: ...
def get_all_valid_queryable_attributes(model: type[DeclarativeBase]) -> set[str]: ...
def get_related_models(model: type[DeclarativeBase]) -> list[type[DeclarativeBase]]: ...
def is_hybrid_property(orm_descriptor: InspectionAttr) -> bool: ...
def is_hybrid_method(orm_descriptor: InspectionAttr) -> bool: ...
def apply_loads(
    stmt: _T,
    *relationship_names: str,
    load_strategy: Callable[[Any], _AbstractLoad] = ...,
) -> _T: ...
def apply_joins(
    stmt: _T,
    *relationship_names: str,
    left_outer_join: bool = ...,
    full_join: bool = ...,
) -> _T: ...
