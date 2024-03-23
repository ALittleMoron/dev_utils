import enum
import operator as builtin_operator
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Callable, TypeGuard, final

from abstractcp import Abstract, abstract_class_property
from sqlalchemy.sql.elements import ColumnElement

from dev_utils.core.exc import FilterError
from dev_utils.core.utils import get_sqlalchemy_attribute, get_valid_field_names
from dev_utils.sqlalchemy_filters import operators as custom_operator
from dev_utils.sqlalchemy_filters.guards import is_dict_simple_filter_dict

if TYPE_CHECKING:
    from sqlalchemy.orm import DeclarativeBase, QueryableAttribute
IsValid = bool
Message = str
FilterDict = dict[str, Any]
SQLAlchemyFilter = ColumnElement[bool]
OperatorFunction = Callable[[Any, Any], SQLAlchemyFilter]
NestedFilterNames = set[str]
LookupMapping = dict[enum.Enum | str, OperatorFunction]
LookupMappingWithNested = dict[enum.Enum | str, tuple[OperatorFunction, NestedFilterNames]]
AnyLookupMapping = LookupMapping | LookupMappingWithNested

empty_nested_filter_names: NestedFilterNames = set()


def has_nested_lookups(value: AnyLookupMapping) -> TypeGuard[LookupMappingWithNested]:
    return True


class BaseFilterConverter(ABC, Abstract):
    """Base class for filter converters."""

    lookup_mapping: AnyLookupMapping = abstract_class_property(LookupMapping)

    @classmethod
    @abstractmethod
    def _is_filter_valid(
        cls,
        model: type["DeclarativeBase"],
        filter_: FilterDict,
    ) -> tuple[IsValid, Message]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def _convert_filter(
        cls,
        model: type["DeclarativeBase"],
        filter_: FilterDict,
    ) -> Sequence[SQLAlchemyFilter]:
        raise NotImplementedError

    @classmethod
    @final
    def convert(
        cls,
        model: type["DeclarativeBase"],
        filters: FilterDict
        | ColumnElement[bool]
        | Sequence[FilterDict | ColumnElement[bool]]
        | None = None,
    ) -> Sequence[SQLAlchemyFilter]:
        """Convert input dict or list of dicts to SQLAlchemy filter."""
        result: Sequence[SQLAlchemyFilter] = []
        if filters is None:
            return result
        if not isinstance(filters, Sequence):
            filters = [filters]
        for filter_ in filters:
            if isinstance(filter_, ColumnElement):
                result.append(filter_)
                continue
            is_valid, message = cls._is_filter_valid(model, filter_)
            if not is_valid:
                msg = f'Filter with data {filter_} is not valid: {message}'
                raise FilterError(msg)
            result.extend(cls._convert_filter(model, filter_))
        return result


class SimpleFilterConverter(BaseFilterConverter):
    """Simple filter converter, that works with pairs ``"field"-"value"``.

    ...
    """

    lookup_mapping = {}  # no needs for it.

    @classmethod
    def _is_filter_valid(
        cls,
        model: type["DeclarativeBase"],
        filter_: FilterDict,
    ) -> tuple[IsValid, Message]:
        for field_name in filter_:
            if field_name not in get_valid_field_names(model):
                return False, f'Model or select statement {model} has no field "{field_name}".'
        return True, ''

    @classmethod
    def _convert_filter(
        cls,
        model: type["DeclarativeBase"],
        filter_: FilterDict,
    ) -> Sequence[SQLAlchemyFilter]:
        operator_func = builtin_operator.eq
        sqlalchemy_filters: Sequence[SQLAlchemyFilter] = []
        for field_name, value in filter_.items():
            sqlalchemy_field = get_sqlalchemy_attribute(model, field_name)
            sqlalchemy_filters.append(operator_func(sqlalchemy_field, value))
        return sqlalchemy_filters


class AdvancedOperatorFilterConverter(BaseFilterConverter):
    lookup_mapping: LookupMapping = {  # type: ignore
        '==': builtin_operator.eq,
        '>': builtin_operator.gt,
        '<': builtin_operator.lt,
        '>=': builtin_operator.ge,
        '<=': builtin_operator.le,
        'is': custom_operator.is_,
        'is_not': custom_operator.is_not,
        'between': custom_operator.between,
        'contains': custom_operator.contains,
        # TODO: добавить валидацию значений.
        # Например, для between, чтобы передавать строго 2 значения, иначе FilterError.
    }

    @classmethod
    def _is_filter_valid(
        cls,
        model: type["DeclarativeBase"],
        filter_: FilterDict,
    ) -> tuple[IsValid, Message]:
        if not is_dict_simple_filter_dict(filter_):
            return False, 'filter dict is not subtype of OperatorFilterDict.'
        field = filter_['field']
        if field not in get_valid_field_names(model):
            return False, f'Model or select statement {model} has no field "{field}".'
        return True, ''

    @classmethod
    def _convert_filter(
        cls,
        model: type["DeclarativeBase"],
        filter_: FilterDict,
    ) -> Sequence[SQLAlchemyFilter]:
        if not is_dict_simple_filter_dict(filter_):
            msg = "Never situation. Don't use _convert_filter method directly!"
            raise FilterError(msg)
        operator_str = filter_['operator'] if 'operator' in filter_ else '=='
        operator_func = cls.lookup_mapping[operator_str]
        sqlalchemy_field = get_sqlalchemy_attribute(model, filter_['field'])
        return [operator_func(sqlalchemy_field, filter_['value'])]

    @classmethod
    def _recursive_apply_operator(
        cls,
        sqlalchemy_field: "QueryableAttribute[Any]",
        lookup: str,
        rest_lookups: list[str],
        value: Any,
    ) -> list[SQLAlchemyFilter]:
        if not has_nested_lookups(cls.lookup_mapping):
            operator_func = cls.lookup_mapping[lookup]
            return [operator_func(sqlalchemy_field, value)]
        operator_func, nested_filter_names = cls.lookup_mapping[lookup]


