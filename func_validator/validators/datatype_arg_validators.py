from typing import Type

from ._core import ErrorMsg, T, ValidationError, Validator

DATATYPE_VALIDATOR_MSG = (
    "${arg_name} must be of type ${arg_type}, "
    "got ${arg_value_type} instead."
)


def _must_be_a_particular_type(
    arg_value: T,
    arg_name: str,
    *,
    arg_type: Type[T],
    err_msg: ErrorMsg,
) -> None:
    if not isinstance(arg_value, arg_type):
        err_msg = err_msg.transform(
            arg_value=arg_value,
            arg_name=arg_name,
            arg_type=arg_type,
            arg_value_type=type(arg_value),
        )
        raise ValidationError(err_msg)


class MustBeA(Validator):
    def __init__(
        self,
        arg_type: Type[T],
        *,
        err_msg: str = DATATYPE_VALIDATOR_MSG,
    ) -> None:
        """Validates that the value is of the specified type.

        :param arg_type: The type to validate against.
        """
        super().__init__(err_msg=err_msg)
        self.arg_type = arg_type

    def __call__(self, arg_value: T, arg_name: str) -> None:
        _must_be_a_particular_type(
            arg_value,
            arg_name,
            arg_type=self.arg_type,
            err_msg=self.err_msg,
        )
