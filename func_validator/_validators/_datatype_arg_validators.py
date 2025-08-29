from functools import partial
from typing import Optional, Type, Callable

from ._core import T, ValidationError


def _must_be_a_particular_type(value: T, *, arg_type: Type[T]) -> None:
    if not isinstance(value, arg_type):
        exc_msg = f"Value must be of type {arg_type}, got {type(value)} instead."
        raise ValidationError(exc_msg)


def MustBeA(arg_type: Type[T]) -> Callable[[T, Type[T]], None]:
    """Validates that the value is of the specified type.

    :param arg_type: The type to validate against.

    :raises ValidationError: If the value is not of the specified type.
    """
    return partial(_must_be_a_particular_type, arg_type=arg_type)
