import datetime
import zoneinfo

from sqlalchemy import Cast
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, declared_attr

from dev_utils.sqlalchemy.mixins.base import BaseModelMixin

UTC = zoneinfo.ZoneInfo("UTC")

class CreatedAtAuditMixin:
    @declared_attr
    def created_at(cls) -> Mapped[datetime.datetime]: ...
    @hybrid_property
    def created_at_date(self) -> datetime.date:  # type: ignore
        ...

    @created_at_date.expression
    @classmethod
    def created_at_date(cls) -> Cast[datetime.date]: ...
    @hybrid_property
    def created_at_time(self) -> datetime.time:  # type: ignore
        ...

    @created_at_time.expression
    @classmethod
    def created_at_time(cls) -> Cast[datetime.time]: ...
    @property
    def created_at_isoformat(self) -> str: ...

class UpdatedAtAuditMixin(BaseModelMixin):
    @declared_attr
    def updated_at(cls) -> Mapped[datetime.datetime]: ...
    @hybrid_property
    def updated_at_date(self) -> datetime.date:  # type: ignore
        ...

    @updated_at_date.expression
    @classmethod
    def updated_at_date(cls) -> Cast[datetime.date]: ...
    @hybrid_property
    def updated_at_time(self) -> datetime.time:  # type: ignore
        ...

    @updated_at_time.expression
    @classmethod
    def updated_at_time(cls) -> Cast[datetime.time]: ...
    @property
    def updated_at_isoformat(self) -> str: ...

class AuditMixin(CreatedAtAuditMixin, UpdatedAtAuditMixin): ...
