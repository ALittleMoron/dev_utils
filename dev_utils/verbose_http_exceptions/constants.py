from typing import Any

BASE_VERBOSE_HTTP_VALIDATION_ERROR = {
    "properties": {
        "code": {
            "title": "Error code",
            "type": "string",
            "example": "multiple",
        },
        "type": {
            "title": "Error type",
            "type": "string",
            "example": "multiple",
        },
        "message": {
            "title": "Message",
            "type": "string",
            "example": "Multiple errors ocurred. Please check list for nested_errors.",
        },
        "attr": {
            "title": "Attribute name",
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "example": None,
        },
        "location": {
            "title": "Location of attribute",
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "example": None,
        },
    },
    "title": "BaseVerboseHTTPValidationError",
    "type": "object",
    "required": ["code", "type", "message"],
}
VERBOSE_HTTP_VALIDATION_ERROR = {
    "allOf": [
        {"$ref": "#/components/schemas/BaseVerboseHTTPValidationError"},
        {
            "properties": {
                "nested_errors": {
                    "items": {
                        "$ref": "#/components/schemas/BaseVerboseHTTPValidationError",
                    },
                    "type": "array",
                    "title": "Specific errors of request validation",
                    "example": [
                        {
                            "code": "validation_error",
                            "type": "literal_error",
                            "message": (
                                "Input should be 1, 2 or 3 "
                                "(this is example only. Not real message)"
                            ),
                            "attr": "a",
                            "location": "query",
                        },
                        {
                            "code": "validation_error",
                            "type": "literal_error",
                            "message": (
                                "Input should be 25 " "(this is example only. Not real message)"
                            ),
                            "attr": "b",
                            "location": "query",
                        },
                    ],
                },
            },
        },
    ],
    "title": "VerboseHTTPValidationError",
    "type": "object",
}

ABSTRACT_PROPERTY_DEFAULT_VALUE = "<abstract property>"
ABSTRACT_CLS_DEFAULT_VALUE = "<class with abstract properties>"


INFO_START_DIGIT = 1
SUCCESS_START_DIGIT = 2
REDIRECT_START_DIGIT = 3
CLIENT_ERROR_START_DIGIT = 4
SERVER_ERROR_START_DIGIT = 5
ERROR_MAPPING: dict[int, dict[str, Any]] = {
    INFO_START_DIGIT: {
        "code": "info",
        "type": "info",
        "location": None,
        "attr": None,
    },
    SUCCESS_START_DIGIT: {
        "code": "success",
        "type": "success",
        "location": None,
        "attr": None,
    },
    REDIRECT_START_DIGIT: {
        "code": "redirect",
        "type": "redirect",
        "location": None,
        "attr": None,
    },
    CLIENT_ERROR_START_DIGIT: {
        "code": "client_error",
        "type": "client_error",
        "location": None,
        "attr": None,
    },
    SERVER_ERROR_START_DIGIT: {
        "code": "server_error",
        "type": "server_error",
        "location": None,
        "attr": None,
    },
}
