import math
from functools import partial
from operator import eq, ge, gt, le, lt, ne
from typing import Callable

from ._core import Number, T, OPERATOR_SYMBOLS, ValidationError


def _generic_number_validator(
    arg_value: T,
    arg_name: str,
    /,
    *,
    to: T,
    fn: Callable,
    **kwargs,
):
    if not fn(arg_value, to, **kwargs):
        operator_symbol = OPERATOR_SYMBOLS[fn.__name__]
        raise ValidationError(
            f"{arg_name}:{arg_value} must be {operator_symbol} {to}."
        )


def _must_be_between(
    arg_value: T,
    arg_name: str,
    /,
    *,
    min_value: Number,
    max_value: Number,
    min_inclusive: bool,
    max_inclusive: bool,
):
    min_fn = ge if min_inclusive else gt
    max_fn = le if max_inclusive else lt
    if not (min_fn(arg_value, min_value) and max_fn(arg_value, max_value)):
        min_operator_symbol = OPERATOR_SYMBOLS[min_fn.__name__]
        max_operator_symbol = OPERATOR_SYMBOLS[max_fn.__name__]
        exc_msg = (
            f"{arg_name}:{arg_value} must be, {arg_name} {min_operator_symbol} "
            f"{min_value} and {arg_name} {max_operator_symbol} {max_value}."
        )
        raise ValidationError(exc_msg)


# Numeric validation functions


def MustBePositive(arg_value: Number, arg_name: str, /):
    r"""Validates that the number is positive ($x \gt 0$)."""
    _generic_number_validator(arg_value, arg_name, to=0.0, fn=gt)


def MustBeNonPositive(arg_value: Number, arg_name: str, /):
    r"""Validates that the number is non-positive ($x \le 0$)."""
    _generic_number_validator(arg_value, arg_name, to=0.0, fn=le)


def MustBeNegative(arg_value: Number, arg_name: str, /):
    r"""Validates that the number is negative ($x \lt 0$)."""
    _generic_number_validator(arg_value, arg_name, to=0.0, fn=lt)


def MustBeNonNegative(arg_value: Number, arg_name: str, /):
    r"""Validates that the number is non-negative ($x \ge 0$)."""
    _generic_number_validator(arg_value, arg_name, to=0.0, fn=ge)


class MustBeBetween:
    """Validates that the number is between min_value and max_value."""

    def __init__(
        self,
        *,
        min_value: Number,
        max_value: Number,
        min_inclusive: bool = True,
        max_inclusive: bool = True,
    ):
        """
        :param min_value: The minimum value (inclusive or exclusive based
                          on min_inclusive).
        :param max_value: The maximum value (inclusive or exclusive based
                          on max_inclusive).
        :param min_inclusive: If True, min_value is inclusive. Default is True.
        :param max_inclusive: If True, max_value is inclusive. Default is True.
        """
        self.min_value = min_value
        self.max_value = max_value
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive

    def __call__(self, arg_value: Number, arg_name: str):
        _must_be_between(
            arg_value,
            arg_name,
            min_value=self.min_value,
            max_value=self.max_value,
            min_inclusive=self.min_inclusive,
            max_inclusive=self.max_inclusive,
        )


# Comparison validation functions


class MustBeEqual:
    def __init__(self, value: Number):
        """Validates that the number is equal to the specified value"""
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(arg_value, arg_name, to=self.value, fn=eq)


class MustNotBeEqual:
    def __init__(self, value: Number):
        """Validates that the number is not equal to the specified value"""
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(arg_value, arg_name, to=self.value, fn=ne)


class MustBeAlmostEqual:
    def __init__(
        self,
        value: float,
        /,
        *,
        rel_tol=1e-9,
        abs_tol=0.0,
    ):
        """Validates that argument value (float) is almost equal to the
        specified value.

        Uses `math.isclose` (which means key-word arguments provided are
        passed to `math.isclose`) for comparison, see its
        [documentation](https://docs.python.org/3/library/math.html#math.isclose)
        for details.
        """
        self.value = value
        self.rel_tol = rel_tol
        self.abs_tol = abs_tol

    def __call__(self, arg_value: float, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=self.value,
            fn=math.isclose,
            rel_tol=self.rel_tol,
            abs_tol=self.abs_tol,
        )


class MustBeGreaterThan:

    def __init__(self, value: Number):
        """Validates that the number is greater than the specified value"""
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(arg_value, arg_name, to=self.value, fn=gt)


class MustBeGreaterThanOrEqual:

    def __init__(self, value: Number):
        """Validates that the number is greater than or equal to the
        specified value.
        """
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(arg_value, arg_name, to=self.value, fn=ge)


class MustBeLessThan:
    def __init__(self, value: Number):
        """Validates that the number is less than the specified value"""
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(arg_value, arg_name, to=self.value, fn=lt)


class MustBeLessThanOrEqual:
    def __init__(self, value: Number):
        """Validates that the number is less than or equal to the
        specified value.
        """
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(arg_value, arg_name, to=self.value, fn=le)
