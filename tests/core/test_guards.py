from typing import Any, Sequence

import pytest

from dev_utils.core import guards


@pytest.mark.parametrize(
    ("_dct", "expected_result"),
    [
        ({"a": 1, "b": 2}, True),
        ({1: 1, 2: 2}, False),
        ({"a": 1, 2: 2}, False),
        ({True: 1, False: 0}, False),
        ({"a__isnull": True, "b__icontains": [1, 2, 3]}, True),
    ],
)
def test_all_dict_keys_are_str(_dct: dict[Any, Any], expected_result: bool) -> None:  # noqa
    assert guards.all_dict_keys_are_str(_dct) == expected_result


@pytest.mark.parametrize(
    ("seq", "expected_result"),
    [
        ("abc", True),
        (["a", "b", "c"], True),
        (["a", "b", 3], False),
    ],
)
def test_all_elements_in_sequence_are_str(
    seq: Sequence[Any],
    expected_result: bool,  # noqa
) -> None:  # noqa
    assert guards.all_elements_in_sequence_are_str(seq) is expected_result
