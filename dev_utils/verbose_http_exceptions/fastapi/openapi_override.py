from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from dev_utils.verbose_http_exceptions.constants import (
    BASE_VERBOSE_HTTP_VALIDATION_ERROR,
    VERBOSE_HTTP_VALIDATION_ERROR,
)


def _build_verbose_exception_schema(app: FastAPI) -> None:
    """Add verbose http schemas to openapi schema of the given app."""
    app.openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        terms_of_service=app.terms_of_service,
        contact=app.contact,
        license_info=app.license_info,
        routes=app.routes,
        tags=app.openapi_tags,
        servers=app.servers,
    )
    app.openapi_schema.setdefault('components', {})
    app.openapi_schema['components'].setdefault('schemas', {})
    if (
        "BaseVerboseHTTPValidationError" in app.openapi_schema["components"]["schemas"]
        and "VerboseHTTPValidationError" in app.openapi_schema["components"]["schemas"]
    ):  # pragma: no coverage
        return

    app.openapi_schema["components"]["schemas"][
        'BaseVerboseHTTPValidationError'
    ] = BASE_VERBOSE_HTTP_VALIDATION_ERROR
    app.openapi_schema["components"]["schemas"][
        'VerboseHTTPValidationError'
    ] = VERBOSE_HTTP_VALIDATION_ERROR


def override_422_error(app: FastAPI) -> None:
    """Replace all 422 errors in schema with new verbose error format."""
    _build_verbose_exception_schema(app)
    if app.openapi_schema is None:  # pragma: no coverage
        return
    for _, method_item in app.openapi_schema.get('paths', {}).items():
        for _, param in method_item.items():
            responses = param.get('responses')
            # remove 422 response, also can remove other status code
            if '422' in responses:
                responses['422'] = {
                    "description": "Verbose validation error",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/VerboseHTTPValidationError"},
                        },
                    },
                }
