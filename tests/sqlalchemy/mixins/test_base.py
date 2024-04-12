import pytest
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from dev_utils.core.exc import NoDeclarativeModelError
from dev_utils.sqlalchemy.mixins import base as base_mixins


class Base(DeclarativeBase): ...  # noqa: D101


class CorrectBaseMixinUseCase(base_mixins.BaseModelMixin, Base):  # noqa: D101
    __tablename__ = "correct_abc"

    id: Mapped[int] = mapped_column(primary_key=True)

    def some_callable(self):  # noqa: ANN201, D102
        return self.id


class IncorrectCorrectBaseMixinUseCase(base_mixins.BaseModelMixin):  # noqa: D101
    ...


def test_incorrect_mixin_usage() -> None:
    instance = IncorrectCorrectBaseMixinUseCase()
    assert instance._is_mixin_in_declarative_model is False  # type: ignore
    with pytest.raises(NoDeclarativeModelError):
        assert instance._sa_model_class  # type: ignore


def test_correct_mixin_usage() -> None:
    instance = CorrectBaseMixinUseCase(id=1)
    assert instance._is_mixin_in_declarative_model is True  # type: ignore
    assert instance._sa_model_class == CorrectBaseMixinUseCase  # type: ignore
    assert instance._get_instance_attr("id") == 1  # type: ignore
    assert instance._get_instance_attr("some_callable") == 1  # type: ignore
