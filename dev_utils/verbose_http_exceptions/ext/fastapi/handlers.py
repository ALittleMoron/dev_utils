"""Handlers for FastAPI."""

from typing import TYPE_CHECKING

from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response

from dev_utils.core.guards import all_dict_keys_are_str
from dev_utils.verbose_http_exceptions.constants import ERROR_MAPPING
from dev_utils.verbose_http_exceptions.exc import (
    BaseVerboseHTTPException,
    NestedErrorsMainHTTPException,
    RequestValidationVerboseHTTPException,
)
from dev_utils.verbose_http_exceptions.ext.fastapi.openapi_override import (
    override_422_error,
)
from dev_utils.verbose_http_exceptions.ext.fastapi.utils import validation_error_from_error_dict

if TYPE_CHECKING:
    from fastapi import Request


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
    errors = exc.errors()
    if len(errors) == 1:  # pragma: no coverage
        error = errors[0]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=validation_error_from_error_dict(error).as_dict(),
        )
    for error in exc.errors():
        if not isinstance(error, dict) or not all_dict_keys_are_str(error):  # type: ignore  # pragma: no coverage
            continue
        nested_errors.append(validation_error_from_error_dict(error))
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
    content = ERROR_MAPPING[exc.status_code // 100]
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


def apply_all_handlers(app: FastAPI, *, override_422_openapi: bool = True) -> FastAPI:
    """Apply all exception handlers on given FastAPI instance.

    not apply ``verbose_http_exception_handler`` because BaseVerboseHTTPException is handled by
    any_http_exception_handler.
    """
    app.add_exception_handler(
        BaseVerboseHTTPException,
        verbose_http_exception_handler,  # type: ignore
    )
    app.add_exception_handler(
        HTTPException,
        any_http_exception_handler,  # type: ignore
    )
    app.add_exception_handler(
        RequestValidationError,
        verbose_request_validation_error_handler,  # type: ignore
    )
    if override_422_openapi:  # pragma: no coverage
        override_422_error(app)
    return app