class DjangoLikeFilterConverter(BaseFilterConverter):
    lookup_mapping: LookupMappingWithNested = {  # type: ignore
        'exact': (custom_operator.django_exact, empty_nested_filter_names),
        'iexact': (custom_operator.django_iexact, empty_nested_filter_names),
        'contains': (custom_operator.django_contains, empty_nested_filter_names),
        'icontains': (custom_operator.django_icontains, empty_nested_filter_names),
        'in': (custom_operator.contains, empty_nested_filter_names),
        'gt': (builtin_operator.gt, empty_nested_filter_names),
        'gte': (builtin_operator.ge, empty_nested_filter_names),
        'lt': (builtin_operator.lt, empty_nested_filter_names),
        'lte': (builtin_operator.le, empty_nested_filter_names),
        'startswith': (custom_operator.django_startswith, empty_nested_filter_names),
        'istartswith': (custom_operator.django_istartswith, empty_nested_filter_names),
        'endswith': (custom_operator.django_endswith, empty_nested_filter_names),
        'iendswith': (custom_operator.django_iendswith, empty_nested_filter_names),
        'range': (custom_operator.django_range, empty_nested_filter_names),
        'date': (custom_operator.django_date, empty_nested_filter_names),
        'year': (custom_operator.django_year, empty_nested_filter_names),
        'iso_year': (custom_operator.django_iso_year, empty_nested_filter_names),
        'month': (custom_operator.django_month, empty_nested_filter_names),
        'day': (custom_operator.django_day, empty_nested_filter_names),
        'week': (custom_operator.django_week, empty_nested_filter_names),
        'week_day': (custom_operator.django_week_day, empty_nested_filter_names),
        'iso_week_day': (custom_operator.django_iso_week_day, empty_nested_filter_names),
        'quarter': (custom_operator.django_quarter, empty_nested_filter_names),
        'time': (custom_operator.django_time, empty_nested_filter_names),
        'hour': (custom_operator.django_hour, empty_nested_filter_names),
        'minute': (custom_operator.django_minute, empty_nested_filter_names),
        'second': (custom_operator.django_second, empty_nested_filter_names),
        'isnull': (custom_operator.django_isnull, empty_nested_filter_names),
        'regex': (custom_operator.django_regex, empty_nested_filter_names),
        'iregex': (custom_operator.django_iregex, empty_nested_filter_names),
        # TODO: добавить sub-lookups, по типу year__gre, time__range и т.д.
        # NOTE: можно добавить параметр suboperator, который по умолчанию будет ==.
        #       и далее можно переиспользовать эти все функции.
        # NOTE: либо можно доработать _convert_filter для разделения нескольких частей фильтра.
    }

    @classmethod
    def _is_filter_valid(
        cls,
        model: type["DeclarativeBase"],
        filter_: FilterDict,
    ) -> tuple[IsValid, Message]:
        for field in filter_:
            field_parts = field.split('__')
            if len(field_parts) == 1:
                field_name = field_parts[0]
                lookup = 'exact'
            elif len(field_parts) == 2:
                field_name, lookup = field_parts
            else:
                return (
                    False,
                    (
                        "DjangoLikeFilterConverter can't use nested filters or "
                        "related model filters yet."
                    ),
                )
            if field_name not in get_valid_field_names(model):
                return False, f'Model or select statement {model} has no field "{field_name}".'
            if lookup not in cls.lookup_mapping:
                all_lookup_mapping = list(cls.lookup_mapping.keys())
                message = f'Unexpected lookup "{lookup}".' f'Valid lookups: {all_lookup_mapping}.'
                return False, message
        return True, ''

    @classmethod
    def _convert_filter(
        cls,
        model: type["DeclarativeBase"],
        filter_: FilterDict,
    ) -> Sequence[SQLAlchemyFilter]:
        sqlalchemy_filters: Sequence[SQLAlchemyFilter] = []
        for field, value in filter_.items():
            field_parts = field.split('__')
            # TODO: добавить возможность фильтровать по связанным сущностям.
            if len(field_parts) == 1:
                field_name = field_parts[0]
                lookup = 'exact'
                rest_lookups: list[str] = []
            else:
                field_name, lookup, *rest_lookups = field_parts
            if not all(rest_lookup in cls.lookup_mapping for rest_lookup in rest_lookups):
                rest_lookups_str = ', '.join(rest_lookups)
                msg = (
                    f'Not all sub-lookups ({rest_lookups_str}) are in cls.lookup_mapping keys. '
                    'Perhaps, you tried to pass related model name to filter by it. Not it is not '
                    'possible. Use sub-lookups only for filtering inside main model (like '
                    'field__hour__gt=12 or something like this)'
                )
                raise FilterError(msg)
            operator_func, nested_filter_names = cls.lookup_mapping[lookup]
            sqlalchemy_field = get_sqlalchemy_attribute(model, field_name)
            sqlalchemy_filters.append(operator_func(sqlalchemy_field, value))
        return sqlalchemy_filters
