"""Custom operators module.

Contains functions-adapters for sqlalchemy filters.

Contains:

1. Custom, written by me, operators.
2. Aliases for SQLAlchemy operators.
3. Django to SQLAlchemy adapters.
"""

import datetime
from typing import TYPE_CHECKING, Any, Protocol, TypeVar

from sqlalchemy import Date, Time, cast, extract, false, func
from sqlalchemy.orm import QueryableAttribute

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.sql.elements import ColumnElement

    T = TypeVar('T')


class OperatorFunctionProtocol(Protocol):  # noqa: D101
    def __call__(  # noqa: D102
        self,
        a: Any,  # noqa: ANN401
        b: Any,  # noqa: ANN401
        *,
        subproduct_use: bool = False,
    ) -> Any:  # noqa: ANN401
        ...


# =================================================================
# |                       COMMON OPERATORS                        |
# =================================================================

# TODO: add links to django docs for all adapters.


def do_nothing(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401, F841
    """Real do nothing function.

    Return None, receive any parameters.
    """
    return None


def return_value(value: 'T') -> 'T':
    """Return value, passed into it."""
    return value


def is_(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: Any,  # noqa
) -> 'ColumnElement[bool]':
    """SQLAlchemy ``a.is_(b)`` alias."""
    return a.is_(b)


def is_not(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: Any,  # noqa
) -> 'ColumnElement[bool]':
    """SQLAlchemy ``a.is_not(b)`` alias."""
    return a.is_not(b)


def between(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: tuple[Any, Any],
) -> 'ColumnElement[bool]':
    """SQLAlchemy ``a.between(b_1, b_2)`` alias.

    Also check [] b length (if not equals 2, then force return false statement).
    """
    if len(b) != 2:
        return false()
    return a.between(*b)


def contains(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: 'Sequence[Any]',
) -> 'ColumnElement[bool]':
    """SQLALchemy ``a.in_(b)`` alias."""
    return a.in_(b)


# =================================================================
# |                       DJANGO OPERATORS                        |
# =================================================================


def django_exact(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: Any,  # noqa: ANN401
) -> 'ColumnElement[bool]':
    """Django to SQLAlchemy adapter of ``exact`` lookup."""
    if b is None or isinstance(b, bool):
        return a.is_(None)
    return a == b


def django_iexact(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: Any,  # noqa
) -> 'ColumnElement[bool]':
    """Django to SQLAlchemy adapter of ``iexact`` lookup."""
    if b is None or isinstance(b, bool):
        return a.is_(None)
    if isinstance(b, str):
        return a.ilike(b)
    return a == b


def django_contains(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: Any,  # noqa: ANN401
) -> 'ColumnElement[bool]':
    """Django to SQLAlchemy adapter of ``contains`` lookup."""
    if isinstance(b, str):
        b = f'%{b}%'
    return a.like(b)


def django_icontains(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: Any,  # noqa: ANN401
) -> 'ColumnElement[bool]':
    """Django to SQLAlchemy adapter of ``icontains`` lookup."""
    if isinstance(b, str):
        b = f'%{b}%'
    return a.ilike(b)


def django_in(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: 'Sequence[Any]',
) -> 'ColumnElement[bool]':
    """Django to SQLAlchemy adapter of ``in`` lookup."""
    return a.in_(b)


def django_startswith(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: Any,  # noqa: ANN401
) -> 'ColumnElement[bool]':
    """Django to SQLAlchemy adapter of ``startswith`` lookup."""
    if isinstance(b, str):
        b = f'{b}%'
    return a.like(b)


def django_istartswith(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: Any,  # noqa: ANN401
) -> 'ColumnElement[bool]':
    """Django to SQLAlchemy adapter of ``istartswith`` lookup."""
    if isinstance(b, str):
        b = f'{b}%'
    return a.ilike(b)


def django_endswith(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: Any,  # noqa: ANN401
) -> 'ColumnElement[bool]':
    """Django to SQLAlchemy adapter of ``endswith`` lookup."""
    if isinstance(b, str):
        b = f'%{b}'
    return a.like(b)


def django_iendswith(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: Any,  # noqa: ANN401
) -> 'ColumnElement[bool]':
    """Django to SQLAlchemy adapter of ``iendswith`` lookup."""
    if isinstance(b, str):
        b = f'%{b}'
    return a.ilike(b)


def django_range(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: tuple[Any, Any],
) -> 'ColumnElement[bool]':
    """Django to SQLAlchemy adapter of ``range`` lookup."""
    return between(a, b)


def django_date(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: datetime.date,
    *,
    subproduct_use: bool = False,
) -> 'ColumnElement[Any]':
    """Django to SQLAlchemy adapter of ``date`` lookup."""
    if subproduct_use:
        return cast(a, Date)
    return cast(a, Date) == b


def django_year(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: int | str,
    *,
    subproduct_use: bool = False,
) -> 'ColumnElement[Any]':
    """Django to SQLAlchemy adapter of ``year`` lookup."""
    if subproduct_use:
        return extract('year', a)
    return extract('year', a) == b


def django_iso_year(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: int | str,
    *,
    subproduct_use: bool = False,
) -> 'ColumnElement[Any]':
    """Django to SQLAlchemy adapter of ``iso_year`` lookup."""
    if subproduct_use:
        return extract('isoyear', a)
    return extract('isoyear', a) == b


def django_month(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: int | str,
    *,
    subproduct_use: bool = False,
) -> 'ColumnElement[Any]':
    """Django to SQLAlchemy adapter of ``month`` lookup."""
    if subproduct_use:
        return extract('month', a)
    return extract('month', a) == b


def django_day(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: int | str,
    *,
    subproduct_use: bool = False,
) -> 'ColumnElement[Any]':
    """Django to SQLAlchemy adapter of ``day`` lookup."""
    if subproduct_use:
        return extract('day', a)
    return extract('day', a) == b


def django_week(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: int | str,
    *,
    subproduct_use: bool = False,
) -> 'ColumnElement[Any]':
    """Django to SQLAlchemy adapter of ``week`` lookup."""
    if subproduct_use:
        return extract('week', a)
    return extract('week', a) == b


def django_week_day(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: int | str,
    *,
    subproduct_use: bool = False,
) -> 'ColumnElement[Any]':
    """Django to SQLAlchemy adapter of ``week_day`` lookup."""
    if subproduct_use:
        return extract('dow', a)
    return extract('dow', a) == b


def django_iso_week_day(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: int | str,
    *,
    subproduct_use: bool = False,
) -> 'ColumnElement[Any]':
    """Django to SQLAlchemy adapter of ``iso_week_day`` lookup."""
    if subproduct_use:
        return extract('isodow', a)
    return extract('isodow', a) == b


def django_quarter(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: int | str,
    *,
    subproduct_use: bool = False,
) -> 'ColumnElement[Any]':
    """Django to SQLAlchemy adapter of ``quarter`` lookup."""
    if subproduct_use:
        return extract('quarter', a)
    return extract('quarter', a) == b


def django_time(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: datetime.time,
    *,
    subproduct_use: bool = False,
) -> 'ColumnElement[Any]':
    """Django to SQLAlchemy adapter of ``time`` lookup."""
    if subproduct_use:
        return cast(a, Time)
    return cast(a, Time) == b


def django_hour(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: int,
    *,
    subproduct_use: bool = False,
) -> 'ColumnElement[Any]':
    """Django to SQLAlchemy adapter of ``hour`` lookup."""
    if subproduct_use:
        return extract('hour', a)
    return extract('hour', a) == b


def django_minute(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: int,
    *,
    subproduct_use: bool = False,
) -> 'ColumnElement[Any]':
    """Django to SQLAlchemy adapter of ``minute`` lookup."""
    if subproduct_use:
        return extract('minute', a)
    return extract('minute', a) == b


def django_second(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: int,
    *,
    subproduct_use: bool = False,
) -> 'ColumnElement[Any]':
    """Django to SQLAlchemy adapter of ``second`` lookup."""
    if subproduct_use:
        return extract('second', a)
    return extract('second', a) == b


def django_isnull(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: bool,  # noqa: FBT001
) -> 'ColumnElement[bool]':
    """Django to SQLAlchemy adapter of ``isnull`` lookup."""
    return a.is_(None) if b else a.is_not(None)


def django_regex(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: str,
) -> 'ColumnElement[bool]':
    """Django to SQLAlchemy adapter of ``regex`` lookup."""
    return a.regexp_match(b)


def django_iregex(
    a: QueryableAttribute[Any],  # noqa: ANN401
    b: str,
) -> 'ColumnElement[bool]':
    """Django to SQLAlchemy adapter of ``iregex`` lookup."""
    return func.lower(a).regexp_match(b.lower())
