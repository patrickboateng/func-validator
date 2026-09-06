import math
from functools import partial
from operator import eq, ge, gt, le, lt, ne
from typing import Callable, Final, Optional

from ._core import (
    OPERATOR_SYMBOLS,
    ErrorMsg,
    Number,
    T,
    ValidationError,
    Validator,
)

DEFAULT_NUMERIC_VALIDATOR_ERR_MSG = (
    "${arg_name}: ${arg_value} must be " "${fn_symbol} ${to}."
)
MUST_BE_BTWN_VALIDATOR_ERR_MSG = (
    "${arg_name}:${arg_value} must be, ${arg_name} ${min_fn_symbol} "
    "${min_value} and ${arg_name} ${max_fn_symbol} ${max_value}."
)


def _generic_number_validator(
    arg_value: T,
    arg_name: str,
    /,
    *,
    to: T,
    fn: Callable,
    err_msg: str,
    extra_err_msg_args: dict,
):
    if not fn(arg_value, to):
        # if fn is wrapped with functools.partial
        if hasattr(fn, "func"):
            fn_name = fn.func.__name__
        else:
            fn_name = fn.__name__
        fn_symbol = OPERATOR_SYMBOLS[fn_name]
        err_msg = ErrorMsg(err_msg).transform(
            arg_name=arg_name,
            arg_value=arg_value,
            to=to,
            fn_symbol=fn_symbol,
            **extra_err_msg_args,
        )
        raise ValidationError(err_msg)


def _must_be_between(
    arg_value: T,
    arg_name: str,
    /,
    *,
    min_value: Number,
    max_value: Number,
    min_inclusive: bool,
    max_inclusive: bool,
    err_msg: str,
    extra_err_msg_args: dict,
):
    min_fn = ge if min_inclusive else gt
    max_fn = le if max_inclusive else lt
    if not (min_fn(arg_value, min_value) and max_fn(arg_value, max_value)):
        min_fn_symbol = OPERATOR_SYMBOLS[min_fn.__name__]
        max_fn_symbol = OPERATOR_SYMBOLS[max_fn.__name__]
        err_msg = ErrorMsg(err_msg).transform(
            arg_name=arg_name,
            arg_value=arg_value,
            min_value=min_value,
            max_value=max_value,
            min_fn_symbol=min_fn_symbol,
            max_fn_symbol=max_fn_symbol,
            **extra_err_msg_args,
        )
        raise ValidationError(err_msg)


class NumericValidator(Validator):

    DEFAULT_ERROR_MSG = DEFAULT_NUMERIC_VALIDATOR_ERR_MSG

    def __init__(
        self,
        *,
        err_msg: Optional[str] = None,
        extra_err_msg_args: Optional[dict] = None,
    ):
        super().__init__(
            err_msg=err_msg,
            extra_err_msg_args=extra_err_msg_args,
        )


class MustBeBetween(NumericValidator):
    """Validates that the number is between min_value and max_value."""

    DEFAULT_ERROR_MSG: Final[str] = MUST_BE_BTWN_VALIDATOR_ERR_MSG

    def __init__(
        self,
        *,
        min_value: Number,
        max_value: Number,
        min_inclusive: bool = True,
        max_inclusive: bool = True,
        err_msg: Optional[str] = None,
        extra_err_msg_args: Optional[dict] = None,
    ):
        """
        :param min_value: The minimum value (inclusive or exclusive based
                          on min_inclusive).
        :param max_value: The maximum value (inclusive or exclusive based
                          on max_inclusive).
        :param min_inclusive: If True, min_value is inclusive. Default is True.
        :param max_inclusive: If True, max_value is inclusive. Default is True.
        :param err_msg: error message.
        """
        super().__init__(
            err_msg=err_msg,
            extra_err_msg_args=extra_err_msg_args,
        )

        self.min_value = min_value
        self.max_value = max_value
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive

    def __call__(self, arg_value: Number, arg_name: str):
        _must_be_between(
            arg_value,
            arg_name,
            min_value=self.min_value,
            max_value=self.max_value,
            min_inclusive=self.min_inclusive,
            max_inclusive=self.max_inclusive,
            err_msg=self.err_msg,
            extra_err_msg_args=self.extra_err_msg_args,
        )


# Numeric validation functions


class MustBePositive(NumericValidator):
    r"""Validates that the number is positive ($x \gt 0$)."""

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=0.0,
            fn=gt,
            err_msg=self.err_msg,
            extra_err_msg_args=self.extra_err_msg_args,
        )


must_be_positive: Final = MustBePositive()


class MustBeNonPositive(NumericValidator):
    r"""Validates that the number is non-positive ($x \le 0$)."""

    def __call__(self, arg_value: Number, arg_name: str, /):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=0.0,
            fn=le,
            err_msg=self.err_msg,
            extra_err_msg_args=self.extra_err_msg_args,
        )


must_be_non_positive: Final = MustBeNonPositive()


