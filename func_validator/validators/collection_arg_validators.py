from operator import contains
from typing import Callable, Container, Iterable, Sized

from ._core import ErrorMsg, Number, T, ValidationError, Validator
from .numeric_arg_validators import (
    MustBeBetween,
    MustBeEqual,
    MustBeGreaterThan,
    MustBeGreaterThanOrEqual,
    MustBeLessThan,
    MustBeLessThanOrEqual,
    MustNotBeEqual,
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
    err_msg: ErrorMsg,
):
    if not contains(value_set, arg_value):
        err_msg = err_msg.transform(
            arg_value=arg_value,
            arg_name=arg_name,
            value_set=repr(value_set),
        )
        raise ValidationError(err_msg)


class MustBeMemberOf(Validator):

    def __init__(
        self,
        value_set: Container,
        *,
        err_msg: str = "${arg_name}:${arg_value} must be in ${value_set}",
    ):
        """Validates that the value is a member of the specified set.

        :param value_set: The set of values to validate against.
                          `value_set` must support the `in` operator.
        :param err_msg: Error message.
        """
        super().__init__(err_msg=err_msg)
        self.value_set = value_set

    def __call__(self, arg_value: T, arg_name: str):
        _must_be_member_of(
            arg_value,
            arg_name,
            value_set=self.value_set,
            err_msg=self.err_msg,
        )


# Size validation functions


class MustBeEmpty(Validator):

    def __init__(self, *, err_msg: str = ""):
        """
        :param err_msg: Error message.
        """
        super().__init__(err_msg=err_msg)

    def __call__(self, arg_value: Sized, arg_name: str, /):
        """Validates that the iterable is empty."""
        if self.err_msg is None:
            fn = MustBeEqual(0)
        else:
            fn = MustBeEqual(0, err_msg=self.err_msg)
        _iterable_len_validator(arg_value, arg_name, func=fn)


class MustBeNonEmpty(Validator):

    def __init__(self, *, err_msg: str = ""):
        """
        :param err_msg: Error message.
        """
        super().__init__(err_msg=err_msg)

    def __call__(self, arg_value: Sized, arg_name: str, /):
        """Validates that the iterable is not empty."""
        if self.err_msg is None:
            fn = MustNotBeEqual(0)
        else:
            fn = MustNotBeEqual(0, err_msg=self.err_msg)
        _iterable_len_validator(arg_value, arg_name, func=fn)


class MustHaveLengthEqual(Validator):
    """Validates that the iterable has length equal to the specified
    value.
    """

    def __init__(self, value: int, *, err_msg: str = ""):
        """
        :param value: The length of the iterable.
        :param err_msg: Error message.
        """
        super().__init__(err_msg=err_msg)
        self.value = value

    def __call__(self, arg_value: Sized, arg_name: str):
        if self.err_msg is None:
            fn = MustBeEqual(self.value)
        else:
            fn = MustBeEqual(self.value, err_msg=self.err_msg)
        _iterable_len_validator(arg_value, arg_name, func=fn)


class MustHaveLengthGreaterThan(Validator):
    """Validates that the iterable has length greater than the specified
    value.
    """

    def __init__(self, value: int, *, err_msg: str = ""):
        """
        :param value: The length of the iterable.
        :param err_msg: Error message.
        """
        super().__init__(err_msg=err_msg)
        self.value = value

    def __call__(self, arg_value: Sized, arg_name: str):
        if self.err_msg is None:
            fn = MustBeGreaterThan(self.value)
        else:
            fn = MustBeGreaterThan(self.value, err_msg=self.err_msg)
        _iterable_len_validator(arg_value, arg_name, func=fn)


class MustHaveLengthGreaterThanOrEqual(Validator):
    """Validates that the iterable has length greater than or equal to
    the specified value.
    """

    def __init__(self, value: int, *, err_msg: str = ""):
        """
        :param value: The length of the iterable.
        :param err_msg: Error message
        """
        super().__init__(err_msg=err_msg)
        self.value = value

    def __call__(self, arg_value: Sized, arg_name: str):
        if self.err_msg is None:
            fn = MustBeGreaterThanOrEqual(self.value)
        else:
            fn = MustBeGreaterThanOrEqual(self.value, err_msg=self.err_msg)
        _iterable_len_validator(arg_value, arg_name, func=fn)


class MustHaveLengthLessThan(Validator):
    """Validates that the iterable has length less than the specified
    value.
    """

    def __init__(self, value: int, *, err_msg: str = ""):
        """
        :param value: The length of the iterable.
        :param err_msg: Error message.
        """
        super().__init__(err_msg=err_msg)
        self.value = value

    def __call__(self, arg_value: Sized, arg_name: str):
        if self.err_msg is None:
            fn = MustBeLessThan(self.value)
        else:
            fn = MustBeLessThan(self.value, err_msg=self.err_msg)
        _iterable_len_validator(arg_value, arg_name, func=fn)


