from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response

from dev_utils.fastapi.verbose_http_exceptions.exc import BaseVerboseHTTPException

INFO_START_DIGIT: int = ...
SUCCESS_START_DIGIT: int = ...
REDIRECT_START_DIGIT: int = ...
CLIENT_ERROR_START_DIGIT: int = ...
SERVER_ERROR_START_DIGIT: int = ...
error_mapping: dict[int, dict[str, Any]] = ...

async def verbose_http_exception_handler(_: Request, exc: BaseVerboseHTTPException) -> Response: ...
async def verbose_request_validation_error_handler(
    _: Request,
    exc: RequestValidationError,
) -> Response: ...
async def any_http_exception_handler(_: Request, exc: HTTPException) -> Response: ...
def apply_verbose_http_exception_handler(app: FastAPI) -> FastAPI: ...
def apply_all_handlers(app: FastAPI) -> FastAPI: ...
