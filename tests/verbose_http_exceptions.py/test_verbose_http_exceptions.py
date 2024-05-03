from string import Template

import pytest

from dev_utils.core.utils import get_object_class_absolute_name
from dev_utils.verbose_http_exceptions import exc as base_http_exceptions

attr = "attr"
loc = "loc"
code = "test"
test_http_exception1_dict = {
    "code": "test",
    "type": "Test",
    "message": "test message: test",
    "attr": "attr",
    "location": "loc",
}
http_exception_dict_with_nested_errors = {
    "code": "test",
    "type": "Test",
    "message": "test message: test",
    "attr": "attr",
    "location": "loc",
    "nested_errors": [
        {
            "code": "test",
            "type": "Test",
            "message": "test message: test",
            "attr": "attr",
            "location": "loc",
        },
        {
            "code": "test",
            "type": "Test",
            "message": "test message: test",
            "attr": "attr",
            "location": "loc",
        },
    ],
}


class TestHttpException0(base_http_exceptions.BaseVerboseHTTPException):  # noqa: D101
    __test__ = False

    status_code = 400
    code = "test"
    type_ = "Test"
    message = "test message"


class TestHttpException1(base_http_exceptions.BaseVerboseHTTPException):  # noqa: D101
    __test__ = False

    status_code = 400
    code = "test"
    type_ = "Test"
    message = "test message"
    template = Template("test message: $test")


class TestHttpException2(base_http_exceptions.BaseVerboseHTTPException):  # noqa: D101
    __test__ = False

    status_code = 400
    code = "test"
    type_ = "Test"
    message = "test message"
    template = "test message: {test}"


def test_from_template_method() -> None:
    with pytest.raises(TestHttpException1) as exc_info:
        raise TestHttpException1().from_template(test="test")
    assert isinstance(TestHttpException1.template, Template)
    assert (
        exc_info.value.message
        == TestHttpException1.template.safe_substitute(test="test")
        == "test message: test"
    )


def test_from_template_no_template() -> None:
    with pytest.raises(TestHttpException0) as exc_info:
        raise TestHttpException0().from_template(test="test")
    assert TestHttpException0.template is None
    assert exc_info.value.message == TestHttpException0.message


def test_from_template_string_method() -> None:
    with pytest.raises(TestHttpException2) as exc_info:
        raise TestHttpException2().from_template(test="test")
    assert isinstance(TestHttpException2.template, str)
    assert (
        exc_info.value.message
        == TestHttpException2.template.format(test="test")
        == "test message: test"
    )


def test_with_attr_method() -> None:
    with pytest.raises(TestHttpException1) as exc_info:
        raise TestHttpException1().with_attr(attr)
    assert exc_info.value.attr == attr


def test_with_nested_errors() -> None:
    errors = [TestHttpException2(), TestHttpException2()]
    with pytest.raises(TestHttpException1) as exc_info:
        raise TestHttpException1().with_nested_errors(errors)
    assert exc_info.value.nested_errors == errors


def test_with_nested_errors_double_usage() -> None:
    errors_1 = [TestHttpException2(), TestHttpException2()]
    errors_2 = [TestHttpException2(), TestHttpException2()]
    with pytest.raises(TestHttpException1) as exc_info:
        raise TestHttpException1().with_nested_errors(errors_1).with_nested_errors(errors_2)
    assert exc_info.value.nested_errors == errors_1 + errors_2


def test_class_methods_chain() -> None:
    with pytest.raises(TestHttpException1) as exc_info:
        raise TestHttpException1().from_template(test="test").with_attr(attr)
    assert isinstance(TestHttpException1.template, Template)
    assert (
        exc_info.value.message
        == TestHttpException1.template.safe_substitute(test="test")
        == "test message: test"
    )
    assert exc_info.value.attr == attr
    assert exc_info.value.message == TestHttpException1.template.safe_substitute(test="test")


def test_class_as_dict() -> None:
    with pytest.raises(TestHttpException1) as exc_info:
        raise TestHttpException1().from_template(test="test").with_attr(attr).with_location(loc)
    assert exc_info.value.as_dict() == test_http_exception1_dict


def test_class_as_dict_with_params() -> None:
    with pytest.raises(TestHttpException1) as exc_info:
        raise TestHttpException1()
    nested_errors = [
        TestHttpException2().from_template(test="test").with_attr(attr).with_location(loc),
        TestHttpException2().from_template(test="test").with_attr(attr).with_location(loc),
    ]
    assert (
        exc_info.value.as_dict(attr, loc, nested_errors, test="test")
        == http_exception_dict_with_nested_errors
    )


def test_class_as_dict_with_init() -> None:
    with pytest.raises(TestHttpException1) as exc_info:
        raise TestHttpException1(
            TestHttpException1(attr_name=attr, location=loc, test="test"),
            TestHttpException2(attr_name=attr, location=loc, test="test"),
            status_code=1000,
            headers={"X-USER-ID": 25},
            attr_name=attr,
            location=loc,
            code=code,
            message="test message.",
            template="test message: {test}",
            test="test",
        )
    assert exc_info.value.status_code == 1000
    assert exc_info.value.headers == {"X-USER-ID": 25}
    assert exc_info.value.as_dict() == http_exception_dict_with_nested_errors


def test_class_repr() -> None:
    with pytest.raises(TestHttpException1) as exc_info:
        raise TestHttpException1()
    exc = exc_info.value
    assert repr(exc) == (
        f"{get_object_class_absolute_name(exc)}(status_code={exc.status_code}, "
        f"code='{exc.code}', type='{exc.type_}', message='{exc.message}', location={exc.location}, "
        f"template={repr(exc.template)}, attr={exc.attr})"
    )


def test_class_str() -> None:
    with pytest.raises(TestHttpException1) as exc_info:
        raise TestHttpException1()
    assert str(exc_info.value) == exc_info.value.message
