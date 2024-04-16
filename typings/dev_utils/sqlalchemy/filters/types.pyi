from typing import Any, Literal, NotRequired, TypeAlias, TypedDict

DjangoOperatorsLiteral: TypeAlias = Literal[
    "exact",
    "iexact",
    "contains",
    "icontains",
    "in",
    "gt",
    "gte",
    "lt",
    "lte",
    "startswith",
    "istartswith",
    "endswith",
    "iendswith",
    "range",
    "date",
    "year",
    "iso_year",
    "month",
    "day",
    "week",
    "week_day",
    "iso_week_day",
    "quarter",
    "time",
    "hour",
    "minute",
    "second",
    "isnull",
    "regex",
    "iregex",
]
DjangoOperatorsSet: set[DjangoOperatorsLiteral] = ...
AdvancedOperatorsLiteral: TypeAlias = Literal["=", ">", "<", ">=", "<=", "between", "contains"]
AdvancedOperatorsSet: set[AdvancedOperatorsLiteral] = ...
FilterConverterStrategiesLiteral: TypeAlias = Literal["simple", "advanced", "django"]
FilterConverterStrategiesSet: set[FilterConverterStrategiesLiteral] = ...

class OperatorFilterDict(TypedDict):
    field: str
    value: Any
    operator: NotRequired[AdvancedOperatorsLiteral]
