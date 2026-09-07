from typing import Final

from ._core import ErrorMsg, T, ValidationError, Validator


__all__ = ["MustBeTruthy", "must_be_truthy"]


def _must_be_truthy(
    arg_value: T,
    arg_name: str,
    err_msg: str,
    extra_err_msg_args: dict,
):
    if not bool(arg_value):
        err_msg = ErrorMsg(err_msg).transform(
            arg_value=arg_value, arg_name=arg_name, **extra_err_msg_args
        )
        raise ValidationError(err_msg)


class MustBeTruthy(Validator):
    DEFAULT_ERROR_MSG: Final[str] = (
        "${arg_name} must have a truthy value if "
        "${parent_arg_name} is equal to ${parent_arg_value}"
    )

    def __call__(self, arg_value: T, arg_name: str):
        _must_be_truthy(
            arg_value,
            arg_name,
            err_msg=self.err_msg,
            extra_err_msg_args=self.extra_err_msg_args,
        )


# Shorter forms for some validators
must_be_truthy = MustBeTruthy()
