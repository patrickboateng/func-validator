import re
from typing import Literal


def MustMatchRegex(
    regex: str | re.Pattern,
    *,
    match_type: Literal["match", "fullmatch", "search"] = "match",
    flags: int | re.RegexFlag = 0,
):
    """Validates that the value matches the provided regular expression.

    :param regex: The regular expression to validate.
    :type regex: str | re.Pattern

    :param match_type: The type of match to perform. Must be one of
                       'match', 'fullmatch', or 'search'.
                       Default is 'match'.
    :type match_type: LiteralString["match", "fullmatch", "search"]

    :param flags: Optional regex flags to modify the regex behavior.
                  Default is 0 (no flags).
    :type flags: int | re.RegexFlag

    :raises ValueError: If the value does not match the regex pattern.
    """
    regex_pattern = regex
    if not isinstance(regex, re.Pattern):
        regex_pattern = re.compile(regex, flags=flags)

    match match_type:
        case "match":
            match_func = regex_pattern.match
        case "fullmatch":
            match_func = regex_pattern.fullmatch
        case "search":
            match_func = regex_pattern.search
        case _:
            raise ValueError(
                "Invalid match_type. Must be one of 'match', "
                "'fullmatch', or 'search'."
            )

    def validator(value: str) -> None:
        if not match_func(value):
            exc_msg = (
                f"Value '{value}' does not match the "
                f"regex pattern '{regex_pattern.pattern}'."
            )
            raise ValueError(exc_msg)

    return validator
