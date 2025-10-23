from typing import Type, Optional

from ._core import T, ValidationError, Validator


def _must_be_a_particular_type(
        arg_value: T,
        arg_name: str,
        *,
        arg_type: Type[T],
        err_msg: str,
) -> None:
    if not isinstance(arg_value, arg_type):
        msg = (
            err_msg
            if err_msg
            else (
                f"{arg_name} must be of type {arg_type}, "
                f"got {type(arg_value)} instead."
            )
        )
        raise ValidationError(msg)


class MustBeA(Validator):
    def __init__(
            self,
            arg_type: Type[T],
            *,
            err_msg: Optional[str] = None,
    ) -> None:
        """Validates that the value is of the specified type.

        :param arg_type: The type to validate against.
        """
        self.arg_type = arg_type
        self.err_msg = err_msg

    def __call__(self, arg_value: T, arg_name: str) -> None:
        _must_be_a_particular_type(
            arg_value,
            arg_name,
            arg_type=self.arg_type,
            err_msg=self.err_msg,
        )
