from typing import TYPE_CHECKING, Any, Protocol

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.params import Query
from pydantic import BaseModel, Field, Json, ValidationError

from dev_utils.core.guards import all_dict_keys_are_str
from dev_utils.sqlalchemy.filters.converters import (
    AdvancedOperatorFilterConverter,
    DjangoLikeFilterConverter,
    SimpleFilterConverter,
)
from dev_utils.sqlalchemy.filters.types import AdvancedOperatorsLiteral

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.orm.decl_api import DeclarativeBase
    from sqlalchemy.sql.elements import ColumnElement

    class GetSQLFiltersDepends(Protocol):  # noqa: D101
        @staticmethod
        def __call__(  # noqa: D102
            filters: list[dict[str, Any]] = ...,
        ) -> Sequence[ColumnElement[bool]]: ...


class AdvancedFilterSchema(BaseModel):  # noqa: D101
    field: str = Field(
        title="Filter field",
        description=(
            "Model field to filter. Be careful! if there is no field in model or it not allowed "
            "to filter by, the error wil be raised."
        ),
        examples=["id", "name"],
    )
    value: Any = Field(
        title="Filter value",
        description=(
            "Value to filter by. Must be instance of type, that stores in db in given field."
        ),
        examples=["id", "name"],
    )
    operator: AdvancedOperatorsLiteral = Field(
        default="=",
        title="Filter operator",
        description=(
            "Filter operator for given field and value. Choose it from enumerated values."
        ),
        examples=["=", ">"],
    )


def _convert_key_value_filters(filters: Any) -> list[dict[str, Any]]:  # noqa: ANN401
    """Check for dictionary or raise HTTPEXception error."""
    values_to_filter = [filters] if not isinstance(filters, list) else filters  # type: ignore
    errors: list[dict[str, Any]] = []
    for idx, _filter in enumerate(values_to_filter):  # type: ignore
        if not isinstance(_filter, dict) or not all_dict_keys_are_str(_filter):  # type: ignore
            errors.append(
                {
                    'type': 'json error',
                    'loc': ['json_element', str(idx)],
                    'msg': 'incorrect filter - is not object.',
                    'input': _filter,
                },
            )

    if len(errors) > 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=jsonable_encoder(errors),
        )
    return values_to_filter  # type: ignore


def get_advanced_filters(
    filters: Json[Any] | None = Query(
        None,
        title='Filters',
        description=(
            'Filters with following format: '
            '``[{"field": "field_name", "value": anyValue, "operator": "operator"}]``.'
        ),
    ),
) -> list[AdvancedFilterSchema]:
    """Depends, converts filters from JSON to pydantic schema."""
    res: list[AdvancedFilterSchema] = []
    try:
        if isinstance(filters, list):
            for _filter in filters:  # type: ignore
                res.append(AdvancedFilterSchema.model_validate(_filter))  # type: ignore
        else:
            res.append(AdvancedFilterSchema.model_validate(filters))  # type: ignore
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=jsonable_encoder(exc.errors()),
        ) from exc
    return res


def get_simple_filters(
    filters: Json[Any] | None = Query(
        None,
        title='Filters',
        description=(
            'Filters with ``{Key: Value}`` format, where ``Key`` - field of model to filter by '
            '``Value`` - value to filter by. Example: ``{"id": 25, "name": "name"}``.'
        ),
    ),
) -> list[dict[str, Any]]:
    """Depends, that validate given JSON as dict with str keys."""
    return _convert_key_value_filters(filters)


def get_django_filters(
    filters: Json[Any] | None = Query(
        None,
        title='Фильтры',
        description=(
            'Filters with ``{Key: Value}`` format, where ``Key`` - field of model to filter by '
            '``Value`` - value to filter by. Example: '
            '``{"id__exact": 25, "datetime_field__year__exact": 1995}``.\n\n'
            '``Attention!`` Django filters in current state does not support sub-lookups to '
            'related models and will not support because of security issues.'
        ),
    ),
) -> list[dict[str, Any]]:
    """Depends, that validate given JSON as dict with str keys."""
    return _convert_key_value_filters(filters)


def get_advanced_filter_dicts(
    filters: list[AdvancedFilterSchema] = Depends(get_advanced_filters),
) -> list[dict[str, Any]]:
    """Depends, converts filters from pydantic to dicts."""
    return [_filter.model_dump() for _filter in filters]


def advanced_converter_depends(model: "type[DeclarativeBase]") -> "GetSQLFiltersDepends":
    """Dependency fabric for advanced filters convert.

    You need to call this function and pass result in ``Depends`` like this:

    ```
    from typing import Sequence

    from sqlalchemy import ColumnElement
    from dev_utils.sqlalchemy.filters.ext.fastapi import advanced_converter_depends

    from myapp.models import MyModel

    router = APIRouter("/my-routes")
    advanced_filters_depends = advanced_converter_depends(MyModel)

    @router.get("/")
    def my_function(filters: Sequence[ColumnElement[bool]] = Depends(advanced_filters_depends)):
        stmt = select(MyModel).where(*filters)
        ...
    ```
    """

    def _get_filters(
        filters: list[dict[str, Any]] = Depends(get_advanced_filter_dicts),
    ) -> "Sequence[ColumnElement[bool]]":
        return AdvancedOperatorFilterConverter.convert(model, filters)

    return _get_filters


def simple_converter_depends(model: "type[DeclarativeBase]") -> "GetSQLFiltersDepends":
    """Dependency fabric for simple filters convert.

    You need to call this function and pass result in ``Depends`` like this:

    ```
    from typing import Sequence

    from sqlalchemy import ColumnElement
    from dev_utils.sqlalchemy.filters.ext.fastapi import simple_converter_depends

    from myapp.models import MyModel

    router = APIRouter("/my-routes")
    simple_filters_depends = simple_converter_depends(MyModel)

    @router.get("/")
    def my_function(filters: Sequence[ColumnElement[bool]] = Depends(simple_filters_depends)):
        stmt = select(MyModel).where(*filters)
        ...
    ```
    """

    def _get_filters(
        filters: list[dict[str, Any]] = Depends(get_simple_filters),
    ) -> "Sequence[ColumnElement[bool]]":
        return SimpleFilterConverter.convert(model, filters)

    return _get_filters


def django_converter_depends(model: "type[DeclarativeBase]") -> "GetSQLFiltersDepends":
    """Dependency fabric for django filters convert.

    You need to call this function and pass result in ``Depends`` like this:

    ```
    from typing import Sequence

    from sqlalchemy import ColumnElement
    from dev_utils.sqlalchemy.filters.ext.fastapi import django_converter_depends

    from myapp.models import MyModel

    router = APIRouter("/my-routes")
    django_filters_depends = django_converter_depends(MyModel)

    @router.get("/")
    def my_function(filters: Sequence[ColumnElement[bool]] = Depends(django_filters_depends)):
        stmt = select(MyModel).where(*filters)
        ...
    ```
    """

    def _get_filters(
        filters: list[dict[str, Any]] = Depends(get_django_filters),
    ) -> "Sequence[ColumnElement[bool]]":
        return DjangoLikeFilterConverter.convert(model, filters)

    return _get_filters
