from typing import TYPE_CHECKING, Literal

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from dev_utils.verbose_http_exceptions.exc import ServerErrorVerboseHTTPException
from dev_utils.verbose_http_exceptions.ext.fastapi.handlers import (
    apply_all_handlers,
    apply_verbose_http_exception_handler,
)

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture()
def test_app_only_verbose() -> "Generator[TestClient, None, None]":
    app = FastAPI()

    @app.get("/")
    def index():  # type: ignore  # noqa: ANN202
        raise ServerErrorVerboseHTTPException(reason="test")

    apply_verbose_http_exception_handler(app)

    with TestClient(
        app=app,
        base_url="http://test/",
    ) as c:
        yield c


@pytest.fixture()
def test_app_all_verbose() -> "Generator[TestClient, None, None]":
    app = FastAPI()

    @app.get("/")
    def index(a: Literal[1, 2], b: Literal[25]):  # type: ignore  # noqa: ANN202
        return {"message": "abc"}

    @app.get("/error")
    def error():  # type: ignore  # noqa: ANN202
        raise HTTPException(status_code=500, detail="test detail")

    @app.get("/verbose_error")
    def verbose_error():  # type: ignore  # noqa: ANN202
        raise ServerErrorVerboseHTTPException(reason="test")

    apply_all_handlers(app)

    with TestClient(
        app=app,
        base_url="http://test/",
    ) as c:
        yield c
