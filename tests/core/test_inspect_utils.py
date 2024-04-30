import pytest

from dev_utils.core import utils

obj = object()


class MyObject:  # noqa: D101
    pass


@pytest.mark.parametrize(
    ("obj", "expected_result"),
    [
        (obj, "object"),
        (MyObject, "tests.core.test_inspect_utils.MyObject"),
        (MyObject(), "tests.core.test_inspect_utils.MyObject"),
    ],
)
def test_get_object_class_absolute_name(obj: object, expected_result: str) -> None:
    assert utils.get_object_class_absolute_name(obj) == expected_result
