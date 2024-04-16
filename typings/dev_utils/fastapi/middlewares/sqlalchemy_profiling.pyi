from logging import Logger
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy import Engine

def add_query_profiling_middleware(
    app: FastAPI,
    engine: Engine | type[Engine] = ...,
    *,
    profiler_id: str | None = ...,
    logger: Logger = ...,
    report_to: str | Logger | Path = ...,
    log_query_stats: bool = ...,
) -> FastAPI: ...
def add_query_counter_middleware(
    app: FastAPI,
    engine: Engine | type[Engine] = ...,
    *,
    profiler_id: str | None = ...,
    logger: Logger = ...,
    log_query_stats: bool = ...,
) -> FastAPI: ...