class MustBeNegative(NumericValidator):
    r"""Validates that the number is negative ($x \lt 0$)."""

    def __call__(self, arg_value: Number, arg_name: str, /):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=0.0,
            fn=lt,
            err_msg=self.err_msg,
            extra_err_msg_args=self.extra_err_msg_args,
        )


must_be_negative: Final = MustBeNegative()


class MustBeNonNegative(NumericValidator):
    r"""Validates that the number is non-negative ($x \ge 0$)."""

    def __call__(self, arg_value: Number, arg_name: str, /):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=0.0,
            fn=ge,
            err_msg=self.err_msg,
            extra_err_msg_args=self.extra_err_msg_args,
        )


must_be_non_negative: Final = MustBeNonNegative()

# Comparison validation functions


class MustBeEqual(NumericValidator):
    """Validates that the number is equal to the specified value"""

    def __init__(
        self,
        value: Number,
        /,
        *,
        err_msg: Optional[str] = None,
        extra_err_msg_args: Optional[dict] = None,
    ) -> None:
        super().__init__(
            err_msg=err_msg,
            extra_err_msg_args=extra_err_msg_args,
        )
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=self.value,
            fn=eq,
            err_msg=self.err_msg,
            extra_err_msg_args=self.extra_err_msg_args,
        )


class MustNotBeEqual(NumericValidator):
    """Validates that the number is not equal to the specified value"""

    def __init__(
        self,
        value: Number,
        /,
        *,
        err_msg: Optional[str] = None,
        extra_err_msg_args: Optional[dict] = None,
    ) -> None:
        super().__init__(
            err_msg=err_msg,
            extra_err_msg_args=extra_err_msg_args,
        )
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=self.value,
            fn=ne,
            err_msg=self.err_msg,
            extra_err_msg_args=self.extra_err_msg_args,
        )


class MustBeAlmostEqual(NumericValidator):
    """Validates that argument value (float) is almost equal to the
    specified value.

    Uses `math.isclose` (which means key-word arguments with the exception
    of `err_msg` and `extra_err_msg_args`, are passed to `math.isclose`)
    for comparison, see its
    [documentation](https://docs.python.org/3/library/math.html#math.isclose)
    for details.
    """

    def __init__(
        self,
        value: float,
        /,
        *,
        rel_tol=1e-9,
        abs_tol=0.0,
        err_msg: Optional[str] = None,
        extra_err_msg_args: Optional[dict] = None,
    ):
        super().__init__(
            err_msg=err_msg,
            extra_err_msg_args=extra_err_msg_args,
        )
        self.value = value
        self.rel_tol = rel_tol
        self.abs_tol = abs_tol

    def __call__(self, arg_value: float, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=self.value,
            fn=partial(
                math.isclose, rel_tol=self.rel_tol, abs_tol=self.abs_tol
            ),
            err_msg=self.err_msg,
            extra_err_msg_args=self.extra_err_msg_args,
        )


class MustBeGreaterThan(NumericValidator):
    """Validates that the number is greater than the specified value"""

    def __init__(
        self,
        value: Number,
        /,
        *,
        err_msg: Optional[str] = None,
        extra_err_msg_args: Optional[dict] = None,
    ) -> None:
        super().__init__(
            err_msg=err_msg,
            extra_err_msg_args=extra_err_msg_args,
        )
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=self.value,
            fn=gt,
            err_msg=self.err_msg,
            extra_err_msg_args=self.extra_err_msg_args,
        )


class MustBeGreaterThanOrEqual(NumericValidator):

    def __init__(
        self,
        value: Number,
        /,
        *,
        err_msg: Optional[str] = None,
        extra_err_msg_args: Optional[dict] = None,
    ) -> None:
        """Validates that the number is greater than or equal to the
        specified value.
        """
        super().__init__(
            err_msg=err_msg,
            extra_err_msg_args=extra_err_msg_args,
        )
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=self.value,
            fn=ge,
            err_msg=self.err_msg,
            extra_err_msg_args=self.extra_err_msg_args,
        )


class MustBeLessThan(NumericValidator):

    def __init__(
        self,
        value: Number,
        /,
        *,
        err_msg: Optional[str] = None,
        extra_err_msg_args: Optional[dict] = None,
    ) -> None:
        """Validates that the number is less than the specified value"""
        super().__init__(
            err_msg=err_msg,
            extra_err_msg_args=extra_err_msg_args,
        )
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=self.value,
            fn=lt,
            err_msg=self.err_msg,
            extra_err_msg_args=self.extra_err_msg_args,
        )


class MustBeLessThanOrEqual(NumericValidator):

    def __init__(
        self,
        value: Number,
        /,
        *,
        err_msg: Optional[str] = None,
        extra_err_msg_args: Optional[dict] = None,
    ) -> None:
        """Validates that the number is less than or equal to the
        specified value.
        """
        super().__init__(
            err_msg=err_msg,
            extra_err_msg_args=extra_err_msg_args,
        )
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=self.value,
            fn=le,
            err_msg=self.err_msg,
            extra_err_msg_args=self.extra_err_msg_args,
        )
