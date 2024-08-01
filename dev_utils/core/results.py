"""Rust-like error handling."""

from typing import Generic, NoReturn, TypeVar, final

Value = TypeVar("Value")
Error = TypeVar("Error", bound=Exception)
DefaultT = TypeVar("DefaultT")


@final
class Ok(Generic[Value]):
    """Success result class."""

    _value: Value
    __match_args__ = ("_value",)

    def __init__(self, value: Value) -> None:
        self._value = value

    def __repr__(self) -> str:  # noqa: D105
        return f"Ok({repr(self._value)})"

    def __eq__(self, other: object) -> bool:  # noqa: D105 ANN401
        if isinstance(other, Ok) and type(self) is type(other):  # type: ignore
            return self._value == other._value  # type: ignore
        return False

    def err(self) -> None:
        """Return None, because OK has no errors."""
        return None

    def unwrap(self) -> Value:
        """Get success result value."""
        return self._value


@final
class Err(Generic[Error]):
    """Error result class."""

    _err: Error
    __match_args__ = ("_err",)

    def __init__(self, err: Error) -> None:
        self._err = err

    def __repr__(self) -> str:  # noqa: D105
        return f"Err({repr(self._err)})"

    def __eq__(self, other: object) -> bool:  # noqa: D105 ANN401
        if isinstance(other, Err) and type(self) is type(other):  # type: ignore
            return self._err.args == other._err.args  # type: ignore
        return False

    def err(self) -> Error:
        """Get error without raises.."""
        return self._err

    def unwrap(self) -> NoReturn:
        """Raise error."""
        raise self._err


Result = Ok[Value] | Err[Error]
