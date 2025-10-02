import re
from typing import Literal, Callable

from ._core import ValidationError, T


def _generic_text_validator(
        arg_value: str,
        arg_name: str,
        /,
        *,
        to: T | None = None,
        fn: Callable,
        **kwargs,
) -> None:
    if not isinstance(arg_value, str):
        exc_msg = (
            f"{arg_name} must be a string, got {type(arg_value)} instead."
        )
        raise TypeError(exc_msg)

    if to is None:
        if not fn(arg_value, **kwargs):
            exc_msg = f"{arg_name}:{arg_value} is not valid."
            raise ValidationError(exc_msg)
    else:
        if not fn(to, arg_value, **kwargs):
            exc_msg = f"{arg_name}:{arg_value} does not match or equal {to}"
            raise ValidationError(exc_msg)


class MustMatchRegex:
    def __init__(
            self,
            regex: str | re.Pattern,
            /,
            *,
            match_type: Literal["match", "fullmatch", "search"] = "match",
            flags: int | re.RegexFlag = 0,
    ):
        """Validates that the value matches the provided regular expression.

        :param regex: The regular expression to validate.
        :param match_type: The type of match to perform. Must be one of
                           'match', 'fullmatch', or 'search'.
        :param flags: Optional regex flags to modify the regex behavior.
                      If `regex` is a compiled Pattern, flags are ignored.
                      See `re` module for available flags.

        :raises ValueError: If the value does not match the regex pattern.
        """
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
        )
