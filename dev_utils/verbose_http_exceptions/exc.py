"""Module with custom verbose HTTP exceptions."""

from collections.abc import Sequence
from string import Template
from typing import Any, NotRequired, Self, TypedDict

from dev_utils.core.abstract import Abstract, abstract_class_property
from dev_utils.core.utils import get_object_class_absolute_name
from dev_utils.verbose_http_exceptions.constants import (
    ABSTRACT_CLS_DEFAULT_VALUE,
    ABSTRACT_PROPERTY_DEFAULT_VALUE,
)


class VerboseHTTPExceptionDict(TypedDict):
    """TypedDict for verbose http exceptions."""

    code: str
    type: str  # noqa: A003
    message: str
    location: str | None
    attr: str | None
    nested_errors: NotRequired[list["VerboseHTTPExceptionDict"]]


class BaseVerboseHTTPException(Abstract, Exception):  # noqa: N818
    """Base verbose HTTP-exception.

    Exception has abstract class properties, which must be set in inherited classes.

    Properties description
    ----------------------

    ``status_code``
        HTTP status code (use fastapi.status for it).

    ``code``
        Error code (like "server_error", "validation_error") - general identity.

    ``type_``
        Error code type used as description of code property. For example, if there
        is validation_error in code, you can specify it with "required" type_
        to show, that validation error raises because of required field was not passed
        in request body/query/header/cookie.

    ``message``
        Error message used as description of type_ property. For example, for "required"
        type_ you can specify it with "This field is required" message to show verbose message
        in response.

    Optional class properties
    -------------------------

    There are some optional properties, which could be passed in inherited class to specify some
    extra context.

    ``template``
        Message template, that will be used, if any extra attributes fill be passed in ``as_dict``
        method, or ``from_template`` will be executed directly.

    Dynamic attributes
    ------------------

    Dynamic attributes can be passed only in instances of verbose exceptions.

    ``location``
        Specific location of error. For example, in "validation_error" you can pass location as
        "body" or "query" or "headers" or "queries" or some other location (maybe your custom, if
        you want).

    ``attr``
        Specific attribute name, that cause the error. For example, in "validation_error" your attr
        can be any field, which was used in validation, and which was the reason, why this
        validation error was raised.

    ``nested_errors``
        list of nested BaseVerboseHTTPException information. Necessary for multiple errors in one
        response. For example, in "validation_error" you can pass exceptions about multiple attrs
        were not passed, but required.
    """

    status_code: int = abstract_class_property(int)
    code: str = abstract_class_property(str)
    type_: str = abstract_class_property(str)
    message: str = abstract_class_property(str)
    location: str | None = None
    template: Template | str | None = None
    attr: str | None = None
    nested_errors: list["BaseVerboseHTTPException"] | None = None

    def __init__(  # noqa: D105
        self,
        *nested_errors: "BaseVerboseHTTPException",
        status_code: int | None = None,
        code: str | None = None,
        type_: str | None = None,
        message: str | None = None,
        location: str | None = None,
        template: Template | str | None = None,
        attr_name: str | None = None,
        headers: dict[str, Any] | None = None,
        **mapping: object,
    ) -> None:
        if attr_name is not None:
            self.attr = attr_name
        if location is not None:
            self.location = location
        if code is not None:
            self.code = code
        if type_ is not None:
            self.type_ = type_
        if message is not None:
            self.message = message
        if template is not None:
            self.template = template
        if mapping and isinstance(self.template, Template):
            self.message = self.template.safe_substitute(**mapping)
        elif mapping and isinstance(self.template, str):
            self.message = self.template.format(**mapping)
        if status_code is not None:
            self.status_code = status_code
        if nested_errors:
            self.nested_errors = list(nested_errors)
        self.headers = headers

    def _get_attribute(self, name: str) -> Any:  # noqa: ANN401  # pragma: no coverage
        """Safe getattr for verbose http exceptions."""
        try:
            return repr(getattr(self, name))
        except (AttributeError, TypeError):
            return ABSTRACT_PROPERTY_DEFAULT_VALUE

    def __repr__(self) -> str:  # noqa: D105
        cls_path = get_object_class_absolute_name(self.__class__)
        attrs = (
            f'status_code={self.status_code}, code={self._get_attribute("code")}, '
            f'type={self._get_attribute("type_")}, message={self._get_attribute("message")}, '
            f'location={self.location}, template={self.template}, attr={self.attr}'
        )
        return f"{cls_path}({attrs})"

    def __str__(self) -> str:  # noqa: D105  # pragma: no coverage
        try:
            return self.message
        except (AttributeError, TypeError):
            return ABSTRACT_CLS_DEFAULT_VALUE

    def from_template(
        self,
        **mapping: object,
    ) -> Self:
        """Fill message with template and return self.

        Usage:
        ```
        class SomeClass(BaseVerboseHTTPException):
            status_code = status.HTTP_400_BAD_REQUEST
            code = 'abc'
            type_ = 'abc'
            message = 'abc'
            template = Template('abc with template : $abc')

        SomeClass().from_template(abc='25)
        ```

        Due to this code, message will be the following:

        >>> SomeClass().from_template(abc='25).message
        'abc with template : 25'
        """
        if self.template is None:
            return self
        if isinstance(self.template, Template):
            self.message = self.template.safe_substitute(**mapping)
        else:
            self.message = self.template.format(**mapping)
        return self

    def with_attr(self, attr_name: str) -> Self:
        """Add attribute of the error.

        Usage:
        ```
        class SomeClass(BaseVerboseHTTPException):
            status_code = status.HTTP_400_BAD_REQUEST
            code = 'abc'
            type_ = 'abc'
            message = 'abc'

        SomeClass().with_attr('attr')
        ```

        Due to this code, attr will be the following:

        >>> SomeClass().with_attr('attr').attr
        'attr'
        """
        self.attr = attr_name
        return self

    def with_location(self, location: str) -> Self:
        """Add location of the error.

        Usage:
        ```
        class SomeClass(BaseVerboseHTTPException):
            status_code = status.HTTP_400_BAD_REQUEST
            code = 'abc'
            type_ = 'abc'
            message = 'abc'

        SomeClass().with_location('loc')
        ```

        Due to this code, location will be the following:

        >>> SomeClass().with_location('loc').location
        'loc'
        """
        self.location = location
        return self

    def with_nested_errors(
        self,
        nested_errors: Sequence["BaseVerboseHTTPException"],
    ) -> Self:
        """Add nested errors to parent (self) error.

        Usage:
        ```
        class SomeClass(BaseVerboseHTTPException):
            code = 'abc'
            type_ = 'abc'
            message = 'abc'
            template = Template('abc with template : $abc')

        SomeClass().from_template(abc='25).with_attr('my_attr).as_dict()
        ```

        Due to this code, returning dict will be the following:

        >>> SomeClass().from_template(abc='25).with_attr('my_attr).as_dict()
        {"code": "abc", "type": "abc", "message": "abc with template : 25", "attr": "my_attr"}
        """
        if self.nested_errors is not None:
            self.nested_errors.extend(nested_errors)
        else:
            self.nested_errors = (
                nested_errors.copy() if isinstance(nested_errors, list) else list(nested_errors)
            )
        return self

    def as_dict(
        self,
        attr_name: str | None = None,
        location: str | None = None,
        nested_errors: Sequence["BaseVerboseHTTPException"] | None = None,
        **mapping: object,
    ) -> VerboseHTTPExceptionDict:
        """Convert Exception instance into dict.

        Usage:
        ```
        class SomeClass(BaseVerboseHTTPException):
            code = 'abc'
            type_ = 'abc'
            message = 'abc'
            template = Template('abc with template : $abc')

        SomeClass().from_template(abc='25).with_attr('my_attr).as_dict()
        ```

        Due to this code, returning dict will be the following:

        >>> SomeClass().from_template(abc='25).with_attr('my_attr).as_dict()
        {"code": "abc", "type": "abc", "message": "abc with template : 25", "attr": "my_attr"}
        """
        if mapping:
            self.from_template(**mapping)
        if attr_name is not None:
            self.with_attr(attr_name)
        if location is not None:
            self.with_location(location)
        if nested_errors is not None:
            self.with_nested_errors(nested_errors)
        if self.nested_errors is not None:
            return {
                "code": self.code,
                "type": self.type_,
                "message": self.message,
                "location": self.location,
                "attr": self.attr,
                "nested_errors": [nested_error.as_dict() for nested_error in self.nested_errors],
            }
        return {
            "code": self.code,
            "type": self.type_,
            "message": self.message,
            "location": self.location,
            "attr": self.attr,
        }


