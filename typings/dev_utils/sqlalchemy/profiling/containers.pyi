import traceback
from typing import Any, ClassVar

from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.sql import ClauseElement
from sqlalchemy.sql.compiler import Compiled

class QueryInfo:
    repr_full_query_text: ClassVar[bool] = ...
    repr_template: ClassVar[str] = ...
    def __init__(
        self,
        *,
        text: ClauseElement | Compiled,
        stack: list[traceback.FrameSummary],
        start_time: float,
        end_time: float,
        params_dict: dict[Any, Any],
        results: CursorResult[Any],
    ) -> None: ...
