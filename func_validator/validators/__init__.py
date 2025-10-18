from typing import Optional, TypeVar, Type

from ._core import ValidationError, Validator
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
    MustBeAlmostEqual,
    MustBeBetween,
    MustBeEqual,
    MustBeGreaterThan,
    MustBeGreaterThanOrEqual,
    MustBeLessThan,
    MustBeLessThanOrEqual,
    MustBeNegative,
    MustBeNonNegative,
    MustBeNonPositive,
    MustBePositive,
    MustBeTruthy,
    MustNotBeEqual,
)
from .text_arg_validators import MustMatchRegex

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
    "Validator",
]

T = TypeVar("T")


class DependsOn(Validator):
    """Class to indicate that a function argument depends on another
    argument.

    When an argument is marked as depending on another, it implies that
    the presence or value of one argument may influence the validation
    or necessity of the other.
    """

    def __init__(
            self,
            *args: str,
            args_strategy: Type[Validator] = MustBeLessThan,
            kw_strategy: Type[Validator] = MustBeTruthy,
            **kwargs: T,
    ):
        """
        :param args: The names of the arguments that the current argument
                     depends on.
        :param args_strategy: The validation strategy to apply based on
                              the values of the dependent arguments.
        :param kw_strategy: The validation strategy to apply when
                            dependent arguments match specific values.
        :param kwargs: Key-value pairs where the key is the name of the
                       dependent argument and the value is the specific
                       value to match for applying the strategy.
        """
        self.args_dependencies = args
        self.kw_dependencies = kwargs.items()
        self.args_strategy = args_strategy
        self.kw_strategy = kw_strategy
        self.arguments: dict = {}

    def _get_depenency_value(self, dep_arg_name: str) -> T:
        try:
            actual_value = self.arguments[dep_arg_name]
        except KeyError:
            try:
                __obj = self.arguments["self"]
                actual_value = getattr(__obj, dep_arg_name)
            except (AttributeError, KeyError):
                msg = f"Dependency argument '{dep_arg_name}' not found."
                raise ValidationError(msg)
        return actual_value

    def _validate_args_dependencies(self, arg_val, arg_name: str):
        for dep_arg_name in self.args_dependencies:
            actual_dep_arg_val = self._get_depenency_value(dep_arg_name)
            strategy = self.args_strategy(actual_dep_arg_val)
            strategy(arg_val, arg_name)

    def _validate_kw_dependencies(self, arg_val, arg_name: str):
        for dep_arg_name, dep_arg_val in self.kw_dependencies:
            actual_dep_arg_val = self._get_depenency_value(dep_arg_name)
            if actual_dep_arg_val == dep_arg_val:
                strategy = self.kw_strategy()
                strategy(arg_val, arg_name)

    def __call__(self, arg_val, arg_name: str):
        if self.args_dependencies:
            self._validate_args_dependencies(arg_val, arg_name)
        if self.kw_dependencies:
            self._validate_kw_dependencies(arg_val, arg_name)
