import inspect
from functools import wraps
from typing import (
    Annotated,
    Callable,
    ParamSpec,
    TypeAlias,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
)

P = ParamSpec("P")
R = TypeVar("R")
DecoratorOrCallable: TypeAlias = (
        Callable[[Callable[P, R]], Callable[P, R]] | Callable[P, R]
)


def validate_func_args(func: Callable[P, R] | None = None,
                       /) -> DecoratorOrCallable:
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

                _, *arg_validator_funcs = get_args(arg_annotation)
                arg_value = arguments[arg_name]

                for arg_validator_fn in arg_validator_funcs:
                    if not callable(arg_validator_fn):
                        raise TypeError(
                            f"Validator for argument '{arg_name}' "
                            f"is not callable: {arg_validator_fn}"
                        )

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
