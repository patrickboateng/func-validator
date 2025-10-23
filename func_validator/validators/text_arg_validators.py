import re
from typing import Callable, Literal, Optional

from ._core import T, ValidationError, Validator


def _generic_text_validator(
        arg_value: str,
        arg_name: str,
        /,
        *,
        to: T | None = None,
        fn: Callable,
        err_msg: str,
) -> None:
    if not fn(to, arg_value):
        msg = (
            err_msg
            if err_msg
            else f"{arg_name}:{arg_value} does not match or equal {to}"
        )
        raise ValidationError(msg)


class MustMatchRegex(Validator):
    def __init__(
            self,
            regex: str | re.Pattern,
            /,
            *,
            match_type: Literal["match", "fullmatch", "search"] = "match",
            flags: int | re.RegexFlag = 0,
            err_msg: Optional[str] = None,
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
        if not isinstance(regex, re.Pattern):
            self.regex_pattern = re.compile(regex, flags=flags)
        else:
            self.regex_pattern = regex

        self.err_msg = err_msg

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
        )
