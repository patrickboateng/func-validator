from operator import contains
from typing import Callable, Container, Iterable, Sized, Optional

from ._core import Number, T, ValidationError, Validator
from .numeric_arg_validators import (
    MustBeBetween,
    MustBeEqual,
    MustNotBeEqual,
    MustBeGreaterThan,
    MustBeGreaterThanOrEqual,
    MustBeLessThan,
    MustBeLessThanOrEqual,
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


def _must_be_member_of(
        arg_value,
        arg_name: str,
        /,
        *,
        value_set: Container,
        err_msg: str,
):
    if not contains(value_set, arg_value):
        msg = (
            err_msg
            if err_msg is not None
            else f"{arg_name}:{arg_value} must be in {value_set!r}"
        )
        raise ValidationError(msg)


class MustBeMemberOf(Validator):

    def __init__(self, value_set: Container, *, err_msg: Optional[str] = None):
        """Validates that the value is a member of the specified set.

        :param value_set: The set of values to validate against.
                          `value_set` must support the `in` operator.
        """
        self.value_set = value_set
        self.err_msg = err_msg

    def __call__(self, arg_value: T, arg_name: str):
        _must_be_member_of(
            arg_value,
            arg_name,
            value_set=self.value_set,
            err_msg=self.err_msg,
        )


# Size validation functions


class MustBeEmpty(Validator):

    def __init__(self, *, err_msg: Optional[str] = None):
        self.err_msg = err_msg

    def __call__(self, arg_value: Sized, arg_name: str, /):
        """Validates that the iterable is empty."""
        _iterable_len_validator(
            arg_value,
            arg_name,
            func=MustBeEqual(0, err_msg=self.err_msg),
        )


class MustBeNonEmpty(Validator):

    def __init__(self, *, err_msg: Optional[str] = None):
        self.err_msg = err_msg

    def __call__(self, arg_value: Sized, arg_name: str, /):
        """Validates that the iterable is not empty."""
        _iterable_len_validator(
            arg_value,
            arg_name,
            func=MustNotBeEqual(0, err_msg=self.err_msg),
        )


class MustHaveLengthEqual(Validator):
    """Validates that the iterable has length equal to the specified
    value.
    """

    def __init__(self, value: int, *, err_msg: Optional[str] = None):
        self.value = value
        self.err_msg = err_msg

    def __call__(self, arg_value: Sized, arg_name: str):
        _iterable_len_validator(
            arg_value,
            arg_name,
            func=MustBeEqual(self.value, err_msg=self.err_msg),
        )


class MustHaveLengthGreaterThan(Validator):
    """Validates that the iterable has length greater than the specified
    value.
    """

    def __init__(self, value: int, *, err_msg: Optional[str] = None):
        self.value = value
        self.err_msg = err_msg

    def __call__(self, arg_value: Sized, arg_name: str):
        _iterable_len_validator(
            arg_value,
            arg_name,
            func=MustBeGreaterThan(self.value, err_msg=self.err_msg),
        )


class MustHaveLengthGreaterThanOrEqual(Validator):
    """Validates that the iterable has length greater than or equal to
    the specified value.
    """

    def __init__(self, value: int, *, err_msg: Optional[str] = None):
        self.value = value
        self.err_msg = err_msg

    def __call__(self, arg_value: Sized, arg_name: str):
        _iterable_len_validator(
            arg_value,
            arg_name,
            func=MustBeGreaterThanOrEqual(self.value, err_msg=self.err_msg),
        )


class MustHaveLengthLessThan(Validator):
    """Validates that the iterable has length less than the specified
    value.
    """

    def __init__(self, value: int, *, err_msg: Optional[str] = None):
        self.value = value
        self.err_msg = err_msg

    def __call__(self, arg_value: Sized, arg_name: str):
        _iterable_len_validator(
            arg_value,
            arg_name,
            func=MustBeLessThan(self.value, err_msg=self.err_msg),
        )


class MustHaveLengthLessThanOrEqual(Validator):
    """Validates that the iterable has length less than or equal to
    the specified value.
    """

    def __init__(self, value: int, *, err_msg: Optional[str] = None):
        self.value = value
        self.err_msg = err_msg

    def __call__(self, arg_value: Sized, arg_name: str):
        _iterable_len_validator(
            arg_value,
            arg_name,
            func=MustBeLessThanOrEqual(self.value, err_msg=self.err_msg),
        )


class MustHaveLengthBetween(Validator):
    """Validates that the iterable has length between the specified
    min_value and max_value.
    """

    def __init__(
            self,
            *,
            min_value: int,
            max_value: int,
            min_inclusive: bool = True,
            max_inclusive: bool = True,
            err_msg: Optional[str] = None,
    ):
        """
        :param min_value: The minimum value (inclusive or exclusive based
                          on min_inclusive).
        :param max_value: The maximum value (inclusive or exclusive based
                          on max_inclusive).
        :param min_inclusive: If True, min_value is inclusive.
        :param max_inclusive: If True, max_value is inclusive.
        :param err_msg: error message.
        """

        self.min_value = min_value
        self.max_value = max_value
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive
        self.err_msg = err_msg

    def __call__(self, arg_value: Sized, arg_name: str):
        func = MustBeBetween(
            min_value=self.min_value,
            max_value=self.max_value,
            min_inclusive=self.min_inclusive,
            max_inclusive=self.max_inclusive,
            err_msg=self.err_msg,
        )
        _iterable_len_validator(arg_value, arg_name, func=func)


class MustHaveValuesGreaterThan(Validator):
    """Validates that all values in the iterable are greater than the
    specified min_value.
    """

    def __init__(self, min_value: Number, *, err_msg: Optional[str] = None):
        self.min_value = min_value
        self.err_msg = err_msg

    def __call__(self, values: Iterable, arg_name: str):
        _iterable_values_validator(
            values,
            arg_name,
            func=MustBeGreaterThan(self.min_value, err_msg=self.err_msg),
        )


class MustHaveValuesGreaterThanOrEqual(Validator):
    """Validates that all values in the iterable are greater than or
    equal to the specified min_value.
    """

    def __init__(self, min_value: Number, *, err_msg: Optional[str] = None):
        self.min_value = min_value
        self.err_msg = err_msg

    def __call__(self, values: Iterable, arg_name: str):
        _iterable_values_validator(
            values,
            arg_name,
            func=MustBeGreaterThanOrEqual(
                self.min_value, err_msg=self.err_msg
            ),
        )


class MustHaveValuesLessThan(Validator):
    """Validates that all values in the iterable are less than the
    specified max_value.
    """

    def __init__(self, max_value: Number, *, err_msg: Optional[str] = None):
        self.max_value = max_value
        self.err_msg = err_msg

    def __call__(self, values: Iterable, arg_name: str):
        _iterable_values_validator(
            values,
            arg_name,
            func=MustBeLessThan(self.max_value, err_msg=self.err_msg),
        )


class MustHaveValuesLessThanOrEqual(Validator):
    """Validates that all values in the iterable are less than or
    equal to the specified max_value.
    """

    def __init__(self, max_value: Number, *, err_msg: Optional[str] = None):
        self.max_value = max_value
        self.err_msg = err_msg

    def __call__(self, values: Iterable, arg_name: str):
        _iterable_values_validator(
            values,
            arg_name,
            func=MustBeLessThanOrEqual(self.max_value, err_msg=self.err_msg),
        )


class MustHaveValuesBetween(Validator):
    """Validates that all values in the iterable are between the
    specified min_value and max_value.
    """

    def __init__(
            self,
            *,
            min_value: Number,
            max_value: Number,
            min_inclusive: bool = True,
            max_inclusive: bool = True,
            err_msg: Optional[str] = None,
    ):
        """
        :param min_value: The minimum value (inclusive or exclusive based
                          on min_inclusive).
        :param max_value: The maximum value (inclusive or exclusive based
                          on max_inclusive).
        :param min_inclusive: If True, min_value is inclusive.
        :param max_inclusive: If True, max_value is inclusive.
        :param err_msg: error message.
        """
        self.min_value = min_value
        self.max_value = max_value
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive
        self.err_msg = err_msg

    def __call__(self, values: Iterable, arg_name: str):
        func = MustBeBetween(
            min_value=self.min_value,
            max_value=self.max_value,
            min_inclusive=self.min_inclusive,
            max_inclusive=self.max_inclusive,
            err_msg=self.err_msg,
        )
        _iterable_values_validator(values, arg_name, func=func)
