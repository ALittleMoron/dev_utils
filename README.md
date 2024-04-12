
# Dev utils

![coverage](./coverage.svg)

## For what?

I made this project to avoid copy-pasting with utils in my projects. I was aiming to simplify
working with sqlalchemy, FastAPI and other libs.

## Profiling

Profiling utils. Now available 2 profilers and 2 middlewares (FastAPI) for such profilers:

1. SQLAlchemyQueryProfiler - profile entire sqlalchemy query - it text, params, duration.
2. SQLAlchemyQueryCounter - count sqlalchemy queries.

## SQLAlchemy Filters

Converters for SQLAlchemy filters. Now available 3 converters:

1. Simple filter converter (key-value with equals operator).
2. Advanced filter converter (key-value with custom operators).
3. Django filter converter (Django filters adapter with double underscore lookups).

Filters must be provided in a dict or list or dicts and will be applied sequentially.

### Simple filters

Simple filters are simle. There are `key` - `value` dicts (you can use one dict with all filters,
or list of dicts. There is no difference), which converts to SQLAlchemy filters with `==` operator.

``` python
filter_spec = [
    {'field_name_1': 123, 'field_name_2': 'value'},
    {'other_name_1': 'other_name', 'other_name_2': 123},
    # ...
]
```

No other specific usages presents. it is simple.

### Advanced filters

Advanced filters continues the idea of simple-filter, but add operator key.

This is the list of operators that can be used:

- `=`
- `>`
- `<`
- `>`'
- `<=`
- `is`
- `is_not`
- `between`
- `contains`

### Django filters

Django filters implements django ORM adapter for filters.

Now implements all field filters, except nester models.

This is the list of operators that can be used:

- `exact`
- `iexact`
- `contains`
- `icontains`
- `in`
- `gt`
- `gte`
- `lt`
- `lte`
- `startswith`
- `istartswith`
- `endswith`
- `iendswith`
- `range`
- `date`
- `year`
- `iso_year`
- `month`
- `day`
- `week`
- `week_day`
- `iso_week_day`
- `quarter`
- `time`
- `hour`
- `minute`
- `second`
- `isnull`
- `regex`
- `iregex`
