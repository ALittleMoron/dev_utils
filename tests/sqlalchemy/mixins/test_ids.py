from sqlalchemy.orm import DeclarativeBase

from dev_utils.sqlalchemy.mixins import ids as ids_mixins


class Base(DeclarativeBase): ...  # noqa: D101


def test_ids() -> None:
    class CorrectIntegerIdMixinUseCase(ids_mixins.IntegerIDMixin, Base):  # type: ignore # noqa: D101
        __tablename__ = "correct_abc_1"

    class CorrectUUIDMixinUseCase(ids_mixins.UUIDMixin, Base):  # type: ignore # noqa: D101
        __tablename__ = "correct_abc_2"
