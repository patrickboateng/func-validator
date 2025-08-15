from functools import partial
from operator import ge, le, gt, lt, eq, ne, contains


# Numeric validation functions
def MustBePositive(value, /):
    if not gt(value, 0):
        raise ValueError(f"Value {value} must be greater than 0.")


def MustBeNonPositive(value, /):
    if not le(value, 0):
        raise ValueError(f"Value {value} must be less than or equal to 0.")


def MustBeNegative(value, /):
    if not lt(value, 0):
        raise ValueError(f"Value {value} must be less than 0.")


def MustBeNonNegative(value, /):
    if not ge(value, 0):
        exc_msg = f"Value {value} must be greater than or equal to 0."
        raise ValueError(exc_msg)


# Comparison validation functions


def _comparison_validator(value, *, to, fn, symbol):
    if not fn(value, to):
        raise ValueError(f"Value {value} must be {symbol} {to}.")


def MustBeEqual(value, /):
    return partial(_comparison_validator, to=value, fn=eq, symbol="==")


def MustBeNotEqual(value, /):
    return partial(_comparison_validator, to=value, fn=ne, symbol="!=")


def MustBeGreaterThan(value, /):
    return partial(_comparison_validator, to=value, fn=gt, symbol=">")


def MustBeGreaterThanOrEqual(value, /):
    return partial(_comparison_validator, to=value, fn=ge, symbol=">=")


def MustBeLessThan(value, /):
    return partial(_comparison_validator, to=value, fn=lt, symbol="<")


def MustBeLessThanOrEqual(value, /):
    return partial(_comparison_validator, to=value, fn=le, symbol="<=")


# Membership and range validation functions


def MustBeIn(value_set, /):
    def f(value):
        if not contains(set(value_set), value):
            raise ValueError(f"Value {value} must be in {set(value_set)}")

    return f


def MustBeBetween(*, min_value, max_value):
    def f(value):
        if not (ge(value, min_value) and le(value, max_value)):
            exc_msg = f"Value {value} must be between " f"{min_value} and {max_value}."
            raise ValueError(exc_msg)

    return f


# Size validation functions

def MustBeEmpty(value, /):
    if value:
        raise ValueError(f"Value {value} must be empty.")


def MustBeNonEmpty(value, /):
    if not value:
        raise ValueError(f"Value {value} must not be empty.")


def MustHaveLength(value, /):
    def f(val):
        if len(val) != value:
            raise ValueError(f"Length of {val} should be {value}.")
    return f

# TODO: Add MustHaveLengthBetween


# TODO: Add more validation functions as needed
# TODO: Add support for datatypes
