import pytest

from dev_utils.core.utils import strings as strings_utils


@pytest.mark.parametrize(
    ("obj", "expected_result"),
    [
        ("                 abc                ", "abc"),
        ("                 abc\nabc                ", "abc abc"),
        ("                 abc  abc                ", "abc abc"),
        ("                 abc   abc                ", "abc abc"),
    ],
)
def test_trim_and_plain_text(obj: str, expected_result: str) -> None:
    assert strings_utils.trim_and_plain_text(obj) == expected_result


@pytest.mark.parametrize(
    ("string", "expected_result"),
    [
        ("some string", False),
        ("{} string", True),
        ("Some value {} string", True),
        ("Somevalue{}string", True),
        ("{some_variables}", True),
        ("{", False),
        ("}", False),
        ("{{}", False),
        ("{}}", False),
        ("{{}}", True),
        ("\\{}", True),
        ("{\\}", False),
        ("{%}", False),
        ("{!}", False),
        ("{?}", False),
        ("{1a}", False),
        ("{a1}", True),
        ("{a1}}", False),
        ("{{a1}}", True),
    ],
)
def test(string: str, expected_result: str) -> None:
    assert strings_utils.has_format_brackets(string) is expected_result
