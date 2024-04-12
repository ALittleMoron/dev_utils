"""FastAPI custom middlewares package.

Contains different middlewares (now only sqlalchemy profiling middlewares).
"""

from .sqlalchemy_profiling import add_query_counter_middleware as add_query_counter_middleware
from .sqlalchemy_profiling import add_query_profiling_middleware as add_query_profiling_middleware
