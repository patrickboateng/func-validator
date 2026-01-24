import re
from typing import Callable, Final, Literal, Optional

from ._core import ErrorMsg, T, ValidationError, Validator


def _generic_text_validator(
    arg_value: str,
    arg_name: str,
    /,
    *,
    to: T | None = None,
    fn: Callable,
    err_msg: str,
    extra_msg_args: dict,
) -> None:
    if not fn(to, arg_value):
        err_msg = ErrorMsg(err_msg).transform(
            arg_name=arg_name,
            arg_value=arg_value,
            to=to,
            **extra_msg_args,
        )
        raise ValidationError(err_msg)


TEXT_VALIDATOR_DEFAULT_MSG = (
    "${arg_name}:${arg_value} does not match or equal ${to}"
)


class MustMatchRegex(Validator):

    DEFAULT_ERROR_MSG: Final[str] = TEXT_VALIDATOR_DEFAULT_MSG

    def __init__(
        self,
        regex: str | re.Pattern,
        /,
        *,
        match_type: Literal["match", "fullmatch", "search"] = "match",
        flags: int | re.RegexFlag = 0,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
    ):
        """Validates that the value matches the provided regular expression.

        :param regex: The regular expression to validate.
        :param match_type: The type of match to perform. Must be one of
                           'match', 'fullmatch', or 'search'.
        :param flags: Optional regex flags to modify the regex behavior.
                      If `regex` is a compiled Pattern, flags are ignored.
                      See `re` module for available flags.
        :param err_msg: error message.

        :raises ValueError: If the value does not match the regex pattern.
        """
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )

        if not isinstance(regex, re.Pattern):
            self.regex_pattern = re.compile(regex, flags=flags)
        else:
            self.regex_pattern = regex

        match match_type:
            case "match":
                self.regex_func = re.match
            case "fullmatch":
                self.regex_func = re.fullmatch
            case "search":
                self.regex_func = re.search
            case _:
                raise ValidationError(
                    "Invalid match_type. Must be one of 'match', "
                    "'fullmatch', or 'search'."
                )

    def __call__(self, arg_value: str, arg_name: str) -> None:
        _generic_text_validator(
            arg_value,
            arg_name,
            to=self.regex_pattern,
            fn=self.regex_func,
            err_msg=self.err_msg,
            extra_msg_args=self.extra_msg_args,
        )
