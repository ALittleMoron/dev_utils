"""Mixin module with audit columns of model (created_at, updated_at)."""

import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Cast, Date, Time, cast, event
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm.decl_api import declarative_mixin, declared_attr

from dev_utils.core.utils import get_utc_now
from dev_utils.sqlalchemy.mixins.base import BaseModelMixin
from dev_utils.sqlalchemy.types.datetime import UTCDateTime, Utcnow

if TYPE_CHECKING:
    from sqlalchemy.engine import Connection


@declarative_mixin
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


@declarative_mixin
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


@declarative_mixin
class AuditMixin(CreatedAtAuditMixin, UpdatedAtAuditMixin):
    """Full audit mixin with created_at and updated_at columns."""


def add_audit_column_populate_event() -> None:
    """Add event for audit columns to populate updated_at and ."""

    def _update_created_at_on_create_listener(
        mapper: Mapped[CreatedAtAuditMixin],  # noqa
        connection: "Connection",  # noqa
        target: CreatedAtAuditMixin,
    ) -> None:
        target.created_at = get_utc_now()

    def _update_updated_at_on_update_listener(
        mapper: Mapped[UpdatedAtAuditMixin],  # noqa
        connection: "Connection",  # noqa
        target: UpdatedAtAuditMixin,
    ) -> None:
        target.updated_at = get_utc_now()

    # TODO: test all cases: insert, update, session.add (maybe, in some cases it will work bad).
    event.listen(UpdatedAtAuditMixin, 'before_update', _update_updated_at_on_update_listener)
    event.listen(CreatedAtAuditMixin, 'before_insert', _update_created_at_on_create_listener)
