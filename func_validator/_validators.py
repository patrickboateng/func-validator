from functools import partial
from operator import ge, le, gt, lt, eq, ne, contains
from typing import TypeAlias, Iterable, Sized

Number: TypeAlias = int | float


# Numeric validation functions
def MustBePositive(value: Number, /):
    if not gt(value, 0):
        raise ValueError(f"Value {value} must be greater than 0.")


def MustBeNonPositive(value: Number, /):
    if not le(value, 0):
        raise ValueError(f"Value {value} must be less than or equal to 0.")


def MustBeNegative(value: Number, /):
    if not lt(value, 0):
        raise ValueError(f"Value {value} must be less than 0.")


def MustBeNonNegative(value: Number, /):
    if not ge(value, 0):
        exc_msg = f"Value {value} must be greater than or equal to 0."
        raise ValueError(exc_msg)


# Comparison validation functions


def _comparison_validator(value, *, to, fn, symbol):
    if not fn(value, to):
        raise ValueError(f"Value {value} must be {symbol} {to}.")


def MustBeEqual(value: Number, /):
    return partial(_comparison_validator, to=value, fn=eq, symbol="==")


def MustBeNotEqual(value: Number, /):
    return partial(_comparison_validator, to=value, fn=ne, symbol="!=")


def MustBeGreaterThan(value: Number, /):
    return partial(_comparison_validator, to=value, fn=gt, symbol=">")


def MustBeGreaterThanOrEqual(value: Number, /):
    return partial(_comparison_validator, to=value, fn=ge, symbol=">=")


def MustBeLessThan(value: Number, /):
    return partial(_comparison_validator, to=value, fn=lt, symbol="<")


def MustBeLessThanOrEqual(value: Number, /):
    return partial(_comparison_validator, to=value, fn=le, symbol="<=")


# Membership and range validation functions


def MustBeIn(value_set: Iterable, /):
    def f(value):
        if not contains(set(value_set), value):
            raise ValueError(f"Value {value} must be in {set(value_set)}")

    return f


def _must_be_between(value, *, min_value: Number, max_value: Number):
    if not (ge(value, min_value) and le(value, max_value)):
        exc_msg = f"Value {value} must be between {min_value} and {max_value}."
        raise ValueError(exc_msg)


def MustBeBetween(*, min_value: Number, max_value: Number):
    return lambda value: _must_be_between(
        value, min_value=min_value, max_value=max_value
    )


# Size validation functions


def MustBeEmpty(value: Iterable, /):
    if value:
        raise ValueError(f"Value {value} must be empty.")


def MustBeNonEmpty(value: Iterable, /):
    if not value:
        raise ValueError(f"Value {value} must not be empty.")


def MustHaveLengthEqual(value: int, /):
    def f(val: Sized, /):
        if len(val) != value:
            raise ValueError(f"Length of {val} must be equal to {value}.")

    return f


def MustHaveLengthGreaterThan(value: int, /):
    def f(val: Sized, /):
        if not (len(val) > value):
            raise ValueError(f"Length of {val} must be equal to {value}")

    return f


def MustHaveValuesBetween(*, min_value: Number, max_value: Number):
    def f(values: Iterable, /):
        for val in values:
            _must_be_between(val, min_value=min_value, max_value=max_value)

    return f

# TODO: Add MustHaveLengthBetween

# TODO: Add more validation functions as needed
# TODO: Add support for datatypes