# Base implementations


class NestedErrorsMainHTTPException(BaseVerboseHTTPException):
    """Main verbose response with nested errors."""

    __skip_abstract_raise_error__ = True

    code = "multiple"
    type_ = "multiple"
    message = "Multiple errors ocurred. Please check list for nested_errors."


class InfoVerboseHTTPException(BaseVerboseHTTPException):
    """Base info verbose response."""

    __skip_abstract_raise_error__ = True

    status_code = 100
    code = "info"
    type_ = "info"


class SuccessVerboseHTTPException(BaseVerboseHTTPException):
    """Base success verbose response."""

    __skip_abstract_raise_error__ = True

    status_code = 200
    code = "success"
    type_ = "success"


class RedirectVerboseHTTPException(BaseVerboseHTTPException):
    """Base redirect verbose response."""

    __skip_abstract_raise_error__ = True

    status_code = 300
    code = "redirect"
    type_ = "redirect"


class ClientVerboseHTTPException(BaseVerboseHTTPException):
    """Base client verbose error."""

    status_code = 400
    code = "client_error"
    type_ = "client_error"
    message = "Unexpected client error was found."
    template = Template("Unexpected client error was found: $reason")


class RequestValidationVerboseHTTPException(BaseVerboseHTTPException):
    """Request validation verbose error."""

    __skip_abstract_raise_error__ = True

    status_code = 422
    code = "validation_error"


class ServerErrorVerboseHTTPException(BaseVerboseHTTPException):
    """Base server verbose error."""

    status_code = 500
    code = "server_error"
    type_ = "server_error"
    message = "Unexpected server error was found."
    template = Template("Unexpected server error was found: $reason.")


class DatabaseErrorVerboseHTTPException(ServerErrorVerboseHTTPException):
    """Base database verbose error."""

    type_ = "database_error"
    message = "Unexpected database error was found."
    template = Template("Unexpected database error was found: $reason")
