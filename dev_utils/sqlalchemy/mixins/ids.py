import uuid

from sqlalchemy import UUID, BigInteger, Integer
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from dev_utils.sqlalchemy.mixins.base import BaseModelMixin


class IntegerIDMixin(BaseModelMixin):
    """Integer primary key field (id) mixin."""

    @declared_attr
    def id(cls) -> Mapped[int]:
        """Id field."""
        return mapped_column(
            BigInteger().with_variant(Integer, "sqlite"),
            nullable=False,
            unique=True,
            primary_key=True,
            autoincrement=True,
        )


class UUIDMixin(BaseModelMixin):
    """UUID primary key field (id) mixin."""

    @declared_attr
    def id(cls) -> Mapped[uuid.UUID]:
        """Id field."""
        return mapped_column(
            UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
        )
