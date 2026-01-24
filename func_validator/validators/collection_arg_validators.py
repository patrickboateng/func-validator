from operator import contains
from typing import Callable, Container, Final, Iterable, Optional, Sized

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

COLLECTION_LEN_VALIDATOR_ERR_MSG = (
    "Length of ${arg_name}: ${arg_value} must be ${fn_symbol} ${to}"
)
COLLECTION_VALUES_VALIDATOR_ERR_MSG = (
    "Values of ${arg_name}: ${arg_value} must be ${fn_symbol} ${to}"
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
    extra_msg_args: dict,
):
    if not contains(value_set, arg_value):
        err_msg = ErrorMsg(err_msg).transform(
            arg_value=arg_value,
            arg_name=arg_name,
            value_set=repr(value_set),
            **extra_msg_args,
        )
        raise ValidationError(err_msg)


class MustBeMemberOf(Validator):

    DEFAULT_ERROR_MSG: Final[str] = (
        "${arg_name}: ${arg_value} must be in ${value_set}"
    )

    def __init__(
        self,
        value_set: Container,
        *,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
    ):
        """Validates that the value is a member of the specified set.

        :param value_set: The set of values to validate against.
                          `value_set` must support the `in` operator.
        :param err_msg: Error message.
        """
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )
        self.value_set = value_set

    def __call__(self, arg_value: T, arg_name: str):
        _must_be_member_of(
            arg_value,
            arg_name,
            value_set=self.value_set,
            err_msg=self.err_msg,
            extra_msg_args=self.extra_msg_args,
        )


# Size validation functions


class MustBeEmpty(Validator):

    DEFAULT_ERROR_MSG: Final[str] = COLLECTION_LEN_VALIDATOR_ERR_MSG

    def __init__(
        self,
        *,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
    ):
        """
        :param err_msg: Error message.
        """
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )

    def __call__(self, arg_value: Sized, arg_name: str, /):
        """Validates that the iterable is empty."""
        fn = MustBeEqual(
            0, err_msg=self.err_msg, extra_msg_args=self.extra_msg_args
        )
        _iterable_len_validator(arg_value, arg_name, func=fn)


class MustBeNonEmpty(Validator):

    DEFAULT_ERROR_MSG: Final[str] = COLLECTION_LEN_VALIDATOR_ERR_MSG

    def __init__(
        self,
        *,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
    ):
        """
        :param err_msg: Error message.
        """
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )

    def __call__(self, arg_value: Sized, arg_name: str, /):
        """Validates that the iterable is not empty."""
        fn = MustNotBeEqual(
            0, err_msg=self.err_msg, extra_msg_args=self.extra_msg_args
        )
        _iterable_len_validator(arg_value, arg_name, func=fn)


class MustHaveLengthEqual(Validator):
    """Validates that the iterable has length equal to the specified
    value.
    """

    DEFAULT_ERROR_MSG: Final[str] = COLLECTION_LEN_VALIDATOR_ERR_MSG

    def __init__(
        self,
        value: int,
        *,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
    ):
        """
        :param value: The length of the iterable.
        :param err_msg: Error message.
        """
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )
        self.value = value

    def __call__(self, arg_value: Sized, arg_name: str):
        fn = MustBeEqual(
            self.value,
            err_msg=self.err_msg,
            extra_msg_args=self.extra_msg_args,
        )
        _iterable_len_validator(arg_value, arg_name, func=fn)


class MustHaveLengthGreaterThan(Validator):
    """Validates that the iterable has length greater than the specified
    value.
    """

    DEFAULT_ERROR_MSG: Final[str] = COLLECTION_LEN_VALIDATOR_ERR_MSG

    def __init__(
        self,
        value: int,
        *,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
    ):
        """
        :param value: The length of the iterable.
        :param err_msg: Error message.
        """
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )
        self.value = value

    def __call__(self, arg_value: Sized, arg_name: str):
        fn = MustBeGreaterThan(
            self.value,
            err_msg=self.err_msg,
            extra_msg_args=self.extra_msg_args,
        )
        _iterable_len_validator(arg_value, arg_name, func=fn)


class MustHaveLengthGreaterThanOrEqual(Validator):
    """Validates that the iterable has length greater than or equal to
    the specified value.
    """

    DEFAULT_ERROR_MSG: Final[str] = COLLECTION_LEN_VALIDATOR_ERR_MSG

    def __init__(
        self,
        value: int,
        *,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
    ):
        """
        :param value: The length of the iterable.
        :param err_msg: Error message
        """
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )
        self.value = value

    def __call__(self, arg_value: Sized, arg_name: str):
        fn = MustBeGreaterThanOrEqual(
            self.value,
            err_msg=self.err_msg,
            extra_msg_args=self.extra_msg_args,
        )
        _iterable_len_validator(arg_value, arg_name, func=fn)


class MustHaveLengthLessThan(Validator):
    """Validates that the iterable has length less than the specified
    value.
    """

    DEFAULT_ERROR_MSG: Final[str] = COLLECTION_LEN_VALIDATOR_ERR_MSG

    def __init__(
        self,
        value: int,
        *,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
    ):
        """
        :param value: The length of the iterable.
        :param err_msg: Error message.
        """
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )
        self.value = value

    def __call__(self, arg_value: Sized, arg_name: str):
        fn = MustBeLessThan(
            self.value,
            err_msg=self.err_msg,
            extra_msg_args=self.extra_msg_args,
        )
        _iterable_len_validator(arg_value, arg_name, func=fn)


