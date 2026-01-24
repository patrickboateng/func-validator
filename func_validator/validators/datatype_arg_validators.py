from typing import Final, Optional, Type

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
    err_msg: str,
    extra_msg_args: dict,
) -> None:
    if not isinstance(arg_value, arg_type):
        err_msg = ErrorMsg(err_msg).transform(
            arg_value=arg_value,
            arg_name=arg_name,
            arg_type=arg_type,
            arg_value_type=type(arg_value),
            **extra_msg_args,
        )
        raise ValidationError(err_msg)


class MustBeA(Validator):

    DEFAULT_ERROR_MSG: Final[str] = DATATYPE_VALIDATOR_MSG

    def __init__(
        self,
        arg_type: Type[T],
        *,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
    ) -> None:
        """Validates that the value is of the specified type.

        :param arg_type: The type to validate against.
        """
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )
        self.arg_type = arg_type

    def __call__(self, arg_value: T, arg_name: str) -> None:
        _must_be_a_particular_type(
            arg_value,
            arg_name,
            arg_type=self.arg_type,
            err_msg=self.err_msg,
            extra_msg_args=self.extra_msg_args,
        )
