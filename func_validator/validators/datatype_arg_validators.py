from functools import partial
from typing import Type, Callable

from ._core import T, ValidationError


def _must_be_a_particular_type(
    arg_value: T,
    arg_name: str,
    *,
    arg_type: Type[T],
) -> None:
    if not isinstance(arg_value, arg_type):
        exc_msg = (
            f"{arg_name} must be of type {arg_type}, "
            f"got {type(arg_value)} instead."
        )
        raise ValidationError(exc_msg)


class MustBeA:
    def __init__(self, arg_type: Type[T]):
        """Validates that the value is of the specified type.

        :param arg_type: The type to validate against.
        """
        self.arg_type = arg_type

    def __call__(self, arg_value: T, arg_name: str) -> None:
        _must_be_a_particular_type(
            arg_value,
            arg_name,
            arg_type=self.arg_type,
        )
