"""Mixin module with audit columns of model (created_at, updated_at)."""

import datetime
import zoneinfo

from sqlalchemy import Cast, Date, Time, cast
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from dev_utils.sqlalchemy.mixins.base import BaseModelMixin
from dev_utils.sqlalchemy.types.datetime import UTCDateTime, Utcnow

UTC = zoneinfo.ZoneInfo("UTC")


class CreatedAtAuditMixin(BaseModelMixin):
    """Audit mixin with created_at column (datetime)."""

    @declared_attr
    def created_at(cls) -> Mapped[datetime.datetime]:
        """Audit created_at column."""
        return mapped_column(UTCDateTime, server_default=Utcnow())

    @hybrid_property
    def created_at_date(self) -> "datetime.date":  # type: ignore
        """Date value of created_at datetime field."""
        return self.created_at.date()

    @created_at_date.expression
    @classmethod
    def created_at_date(cls) -> Cast[datetime.date]:
        """Date expression of created_at datetime field."""
        return cast(cls.created_at, Date)

    @hybrid_property
    def created_at_time(self) -> datetime.time:  # type: ignore
        """Time of created_at datetime field."""
        return self.created_at.time()

    @created_at_time.expression
    @classmethod
    def created_at_time(cls) -> Cast[datetime.time]:
        """Time expression of created_at datetime field."""
        return cast(cls.created_at, Time)

    @property
    def created_at_isoformat(self) -> str:
        """ISO string of created_at datetime field."""
        return self.created_at.isoformat()


class UpdatedAtAuditMixin(BaseModelMixin):
    """Audit mixin with created_at column (datetime)."""

    @declared_attr
    def updated_at(cls) -> Mapped[datetime.datetime]:
        """Audit created_at column."""
        return mapped_column(
            UTCDateTime,
            server_default=Utcnow(),
            server_onupdate=Utcnow(),  # type: ignore
        )

    @hybrid_property
    def updated_at_date(self) -> "datetime.date":  # type: ignore
        """Date value of updated_at datetime field."""
        return self.updated_at.date()

    @updated_at_date.expression
    @classmethod
    def updated_at_date(cls) -> Cast[datetime.date]:
        """Date expression of updated_at datetime field."""
        return cast(cls.updated_at, Date)

    @hybrid_property
    def updated_at_time(self) -> datetime.time:  # type: ignore
        """Time of updated_at datetime field."""
        return self.updated_at.time()

    @updated_at_time.expression
    @classmethod
    def updated_at_time(cls) -> Cast[datetime.time]:
        """Time expression of updated_at datetime field."""
        return cast(cls.updated_at, Time)

    @property
    def updated_at_isoformat(self) -> str:
        """ISO string of updated_at datetime field."""
        return self.updated_at.isoformat()


class AuditMixin(CreatedAtAuditMixin, UpdatedAtAuditMixin):
    """Full audit mixin with created_at and updated_at columns."""
