import re
from typing import Final, Literal, Optional

from ._core import ErrorMsg, T, ValidationError, Validator


def _generic_text_validator(
    arg_value: str,
    arg_name: str,
    /,
    *,
    regex_pattern: T | None = None,
    flags: int | re.RegexFlag,
    err_msg: str,
    match_type: str,
    extra_err_msg_args: dict,
) -> None:
    if match_type == "match":
        regex_fn = re.match
    elif match_type == "fullmatch":
        regex_fn = re.fullmatch
    elif match_type == "search":
        regex_fn = re.search
    else:
        err_msg = "Invalid match type, must be one of the following: " \
                  "'match', 'fullmatch', or 'search'"
        raise ValidationError(err_msg)

    if not regex_fn(regex_pattern, arg_value, flags):
        err_msg = ErrorMsg(err_msg).transform(
            arg_name=arg_name,
            arg_value=arg_value,
            to=regex_pattern,
            **extra_err_msg_args,
        )
        raise ValidationError(err_msg)


TEXT_VALIDATOR_DEFAULT_MSG = (
    "${arg_name}:${arg_value} does not match or equal ${to}"
)


class MustMatchRegex(Validator):

    DEFAULT_ERROR_MSG: Final[str] = TEXT_VALIDATOR_DEFAULT_MSG

    def __init__(
        self,
        regex: str,
        /,
        *,
        match_type: Literal["match", "fullmatch", "search"] = "match",
        flags: int | re.RegexFlag = 0,
        err_msg: Optional[str] = None,
        extra_err_msg_args: Optional[dict] = None,
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
            extra_err_msg_args=extra_err_msg_args,
        )
        self.regex_pattern = regex
        self.flags = flags
        self.match_type = match_type

    def __call__(self, arg_value: str, arg_name: str) -> None:
        _generic_text_validator(
            arg_value,
            arg_name,
            regex_pattern=self.regex_pattern,
            flags=self.flags,
            match_type=self.match_type,
            err_msg=self.err_msg,
            extra_err_msg_args=self.extra_err_msg_args,
        )
