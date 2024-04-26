from typing import TYPE_CHECKING, Any, ClassVar, TypeAlias

from dev_utils.core.logging import logger
from dev_utils.core.utils.inspect import get_object_class_absolute_name
from dev_utils.sqlalchemy.mixins.base import BaseModelMixin
from dev_utils.sqlalchemy.utils import (
    get_model_instance_data_as_dict,
    get_unloaded_fields,
    get_valid_field_names,
)

if TYPE_CHECKING:
    from sqlalchemy.orm.decl_api import DeclarativeBase

    DictStrAny: TypeAlias = dict[str, Any]


class DictConverterMixin(BaseModelMixin):
    """Mixin for converting models to dict."""

    def _replace(
        self,
        item: dict[str, Any],
        **replace: str,
    ) -> None:
        """Add replace field for item.

        Uses like alias: rename existing fields
        """
        for original, replaced in replace.items():
            value_to_replace = self._get_instance_attr(original)
            item[replaced] = value_to_replace
            item.pop(original, None)

    def as_dict(
        self,
        exclude: set[str] | None = None,
        **replace: str,
    ) -> dict[str, Any]:
        """Convert model instance to dict."""
        valid_fields = get_valid_field_names(self._sa_model_class)
        exclude_fields: set[str] = (exclude or set()).union(
            self._sa_instance_state.unloaded,  # type: ignore
        )
        available_fields = valid_fields - exclude_fields
        item: dict[str, Any] = {field: self._get_instance_attr(field) for field in available_fields}
        replace = {key: value for key, value in replace.items() if key in item}
        self._replace(item, **replace)
        return item


class DifferenceMixin(BaseModelMixin):
    """Mixin for checking difference between instance and other objects.

    It will not override double underscore methods like __eq__ or other to avoid Incorrect behavior.
    """

    safe_difference_flag: ClassVar[bool] = False

    def _is_dict_different_from(
        self,
        item: "DictStrAny",
        exclude: set[str] | None = None,
    ) -> bool:
        """Check is self Declarative instance is different from other dictionary.

        Raises
        ------
        AttributeError
            throw, if there is no attribute in self instance and ``safe_difference_flag``
            is not set.
        """
        unloaded_fields = get_unloaded_fields(self)  # type: ignore
        for field, value in item.items():
            if exclude is not None and field in exclude:
                continue
            if field in unloaded_fields:
                cls_path = get_object_class_absolute_name(self)
                msg = f'Field "{field}" is not loaded in {cls_path} instance.'
                if self.safe_difference_flag:
                    logger.warning(msg)
                    return True
                raise AttributeError(msg)
            elif not hasattr(self, field):
                cls_path = get_object_class_absolute_name(self)
                msg = f'Field "{field}" is not present in {cls_path} instance. It may be unloaded.'
                if self.safe_difference_flag:
                    logger.warning(msg)
                    return True
                raise AttributeError(msg)
            self_field_value = getattr(self, field)
            if self_field_value != value:
                return True
        return False

    def _is_model_different_from(
        self,
        item: "DeclarativeBase",
        exclude: set[str] | None = None,
    ) -> bool:
        """Check is self Declarative instance is different from other Declarative instance.

        Raises
        ------
        AttributeError
            throw, if there is no attribute in self instance and ``safe_difference_flag``
            is not set.
        """
        item_dict = get_model_instance_data_as_dict(item)
        return self._is_dict_different_from(item_dict, exclude)

    def is_different_from(
        self,
        item: "DictStrAny | DeclarativeBase",
        exclude: set[str] | None = None,
    ) -> bool:
        """Check is self instance is different from other object (dict or DeclarativeBase).

        Raises
        ------
        TypeError
            throw, if ``item`` param has unsupported type (now only dict and DeclarativeBase
            are supported).
        AttributeError
            throw, if there is no attribute in self instance and ``safe_difference_flag``
            is not set.
        """
        self._sa_model_class  # noqa: B018
        if exclude is None:
            exclude = set()
        if isinstance(item, dict):
            return self._is_dict_different_from(item, exclude)
        elif self.__class__ == item.__class__:  # type: ignore
            return self._is_model_different_from(item, exclude)
        if self.safe_difference_flag:
            return True
        msg = f"Incorrect item. Ожидались: Dict, {self.__class__.__name__}. Got: {type(item)}."
        raise TypeError(msg)


class BetterReprMixin(BaseModelMixin):
    """Mixin with better __repr__ method for SQLAlchemy model instances."""

    use_full_class_path: ClassVar[bool] = False
    max_repr_elements: ClassVar[int | None] = None
    repr_include_fields: ClassVar[set[str] | None] = None

    def __repr__(self) -> str:  # noqa: D105
        fields = get_valid_field_names(self._sa_model_class, only_columns=True)
        unloaded = get_unloaded_fields(self)  # type: ignore
        values_pairs_list: list[str] = []
        # NOTE: id is always loaded, so this if statement part with unloaded is not needed.
        # But I made it for sure.
        if "id" not in unloaded and "id" in fields:
            id_value = repr(self.id)  # type: ignore
            values_pairs_list.append(f'id={id_value}')
            fields.discard("id")
        for col in fields:
            if col in unloaded:  # type: ignore
                values_pairs_list.append(f"{col}=<Not loaded>")
            elif self.repr_include_fields is None or col in self.repr_include_fields:
                values_pairs_list.append(f"{col}={repr(getattr(self, col))}")
        if self.max_repr_elements is not None:
            values_pairs_list = values_pairs_list[: self.max_repr_elements]
        class_name = (
            get_object_class_absolute_name(self)
            if self.use_full_class_path
            else self.__class__.__name__
        )
        values_pairs = ", ".join(values_pairs_list)
        return f"{class_name}({values_pairs})"
