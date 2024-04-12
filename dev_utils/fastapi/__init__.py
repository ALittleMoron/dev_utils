"""FastAPI utils package.

Contains middlewares and verbose HTTP exception extensions.
"""

from .middlewares.sqlalchemy_profiling import (
    add_query_counter_middleware as add_query_counter_middleware,
)
from .middlewares.sqlalchemy_profiling import (
    add_query_profiling_middleware as add_query_profiling_middleware,
)
from .verbose_http_exceptions.exc import BaseVerboseHTTPException as BaseVerboseHTTPException
from .verbose_http_exceptions.exc import ClientVerboseHTTPException as ClientVerboseHTTPException
from .verbose_http_exceptions.exc import (
    DatabaseErrorVerboseHTTPException as DatabaseErrorVerboseHTTPException,
)
from .verbose_http_exceptions.exc import InfoVerboseHTTPException as InfoVerboseHTTPException
from .verbose_http_exceptions.exc import (
    NestedErrorsMainHTTPException as NestedErrorsMainHTTPException,
)
from .verbose_http_exceptions.exc import (
    RedirectVerboseHTTPException as RedirectVerboseHTTPException,
)
from .verbose_http_exceptions.exc import (
    RequestValidationVerboseHTTPException as RequestValidationVerboseHTTPException,
)
from .verbose_http_exceptions.exc import (
    ServerErrorVerboseHTTPException as ServerErrorVerboseHTTPException,
)
from .verbose_http_exceptions.exc import SuccessVerboseHTTPException as SuccessVerboseHTTPException
from .verbose_http_exceptions.exc import VerboseHTTPExceptionDict as VerboseHTTPExceptionDict
from .verbose_http_exceptions.handlers import apply_all_handlers as apply_all_handlers
from .verbose_http_exceptions.handlers import (
    apply_verbose_http_exception_handler as apply_verbose_http_exception_handler,
)
