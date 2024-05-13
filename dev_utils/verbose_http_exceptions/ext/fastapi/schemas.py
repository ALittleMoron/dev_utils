from pydantic import BaseModel, Field


class VerboseHTTPExceptionSchema(BaseModel):  # noqa: D101
    code: str = Field(
        title="Error code",
        description="Error code to specify area of error like server, client, etc.",
        examples=[
            "validation_error",
            "server_error",
            "client_error",
        ],
    )
    type: str = Field(
        title="Error type",
        description=(
            "Error type to specify subarea of error code like database error on server side "
            "or literal error on client side (validation error)."
        ),
        examples=[
            "database_error",
            "literal_error",
            "missing",
        ],
    )
    message: str = Field(
        title="Error message",
        description=(
            "Error message with content for API user to show him the information about error."
        ),
        examples=[
            "Field required",
            "Input should be 1 or 2",
            "Unexpected server error was found.",
        ],
    )
    attr: str | None = Field(
        default=None,
        title="Error attribute",
        description=(
            "Error attribute to specify concrete object, where the error was raised, "
            "like field name in Pydantic-schema."
        ),
        examples=["a", "b", "your_model_name"],
    )
    location: str | None = Field(
        default=None,
        title="Error location",
        description=(
            "Error location to specify path for concrete object, where the error was raised "
            "field name in pydantic-schema, that was used in Body or Query."
        ),
        examples=["query", "path", "body"],
    )
    nested_errors: "list[VerboseHTTPExceptionSchema] | None" = Field(
        default=None,
        title="Nested errors",
        description=(
            "Nested errors to specify multiple errors in one route, like multiple validation "
            "errors in Pydantic-schema."
        ),
        examples=[
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
            },
        ],
    )


VerboseHTTPExceptionSchema.model_rebuild()
