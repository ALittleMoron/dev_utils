from abc import ABC

import pytest

from dev_utils.core import abstract


class CorrectClass(abstract.Abstract):
    a: str = abstract.abstract_class_property(str)


class CorrectClassWithABC(ABC, abstract.Abstract):
    a: str = abstract.abstract_class_property(str)


def test_attr_warning_no_abstract_property() -> None:
    with pytest.warns(abstract.AbstractClassWithoutAbstractPropertiesWarning):

        class ClassWithoutProperties(abstract.Abstract):
            pass


def test_attr_abstract_without_class() -> None:
    with pytest.raises(RuntimeError):

        class ClassWithoutProperties:
            a: str = abstract.abstract_class_property(str)


def test_attr_raises() -> None:
    with pytest.raises(TypeError):
        str(CorrectClass.a)
    with pytest.raises(TypeError):
        bool(CorrectClass.a)
    with pytest.raises(TypeError):
        CorrectClass.a == '2'  # type: ignore  # noqa: B015
    with pytest.raises(TypeError):
        CorrectClass.a > '2'  # type: ignore  # noqa: B015
    with pytest.raises(TypeError):
        CorrectClass.a < '2'  # type: ignore  # noqa: B015
    with pytest.raises(TypeError):
        CorrectClass.a >= '2'  # type: ignore  # noqa: B015
    with pytest.raises(TypeError):
        CorrectClass.a <= '2'  # type: ignore  # noqa: B015
    with pytest.raises(TypeError):
        CorrectClass.a.some_attr  # type: ignore  # noqa: B015, B018
    with pytest.raises(TypeError):
        CorrectClass.a.some_attr = ''  # type: ignore  # noqa: B015, B018
