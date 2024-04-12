from typing import Any, Generic, Never, TypeVar, cast
from warnings import warn

from dev_utils.core.utils import get_object_class_absolute_name

T = TypeVar("T")


class AbstractClassWithoutAbstractPropertiesWarning(Warning):
    """Warning about situation, when class inherited by Abstract, but has no abstract props."""


class _AbstractClassProperty(Generic[T]):
    __repr_template: str = (
        "{cls_path}({property_type_name}) on {containing_klass_name}.{property_name}"
    )
    __name__: str
    __containing_klass_name__: str
    __propertytype_name__: str

    def __init__(self, propertytype: type[T]) -> None:
        object.__setattr__(self, "__propertytype_name__", str(propertytype))

    def __set_name__(self, containing_klass: type[Any], name: str) -> None:
        if Abstract not in containing_klass.__bases__:  # pragma: no coverage
            msg = (
                f"Abstract class property {name} defined on non-abstract "
                f"class {containing_klass.__name__}. Make sure "
                f"{containing_klass.__name__} inherits directly from Abstract."
            )
            raise TypeError(msg)
        object.__setattr__(self, "__name__", name)
        object.__setattr__(self, "__containing_klass_name__", containing_klass.__name__)

    def raise_use(self, *args: Any, **kwargs: Any) -> Never:  # noqa: ANN401, F841
        name = object.__getattribute__(self, "__name__")
        containing_klass_name = object.__getattribute__(self, "__containing_klass_name__")
        msg = (
            f"Trying to use property {name} on "
            f"{containing_klass_name}. This is an abstract property."
        )
        raise TypeError(msg)

    def raise_use_compare(self, other: Any) -> Never:  # noqa: ANN401, F841
        self.raise_use()

    def __repr__(self) -> str:  # pragma: no coverage
        return self.__repr_template.format(
            cls_path=get_object_class_absolute_name(self.__class__),
            property_type_name=self.__propertytype_name__,
            containing_klass_name=self.__containing_klass_name__,
            property_name=self.__name__,
        )

    def __getattr__(self, name: str) -> Never:
        if name == "__isabstractmethod__":
            raise AttributeError()
        self.raise_use()

    def __setattr__(self, name: str, value: Any) -> Never:  # noqa: ANN401
        self.raise_use()

    __hash__ = None  # type: ignore
    __eq__ = __ne__ = __lt__ = __le__ = __gt__ = __ge__ = raise_use_compare
    __bool__ = __str__ = raise_use


def abstract_class_property(propertytype: type[T]) -> T:
    """Add abstract class property support for given property.

    WARNING! It should be only used with Abstract class inheritance.

    Usage
    -----

    correct
    =======

    ```
        from abstract import abstract_class_property, Abstract

        class A(Abstract):
            my_abstract_attr: str = abstract_class_property(str)
    ```

    or

    ```
        from abc import ABC
        from abstract import abstract_class_property, Abstract

        class A(ABC, Abstract):
            my_abstract_attr: str = abstract_class_property(str)
    ```

    incorrect
    =========

    ```
        class A:  # no Abstract class
            my_abstract_attr: str = abstract_class_property(str)
    ```

    or

    ```
        from abc import ABC

        class A(ABC):  # Only ABC, not Abstract class
            my_abstract_attr: str = abstract_class_property(str)
    ```
    """
    return cast(T, _AbstractClassProperty(propertytype))


class Abstract:
    """Abstract class for to use with abstract_class_property."""

    __skip_abstract_raise_error__: bool = False

    def __init_subclass__(cls, **kwargs: Any) -> None:  # noqa: ANN401, D105
        super().__init_subclass__(**kwargs)
        if cls.__skip_abstract_raise_error__:
            # NOTE: for further inherit.
            cls.__skip_abstract_raise_error__ = False
            return
        if Abstract in cls.__bases__:
            for name in dir(cls):
                if name.startswith("__") and name.endswith("__"):
                    continue
                if isinstance(getattr(cls, name), _AbstractClassProperty):
                    break
            else:
                msg = (
                    f"Class {cls.__name__} is defined as abstract but does not "
                    "have any abstract class properties defined."
                )
                warn(AbstractClassWithoutAbstractPropertiesWarning(msg), stacklevel=2)
        else:
            for name in dir(cls):
                if name.startswith("__") and name.endswith("__"):
                    continue
                if isinstance(getattr(cls, name), _AbstractClassProperty):  # pragma: no coverage
                    msg = (
                        f"Class {cls.__name__} must define abstract class "
                        f"property {name}, or have Abstract as direct parent."
                    )
                    raise TypeError(msg)
