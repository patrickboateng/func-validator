from typing import Type, Optional

from ._core import Validator, ValidationError, T
from .numeric_arg_validators import MustBeLessThan, MustBeTruthy

__all__ = ["DependsOn"]


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
            err_msg: Optional[str] = None,
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
        self.err_msg = err_msg
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
            strategy = self.args_strategy(
                actual_dep_arg_val,
                err_msg=self.err_msg,
            )
            strategy(arg_val, arg_name)

    def _validate_kw_dependencies(self, arg_val, arg_name: str):
        for dep_arg_name, dep_arg_val in self.kw_dependencies:
            actual_dep_arg_val = self._get_depenency_value(dep_arg_name)
            if actual_dep_arg_val == dep_arg_val:
                strategy = self.kw_strategy(err_msg=self.err_msg)
                strategy(arg_val, arg_name)

    def __call__(self, arg_val, arg_name: str):
        if self.args_dependencies:
            self._validate_args_dependencies(arg_val, arg_name)
        if self.kw_dependencies:
            self._validate_kw_dependencies(arg_val, arg_name)
