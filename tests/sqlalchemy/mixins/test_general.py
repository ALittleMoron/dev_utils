from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import DeclarativeBase, Mapped

from dev_utils.sqlalchemy.mixins import general as general_mixins
from dev_utils.sqlalchemy.mixins import ids as ids_mixins


class Base(DeclarativeBase): ...  # noqa: D101


class DictConvertModel(  # noqa: D101
    general_mixins.DictConverterMixin,
    ids_mixins.IntegerIDMixin,
    Base,
):
    __tablename__ = "dct_convert"

    some_other_attr: Mapped[str]

    @hybrid_method
    def some_hybrid_method(self) -> Mapped[int]:  # noqa: D102
        return self.id  # type: ignore


def test_dict_convert() -> None:
    instance = DictConvertModel(id=1, some_other_attr="aboba")
    assert instance.as_dict() == {"id": 1, "some_other_attr": "aboba", "some_hybrid_method": 1}
    assert instance.as_dict(exclude={"some_other_attr", "some_hybrid_method"}) == {"id": 1}
    assert instance.as_dict(exclude={"some_other_attr", "some_hybrid_method"}, id="other_id") == {
        "other_id": 1,
    }
    assert instance.as_dict(exclude={"some_other_attr", "id"}, some_hybrid_method="other") == {
        "other": 1,
    }
