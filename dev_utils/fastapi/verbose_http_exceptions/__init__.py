"""Verbose HTTP exception package.

Contains exceptions and handlers for FastAPI.

Full verbose http exception result is the following (example):

```
{
  "code": "multiple",
  "type": "multiple",
  "message": "check list",
  "location": None,
  "attr": None,
  "nested_errors": [
    {
      "code": "validation_error",
      "type": "literal_error",
      "message": "Input should be 1, 2 or 3",
      "attr": "a",
      "location": "query"
    },
    {
      "code": "validation_error",
      "type": "missing",
      "message": "Field required",
      "attr": "b",
      "location": "query"
    }
  ]
}
```
"""

from .exc import BaseVerboseHTTPException as BaseVerboseHTTPException
from .exc import ClientVerboseHTTPException as ClientVerboseHTTPException
from .exc import DatabaseErrorVerboseHTTPException as DatabaseErrorVerboseHTTPException
from .exc import InfoVerboseHTTPException as InfoVerboseHTTPException
from .exc import NestedErrorsMainHTTPException as NestedErrorsMainHTTPException
from .exc import RedirectVerboseHTTPException as RedirectVerboseHTTPException
from .exc import RequestValidationVerboseHTTPException as RequestValidationVerboseHTTPException
from .exc import ServerErrorVerboseHTTPException as ServerErrorVerboseHTTPException
from .exc import SuccessVerboseHTTPException as SuccessVerboseHTTPException
from .exc import VerboseHTTPExceptionDict as VerboseHTTPExceptionDict
from .handlers import apply_all_handlers as apply_all_handlers
from .handlers import apply_verbose_http_exception_handler as apply_verbose_http_exception_handler
