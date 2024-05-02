from typing import TYPE_CHECKING

import pytest
from sqlalchemy import select
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import DeclarativeBase, Mapped, load_only

from dev_utils.sqlalchemy.mixins import general as general_mixins
from dev_utils.sqlalchemy.mixins import ids as ids_mixins
from tests.utils import MyModel

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from tests.types import AsyncFactoryFunctionProtocol


class Base(DeclarativeBase): ...  # noqa: D101


class DictConvertModel(  # noqa: D101
    general_mixins.DictConverterMixin,
    ids_mixins.IntegerIDMixin,
    Base,
):
    __tablename__ = "dct_convert"

    some_other_attr: Mapped[str]

    @hybrid_method
    def some_hybrid_method(self) -> Mapped[int]:  # noqa: D102
        return self.id  # type: ignore


class DifferenceModel(  # noqa: D101
    general_mixins.DifferenceMixin,
    ids_mixins.IntegerIDMixin,
    Base,
):
    __tablename__ = "diff_model"

    some_other_attr: Mapped[str]


class BetterReprModel(  # noqa: D101
    general_mixins.BetterReprMixin,
    ids_mixins.IntegerIDMixin,
    Base,
):
    __tablename__ = "table_with_good_repr"

    some_other_attr: Mapped[str]


def test_dict_convert() -> None:
    instance = DictConvertModel(id=1, some_other_attr="aboba")
    assert instance.as_dict() == {"id": 1, "some_other_attr": "aboba", "some_hybrid_method": 1}
    assert instance.as_dict(exclude={"some_other_attr", "some_hybrid_method"}) == {"id": 1}
    assert instance.as_dict(exclude={"some_other_attr", "some_hybrid_method"}, id="other_id") == {
        "other_id": 1,
    }
    assert instance.as_dict(exclude={"some_other_attr", "id"}, some_hybrid_method="other") == {
        "other": 1,
    }


def test_difference() -> None:
    DifferenceModel.safe_difference_flag = True
    instance = DifferenceModel(id=1, some_other_attr="bib")
    same = DifferenceModel(id=1, some_other_attr="bib")
    different = DifferenceModel(id=2, some_other_attr="bob")
    same_id = DifferenceModel(id=1, some_other_attr="bobob")
    other = DictConvertModel(id=1, some_other_attr="aboba")
    assert instance.is_different_from({"id": 2, "some_other_attr": "bob"}) is True
    assert instance.is_different_from(same) is False
    assert instance.is_different_from(different) is True
    assert instance.is_different_from({"id": 1, "some_other_attr": "bib"}) is False
    assert instance.is_different_from({"some_other_attr": "bib"}) is False
    assert instance.is_different_from({"id": 1}) is False
    assert instance.is_different_from({"incorrect_attribute": 255}) is True
    assert instance.is_different_from(same_id, exclude={"some_other_attr"}) is False
    assert (
        instance.is_different_from(
            {"id": 1, "some_other_attr": "bobobo"},
            exclude={"some_other_attr"},
        )
        is False
    )
    assert instance.is_different_from(other) is True
    DifferenceModel.safe_difference_flag = False


@pytest.mark.asyncio()
async def test_difference_with_unloaded_fields(
    db_async_session: "AsyncSession",
    mymodel_async_factory: "AsyncFactoryFunctionProtocol[MyModel]",
) -> None:
    orig_value = await mymodel_async_factory(db_async_session)
    assert orig_value.name is not None, "incorrect MyModel create in factory."
    assert orig_value.other_name is not None, "incorrect MyModel create in factory."
    my_model_instance = MyModel(
        id=orig_value.id + 1,
        name=orig_value.name + "abc",
        other_name=orig_value.other_name + "abc",
    )
    db_async_session.expire(orig_value)
    MyModel.safe_difference_flag = True
    selected_with_unload = await db_async_session.scalar(
        select(MyModel).options(load_only(MyModel.id)),
    )
    assert selected_with_unload is not None, "selected MyModel not found (but must be in DB)"
    assert selected_with_unload.is_different_from({"name": "abc"}) is True
    assert selected_with_unload.is_different_from(my_model_instance) is True
    MyModel.safe_difference_flag = False


@pytest.mark.asyncio()
async def test_difference_with_unloaded_fields_unsafe(
    db_async_session: "AsyncSession",
    mymodel_async_factory: "AsyncFactoryFunctionProtocol[MyModel]",
) -> None:
    await mymodel_async_factory(db_async_session)
    MyModel.safe_difference_flag = False
    selected_with_unload = await db_async_session.scalar(
        select(MyModel).options(load_only(MyModel.id)),
    )
    assert selected_with_unload is not None, "selected MyModel not found (but must be in DB)"
    with pytest.raises(AttributeError):
        selected_with_unload.is_different_from({"name": "abc"})


