"""
This type stub file was generated by pyright.
"""

import enum
from abc import ABC
from collections.abc import Sequence
from typing import Any, TypeAlias, final

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.elements import ColumnElement

from dev_utils.core.abstract import Abstract
from dev_utils.sqlalchemy.filters import operators as custom_operator

IsValid = bool
Message = str
FilterDict: TypeAlias = dict[str, Any]
SQLAlchemyFilter: TypeAlias = ColumnElement[bool]
OperatorFunction = custom_operator.OperatorFunctionProtocol
NestedFilterNames: TypeAlias = set[str]
LookupMapping: TypeAlias = dict[enum.Enum | str, OperatorFunction]
LookupMappingWithNested: TypeAlias = dict[
    enum.Enum | str,
    tuple[OperatorFunction, NestedFilterNames],
]
AnyLookupMapping: TypeAlias = LookupMapping | LookupMappingWithNested
empty_nested_filter_names: NestedFilterNames = ...
django_nested_filter_names: NestedFilterNames = ...

def execute_operator_function(
    func: OperatorFunction,
    a: Any,
    b: Any,
    subproduct_use: bool = ...,  # noqa: FBT001
) -> Any: ...

class BaseFilterConverter(ABC, Abstract):

    lookup_mapping: AnyLookupMapping = ...
    @classmethod
    @final
    def convert(
        cls,
        model: type[DeclarativeBase],
        filters: (
            FilterDict | ColumnElement[bool] | Sequence[FilterDict | ColumnElement[bool]] | None
        ) = ...,
    ) -> Sequence[SQLAlchemyFilter]: ...

class SimpleFilterConverter(BaseFilterConverter):
    lookup_mapping = ...

class AdvancedOperatorFilterConverter(BaseFilterConverter):
    lookup_mapping: LookupMapping = ...  # type: ignore

class DjangoLikeFilterConverter(BaseFilterConverter):
    lookup_mapping: LookupMappingWithNested = ...  # type: ignore