import queue
import time
import traceback
import uuid
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from contextlib import suppress
from logging import Logger
from types import TracebackType
from typing import TYPE_CHECKING, Any, Generic, Self, TypeVar, final

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine

from dev_utils.core.guards import all_dict_keys_are_str
from dev_utils.core.logging import logger as default_logger
from dev_utils.core.utils import trim_and_plain_text
from dev_utils.profiling.containers import QueryInfo

if TYPE_CHECKING:
    from sqlalchemy.engine import Connection
    from sqlalchemy.engine.cursor import CursorResult
    from sqlalchemy.sql import ClauseElement
    from sqlalchemy.sql.compiler import SQLCompiler
    from sqlalchemy.util import immutabledict

T = TypeVar('T')


class BaseSQLAlchemyProfiler(ABC, Generic[T]):
    """Abstract base sqlalchemy profiling class.

    It is a generic class, so use it with typing. Generic uses in:

    * ``__init__``: self.collector - queue of ``<Generic>`` objects. For example, it could be
        queue of QueryInfo objects.
    * ``collect``: return value - Sequence of ``<Generic>``.
    """

    def __init__(
        self,
        engine: 'type[Engine] | Engine | AsyncEngine' = Engine,
        *,
        profiler_id: str | None = None,
        logger: Logger = default_logger,
        log_query_states: bool = False,
    ) -> None:
        self.started = False
        if isinstance(engine, AsyncEngine):
            self.engine = engine.sync_engine
        else:
            self.engine = engine
        self.logger = logger
        self.log_query_states = log_query_states

        self.profiler_id = profiler_id if profiler_id is not None else str(uuid.uuid4())

        self._result: T | None = None
        self.collector: queue.Queue[T] = queue.Queue()

    @abstractmethod
    def _before_exec(
        self,
        conn: 'Connection',
        clause: 'SQLCompiler',
        multiparams: 'Sequence[Mapping[str, Any]]',  # noqa: F841
        params: 'Mapping[str, Any]',
        execution_options: 'immutabledict[str, Any]',  # noqa: F841
    ) -> None:
        """Method, which will be bounded to `before_execute` handler in SQLAlchemy."""  # noqa: D401
        raise NotImplementedError()

    @abstractmethod
    def _after_exec(
        self,
        conn: 'Connection',
        clause: 'ClauseElement',
        multiparams: 'Sequence[Mapping[str, Any]]',  # noqa: F841
        params: 'Mapping[str, Any]',
        execution_options: 'immutabledict[str, Any]',  # noqa: F841
        results: 'CursorResult[Any]',
    ) -> None:
        """Method, which will be bounded to `after_execute` handler in SQLAlchemy."""  # noqa: D401
        raise NotImplementedError()

    @final
    def _extract_parameters_from_results(
        self,
        query_results: 'CursorResult[Any]',
    ) -> dict[str, Any]:
        """Get parameters from query results object."""
        params_dict: dict[str, Any] = {}
        compiled_parameters = getattr(query_results.context, 'compiled_parameters', [])
        if not compiled_parameters or not isinstance(  # pragma: no cover
            compiled_parameters,
            Sequence,
        ):
            return {}
        for compiled_param_dict in compiled_parameters:
            if not isinstance(compiled_param_dict, dict):  # pragma: no cover
                continue
            if not all_dict_keys_are_str(compiled_param_dict):  # type: ignore  pragma: no cover
                continue
            params_dict.update(compiled_param_dict)
        return params_dict

    def start(self) -> None:
        """Start the profiling process.

        Add engine-level handlers from events, which will fill collector with data.
        """
        if self.started is True:  # pragma: no cover
            msg = "Profiling session is already started!"
            self.logger.warning(msg)

        self.started = True
        if not event.contains(self.engine, "before_execute", self._before_exec):
            event.listen(self.engine, "before_execute", self._before_exec)
        if not event.contains(self.engine, "after_execute", self._after_exec):
            event.listen(self.engine, "after_execute", self._after_exec)

    def stop(self) -> None:
        """Stop the profiling process.

        Remove engine-level handlers from events - no other data will be put in collector.
        """
        if self.started is False:  # pragma: no cover
            msg = "Profiling session is already stopped"
            self.logger.warning(msg)

        self.started = False
        if event.contains(self.engine, "before_execute", self._before_exec):
            event.remove(self.engine, "before_execute", self._before_exec)
        if event.contains(self.engine, "after_execute", self._after_exec):
            event.remove(self.engine, "after_execute", self._after_exec)

    def __enter__(self) -> Self:
        """Enter of context manager.

        Start the profiler by executing ``self.start()`` method.
        """
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,  # noqa: F841
        exc: BaseException | None,  # noqa: F841
        traceback: TracebackType | None,  # noqa: F841
    ) -> None:
        """Exit of context manager.

        Stop the profiler by executing ``self.stop()`` method.
        """
        self.stop()

    def collect(self) -> Sequence[T]:
        """Collect all information from queue.

        Collect means "transform to list". You can override this method, if you want to return
        other type. Use self._result as return value and assign this attribute in profiling methods.
        """
        queries: list[T] = []
        with suppress(queue.Empty):
            while True:
                queries.append(self.collector.get(block=False))

        return queries