def test_difference_incorrect_type() -> None:
    instance = DifferenceModel(id=1, some_other_attr="bib")
    other = DictConvertModel(id=1, some_other_attr="aboba")
    with pytest.raises(TypeError):
        instance.is_different_from(other)


def test_difference_unsafe() -> None:
    instance = DifferenceModel(id=1, some_other_attr="bib")
    with pytest.raises(AttributeError):
        instance.is_different_from({"incorrect_attribute": 255})


def test_default_better_repr() -> None:

    instance = BetterReprModel(id=1, some_other_attr="some")
    instance_repr = repr(instance)
    assert instance_repr.startswith('BetterReprModel')
    assert "id=1" in instance_repr
    assert "some_other_attr='some'" in instance_repr


def test_full_class_path_in_repr() -> None:
    class OtherBetterReprModel(
        general_mixins.BetterReprMixin,
        ids_mixins.IntegerIDMixin,
        Base,
    ):
        __tablename__ = "other_table_with_good_repr"

        use_full_class_path = True

        some_other_attr: Mapped[str]

    instance = OtherBetterReprModel(id=1, some_other_attr="some")
    instance_repr = repr(instance)
    assert instance_repr.startswith(
        'tests.sqlalchemy.mixins.test_general.'
        'test_full_class_path_in_repr.<locals>.OtherBetterReprModel',
    )


def test_repr_include_fields() -> None:
    class OtherOtherBetterReprModel(
        general_mixins.BetterReprMixin,
        ids_mixins.IntegerIDMixin,
        Base,
    ):
        __tablename__ = "other_other_table_with_good_repr"

        repr_include_fields = {"id"}

        some_other_attr: Mapped[str]

    instance = OtherOtherBetterReprModel(id=1, some_other_attr="some")
    instance_repr = repr(instance)
    assert instance_repr == 'OtherOtherBetterReprModel(id=1)'


def test_max_repr_elements() -> None:
    class MaxReprOtherBetterReprModel(
        general_mixins.BetterReprMixin,
        ids_mixins.IntegerIDMixin,
        Base,
    ):
        __tablename__ = "max_repr_other_table_with_good_repr"

        max_repr_elements = 1

        some_other_attr: Mapped[str]

    instance = MaxReprOtherBetterReprModel(id=1, some_other_attr="some")
    instance_repr = repr(instance)
    assert instance_repr == 'MaxReprOtherBetterReprModel(id=1)'


@pytest.mark.asyncio()
async def test_unload_fields_in_repr(
    db_async_session: "AsyncSession",
    mymodel_async_factory: "AsyncFactoryFunctionProtocol[MyModel]",
) -> None:
    orig_value = await mymodel_async_factory(db_async_session)
    db_async_session.expire(orig_value)
    MyModel.safe_difference_flag = True
    selected_with_unload = await db_async_session.scalar(
        select(MyModel).options(load_only(MyModel.id)),
    )
    assert selected_with_unload, "MyModel instance not found (but it must be in DB)"
    selected_with_unload_repr = repr(selected_with_unload)
    assert "<Not loaded>" in selected_with_unload_repr


def test_table_name_auto() -> None:
    class TableNameModel(
        general_mixins.TableNameMixin,
        ids_mixins.IntegerIDMixin,
        Base,
    ):  # noqa: D101
        some_other_attr: Mapped[str]

    assert TableNameModel.__tablename__ == "table_name_model"


def test_table_name_with_app_name_auto() -> None:
    class TableNameWithAppNameModel(
        general_mixins.TableNameMixin,
        ids_mixins.IntegerIDMixin,
        Base,
    ):  # noqa: D101
        __join_application_prefix__ = True
        some_other_attr: Mapped[str]

    assert TableNameWithAppNameModel.__tablename__ == "test_general_table_name_with_app_name_model"
    TableNameWithAppNameModel.__module__ = '__main__'
    assert TableNameWithAppNameModel.__tablename__ == "table_name_with_app_name_model"
    TableNameWithAppNameModel.__module__ = 'models'
    assert TableNameWithAppNameModel.__tablename__ == "table_name_with_app_name_model"
    TableNameWithAppNameModel.__module__ = 'users.models'
    assert TableNameWithAppNameModel.__tablename__ == "users_table_name_with_app_name_model"
