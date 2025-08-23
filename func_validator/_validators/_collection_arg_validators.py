from functools import partial
from operator import contains
from typing import Container, Iterable, Sized, Callable

from ._core import Number
from ._numeric_arg_validators import (
    MustBeLessThan,
    MustBeLessThanOrEqual,
    MustBeGreaterThanOrEqual,
    MustBeGreaterThan,
    MustBeEqual,
    MustBeBetween,
)


def _iterable_len_validator(values: Sized, /, *, func: Callable):
    func(len(values))


def _iterable_values_validator(values: Iterable, /, *, func: Callable):
    for value in values:
        func(value)


# Membership and range validation functions


# value_set must support the `in` operator
def MustBeIn(value_set: Container, /):
    def f(value):
        if not contains(value_set, value):
            raise ValueError(f"Value {value} must be in {value_set!r}")

    return f


# Size validation functions


def MustBeEmpty(value: Iterable, /):
    if value:
        raise ValueError(f"Value {value} must be empty.")


def MustBeNonEmpty(value: Iterable, /):
    if not value:
        raise ValueError(f"Value {value} must not be empty.")


def MustHaveLengthEqual(value: int, /):
    return partial(_iterable_len_validator, func=MustBeEqual(value))


def MustHaveLengthGreaterThan(value: int, /):
    return partial(_iterable_len_validator, func=MustBeGreaterThan(value))


def MustHaveLengthGreaterThanOrEqual(value: int, /):
    return partial(_iterable_len_validator,
                   func=MustBeGreaterThanOrEqual(value))


def MustHaveLengthLessThan(value: int, /):
    return partial(_iterable_len_validator, func=MustBeLessThan(value))


def MustHaveLengthLessThanOrEqual(value: int, /):
    return partial(_iterable_len_validator, func=MustBeLessThanOrEqual(value))


def MustHaveLengthBetween(
        *,
        min_value: int,
        max_value: int,
        min_inclusive: bool = True,
        max_inclusive: bool = True,
):
    return partial(
        _iterable_len_validator,
        func=MustBeBetween(
            min_value=min_value,
            max_value=max_value,
            min_inclusive=min_inclusive,
            max_inclusive=max_inclusive,
        ),
    )


def MustHaveValuesBetween(
        *,
        min_value: Number,
        max_value: Number,
        min_inclusive: bool = True,
        max_inclusive: bool = True,
):
    return partial(
        _iterable_values_validator,
        func=MustBeBetween(
            min_value=min_value,
            max_value=max_value,
            min_inclusive=min_inclusive,
            max_inclusive=max_inclusive,
        ),
    )


def MustHaveValuesGreaterThan(min_value: Number):
    return partial(_iterable_values_validator,
                   func=MustBeGreaterThan(min_value))


def MustHaveValuesGreaterThanOrEqual(min_value: Number):
    return partial(_iterable_values_validator,
                   func=MustBeGreaterThanOrEqual(min_value))


def MustHaveValuesLessThan(max_value: Number):
    return partial(_iterable_values_validator, func=MustBeLessThan(max_value))


def MustHaveValuesLessThanOrEqual(max_value: Number):
    return partial(_iterable_values_validator,
                   func=MustBeLessThanOrEqual(max_value))
