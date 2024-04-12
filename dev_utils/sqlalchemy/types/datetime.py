"""Type module with datetime types for columns."""

import datetime
import zoneinfo
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, TypeDecorator
from sqlalchemy.ext.compiler import compiles  # type: ignore
from sqlalchemy.sql import expression

if TYPE_CHECKING:
    from sqlalchemy import Dialect


UTC = zoneinfo.ZoneInfo("UTC")


class Utcnow(expression.FunctionElement):  # type: ignore
    """Alias for DateTime type for new mapping.

    Needs to avoid incorrect type mapping (use only Utcnow type, not all DateTime columns).
    """

    type = DateTime()  # noqa: A003


class UTCDateTime(TypeDecorator[datetime.datetime]):
    """Type decorator for DateTime with UTC."""

    impl = DateTime(timezone=True)
    cache_ok = True

    @property
    def python_type(self) -> type[datetime.datetime]:  # noqa: D102  # pragma: no coverage
        return datetime.datetime

    def process_result_value(  # noqa: D102
        self: "UTCDateTime",
        value: "datetime.datetime | None",
        dialect: "Dialect",  # noqa
    ) -> "datetime.datetime | None":
        if isinstance(value, datetime.datetime) and value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value

    def process_bind_param(  # noqa: D102
        self: "UTCDateTime",
        value: "datetime.datetime | None",
        dialect: "Dialect",  # noqa
    ) -> "datetime.datetime | None":
        if isinstance(value, datetime.datetime) and value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value


@compiles(Utcnow, "postgresql")
def pg_utcnow(type_: Any, compiler: Any, **kwargs: Any) -> str:  # noqa
    """Mapping for Utcnow on postgresql current time func with timezone."""  # noqa: D401
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


@compiles(Utcnow, "sqlite")
def sqlite_utcnow(type_: Any, compiler: Any, **kwargs: Any) -> str:  # noqa
    """Mapping for Utcnow on sqlite current time func with timezone."""  # noqa: D401
    return "DATETIME('now')"


@compiles(Utcnow, "mysql")
def mysql_utcnow(type_: Any, compiler: Any, **kwargs: Any) -> str:  # noqa
    """Mapping for Utcnow on mysql current time func with timezone."""  # noqa: D401
    return "UTC_TIMESTAMP()"
