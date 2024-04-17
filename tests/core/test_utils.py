import datetime
import zoneinfo

import pytest
from freezegun import freeze_time

from dev_utils.core import utils
from tests.utils import generate_datetime_list

obj = object()


class MyObject:  # noqa: D101
    pass


@pytest.mark.parametrize(
    "dt",
    generate_datetime_list(n=10, tz=zoneinfo.ZoneInfo("UTC")),
)
def test_get_utc_now(dt: datetime.datetime) -> None:  # noqa
    with freeze_time(dt):
        assert utils.get_utc_now() == dt


@pytest.mark.parametrize(
    ("obj", "expected_result"),
    [
        (obj, "object"),
        (MyObject, "tests.core.test_utils.MyObject"),
        (MyObject(), "tests.core.test_utils.MyObject"),
    ],
)
def test_get_object_class_absolute_name(obj: object, expected_result: str) -> None:
    assert utils.get_object_class_absolute_name(obj) == expected_result


@pytest.mark.parametrize(
    ("obj", "expected_result"),
    [
        ("                 abc                ", "abc"),
        ("                 abc\nabc                ", "abc abc"),
        ("                 abc  abc                ", "abc abc"),
        ("                 abc   abc                ", "abc abc"),
    ],
)
def test_trim_and_plain_text(obj: str, expected_result: str) -> None:
    assert utils.trim_and_plain_text(obj) == expected_result
