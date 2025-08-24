import re
from typing import Literal


class MustMatchRegex:
    def __init__(
            self,
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
        :type match_type: Literal["match", "fullmatch", "search"]

        :param flags: Optional regex flags to modify the regex behavior.
                      Default is 0 (no flags). if `regex` is a compiled
                      Pattern, flags are ignored.
                      See `re` module for available flags.
        :type flags: int | re.RegexFlag

        :raises ValueError: If the value does not match the regex pattern.

        :return: A validator function that accepts a string and raises
                 ValueError if it does not match.
        :rtype: Callable[[str], None]
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

        self.regex_pattern = regex_pattern
        self.match_func = match_func

    def __call__(self, value: str) -> None:
        """Validator function to check if the value matches the
        regex pattern.
        """
        if not isinstance(value, str):
            exc_msg = f"Value must be a string, got {type(value)} instead."
            raise TypeError(exc_msg)
        if not self.match_func(value):
            exc_msg = (
                f"Value '{value}' does not match the "
                f"regex pattern '{self.regex_pattern.pattern}'."
            )
            raise ValueError(exc_msg)
