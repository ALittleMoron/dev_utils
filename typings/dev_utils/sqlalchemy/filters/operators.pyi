import datetime
from collections.abc import Sequence
from typing import Any, Protocol, TypeVar

from sqlalchemy.orm import QueryableAttribute
from sqlalchemy.sql.elements import ColumnElement

_T = TypeVar("_T")

class OperatorFunctionProtocol(Protocol):
    def __call__(self, a: Any, b: Any, *, subproduct_use: bool = ...) -> Any: ...

def do_nothing(*args: Any, **kwargs: Any) -> None: ...
def return_value(value: _T) -> _T: ...
def is_(a: QueryableAttribute[Any], b: Any) -> ColumnElement[bool]: ...
def is_not(a: QueryableAttribute[Any], b: Any) -> ColumnElement[bool]: ...
def between(a: QueryableAttribute[Any], b: tuple[Any, Any]) -> ColumnElement[bool]: ...
def contains(a: QueryableAttribute[Any], b: Sequence[Any]) -> ColumnElement[bool]: ...
def django_exact(a: QueryableAttribute[Any], b: Any) -> ColumnElement[bool]: ...
def django_iexact(a: QueryableAttribute[Any], b: Any) -> ColumnElement[bool]: ...
def django_contains(a: QueryableAttribute[Any], b: Any) -> ColumnElement[bool]: ...
def django_icontains(a: QueryableAttribute[Any], b: Any) -> ColumnElement[bool]: ...
def django_in(a: QueryableAttribute[Any], b: Sequence[Any]) -> ColumnElement[bool]: ...
def django_startswith(a: QueryableAttribute[Any], b: Any) -> ColumnElement[bool]: ...
def django_istartswith(a: QueryableAttribute[Any], b: Any) -> ColumnElement[bool]: ...
def django_endswith(a: QueryableAttribute[Any], b: Any) -> ColumnElement[bool]: ...
def django_iendswith(a: QueryableAttribute[Any], b: Any) -> ColumnElement[bool]: ...
def django_range(a: QueryableAttribute[Any], b: tuple[Any, Any]) -> ColumnElement[bool]: ...
def django_date(
    a: QueryableAttribute[Any],
    b: datetime.date,
    *,
    subproduct_use: bool = ...,
) -> ColumnElement[Any]: ...
def django_year(
    a: QueryableAttribute[Any],
    b: int | str,
    *,
    subproduct_use: bool = ...,
) -> ColumnElement[Any]: ...
def django_iso_year(
    a: QueryableAttribute[Any],
    b: int | str,
    *,
    subproduct_use: bool = ...,
) -> ColumnElement[Any]: ...
def django_month(
    a: QueryableAttribute[Any],
    b: int | str,
    *,
    subproduct_use: bool = ...,
) -> ColumnElement[Any]: ...
def django_day(
    a: QueryableAttribute[Any],
    b: int | str,
    *,
    subproduct_use: bool = ...,
) -> ColumnElement[Any]: ...
def django_week(
    a: QueryableAttribute[Any],
    b: int | str,
    *,
    subproduct_use: bool = ...,
) -> ColumnElement[Any]: ...
def django_week_day(
    a: QueryableAttribute[Any],
    b: int | str,
    *,
    subproduct_use: bool = ...,
) -> ColumnElement[Any]: ...
def django_iso_week_day(
    a: QueryableAttribute[Any],
    b: int | str,
    *,
    subproduct_use: bool = ...,
) -> ColumnElement[Any]: ...
def django_quarter(
    a: QueryableAttribute[Any],
    b: int | str,
    *,
    subproduct_use: bool = ...,
) -> ColumnElement[Any]: ...
def django_time(
    a: QueryableAttribute[Any],
    b: datetime.time,
    *,
    subproduct_use: bool = ...,
) -> ColumnElement[Any]: ...
def django_hour(
    a: QueryableAttribute[Any],
    b: int,
    *,
    subproduct_use: bool = ...,
) -> ColumnElement[Any]: ...
def django_minute(
    a: QueryableAttribute[Any],
    b: int,
    *,
    subproduct_use: bool = ...,
) -> ColumnElement[Any]: ...
def django_second(
    a: QueryableAttribute[Any],
    b: int,
    *,
    subproduct_use: bool = ...,
) -> ColumnElement[Any]: ...
def django_isnull(a: QueryableAttribute[Any], b: bool) -> ColumnElement[bool]: ...  # noqa: FBT001
def django_regex(a: QueryableAttribute[Any], b: str) -> ColumnElement[bool]: ...
def django_iregex(a: QueryableAttribute[Any], b: str) -> ColumnElement[bool]: ...
