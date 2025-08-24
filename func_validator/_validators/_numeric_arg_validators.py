from functools import partial
from operator import eq, ge, gt, le, lt, ne
from typing import Callable

from ._core import Number, T, OPERATOR_SYMBOLS


def _generic_number_validator(x: T, /, *, to: T, fn: Callable[[T, T], bool]):
    if not fn(x, to):
        operator_symbol = OPERATOR_SYMBOLS[fn.__name__]
        raise ValueError(f"{x=} must be {operator_symbol} {to}.")


def _must_be_between(
        x,
        /,
        *,
        min_value: Number,
        max_value: Number,
        min_inclusive: bool,
        max_inclusive: bool,
):
    min_fn = ge if min_inclusive else gt
    max_fn = le if max_inclusive else lt
    if not (min_fn(x, min_value) and max_fn(x, max_value)):
        min_operator_symbol = OPERATOR_SYMBOLS[min_fn.__name__]
        max_operator_symbol = OPERATOR_SYMBOLS[max_fn.__name__]
        exc_msg = (
            f"{x=} must be, x {min_operator_symbol} "
            f"{min_value} and x {max_operator_symbol} {max_value}."
        )
        raise ValueError(exc_msg)


# Numeric validation functions


def MustBePositive(value: Number, /):
    """Validates that the number is positive (:math:`x \gt 0`)."""
    _generic_number_validator(value, to=0.0, fn=gt)


def MustBeNonPositive(value: Number, /):
    """Validates that the number is non-positive (:math:`x \le 0`)."""
    _generic_number_validator(value, to=0.0, fn=le)


def MustBeNegative(value: Number, /):
    """Validates that the number is negative (:math:`x \lt 0`)."""
    _generic_number_validator(value, to=0.0, fn=lt)


def MustBeNonNegative(value: Number, /):
    """Validates that the number is non-negative (:math:`x \ge 0`)."""
    _generic_number_validator(value, to=0.0, fn=ge)


def MustBeBetween(
        *,
        min_value: Number,
        max_value: Number,
        min_inclusive: bool = True,
        max_inclusive: bool = True,
):
    """Validates that the number is between min_value and max_value.

    :param min_value: The minimum value (inclusive or exclusive based
                      on min_inclusive).
    :type min_value: Number

    :param max_value: The maximum value (inclusive or exclusive based
                      on max_inclusive).
    :type max_value: Number

    :param min_inclusive: If True, min_value is inclusive. Default is True.
    :type min_inclusive: bool

    :param max_inclusive: If True, max_value is inclusive. Default is True.
    :type max_inclusive: bool

    :raises ValueError: If the number is not within the specified range.

    :return: A validator function that accepts a number and raises
                ValueError if it is not within the specified range.
    :rtype: Callable[[Number], None]
    """

    return partial(
        _must_be_between,
        min_value=min_value,
        max_value=max_value,
        min_inclusive=min_inclusive,
        max_inclusive=max_inclusive,
    )


# Comparison validation functions


def MustBeEqual(value: Number, /):
    """Validates that the number is equal to the specified value"""
    return partial(_generic_number_validator, to=value, fn=eq)


def MustBeNotEqual(value: Number, /):
    """Validates that the number is not equal to the specified value"""
    return partial(_generic_number_validator, to=value, fn=ne)


def MustBeGreaterThan(value: Number, /):
    """Validates that the number is greater than the specified value"""
    return partial(_generic_number_validator, to=value, fn=gt)


def MustBeGreaterThanOrEqual(value: Number, /):
    """Validates that the number is greater than or equal to the
    specified value.
    """
    return partial(_generic_number_validator, to=value, fn=ge)


def MustBeLessThan(value: Number, /):
    """Validates that the number is less than the specified value"""
    return partial(_generic_number_validator, to=value, fn=lt)


def MustBeLessThanOrEqual(value: Number, /):
    """Validates that the number is less than or equal to the
    specified value.
    """
    return partial(_generic_number_validator, to=value, fn=le)
