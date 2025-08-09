from functools import partial
from operator import ge, le, gt, lt, eq, contains

__all__ = [
    "MustBePositive",
    "MustBeNonPositive",
    "MustBeNonNegative",
    "MustBeNegative",
    "MustBeEqual",
    "MustBeGreaterThan",
    "MustBeLessThan",
    "MustBeGreaterThanOrEqual",
    "MustBeLessThanOrEqual",
    "MustBeIn",
    "MustBeBetween"
]


# Numeric validation functions
def MustBePositive(value, /, exc_type=ValueError, exc_msg=""):
    exc_msg = exc_msg or f"Value {value} must be greater than 0."
    if not gt(value, 0):
        raise exc_type(exc_msg)


def MustBeNonPositive(value, /, exc_type=ValueError, exc_msg=""):
    exc_msg = exc_msg or f"Value {value} must be less than or equal to 0."
    if not le(value, 0):
        raise exc_type(exc_msg)


def MustBeNonNegative(value, /, exc_type=ValueError, exc_msg=""):
    exc_msg = exc_msg or f"Value {value} must be greater than or equal to 0."
    if not ge(value, 0):
        raise exc_type(exc_msg)


def MustBeNegative(value, /, exc_type=ValueError, exc_msg=""):
    exc_msg = exc_msg or f"Value {value} must be less than 0."
    if not lt(value, 0):
        raise exc_type(exc_msg)


# Comparison validation functions

def _comparison_validator(value, *, to, fn, symbol, exc_type, exc_msg):
    if not fn(value, to):
        raise exc_type(exc_msg)


def MustBeEqual(value, /, exc_type=ValueError, exc_msg=""):
    return partial(_comparison_validator, to=value, fn=eq, symbol="==",
                   exc_type=exc_type, exc_msg=exc_msg)


def MustBeGreaterThan(value, /, exc_type=ValueError, exc_msg=""):
    return partial(_comparison_validator, to=value, fn=gt, symbol=">",
                   exc_type=exc_type, exc_msg=exc_msg)


def MustBeLessThan(value, /, exc_type=ValueError, exc_msg=""):
    return partial(_comparison_validator, to=value, fn=lt, symbol="<",
                   exc_type=exc_type, exc_msg=exc_msg)


def MustBeGreaterThanOrEqual(value, /, exc_type=ValueError, exc_msg=""):
    return partial(_comparison_validator, to=value, fn=ge, symbol=">=",
                   exc_type=exc_type, exc_msg=exc_msg)


def MustBeLessThanOrEqual(value, /, exc_type=ValueError, exc_msg=""):
    return partial(_comparison_validator, to=value, fn=le, symbol="<=",
                   exc_type=exc_type, exc_msg=exc_msg)


# Membership and range validation functions

def MustBeIn(value_set, /, exc_type=ValueError, exc_msg=""):
    def f(value):
        global exc_msg
        exc_msg = exc_msg or f"Value {value} must be in {value_set}"
        if not exc_msg:
            exc_msg = f"Value {value} must be in {value_set}."
        if not contains(value_set, value):
            raise exc_type(exc_msg)

    return f


def MustBeBetween(min_value, max_value, /, exc_type=ValueError, exc_msg=""):
    def f(value):
        global exc_msg
        exc_msg = exc_msg or (f"Value {value} must be between "
                              f"{min_value} and {max_value}.")

        if not (ge(value, min_value) and le(value, max_value)):
            raise exc_type(exc_msg)

    return f

# TODO: Add more validation functions as needed
# TODO: Add support for datatypes
