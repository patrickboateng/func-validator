from functools import partial
from operator import contains
from typing import Container, Iterable, Sized, Callable

from ._core import Number, T, ValidationError
from .numeric_arg_validators import (
    MustBeLessThan,
    MustBeLessThanOrEqual,
    MustBeGreaterThanOrEqual,
    MustBeGreaterThan,
    MustBeEqual,
    MustBeBetween,
)


def _iterable_len_validator(
    arg_values: Sized,
    arg_name: str,
    /,
    *,
    func: Callable,
):
    func(len(arg_values), arg_name)


def _iterable_values_validator(
    values: Iterable,
    arg_name: str,
    /,
    *,
    func: Callable,
):
    for value in values:
        func(value, arg_name)


# Membership and range validation functions


def _must_be_member_of(arg_value, arg_name: str, /, *, value_set: Container):
    if not contains(value_set, arg_value):
        raise ValidationError(f"{arg_name}:{arg_value} must be in {value_set!r}")


def MustBeMemberOf(value_set: Container, /) -> Callable[[T], None]:
    """Validates that the value is a member of the specified set.

    :param value_set: The set of values to validate against.
                      `value_set` must support the `in` operator.
    """
    return partial(_must_be_member_of, value_set=value_set)


# Size validation functions


def MustBeEmpty(arg_value: Iterable, arg_name: str, /):
    """Validates that the iterable is empty."""
    if arg_value:
        raise ValidationError(f"{arg_name}:{arg_value} must be empty.")


def MustBeNonEmpty(arg_value: Iterable, arg_name: str, /):
    """Validates that the iterable is not empty."""
    if not arg_value:
        raise ValidationError(f"{arg_name}:{arg_value} must not be empty.")


def MustHaveLengthEqual(value: int, /) -> Callable[[Iterable], None]:
    """Validates that the iterable has length equal to the specified
    value.
    """
    return partial(_iterable_len_validator, func=MustBeEqual(value))


def MustHaveLengthGreaterThan(value: int, /) -> Callable[[Iterable], None]:
    """Validates that the iterable has length greater than the specified
    value.
    """
    return partial(_iterable_len_validator, func=MustBeGreaterThan(value))


def MustHaveLengthGreaterThanOrEqual(value: int, /) -> Callable[[Iterable], None]:
    """Validates that the iterable has length greater than or equal to
    the specified value.
    """
    return partial(_iterable_len_validator, func=MustBeGreaterThanOrEqual(value))


def MustHaveLengthLessThan(value: int, /) -> Callable[[Iterable], None]:
    """Validates that the iterable has length less than the specified
    value.
    """
    return partial(_iterable_len_validator, func=MustBeLessThan(value))


def MustHaveLengthLessThanOrEqual(value: int, /) -> Callable[[Iterable], None]:
    """Validates that the iterable has length less than or equal to
    the specified value.
    """
    return partial(_iterable_len_validator, func=MustBeLessThanOrEqual(value))


def MustHaveLengthBetween(
    *,
    min_value: int,
    max_value: int,
    min_inclusive: bool = True,
    max_inclusive: bool = True,
) -> Callable[[Iterable], None]:
    """Validates that the iterable has length between the specified
    min_value and max_value.

    :param min_value: The minimum length (inclusive or exclusive based
                      on min_inclusive).
    :param max_value: The maximum length (inclusive or exclusive based
                       on max_inclusive).
    :param min_inclusive: If True, min_value is inclusive.
    :param max_inclusive: If True, max_value is inclusive.

    :raises ValidationError: If the iterable length is not within the
                             specified range.

    :return: A validator function that accepts an iterable and raises
             ValidationError if its length is not within the specified
             range.
    """
    return partial(
        _iterable_len_validator,
        func=MustBeBetween(
            min_value=min_value,
            max_value=max_value,
            min_inclusive=min_inclusive,
            max_inclusive=max_inclusive,
        ),
    )


def MustHaveValuesGreaterThan(min_value: Number) -> Callable[[Iterable], None]:
    """Validates that all values in the iterable are greater than the
    specified min_value.

    :param min_value: The minimum value (exclusive).

    :raises ValidationError: If any value in the iterable is not greater
                        than min_value.

    :return: A validator function that accepts an iterable and raises
             ValidationError if any of its values are not greater than
             min_value.
    """
    return partial(_iterable_values_validator, func=MustBeGreaterThan(min_value))


def MustHaveValuesGreaterThanOrEqual(min_value: Number) -> Callable[[Iterable], None]:
    """Validates that all values in the iterable are greater than or
    equal to the specified min_value.

    :param min_value: The minimum value (inclusive).

    :raises ValidationError: If any value in the iterable is not greater
                        than or equal to min_value.

    :return: A validator function that accepts an iterable and raises
             ValidationError if any of its values are not greater than
             or equal to min_value.
    """
    return partial(_iterable_values_validator, func=MustBeGreaterThanOrEqual(min_value))


def MustHaveValuesLessThan(max_value: Number) -> Callable[[Iterable], None]:
    """Validates that all values in the iterable are less than the
    specified max_value.

    :param max_value: The maximum value (exclusive).

    :raises ValidationError: If any value in the iterable is not less
                             than max_value.

    :return: A validator function that accepts an iterable and raises
             ValidationError if any of its values are not less than
             max_value.
    """
    return partial(_iterable_values_validator, func=MustBeLessThan(max_value))


def MustHaveValuesLessThanOrEqual(max_value: Number) -> Callable[[Iterable], None]:
    """Validates that all values in the iterable are less than or
    equal to the specified max_value.

    :param max_value: The maximum value (inclusive).

    :raises ValidationError: If any value in the iterable is not less
                            than or equal to max_value.

    :return: A validator function that accepts an iterable and raises
                ValidationError if any of its values are not less than
                or equal to max_value.
    """
    return partial(_iterable_values_validator, func=MustBeLessThanOrEqual(max_value))


def MustHaveValuesBetween(
    *,
    min_value: Number,
    max_value: Number,
    min_inclusive: bool = True,
    max_inclusive: bool = True,
) -> Callable[[Iterable], None]:
    """Validates that all values in the iterable are between the
    specified min_value and max_value.

    :param min_value: The minimum value (inclusive or exclusive based
                      on min_inclusive).
    :param max_value: The maximum value (inclusive or exclusive based
                       on max_inclusive).
    :param min_inclusive: If True, min_value is inclusive.
    :param max_inclusive: If True, max_value is inclusive.

    :raises ValidationError: If any value in the iterable is not within
                            the specified range.

    :return: A validator function that accepts an iterable and raises
             ValidationError if any of its values are not within the
             specified range.
    """
    return partial(
        _iterable_values_validator,
        func=MustBeBetween(
            min_value=min_value,
            max_value=max_value,
            min_inclusive=min_inclusive,
            max_inclusive=max_inclusive,
        ),
    )
