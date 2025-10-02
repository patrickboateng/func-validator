import enum

from .collection_arg_validators import (
    MustBeEmpty,
    MustBeMemberOf,
    MustBeNonEmpty,
    MustHaveLengthBetween,
    MustHaveLengthEqual,
    MustHaveLengthGreaterThan,
    MustHaveLengthGreaterThanOrEqual,
    MustHaveLengthLessThan,
    MustHaveLengthLessThanOrEqual,
    MustHaveValuesBetween,
    MustHaveValuesGreaterThan,
    MustHaveValuesGreaterThanOrEqual,
    MustHaveValuesLessThan,
    MustHaveValuesLessThanOrEqual,
)
from .datatype_arg_validators import MustBeA
from .numeric_arg_validators import (
    MustBeBetween,
    MustBeEqual,
    MustNotBeEqual,
    MustBeAlmostEqual,
    MustBeGreaterThan,
    MustBeGreaterThanOrEqual,
    MustBeLessThan,
    MustBeLessThanOrEqual,
    MustBeNegative,
    MustBeNonNegative,
    MustBeNonPositive,
    MustBePositive,
)
from .text_arg_validators import MustMatchRegex
from ._core import ValidationError, validator

__all__ = [
    # Error
    "ValidationError",
    # Collection Validators
    "MustBeMemberOf",
    "MustBeEmpty",
    "MustBeNonEmpty",
    "MustHaveLengthEqual",
    "MustHaveLengthGreaterThan",
    "MustHaveLengthGreaterThanOrEqual",
    "MustHaveLengthLessThan",
    "MustHaveLengthLessThanOrEqual",
    "MustHaveLengthBetween",
    "MustHaveValuesGreaterThan",
    "MustHaveValuesGreaterThanOrEqual",
    "MustHaveValuesLessThan",
    "MustHaveValuesLessThanOrEqual",
    "MustHaveValuesBetween",
    # DataType Validators
    "MustBeA",
    # Numeric Validators
    "MustBeBetween",
    "MustBeEqual",
    "MustNotBeEqual",
    "MustBeAlmostEqual",
    "MustBeGreaterThan",
    "MustBeGreaterThanOrEqual",
    "MustBeLessThan",
    "MustBeLessThanOrEqual",
    "MustBeNegative",
    "MustBeNonNegative",
    "MustBeNonPositive",
    "MustBePositive",
    # Text Validators
    "MustMatchRegex",
    # Core
    "DependsOn",
    "validator",
]


class Strategy(enum.StrEnum):
    MUST_NOT_BE_EMPTY = "must_not_be_empty"


class DependsOn:
    """Class to indicate that a function argument depends on another
    argument.

    When an argument is marked as depending on another, it implies that
    the presence or value of one argument may influence the validation
    or necessity of the other.
    """

    def __init__(self, strategy=Strategy.MUST_NOT_BE_EMPTY, **kwargs):
        self.strategy = strategy
        self.dependencies = kwargs.items()

    def __call__(
        self,
        arg_val,
        arg_name: str,
        dependent_arg_val,
        dependent_arg_name: str,
    ):
        if self.strategy == Strategy.MUST_NOT_BE_EMPTY:
            if not arg_val:
                msg = (
                    f"{arg_name} must not be empty when {dependent_arg_name} "
                    f"is {dependent_arg_val}."
                )
                raise ValidationError(msg)
