import datetime
import zoneinfo
from typing import Any

from sqlalchemy import Dialect, TypeDecorator
from sqlalchemy.sql import expression

UTC = zoneinfo.ZoneInfo("UTC")

class Utcnow(expression.FunctionElement[datetime.datetime]):
    type = ...

class UTCDateTime(TypeDecorator[datetime.datetime]):
    impl = ...
    cache_ok = ...

    @property
    def python_type(self) -> type[datetime.datetime]:  # noqa: D102  # pragma: no coverage
        ...

    def process_result_value(  # noqa: D102
        self,
        value: datetime.datetime | None,
        dialect: "Dialect",  # noqa
    ) -> datetime.datetime | None: ...
    def process_bind_param(  # noqa: D102
        self,
        value: datetime.datetime | None,
        dialect: Dialect,  # noqa
    ) -> datetime.datetime | None: ...

def pg_utcnow(type_: Any, compiler: Any, **kwargs: Any) -> str:  # noqa
    ...

def sqlite_utcnow(type_: Any, compiler: Any, **kwargs: Any) -> str:  # noqa
    ...

def mysql_utcnow(type_: Any, compiler: Any, **kwargs: Any) -> str:  # noqa
    ...
