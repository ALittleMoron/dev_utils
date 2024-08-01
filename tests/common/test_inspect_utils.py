import pytest

from dev_utils.common import inspect

obj = object()


class MyObject:  # noqa: D101
    pass


@pytest.mark.parametrize(
    ("obj", "expected_result"),
    [
        (obj, "object"),
        (MyObject, "tests.common.test_inspect_utils.MyObject"),
        (MyObject(), "tests.common.test_inspect_utils.MyObject"),
    ],
)
def test_get_object_class_absolute_name(obj: object, expected_result: str) -> None:
    assert inspect.get_object_class_absolute_name(obj) == expected_result
