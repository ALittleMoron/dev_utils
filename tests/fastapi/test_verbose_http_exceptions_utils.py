from typing import Any

import pytest

from dev_utils.fastapi.verbose_http_exceptions import utils as verbose_http_exceptions_utils


@pytest.mark.parametrize(
    ("value", "expected_result"),
    [
        (
            {},
            (None, None),
        ),
        (
            {"loc": None},
            (None, None),
        ),
        (
            {"loc": ("loc",)},
            ("loc", None),
        ),
        (
            {"loc": ("loc", "attr")},
            ("loc", "attr"),
        ),
        (
            {"loc": ("loc", "sub loc", "attr")},
            ("loc -> sub loc", "attr"),
        ),
    ],
)
def test(value: dict[str, Any], expected_result: tuple[str | None, str | None]):
    assert verbose_http_exceptions_utils.resolve_error_location_and_attr(value) == expected_result
