import inspect
from functools import wraps
from math import nan
from typing import (
    Annotated,
    Callable,
    ParamSpec,
    TypeAlias,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
    Union,
)

from .validators import DependsOn, MustBeA

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")
DecoratorOrWrapper: TypeAlias = (
        Callable[[Callable[P, R]], Callable[P, R]] | Callable[P, R]
)

ALLOWED_OPTIONAL_VALUES = (None, nan)


def _is_arg_type_optional(arg_type: T) -> bool:
    is_optional = False
    if get_origin(arg_type) is Union:
        is_optional = get_args(arg_type)[1] is type(None)
    return is_optional


def _skip_validation(
        arg_name: str,
        arg_val: T,
        arg_annotation: T,
) -> bool:
    if arg_name == "return":
        return True
    if get_origin(arg_annotation) is not Annotated:
        return True
    arg_type, *_ = get_args(arg_annotation)
    if _is_arg_type_optional(arg_type) and arg_val in ALLOWED_OPTIONAL_VALUES:
        return True
    return False


def validate_params(
        func: Callable[P, R] | None = None,
        /,
        *,
        check_arg_types: bool = False,
) -> DecoratorOrWrapper:
    """Decorator to validate function arguments at runtime based on their
    type annotations using `typing.Annotated` and custom validators. This
    ensures that each argument passes any attached validators and
    optionally checks type correctness if `check_arg_types` is True.

    :param func: The function to be decorated. If None, the decorator is
                 returned for later application. Default is None.

    :param check_arg_types: If True, checks that all argument types match.
                            Default is False.

    :raises TypeError: If `func` is not callable or None, or if a validator
                       is not callable.

    :return: The decorated function with argument validation, or the
             decorator itself if `func` is None.
    """

    def dec(fn: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            sig = inspect.signature(fn)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            arguments = bound_args.arguments
            func_type_hints = get_type_hints(fn, include_extras=True)

            for arg_name, arg_annotation in func_type_hints.items():
                arg_value = arguments[arg_name]
                if _skip_validation(arg_name, arg_value, arg_annotation):
                    continue

                arg_type, *arg_validator_funcs = get_args(arg_annotation)

                if check_arg_types:
                    type_checker = MustBeA(arg_type)
                    type_checker(arg_value, arg_name)

                for arg_validator_fn in arg_validator_funcs:
                    if isinstance(arg_validator_fn, DependsOn):
                        arg_validator_fn.arguments = arguments
                    if callable(arg_validator_fn):
                        arg_validator_fn(arg_value, arg_name)

            return fn(*args, **kwargs)

        return wrapper

    # If no function is provided, return the decorator
    if func is None:
        return dec

    # If a function is provided, apply the decorator directly and return
    # the wrapper function
    if callable(func):
        return dec(func)

    raise TypeError("The first argument must be a callable function or None.")


validate_func_args_at_runtime = validate_params
validate_func_args = validate_params
