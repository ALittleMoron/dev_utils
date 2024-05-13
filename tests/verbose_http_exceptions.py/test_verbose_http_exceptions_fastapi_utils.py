from typing import Any

import pytest

from dev_utils.verbose_http_exceptions.exc import RequestValidationVerboseHTTPException
from dev_utils.verbose_http_exceptions.ext.fastapi import utils as verbose_http_exceptions_utils


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
def test_resolve_errors(
    value: dict[str, Any],
    expected_result: tuple[str | None, str | None],
) -> None:
    assert verbose_http_exceptions_utils.resolve_error_location_and_attr(value) == expected_result


@pytest.mark.parametrize(
    ("error", "expected_result"),
    [
        (
            {'loc': ("loc", "attr"), "type": "validation_error", "msg": "message"},
            RequestValidationVerboseHTTPException(
                location="loc",
                attr_name="attr",
                message="message",
                type_="validation_error",
            ),
        ),
    ],
)
def test_validation_error_from_error_dict(
    error: dict[str, Any],
    expected_result: RequestValidationVerboseHTTPException,
) -> None:
    assert (
        verbose_http_exceptions_utils.validation_error_from_error_dict(error).as_dict()
        == expected_result.as_dict()
    )
