import enum

from mkdocs.config.config_options import Optional

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
    MustBeTruthy,
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
    "MustBeTruthy",
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


class DependsOn:
    """Class to indicate that a function argument depends on another
    argument.

    When an argument is marked as depending on another, it implies that
    the presence or value of one argument may influence the validation
    or necessity of the other.
    """

    def __init__(self, strategy=MustBeTruthy, **kwargs):
        self.strategy = strategy
        self.dependencies = kwargs.items()
        self.arguments: Optional[dict] = None

    def __call__(self, arg_val, arg_name: str):
        for dep_arg_name, dep_arg_val in self.dependencies:
            type_checker = MustBeA(dict)
            type_checker(self.arguments, "self.arguments")
            actual_dep_arg_val = self.arguments[dep_arg_name]

            if actual_dep_arg_val == dep_arg_val:
                self.strategy(arg_val, arg_name)
