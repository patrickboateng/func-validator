import inspect
from functools import wraps
from typing import (
    Annotated,
    Callable,
    ParamSpec,
    TypeAlias,
    TypeVar,
    Optional,
    get_args,
    get_origin,
    get_type_hints,
)

from ._validators import MustBeA

P = ParamSpec("P")
R = TypeVar("R")
DecoratorOrWrapper: TypeAlias = (
        Callable[[Callable[P, R]], Callable[P, R]] | Callable[P, R]
)


def validate_func_args(
        func: Callable[P, R] | None = None,
        /,
        *,
        check_arg_types: bool = False,
) -> DecoratorOrWrapper:
    def dec(fn: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            sig = inspect.signature(fn)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            arguments = bound_args.arguments
            func_type_hints = get_type_hints(fn, include_extras=True)

            for arg_name, arg_annotation in func_type_hints.items():
                if arg_name == "return" or get_origin(
                        arg_annotation) is not Annotated:
                    continue

                arg_type, *arg_validator_funcs = get_args(arg_annotation)
                arg_value = arguments[arg_name]

                if check_arg_types and not isinstance(arg_value, arg_type):
                    raise TypeError(
                        f"Argument '{arg_name}' must be of type "
                        f"{arg_type}, got {type(arg_value)} instead."
                    )

                for arg_validator_fn in arg_validator_funcs:
                    if not callable(arg_validator_fn):
                        raise TypeError(
                            f"Validator for argument '{arg_name}' "
                            f"is not callable: {arg_validator_fn}"
                        )
                    if arg_type is Optional and arg_value is None:
                        continue

                    if isinstance(arg_validator_fn, MustBeA):
                        if arg_validator_fn.infer:
                            arg_validator_fn.arg_type = arg_type
                        arg_validator_fn(arg_value)
                    else:
                        arg_validator_fn(arg_value)

            return fn(*args, **kwargs)

        return wrapper

    # If no function is provided, return the decorator
    if func is None:
        return dec

    # If a function is provided, apply the decorator directly and return the
    # wrapper function
    if callable(func):
        return dec(func)

    raise TypeError("The first argument must be a callable function or None.")


validate_func_args_at_runtime = validate_func_args
