"""Handlers for FastAPI."""

from typing import TYPE_CHECKING, Any

from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response

from dev_utils.core.guards import all_dict_keys_are_str
from dev_utils.fastapi.verbose_http_exceptions.exc import (
    BaseVerboseHTTPException,
    NestedErrorsMainHTTPException,
    RequestValidationVerboseHTTPException,
)
from dev_utils.fastapi.verbose_http_exceptions.utils import resolve_error_location_and_attr

if TYPE_CHECKING:
    from fastapi import Request


INFO_START_DIGIT = 1
SUCCESS_START_DIGIT = 2
REDIRECT_START_DIGIT = 3
CLIENT_ERROR_START_DIGIT = 4
SERVER_ERROR_START_DIGIT = 5
error_mapping: dict[int, dict[str, Any]] = {
    INFO_START_DIGIT: {
        "code": "info",
        "type": "info",
        "location": None,
        "attr": None,
    },
    SUCCESS_START_DIGIT: {
        "code": "success",
        "type": "success",
        "location": None,
        "attr": None,
    },
    REDIRECT_START_DIGIT: {
        "code": "redirect",
        "type": "redirect",
        "location": None,
        "attr": None,
    },
    CLIENT_ERROR_START_DIGIT: {
        "code": "client_error",
        "type": "client_error",
        "location": None,
        "attr": None,
    },
    SERVER_ERROR_START_DIGIT: {
        "code": "server_error",
        "type": "server_error",
        "location": None,
        "attr": None,
    },
}


async def verbose_http_exception_handler(
    _: "Request",
    exc: "BaseVerboseHTTPException",
) -> "Response":
    """Handle verbose HTTP exception output.

    Handle only BaseVerboseHTTPException inherited instances. For handling all exceptions use
    ``any_http_exception_handler``.
    """
    return JSONResponse(status_code=exc.status_code, content=exc.as_dict(), headers=exc.headers)


async def verbose_request_validation_error_handler(
    _: "Request",
    exc: "RequestValidationError",
) -> "Response":
    """Handle RequestValidationError to override 422 error."""
    main_error = NestedErrorsMainHTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    nested_errors: list[RequestValidationVerboseHTTPException] = []
    for error in exc.errors():
        if not isinstance(error, dict) or not all_dict_keys_are_str(error):  # type: ignore  # pragma: no coverage
            continue
        location, attribute = resolve_error_location_and_attr(error)
        nested_errors.append(
            RequestValidationVerboseHTTPException(
                type_=error.get("type") or "not_known_type",
                message=error.get("msg") or "not_known_message",
                location=location,
                attr_name=attribute,
            ),
        )
    return JSONResponse(
        status_code=main_error.status_code,
        content=main_error.as_dict(nested_errors=nested_errors),
    )


async def any_http_exception_handler(
    _: "Request",
    exc: "HTTPException",
) -> "Response":
    """Handle any HTTPException errors (BaseVerboseHTTPException too).

    Doesn't handle 422 request error. Use ``verbose_request_validation_error_handler`` for it.
    """
    if isinstance(exc, BaseVerboseHTTPException):
        return JSONResponse(status_code=exc.status_code, content=exc.as_dict(), headers=exc.headers)
    content = error_mapping[exc.status_code // 100]
    content["message"] = exc.detail
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        headers=exc.headers,
    )


def apply_verbose_http_exception_handler(app: FastAPI) -> FastAPI:
    """Apply verbose_http_exception_handler on given FastAPI instance."""
    app.add_exception_handler(
        BaseVerboseHTTPException,
        verbose_http_exception_handler,  # type: ignore
    )
    return app


def apply_all_handlers(app: FastAPI) -> FastAPI:
    """Apply all exception handlers on given FastAPI instance.

    not apply ``verbose_http_exception_handler`` because BaseVerboseHTTPException is handled by
    any_http_exception_handler.
    """
    app.add_exception_handler(
        HTTPException,
        any_http_exception_handler,  # type: ignore
    )
    app.add_exception_handler(
        RequestValidationError,
        verbose_request_validation_error_handler,  # type: ignore
    )
    return app
