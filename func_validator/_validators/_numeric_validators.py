from operator import eq, ge, gt, le, lt, ne
from typing import Callable

from ._core import Number, T

# Numeric validation functions


def _generic_number_validator(value: T, *, to: T, fn: Callable, symbol: str):
    if not fn(value, to):
        raise ValueError(f"Value {value} must be {symbol} {to}.")


def MustBePositive(value: Number, /):
    _generic_number_validator(value, to=0.0, fn=gt, symbol=">")


def MustBeNonPositive(value: Number, /):
    _generic_number_validator(value, to=0.0, fn=le, symbol="<=")


def MustBeNegative(value: Number, /):
    _generic_number_validator(value, to=0.0, fn=lt, symbol="<")


def MustBeNonNegative(value: Number, /):
    _generic_number_validator(value, to=0.0, fn=ge, symbol=">=")


# Comparison validation functions


def MustBeEqual(value: Number, /):
    return lambda val: _generic_number_validator(val, to=value, fn=eq,
                                                 symbol="==")


def MustBeNotEqual(value: Number, /):
    return lambda val: _generic_number_validator(val, to=value, fn=ne,
                                                 symbol="!=")


def MustBeGreaterThan(value: Number, /):
    return lambda val: _generic_number_validator(val, to=value, fn=gt,
                                                 symbol=">")


def MustBeGreaterThanOrEqual(value: Number, /):
    return lambda val: _generic_number_validator(val, to=value, fn=ge,
                                                 symbol=">=")


def MustBeLessThan(value: Number, /):
    return lambda val: _generic_number_validator(val, to=value, fn=lt,
                                                 symbol="<")


def MustBeLessThanOrEqual(value: Number, /):
    return lambda val: _generic_number_validator(val, to=value, fn=le,
                                                 symbol="<=")
