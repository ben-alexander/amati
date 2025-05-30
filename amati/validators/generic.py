"""
A generic object to add extra functionality to pydantic.BaseModel.

Should be used as the base class for all classes in the project.
"""

import re
from typing import (
    Any,
    Callable,
    ClassVar,
    Optional,
    Pattern,
    Type,
    TypeVar,
    Union,
    cast,
)

from pydantic import BaseModel, ConfigDict, PrivateAttr

from amati import Reference
from amati.logging import Log, LogMixin


class GenericObject(LogMixin, BaseModel):
    """
    A generic model to overwrite provide extra functionality
    to pydantic.BaseModel.
    """

    _reference: ClassVar[Reference] = PrivateAttr()
    _extra_field_pattern: Optional[Pattern[str]] = PrivateAttr()

    def __init__(self, **data: Any) -> None:

        super().__init__(**data)

        if "extra" in self.model_config:
            return

        # If extra fields aren't allowed log those that aren't going to be added
        # to the model.
        for field in data:
            if (
                field
                # FIXME: https://github.com/ben-alexander/amati/issues/21
                not in self.model_fields  # pylint: disable=unsupported-membership-test # type: ignore
            ):
                message = f"{field} is not a valid field for {self.__repr_name__()}."
                self.log(
                    Log(
                        message=message,
                        type=ValueError,
                    )
                )

    def model_post_init(self, __context: Any) -> None:
        if not self.model_extra:
            return

        excess_fields: set[str] = set()

        # Any extra fields are allowed
        if self._extra_field_pattern is None:
            return
        else:
            pattern: Pattern[str] = re.compile(self._extra_field_pattern)
            excess_fields.update(
                key for key in self.model_extra.keys() if not pattern.match(key)
            )

        for field in excess_fields:
            message = f"{field} is not a valid field for {self.__repr_name__()}."
            LogMixin.log(
                Log(
                    message=message,
                    type=ValueError,
                )
            )


T = TypeVar("T", bound=GenericObject)


def allow_extra_fields(pattern: Optional[str] = None) -> Callable[[Type[T]], Type[T]]:
    """
    A decorator that modifies a Pydantic BaseModel to allow extra fields and optionally
    sets a pattern for those extra fields

    Args:
        pattern: Optional pattern string for extra fields. If not provided all extra
        fields will be allowed

    Returns:
        A decorator function that adds a ConfigDict allowing extra fields
        and the pattern those fields should follow to the class.
    """

    def decorator(cls: Type[T]) -> Type[T]:
        """
        A decorator function that adds a ConfigDict allowing extra fields.
        """
        namespace: dict[str, Union[ConfigDict, Optional[str]]] = {
            "model_config": ConfigDict(extra="allow"),
            "_extra_field_pattern": pattern,
        }
        # Create a new class with the updated configuration
        return cast(Type[T], type(cls.__name__, (cls,), namespace))

    return decorator
