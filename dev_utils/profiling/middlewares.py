from logging import Logger

from fastapi import FastAPI, Request
from sqlalchemy import Engine
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response

from dev_utils.core.logging import logger as default_logger
from dev_utils.profiling import profilers


def add_query_profiling_middleware(
    app: FastAPI,
    engine: Engine | type[Engine] = Engine,
    *,
    profiler_id: str | None = None,
    logger: Logger = default_logger,
    log_query_stats: bool = False,
) -> FastAPI:
    """Add query profiling middleware to FastAPI.

    Note: this function also can be used with starlette instance, but only before version 1.0.0,
    because `middleware` decorator is deprecated and will be (or, maybe, already removed) in this
    version.
    """

    async def _profiling_middleware(
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        with profilers.SQLAlchemyQueryProfiler(
            engine=engine,
            profiler_id=profiler_id,
            logger=logger,
            log_query_states=log_query_stats,
        ) as profiler:
            logger.info('Profiler %s: start profiling %s', profiler.profiler_id, request.url)
            response = await call_next(request)
        logger.info(
            'Profiler %s result: %s',
            profiler.profiler_id,
            profiler.collect(),
        )
        return response

    app.middleware("http")(_profiling_middleware)
    return app


def add_query_counter_middleware(
    app: FastAPI,
    engine: Engine | type[Engine] = Engine,
    *,
    profiler_id: str | None = None,
    logger: Logger = default_logger,
    log_query_stats: bool = False,
) -> FastAPI:
    """Add query counting middleware to FastAPI.

    Note: this function also can be used with starlette instance, but only before version 1.0.0,
    because `middleware` decorator is deprecated and will be (or, maybe, already removed) in this
    version.
    """

    async def _counter_middleware(
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        with profilers.SQLAlchemyQueryCounter(
            engine=engine,
            profiler_id=profiler_id,
            logger=logger,
            log_query_states=log_query_stats,
        ) as profiler:
            logger.info(
                'Counter %s: start counting queries for %s',
                profiler.profiler_id,
                request.url,
            )
            response = await call_next(request)
        logger.info(
            'Counter: %s. Count of queries for %s: %s',
            profiler.profiler_id,
            request.url,
            profiler.collect(),
        )
        return response

    app.middleware("http")(_counter_middleware)
    return app
