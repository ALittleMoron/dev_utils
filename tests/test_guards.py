from typing import Any

import pytest

from dev_utils.sqlalchemy_filters import converters, guards

any_value = object()


@pytest.mark.parametrize(
    ('_dct', 'expected_result'),
    [
        ({'a': 1, 'b': 2}, True),
        ({1: 1, 2: 2}, False),
        ({'a': 1, 2: 2}, False),
        ({True: 1, False: 0}, False),
        ({'a__isnull': True, 'b__icontains': [1, 2, 3]}, True),
    ],
)
def test_all_dict_keys_are_str(_dct: dict[Any, Any], expected_result: bool) -> None:  # noqa
    assert guards.all_dict_keys_are_str(_dct) == expected_result


@pytest.mark.parametrize(
    ('_dct', 'expected_result'),
    [
        ({'field': 'abc', 'value': any_value, 'operator': '>'}, True),
        ({'field': 'abc', 'value': any_value}, True),
        ({'field': 125, 'value': any_value}, False),
        ({'field': 125, 'value': any_value, 'operator': '>'}, False),
        ({'field': 'abc', 'value': any_value, 'operator': 'pow'}, False),  # no such operator
        ({'field': 'abc', 'operator': '>'}, False),  # no value
    ],
)
def test_is_dict_simple_filter_dict(_dct: dict[Any, Any], expected_result: bool) -> None:  # noqa
    assert guards.is_dict_simple_filter_dict(_dct) == expected_result


@pytest.mark.parametrize(
    ('_dct', 'expected_result'),
    [
        (converters.SimpleFilterConverter.lookup_mapping, False),
        (converters.AdvancedOperatorFilterConverter.lookup_mapping, False),
        (converters.DjangoLikeFilterConverter.lookup_mapping, True),
    ],
)
def test_has_nested_lookups(_dct: dict[Any, Any], expected_result: bool) -> None:  # noqa
    assert guards.has_nested_lookups(_dct) == expected_result