class MustHaveLengthLessThanOrEqual(Validator):
    """Validates that the iterable has length less than or equal to
    the specified value.
    """

    def __init__(self, value: int, *, err_msg: str = ""):
        """
        :param value: The length of the iterable.
        :param err_msg: Error message.
        """
        super().__init__(err_msg=err_msg)
        self.value = value

    def __call__(self, arg_value: Sized, arg_name: str):
        if self.err_msg is None:
            fn = MustBeLessThanOrEqual(self.value)
        else:
            fn = MustBeLessThanOrEqual(self.value, err_msg=self.err_msg)
        _iterable_len_validator(arg_value, arg_name, func=fn)


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
        err_msg: str = "",
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
        super().__init__(err_msg=err_msg)
        self.min_value = min_value
        self.max_value = max_value
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive
        self.err_msg = err_msg

    def __call__(self, arg_value: Sized, arg_name: str):
        if self.err_msg is None:
            fn = MustBeBetween(
                min_value=self.min_value,
                max_value=self.max_value,
                min_inclusive=self.min_inclusive,
                max_inclusive=self.max_inclusive,
            )
        else:
            fn = MustBeBetween(
                min_value=self.min_value,
                max_value=self.max_value,
                min_inclusive=self.min_inclusive,
                max_inclusive=self.max_inclusive,
                err_msg=self.err_msg,
            )
        _iterable_len_validator(arg_value, arg_name, func=fn)


class MustHaveValuesGreaterThan(Validator):
    """Validates that all values in the iterable are greater than the
    specified min_value.
    """

    def __init__(self, min_value: Number, *, err_msg: str = ""):
        """
        :param min_value: The minimum value the values in the iterable
                          should be greater than.
        :param err_msg: Error message.
        """
        super().__init__(err_msg=err_msg)
        self.min_value = min_value

    def __call__(self, values: Iterable, arg_name: str):
        if self.err_msg is None:
            fn = MustBeGreaterThan(self.min_value)
        else:
            fn = MustBeGreaterThan(self.min_value, err_msg=self.err_msg)
        _iterable_values_validator(values, arg_name, func=fn)


class MustHaveValuesGreaterThanOrEqual(Validator):
    """Validates that all values in the iterable are greater than or
    equal to the specified min_value.
    """

    def __init__(self, min_value: Number, *, err_msg: str = ""):
        """
        :param min_value: The minimum value the values in the iterable
                          should be greater than or equal to.
        :param err_msg: Error message.
        """
        super().__init__(err_msg=err_msg)
        self.min_value = min_value

    def __call__(self, values: Iterable, arg_name: str):
        if self.err_msg is None:
            fn = MustBeGreaterThanOrEqual(self.min_value)
        else:
            fn = MustBeGreaterThanOrEqual(self.min_value, err_msg=self.err_msg)
        _iterable_values_validator(values, arg_name, func=fn)


class MustHaveValuesLessThan(Validator):
    """Validates that all values in the iterable are less than the
    specified max_value.
    """

    def __init__(self, max_value: Number, *, err_msg: str = ""):
        """
        :param max_value: The maximum value the values in the iterable
                          should be less than.
        :param err_msg: Error message.
        """
        super().__init__(err_msg=err_msg)
        self.max_value = max_value

    def __call__(self, values: Iterable, arg_name: str):
        if self.err_msg is None:
            fn = MustBeLessThan(self.max_value)
        else:
            fn = MustBeLessThan(self.max_value, err_msg=self.err_msg)
        _iterable_values_validator(values, arg_name, func=fn)


class MustHaveValuesLessThanOrEqual(Validator):
    """Validates that all values in the iterable are less than or
    equal to the specified max_value.
    """

    def __init__(self, max_value: Number, *, err_msg: str = ""):
        """
        :param max_value: The maximum value the values in the iterable
                          should be less than or equal to.
        :param err_msg: Error message.
        """
        super().__init__(err_msg=err_msg)
        self.max_value = max_value

    def __call__(self, values: Iterable, arg_name: str):
        if self.err_msg is None:
            fn = MustBeLessThanOrEqual(self.max_value)
        else:
            fn = MustBeLessThanOrEqual(self.max_value, err_msg=self.err_msg)
        _iterable_values_validator(values, arg_name, func=fn)


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
        err_msg: str = "",
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
        super().__init__(err_msg=err_msg)
        self.min_value = min_value
        self.max_value = max_value
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive

    def __call__(self, values: Iterable, arg_name: str):
        if self.err_msg is None:
            fn = MustBeBetween(
                min_value=self.min_value,
                max_value=self.max_value,
                min_inclusive=self.min_inclusive,
                max_inclusive=self.max_inclusive,
            )
        else:
            fn = MustBeBetween(
                min_value=self.min_value,
                max_value=self.max_value,
                min_inclusive=self.min_inclusive,
                max_inclusive=self.max_inclusive,
                err_msg=self.err_msg,
            )
        _iterable_values_validator(values, arg_name, func=fn)
