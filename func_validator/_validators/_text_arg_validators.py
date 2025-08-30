import re
from functools import partial
from typing import Literal, Callable

from ._core import ValidationError


def _must_match_regex(
        arg_value: str, arg_name: str, /, *, match_func: Callable,
        regex_pattern: re.Pattern
) -> None:
    if not isinstance(arg_value, str):
        exc_msg = f"{arg_name} must be a string, got {type(arg_value)} instead."
        raise TypeError(exc_msg)
    if not match_func(arg_value):
        exc_msg = (
            f"{arg_name}:{arg_value} does not match the "
            f"regex pattern '{regex_pattern.pattern}'."
        )
        raise ValidationError(exc_msg)


def MustMatchRegex(
        regex: str | re.Pattern,
        /,
        *,
        match_type: Literal["match", "fullmatch", "search"] = "match",
        flags: int | re.RegexFlag = 0,
) -> Callable[[str], None]:
    """Validates that the value matches the provided regular expression.

    :param regex: The regular expression to validate.

    :param match_type: The type of match to perform. Must be one of
                       'match', 'fullmatch', or 'search'.
                       Default is 'match'.

    :param flags: Optional regex flags to modify the regex behavior.
                  Default is 0 (no flags). if `regex` is a compiled
                  Pattern, flags are ignored.
                  See `re` module for available flags.

    :raises ValueError: If the value does not match the regex pattern.

    :return: A validator function that checks if a string matches the
             regex pattern.
    """
    if not isinstance(regex, re.Pattern):
        regex_pattern = re.compile(regex, flags=flags)
    else:
        regex_pattern = regex

    match match_type:
        case "match":
            match_func = regex_pattern.match
        case "fullmatch":
            match_func = regex_pattern.fullmatch
        case "search":
            match_func = regex_pattern.search
        case _:
            raise TypeError(
                "Invalid match_type. Must be one of 'match', "
                "'fullmatch', or 'search'."
            )

    return partial(
        _must_match_regex,
        match_func=match_func,
        regex_pattern=regex_pattern,
    )
