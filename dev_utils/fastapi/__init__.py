"""FastAPI utils package.

Contains middlewares and verbose HTTP exception extensions.
"""

from .middlewares.sqlalchemy_profiling import (
    add_query_counter_middleware as add_query_counter_middleware,
)
from .middlewares.sqlalchemy_profiling import (
    add_query_profiling_middleware as add_query_profiling_middleware,
)
