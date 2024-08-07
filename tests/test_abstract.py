from abc import ABC

import pytest

from dev_utils import abstract


class CorrectClass(abstract.Abstract):  # noqa: D101
    a: str = abstract.abstract_class_property(str)


class CorrectClassWithABC(ABC, abstract.Abstract):  # noqa: D101
    a: str = abstract.abstract_class_property(str)


def test_attr_warning_no_abstract_property() -> None:
    with pytest.warns(abstract.AbstractClassWithoutAbstractPropertiesWarning):

        class ClassWithoutProperties(abstract.Abstract):  # type: ignore reportUnusedClass
            pass


def test_attr_abstract_without_class() -> None:
    with pytest.raises(Exception):  # noqa: B017, PT011

        class ClassWithoutProperties:  # type: ignore reportUnusedClass
            a: str = abstract.abstract_class_property(str)


def test_attr_raises() -> None:
    with pytest.raises(TypeError):
        str(CorrectClass.a)
    with pytest.raises(TypeError):
        bool(CorrectClass.a)
    with pytest.raises(TypeError):
        CorrectClass.a == "2"  # type: ignore reportUnusedExpression  # noqa: B015
    with pytest.raises(TypeError):
        CorrectClass.a > "2"  # type: ignore reportUnusedExpression  # noqa: B015
    with pytest.raises(TypeError):
        CorrectClass.a < "2"  # type: ignore reportUnusedExpression  # noqa: B015
    with pytest.raises(TypeError):
        CorrectClass.a >= "2"  # type: ignore reportUnusedExpression  # noqa: B015
    with pytest.raises(TypeError):
        CorrectClass.a <= "2"  # type: ignore reportUnusedExpression  # noqa: B015
    with pytest.raises(TypeError):
        CorrectClass.a.some_attr  # type: ignore reportUnusedExpression  # noqa: B018
    with pytest.raises(TypeError):
        CorrectClass.a.some_attr = ""  # type: ignore reportUnusedExpression


def test_inherit_abstract_type_error() -> None:
    class CorrectClass(abstract.Abstract):  # type: ignore reportUnusedClass
        a: str = abstract.abstract_class_property(str)

    with pytest.raises(TypeError):

        class InheritClass(CorrectClass): ...  # type: ignore reportUnusedClass


def test_inherit_abstract_skip() -> None:
    class CorrectClass(abstract.Abstract):  # type: ignore reportUnusedClass
        a: str = abstract.abstract_class_property(str)

    class InheritClass(CorrectClass):  # type: ignore reportUnusedClass
        __skip_abstract_raise_error__ = True
