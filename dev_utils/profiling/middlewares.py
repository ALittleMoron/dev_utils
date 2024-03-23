import uuid
from contextvars import ContextVar
from logging import Logger, getLogger

import_error_msg = (
    '{package} package is not installed. Use pip install dev_utils["profiling"] '
    'to solve it or install'
)

import queue

YAPPI_INSTALLED = False
try:
    import yappi
    from yappi import YFuncStats
except ImportError:
    YAPPI_INSTALLED = False
STARLETTE_INSTALLED = True
try:
    from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
    from starlette.requests import Request
    from starlette.responses import Response
    from starlette.types import ASGIApp
except ImportError:
    STARLETTE_INSTALLED = False
from . import profilers

yappi_request_id: ContextVar[str] = ContextVar('yappi_request_id')
yappi_request_id.set('-1')
default_logger = getLogger('profiling-middlewares')


def get_context_id() -> str:
    try:
        return yappi_request_id.get()
    except LookupError:
        return '-1'


yappi.set_context_id_callback(get_context_id)


class ProfilingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        calls_to_track: dict[str, str],
        logger: Logger = default_logger,
    ) -> None:
        self.calls_to_track = calls_to_track
        self.logger = logger
        super().__init__(app, None)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        ctx_id = str(uuid.uuid4())
        yappi_request_id.set(ctx_id)
        response = await call_next(request)

        tracked_stats: dict[str, YFuncStats] = {}
        for name, call_to_track in self.calls_to_track.items():
            tracked_stats[name] = yappi.get_func_stats({"name": call_to_track, "ctx_id": ctx_id})

        server_timing: list[str] = []
        for name, stats in tracked_stats.items():
            if not stats.empty():
                server_timing.append(f"{name};dur={(stats.pop().ttot * 1000):.3f}")
        if server_timing:
            profiling_message = ','.join(server_timing)
            self.logger.info(profiling_message)
            response.headers["Server-Timing"] = profiling_message
        return response


class SQLAlchemyQueryInfoMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, engine, logger: Logger = default_logger) -> None:
        self.collector: queue.Queue[profilers.QueryInfo] = queue.Queue(0)
        self.stats = []
        self.profiler = profilers.SQLAlchemyQueryProfiler()
        self.logger = logger
        super().__init__(app, None)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        ctx_id = str(uuid.uuid4())
        yappi_request_id.set(ctx_id)
        # TODO: start profiling
        response = await call_next(request)
        # TODO: get report
        # TODO: log report
        # TODO: options for report log (file, console, ...)
        return response
