import math
from functools import partial
from operator import eq, ge, gt, le, lt, ne
from typing import Callable

from ._core import (
    OPERATOR_SYMBOLS,
    ErrorMsg,
    Number,
    T,
    ValidationError,
    Validator,
)

DEFAULT_NUMERIC_VALIDATOR_ERR_MSG = (
    "${arg_name}:${arg_value} must be ${fn_symbol} ${to}."
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
    err_msg: ErrorMsg,
):
    if not fn(arg_value, to):
        if hasattr(fn, "func"):
            fn_name = fn.func.__name__
        else:
            fn_name = fn.__name__
        fn_symbol = OPERATOR_SYMBOLS[fn_name]
        err_msg = err_msg.transform(
            arg_name=arg_name,
            arg_value=arg_value,
            to=to,
            fn_symbol=fn_symbol,
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
    err_msg: ErrorMsg,
):
    min_fn = ge if min_inclusive else gt
    max_fn = le if max_inclusive else lt
    if not (min_fn(arg_value, min_value) and max_fn(arg_value, max_value)):
        min_fn_symbol = OPERATOR_SYMBOLS[min_fn.__name__]
        max_fn_symbol = OPERATOR_SYMBOLS[max_fn.__name__]
        err_msg = err_msg.transform(
            arg_name=arg_name,
            arg_value=arg_value,
            min_value=min_value,
            max_value=max_value,
            min_fn_symbol=min_fn_symbol,
            max_fn_symbol=max_fn_symbol,
        )

        raise ValidationError(err_msg)


class MustBeBetween(Validator):
    """Validates that the number is between min_value and max_value."""

    def __init__(
        self,
        *,
        min_value: Number,
        max_value: Number,
        min_inclusive: bool = True,
        max_inclusive: bool = True,
        err_msg: str = MUST_BE_BTWN_VALIDATOR_ERR_MSG,
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

        super().__init__(err_msg=err_msg)
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
        )


# Numeric validation functions


class MustBePositive(Validator):
    r"""Validates that the number is positive ($x \gt 0$)."""

    def __init__(self, *, err_msg: str = DEFAULT_NUMERIC_VALIDATOR_ERR_MSG):
        super().__init__(err_msg=err_msg)

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=0.0,
            fn=gt,
            err_msg=self.err_msg,
        )


class MustBeNonPositive(Validator):
    r"""Validates that the number is non-positive ($x \le 0$)."""

    def __init__(
        self, *, err_msg: str = DEFAULT_NUMERIC_VALIDATOR_ERR_MSG
    ) -> None:
        super().__init__(err_msg=err_msg)

    def __call__(self, arg_value: Number, arg_name: str, /):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=0.0,
            fn=le,
            err_msg=self.err_msg,
        )


class MustBeNegative(Validator):
    r"""Validates that the number is negative ($x \lt 0$)."""

    def __init__(
        self, *, err_msg: str = DEFAULT_NUMERIC_VALIDATOR_ERR_MSG
    ) -> None:
        super().__init__(err_msg=err_msg)

    def __call__(self, arg_value: Number, arg_name: str, /):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=0.0,
            fn=lt,
            err_msg=self.err_msg,
        )


class MustBeNonNegative(Validator):
    r"""Validates that the number is non-negative ($x \ge 0$)."""

    def __init__(
        self, *, err_msg: str = DEFAULT_NUMERIC_VALIDATOR_ERR_MSG
    ) -> None:
        super().__init__(err_msg=err_msg)

    def __call__(self, arg_value: Number, arg_name: str, /):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=0.0,
            fn=ge,
            err_msg=self.err_msg,
        )


# Comparison validation functions


# TODO: Deprecate this and work on logic in MustBeProvided
class MustBeTruthy(Validator):

    def __init__(self, *, err_msg: str = "") -> None:
        super().__init__(err_msg=err_msg)

    def __call__(self, arg_value: T, arg_name: str):
        if not bool(arg_value):
            msg = (
                self.err_msg
                if self.err_msg
                else f"{arg_name}:{arg_value} must be provided (or truthy)."
            )
            raise ValidationError(msg)


class MustBeProvided(MustBeTruthy):
    pass


class MustBeEqual(Validator):
    """Validates that the number is equal to the specified value"""

    def __init__(
        self,
        value: Number,
        /,
        *,
        err_msg: str = DEFAULT_NUMERIC_VALIDATOR_ERR_MSG,
    ) -> None:
        super().__init__(err_msg=err_msg)
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=self.value,
            fn=eq,
            err_msg=self.err_msg,
        )


class MustNotBeEqual(Validator):
    """Validates that the number is not equal to the specified value"""

    def __init__(
        self,
        value: Number,
        /,
        *,
        err_msg: str = DEFAULT_NUMERIC_VALIDATOR_ERR_MSG,
    ) -> None:
        super().__init__(err_msg=err_msg)
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=self.value,
            fn=ne,
            err_msg=self.err_msg,
        )


class MustBeAlmostEqual(Validator):
    """Validates that argument value (float) is almost equal to the
    specified value.

    Uses `math.isclose` (which means key-word arguments provided are
    passed to `math.isclose`) for comparison, see its
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
        err_msg: str = DEFAULT_NUMERIC_VALIDATOR_ERR_MSG,
    ):
        super().__init__(err_msg=err_msg)
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
        )


class MustBeGreaterThan(Validator):
    """Validates that the number is greater than the specified value"""

    def __init__(
        self,
        value: Number,
        /,
        *,
        err_msg: str = DEFAULT_NUMERIC_VALIDATOR_ERR_MSG,
    ) -> None:
        super().__init__(err_msg=err_msg)
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=self.value,
            fn=gt,
            err_msg=self.err_msg,
        )


class MustBeGreaterThanOrEqual(Validator):

    def __init__(
        self,
        value: Number,
        /,
        *,
        err_msg: str = DEFAULT_NUMERIC_VALIDATOR_ERR_MSG,
    ) -> None:
        """Validates that the number is greater than or equal to the
        specified value.
        """
        super().__init__(err_msg=err_msg)
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=self.value,
            fn=ge,
            err_msg=self.err_msg,
        )


class MustBeLessThan(Validator):
    def __init__(
        self,
        value: Number,
        /,
        *,
        err_msg: str = DEFAULT_NUMERIC_VALIDATOR_ERR_MSG,
    ) -> None:
        """Validates that the number is less than the specified value"""
        super().__init__(err_msg=err_msg)
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=self.value,
            fn=lt,
            err_msg=self.err_msg,
        )


class MustBeLessThanOrEqual(Validator):
    def __init__(
        self,
        value: Number,
        /,
        *,
        err_msg: str = DEFAULT_NUMERIC_VALIDATOR_ERR_MSG,
    ) -> None:
        """Validates that the number is less than or equal to the
        specified value.
        """
        super().__init__(err_msg=err_msg)
        self.value = value

    def __call__(self, arg_value: Number, arg_name: str):
        _generic_number_validator(
            arg_value,
            arg_name,
            to=self.value,
            fn=le,
            err_msg=self.err_msg,
        )
