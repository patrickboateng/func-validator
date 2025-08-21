from functools import partial
from operator import contains, eq, ge, gt, le, lt
from typing import Callable, Container, Iterable, Sized

from ._core import Number, _generic_number_validator


# Membership and range validation functions


# value_set must support the `in` operator
def MustBeIn(value_set: Container, /):
    def f(value):
        if not contains(value_set, value):
            raise ValueError(f"Value {value} must be in {value_set!r}")

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


def _len_validator(values: Sized, /, *, to: int, fn: Callable, symbol: str):
    _generic_number_validator(len(values), to=to, fn=fn, symbol=symbol)


def _iterable_values_validator(values: Iterable, /, *, fn: Callable):
    for value in values:
        fn(value)


def MustBeEmpty(value: Iterable, /):
    if value:
        raise ValueError(f"Value {value} must be empty.")


def MustBeNonEmpty(value: Iterable, /):
    if not value:
        raise ValueError(f"Value {value} must not be empty.")


def MustHaveLengthEqual(value: int, /):
    return lambda values: _len_validator(values, to=value, fn=eq, symbol="==")


def MustHaveLengthGreaterThan(value: int, /):
    return lambda values: _len_validator(values, to=value, fn=gt, symbol=">")


def MustHaveLengthGreaterThanOrEqual(value: int, /):
    return lambda values: _len_validator(values, to=value, fn=ge, symbol=">=")


def MustHaveLengthLessThan(value: int, /):
    return lambda values: _len_validator(values, to=value, fn=lt, symbol="<")


def MustHaveLengthLessThanOrEqual(value: int, /):
    return lambda values: _len_validator(values, to=value, fn=le, symbol="<=")


def MustHaveLengthBetween(*, min_value: int, max_value: int):
    return lambda values: _must_be_between(
        len(values), min_value=min_value, max_value=max_value
    )


def MustHaveValuesBetween(*, min_value: Number, max_value: Number):
    return lambda values: _iterable_values_validator(
        values,
        fn=partial(_must_be_between, min_value=min_value, max_value=max_value)
    )


def MustHaveValuesGreaterThan(*, min_value: Number):
    return lambda values: _iterable_values_validator(
        values,
        fn=partial(_generic_number_validator, to=min_value, fn=gt, symbol=">")
    )


def MustHaveValuesGreaterThanOrEqual(*, min_value: Number):
    return lambda values: _iterable_values_validator(
        values,
        fn=partial(_generic_number_validator, to=min_value, fn=ge, symbol=">=")
    )


def MustHaveValuesLessThan(*, max_value: Number):
    return lambda values: _iterable_values_validator(
        values,
        fn=partial(_generic_number_validator, to=max_value, fn=lt, symbol="<")
    )


def MustHaveValuesLessThanOrEqual(*, max_value: Number):
    return lambda values: _iterable_values_validator(
        values,
        fn=partial(_generic_number_validator, to=max_value, fn=le, symbol="<=")
    )