class MustHaveLengthLessThanOrEqual(Validator):
    """Validates that the iterable has length less than or equal to
    the specified value.
    """

    DEFAULT_ERROR_MSG: Final[str] = COLLECTION_LEN_VALIDATOR_ERR_MSG

    def __init__(
        self,
        value: int,
        *,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
    ):
        """
        :param value: The length of the iterable.
        :param err_msg: Error message.
        """
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )
        self.value = value

    def __call__(self, arg_value: Sized, arg_name: str):
        fn = MustBeLessThanOrEqual(
            self.value,
            err_msg=self.err_msg,
            extra_msg_args=self.extra_msg_args,
        )
        _iterable_len_validator(arg_value, arg_name, func=fn)


class MustHaveLengthBetween(Validator):
    """Validates that the iterable has length between the specified
    min_value and max_value.
    """

    DEFAULT_ERROR_MSG: Final[str] = (
        "Length of ${arg_name}: ${arg_value} must be ${min_fn_symbol} ${min_value} "
        "and ${max_fn_symbol} ${max_value} "
    )

    def __init__(
        self,
        *,
        min_value: int,
        max_value: int,
        min_inclusive: bool = True,
        max_inclusive: bool = True,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
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
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )
        self.min_value = min_value
        self.max_value = max_value
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive
        self.err_msg = err_msg

    def __call__(self, arg_value: Sized, arg_name: str):
        fn = MustBeBetween(
            min_value=self.min_value,
            max_value=self.max_value,
            min_inclusive=self.min_inclusive,
            max_inclusive=self.max_inclusive,
            err_msg=self.err_msg,
            extra_msg_args=self.extra_msg_args,
        )
        _iterable_len_validator(arg_value, arg_name, func=fn)


class MustHaveValuesGreaterThan(Validator):
    """Validates that all values in the iterable are greater than the
    specified min_value.
    """

    DEFAULT_ERROR_MSG: Final[str] = COLLECTION_VALUES_VALIDATOR_ERR_MSG

    def __init__(
        self,
        min_value: Number,
        *,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
    ):
        """
        :param min_value: The minimum value the values in the iterable
                          should be greater than.
        :param err_msg: Error message.
        """
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )
        self.min_value = min_value

    def __call__(self, values: Iterable, arg_name: str):
        fn = MustBeGreaterThan(
            self.min_value,
            err_msg=self.err_msg,
            extra_msg_args=self.extra_msg_args,
        )
        _iterable_values_validator(values, arg_name, func=fn)


class MustHaveValuesGreaterThanOrEqual(Validator):
    """Validates that all values in the iterable are greater than or
    equal to the specified min_value.
    """

    DEFAULT_ERROR_MSG: Final[str] = COLLECTION_VALUES_VALIDATOR_ERR_MSG

    def __init__(
        self,
        min_value: Number,
        *,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
    ):
        """
        :param min_value: The minimum value the values in the iterable
                          should be greater than or equal to.
        :param err_msg: Error message.
        """
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )
        self.min_value = min_value

    def __call__(self, values: Iterable, arg_name: str):
        fn = MustBeGreaterThanOrEqual(
            self.min_value,
            err_msg=self.err_msg,
            extra_msg_args=self.extra_msg_args,
        )
        _iterable_values_validator(values, arg_name, func=fn)


class MustHaveValuesLessThan(Validator):
    """Validates that all values in the iterable are less than the
    specified max_value.
    """

    DEFAULT_ERROR_MSG: Final[str] = COLLECTION_VALUES_VALIDATOR_ERR_MSG

    def __init__(
        self,
        max_value: Number,
        *,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
    ):
        """
        :param max_value: The maximum value the values in the iterable
                          should be less than.
        :param err_msg: Error message.
        """
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )
        self.max_value = max_value

    def __call__(self, values: Iterable, arg_name: str):
        fn = MustBeLessThan(
            self.max_value,
            err_msg=self.err_msg,
            extra_msg_args=self.extra_msg_args,
        )
        _iterable_values_validator(values, arg_name, func=fn)


class MustHaveValuesLessThanOrEqual(Validator):
    """Validates that all values in the iterable are less than or
    equal to the specified max_value.
    """

    DEFAULT_ERROR_MSG: Final[str] = COLLECTION_VALUES_VALIDATOR_ERR_MSG

    def __init__(
        self,
        max_value: Number,
        *,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
    ):
        """
        :param max_value: The maximum value the values in the iterable
                          should be less than or equal to.
        :param err_msg: Error message.
        """
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )
        self.max_value = max_value

    def __call__(self, values: Iterable, arg_name: str):
        fn = MustBeLessThanOrEqual(
            self.max_value,
            err_msg=self.err_msg,
            extra_msg_args=self.extra_msg_args,
        )
        _iterable_values_validator(values, arg_name, func=fn)


class MustHaveValuesBetween(Validator):
    """Validates that all values in the iterable are between the
    specified min_value and max_value.
    """

    DEFAULT_ERROR_MSG: Final[str] = (
        "Values of ${arg_name}: ${arg_value} must be ${min_fn_symbol} ${min_value} "
        "and ${max_fn_symbol} ${max_value} "
    )

    def __init__(
        self,
        *,
        min_value: Number,
        max_value: Number,
        min_inclusive: bool = True,
        max_inclusive: bool = True,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
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
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )
        self.min_value = min_value
        self.max_value = max_value
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive

    def __call__(self, values: Iterable, arg_name: str):
        fn = MustBeBetween(
            min_value=self.min_value,
            max_value=self.max_value,
            min_inclusive=self.min_inclusive,
            max_inclusive=self.max_inclusive,
            err_msg=self.err_msg,
            extra_msg_args=self.extra_msg_args,
        )
        _iterable_values_validator(values, arg_name, func=fn)
