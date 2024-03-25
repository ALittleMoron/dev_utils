import datetime
import zoneinfo
from collections.abc import Sequence
from typing import Any

import pytest
from freezegun import freeze_time
from sqlalchemy import delete, func, insert, inspect, select, update
from sqlalchemy.orm import DeclarativeBase, joinedload, selectinload, subqueryload

from dev_utils.core.exc import NoModelAttributeError, NoModelRelationshipError
from dev_utils.sqlalchemy import utils
from tests.utils import Base, MyModel, OtherModel, generate_datetime_list


@pytest.mark.parametrize(
    'dt',
    generate_datetime_list(n=10, tz=zoneinfo.ZoneInfo('UTC')),
)
def test_get_utc_now(dt: datetime.datetime) -> None:  # noqa
    with freeze_time(dt):
        assert utils.get_utc_now() == dt


@pytest.mark.parametrize(
    ('obj', 'expected_result'),
    [
        (MyModel, True),
        (254, False),
        (MyModel.__table__, False),
    ],
)
def test_is_declarative(obj: Any, expected_result: bool) -> None:  # noqa: D103, ANN401, FBT001
    assert utils.is_declarative(obj) == expected_result


@pytest.mark.parametrize(
    ('field', 'expected_result'),
    [
        ('id', MyModel.id),
        ('name', MyModel.name),
        ('full_name', MyModel.full_name),
        ('get_full_name', MyModel.get_full_name()),
    ],
)
def test_get_sqlalchemy_attribute(field: str, expected_result: Any) -> None:  # noqa
    assert str(utils.get_sqlalchemy_attribute(MyModel, field)) == str(expected_result)


def test_get_sqlalchemy_attribute_incorrect() -> None:  # noqa
    with pytest.raises(NoModelAttributeError):
        utils.get_sqlalchemy_attribute(MyModel, 'incorrect_field')


def test_get_registry_class() -> None:  # noqa
    assert utils.get_registry_class(MyModel) == MyModel.registry._class_registry  # type: ignore


@pytest.mark.parametrize(
    ('stmt', 'expected_result'),
    [
        (select(MyModel), [MyModel]),
        (select(MyModel, OtherModel), [MyModel, OtherModel]),
        (select(), []),
        (insert(MyModel), [MyModel]),
        (update(MyModel), [MyModel]),
        (delete(MyModel), [MyModel]),
        (select(func.count()).select_from(MyModel), [MyModel]),
        (select(MyModel.id).select_from(MyModel), [MyModel]),
        (select(func.count()).select_from(select(MyModel).subquery()), []),  # type: ignore
    ],
)
def test_get_model_classes_from_statement(  # noqa
    stmt: utils.Statement,
    expected_result: Sequence[type[Base]],
) -> None:
    assert set(utils.get_model_classes_from_statement(stmt)) == set(expected_result)


@pytest.mark.parametrize(
    ('name', 'expected_result'),
    [
        ('MyModel', MyModel),
        ('OtherModel', OtherModel),
        ('NoModel', None),
    ],
)
def test_get_model_class_by_name(name: str, expected_result: type[Base] | None) -> None:  # noqa
    register = utils.get_registry_class(MyModel)
    assert utils.get_model_class_by_name(register, name) == expected_result


@pytest.mark.parametrize(
    ('name', 'expected_result'),
    [
        ('my_model', MyModel),
        ('other_model', OtherModel),
        ('no_model', None),
    ],
)
def test_get_model_class_by_tablename(  # noqa
    name: str,
    expected_result: type[Base] | None,
) -> None:
    register = utils.get_registry_class(MyModel)
    assert utils.get_model_class_by_tablename(register, name) == expected_result


def test_get_valid_model_class_names() -> None:  # noqa
    register = utils.get_registry_class(MyModel)
    assert utils.get_valid_model_class_names(register) == set(['MyModel', 'OtherModel'])


@pytest.mark.parametrize(
    ('model', 'expected_result'),
    [
        (MyModel, [OtherModel]),
        (OtherModel, [MyModel]),
    ],
)
def test_get_related_models(  # noqa
    model: type[DeclarativeBase],
    expected_result: list[type[DeclarativeBase]],
):
    assert utils.get_related_models(model) == expected_result


def test_get_valid_field_names() -> None:  # noqa
    assert utils.get_valid_field_names(MyModel) == {
        'id',
        'name',
        'other_name',
        'dt',
        'bl',
        'full_name',
        'get_full_name',
    }


@pytest.mark.parametrize(
    ('field', 'expected_result'),
    [
        ('id', False),
        ('name', False),
        ('other_name', False),
        ('full_name', True),
        ('get_full_name', False),
    ],
)
def test_is_hybrid_property(field: str, expected_result: bool) -> None:  # noqa
    insp = inspect(MyModel).all_orm_descriptors
    assert utils.is_hybrid_property(insp[field]) == expected_result


@pytest.mark.parametrize(
    ('field', 'expected_result'),
    [
        ('id', False),
        ('name', False),
        ('other_name', False),
        ('full_name', False),
        ('get_full_name', True),
    ],
)
def test_is_hybrid_method(field: str, expected_result: bool) -> None:  # noqa
    insp = inspect(MyModel).all_orm_descriptors
    assert utils.is_hybrid_method(insp[field]) == expected_result


@pytest.mark.parametrize(
    ('stmt', 'relationship_names', 'load_strategy', 'expected_result'),
    [
        (
            select(MyModel),
            ('other_models',),
            joinedload,
            select(MyModel).options(joinedload(MyModel.other_models)),
        ),
        (
            select(MyModel),
            ('other_models',),
            selectinload,
            select(MyModel).options(selectinload(MyModel.other_models)),
        ),
        (
            select(MyModel),
            ('other_models',),
            subqueryload,
            select(MyModel).options(subqueryload(MyModel.other_models)),
        ),
    ],
)
def test_apply_loads(  # noqa
    stmt: Any,  # noqa
    relationship_names: tuple[str, ...],
    load_strategy: Any,  # noqa
    expected_result: Any,  # noqa
) -> None:  # noqa
    assert str(
        utils.apply_loads(
            stmt,
            *relationship_names,
            load_strategy=load_strategy,
        ),
    ) == str(  # type: ignore
        expected_result,
    )


def test_apply_incorrect_loads():
    with pytest.raises(NoModelRelationshipError):
        utils.apply_loads(select(MyModel), 'no_model_rel')


@pytest.mark.parametrize(
    ('stmt', 'relationship_names', 'left_outer_join', 'full_join', 'expected_result'),
    [
        (
            select(MyModel),
            ('other_models',),
            False,
            False,
            select(MyModel).join(MyModel.other_models),
        ),
        (
            select(MyModel),
            ('other_models',),
            True,
            False,
            select(MyModel).join(MyModel.other_models, isouter=True),
        ),
        (
            select(MyModel),
            ('other_models',),
            False,
            True,
            select(MyModel).join(MyModel.other_models, full=True),
        ),
    ],
)
def test_apply_joins(  # noqa
    stmt: Any,  # noqa
    relationship_names: tuple[str, ...],
    left_outer_join: bool,  # noqa
    full_join: bool,  # noqa
    expected_result: Any,  # noqa
) -> None:  # noqa
    assert str(
        utils.apply_joins(
            stmt,
            *relationship_names,
            left_outer_join=left_outer_join,
            full_join=full_join,
        ),
    ) == str(  # type: ignore
        expected_result,
    )


def test_apply_incorrect_joins() -> None:
    with pytest.raises(NoModelRelationshipError):
        utils.apply_joins(select(MyModel), 'no_model_rel')
