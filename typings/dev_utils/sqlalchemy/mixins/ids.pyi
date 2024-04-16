import uuid

from sqlalchemy.orm import Mapped, declared_attr

from dev_utils.sqlalchemy.mixins.base import BaseModelMixin

class IntegerIDMixin(BaseModelMixin):
    @declared_attr
    def id(cls) -> Mapped[int]: ...

class UUIDMixin(BaseModelMixin):
    @declared_attr
    def id(cls) -> Mapped[uuid.UUID]: ...
