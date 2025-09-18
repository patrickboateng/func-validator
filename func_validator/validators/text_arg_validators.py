import re
from functools import partial
from typing import Literal, Callable

from validators.crypto_addresses import bsc_address
from validators.email import email

from ._core import ValidationError, Error, T


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
    :param flags: Optional regex flags to modify the regex behavior.
                  If `regex` is a compiled Pattern, flags are ignored.
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
            regex_func = re.match
        case "fullmatch":
            regex_func = re.fullmatch
        case "search":
            regex_func = re.search
        case _:
            raise ValidationError(
                "Invalid match_type. Must be one of 'match', "
                "'fullmatch', or 'search'."
            )

    return partial(_generic_text_validator, to=regex_pattern, fn=regex_func)


def MustMatchEmail(arg_value: str, arg_name: str) -> None:
    """Validates that the value is a valid email address.

    Implementation provided [here](https://yozachar.github.io/pyvalidators/stable/api/email/#validators.email.email)
    by [validators](https://github.com/python-validators/validators)
    """
    _generic_text_validator(arg_value, arg_name, fn=email)


def MustMatchBSCAddress(arg_value: str, arg_name: str) -> None:
    """Validates that the value is a valid binance smart chain address.

    Implementation provided [here](https://yozachar.github.io/pyvalidators/stable/api/crypto_addresses/#validators.crypto_addresses.bsc_address)
    by [validators](https://github.com/python-validators/validators)

    """
    _generic_text_validator(arg_value, arg_name, fn=bsc_address)