class SQLAlchemyQueryProfiler(BaseSQLAlchemyProfiler[QueryInfo]):
    """SQLAlchemy query profiler."""

    def _before_exec(
        self,
        conn: 'Connection',
        clause: 'SQLCompiler',
        multiparams: 'Sequence[Mapping[str, Any]]',  # noqa: F841
        params: 'Mapping[str, Any]',
        execution_options: 'immutabledict[str, Any]',  # noqa: F841
    ) -> None:
        conn.info.setdefault("query_start_time", []).append(time.time())
        if self.log_query_states:  # pragma: no cover
            msg = (
                f'Profiler {self.profiler_id}. '
                f'Query started: {trim_and_plain_text(str(clause))}. Params: {params}'
            )
            self.logger.info(msg)

    def _after_exec(
        self,
        conn: 'Connection',
        clause: 'ClauseElement',
        multiparams: 'Sequence[Mapping[str, Any]]',  # noqa: F841
        params: 'Mapping[str, Any]',
        execution_options: 'immutabledict[str, Any]',  # noqa: F841
        results: 'CursorResult[Any]',
    ) -> None:
        end_time = time.time()
        start_time = conn.info["query_start_time"].pop(-1)
        if self.log_query_states:  # pragma: no cover
            msg = (
                f'Profiler {self.profiler_id}. '
                f'Query "{trim_and_plain_text(str(clause))}" (params: {params}) '
                f'finished in {(end_time - start_time) * 1000} milliseconds.'
            )
            self.logger.info(msg)

        text = clause
        with suppress(AttributeError):
            text = clause.compile(dialect=conn.engine.dialect)

        params_dict = self._extract_parameters_from_results(results)

        stack = traceback.extract_stack()[:-1]
        query_info = QueryInfo(
            text=text,
            stack=stack,
            start_time=start_time,
            end_time=end_time,
            params_dict=params_dict,
            results=results,
        )

        self.collector.put(query_info)


class SQLAlchemyQueryCounter(BaseSQLAlchemyProfiler[int]):
    """SQLAlchemy query counter."""

    def collect(self) -> int:  # type: ignore  # noqa: D102
        if self._result is None:  # pragma: no cover
            return 0
        return self._result

    def _before_exec(
        self,
        conn: 'Connection',
        clause: 'SQLCompiler',
        multiparams: 'Sequence[Mapping[str, Any]]',  # noqa: F841
        params: 'Mapping[str, Any]',
        execution_options: 'immutabledict[str, Any]',  # noqa: F841
    ) -> None:
        if self._result is None:  # pragma: no cover
            self._result = 0
        self._result += 1

    def _after_exec(
        self,
        conn: 'Connection',
        clause: 'ClauseElement',
        multiparams: 'Sequence[Mapping[str, Any]]',  # noqa: F841
        params: 'Mapping[str, Any]',
        execution_options: 'immutabledict[str, Any]',  # noqa: F841
        results: 'CursorResult[Any]',
    ) -> None:
        pass

    def start(self) -> None:  # noqa: D102
        if not self.started:  # pragma: no cover
            self._result = 0
        return super().start()
