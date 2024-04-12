import pytest

from dev_utils.core import results


def some_func(value: int | str) -> results.Result[int, TypeError]:
    if isinstance(value, str):
        return results.Err(TypeError(value))
    return results.Ok(value)


def test_ok() -> None:
    result = some_func(25)
    other_result = some_func(25)
    other_ne_result = some_func(-100)
    assert isinstance(result, results.Ok)
    assert result.err() is None
    assert isinstance(result.unwrap(), int)
    assert result == other_result
    assert result != other_ne_result
    assert result != 25
    assert repr(result) == "Ok(25)"


def test_error() -> None:
    result = some_func("string")
    other_result = some_func("string")
    other_ne_result = some_func("not string")
    assert isinstance(result, results.Err)
    assert isinstance(result.err(), TypeError)
    with pytest.raises(TypeError):
        result.unwrap()
    assert result == other_result
    assert result != other_ne_result
    assert result != 25
    assert repr(result) == "Err(TypeError('string'))"
