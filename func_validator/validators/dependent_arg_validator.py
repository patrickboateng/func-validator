from typing import Final, Optional, Type

from ._core import ErrorMsg, T, ValidationError, Validator
from .numeric_arg_validators import MustBeLessThan

__all__ = ["DependsOn", "MustBeProvided"]


def _must_be_provided(
    arg_value: T,
    arg_name: str,
    err_msg: str,
    extra_msg_args: dict,
):
    if not bool(arg_value):
        err_msg = ErrorMsg(err_msg).transform(
            arg_value=arg_value, arg_name=arg_name, **extra_msg_args
        )
        raise ValidationError(err_msg)


class MustBeProvided(Validator):
    DEFAULT_ERROR_MSG: Final[str] = (
        "${arg_name} must be provided when ${dep_arg_name} "
        "has a value of ${dep_arg_value}"
    )

    def __init__(
        self,
        *,
        err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
    ) -> None:
        super().__init__(
            err_msg=err_msg,
            extra_msg_args=extra_msg_args,
            default_err_msg=self.DEFAULT_ERROR_MSG,
        )

    def __call__(self, arg_value: T, arg_name: str):
        _must_be_provided(
            arg_value,
            arg_name,
            err_msg=self.err_msg,
            extra_msg_args=self.extra_msg_args,
        )


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
        kw_strategy: Type[Validator] = MustBeProvided,
        args_err_msg: Optional[str] = None,
        kw_err_msg: Optional[str] = None,
        extra_msg_args: Optional[dict] = None,
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

        super().__init__(extra_msg_args=extra_msg_args)
        self.args_dependencies = args
        self.kw_dependencies = kwargs.items()
        self.args_strategy = args_strategy
        self.kw_strategy = kw_strategy
        self.args_err_msg = args_err_msg or args_strategy.DEFAULT_ERROR_MSG
        self.kw_err_msg = kw_err_msg or kw_strategy.DEFAULT_ERROR_MSG
        self.arguments: dict = {}

    def _get_depenency_value(self, dep_arg_name: str) -> T:
        try:
            actual_value = self.arguments[dep_arg_name]
        except KeyError:
            try:
                instance = self.arguments["self"]
                actual_value = getattr(instance, dep_arg_name)
            except (AttributeError, KeyError):
                msg = f"Dependency argument '{dep_arg_name}' not found."
                raise ValidationError(msg)
        return actual_value

    def _validate_args_dependencies(self, arg_val, arg_name: str):
        for dep_arg_name in self.args_dependencies:
            actual_dep_arg_val = self._get_depenency_value(dep_arg_name)
            self.extra_msg_args.update(
                {
                    "dep_arg_name": dep_arg_name,
                    "dep_arg_value": actual_dep_arg_val,
                }
            )
            strategy = self.args_strategy(
                actual_dep_arg_val,
                err_msg=self.args_err_msg,
                extra_msg_args=self.extra_msg_args,
            )
            strategy(arg_val, arg_name)

    def _validate_kw_dependencies(self, arg_val, arg_name: str):
        for dep_arg_name, dep_arg_val in self.kw_dependencies:
            actual_dep_arg_val = self._get_depenency_value(dep_arg_name)
            if actual_dep_arg_val == dep_arg_val:
                self.extra_msg_args.update(
                    {
                        "dep_arg_name": dep_arg_name,
                        "dep_arg_value": dep_arg_val,
                    }
                )
                strategy = self.kw_strategy(
                    err_msg=self.kw_err_msg,
                    extra_msg_args=self.extra_msg_args,
                )
                strategy(arg_val, arg_name)

    def __call__(self, arg_val, arg_name: str):
        if self.args_dependencies:
            self._validate_args_dependencies(arg_val, arg_name)
        if self.kw_dependencies:
            self._validate_kw_dependencies(arg_val, arg_name)
