
# Dev utils

![coverage](./coverage.svg)

## For what?

I made this project to avoid copy-pasting with utils in my projects. I was aiming to simplify
working with sqlalchemy, FastAPI and other libraries.

## Install

Package has optional dependencies, so if you use it in some specific cases, install only needed
dependencies.

For profiling:

```bash
pip install "python-dev-utils[profiling]"
```

For FastAPI verbose HTTP exceptions:

```bash
pip install "python-dev-utils[fastapi_exceptions]"
```

For extract OpenAPI cli.

```bash
pip install "python-dev-utils[extract_openapi]"
```

## Profiling

Profiling utils. Now available 2 profilers and 2 middlewares (FastAPI) for such profilers:

1. SQLAlchemyQueryProfiler - profile entire sqlalchemy query - it text, params, duration.
2. SQLAlchemyQueryCounter - count sqlalchemy queries.

## SQLAlchemy Filters

Sqlalchemy filter converters moved [another repository](https://github.com/ALittleMoron/sqlalchemy_filter_converter)
due to dev_utils refactoring.

## Verbose HTTP exceptions

Verbose exceptions with single format. This utils was inspired by
[drf-exceptions-hog](https://github.com/PostHog/drf-exceptions-hog), but implemented for other
Web-frameworks.

Now only FastAPI extension is implemented.

### FastAPI implementation

To work with this util you must add exception handlers in your FastAPI project like this:

```python
from fastapi import FastAPI
from dev_utils.verbose_http_exceptions.fastapi.handlers import (
    apply_verbose_http_exception_handler,
    apply_all_handlers,
)

app = FastAPI()
apply_all_handlers(app)
# or
apply_verbose_http_exception_handler(app)
# See document-strings of functions for more information.
```

Then all (or some specific part of) your exceptions will be returned to users in JSON like this:

```json
{
    "code": "validation_error",
    "type": "literal_error",
    "message": "Input should be 1 or 2",
    "attr": "a",
    "location": "query",
}
```

or this (multiple exceptions supported too):

```json
{
    "code": "multiple",
    "type": "multiple",
    "message": "Multiple exceptions ocurred. Please check list for details.",
    "attr": null,
    "location": null,
    "nested_errors": [
        {
            "code": "validation_error",
            "type": "literal_error",
            "message": "Input should be 1 or 2",
            "attr": "a",
            "location": "query",
        },
        {
            "code": "validation_error",
            "type": "missing",
            "message": "Field required",
            "attr": "b",
            "location": "query",
        }
    ]
}
```

`apply_all_handler` function also has `override_422_openapi` param (default True). You can turn
it off to avoid overriding 422 errors in your application OpenAPI schema.

## Export OpenAPI

If you want to export your OpenAPI schema from FastAPI application via CLI, you can use
OpenAPI exporter from this package.

```bash
python3 -m dev_utils.fastapi.openapi.exporter \
    "main:app" \
    --app-dir "my/path/to/main" \
    --out "custom_name.json"
```

CLI params:

- `"main:app"` - path to app with format "file_name:name_of_app_var"
- `--app-dir`  - directory of app file contains.
- `--out`      - custom file name and format (JSON and YAML available).
