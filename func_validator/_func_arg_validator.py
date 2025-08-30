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
    Union,
)

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
                if arg_name == "return" or get_origin(arg_annotation) is not Annotated:
                    continue

                arg_type, *arg_validator_funcs = get_args(arg_annotation)
                arg_value = arguments[arg_name]

                is_arg_type_optional = get_origin(arg_type) is Union and get_args(
                    arg_type
                )[1] is type(None)

                # If arg_type is Optional, None is allowed as a valid arg_value
                if is_arg_type_optional and arg_value is None:
                    continue  # we are skipping the validation of the arg_value

                if check_arg_types and not isinstance(arg_value, arg_type):
                    raise TypeError(
                        f"Argument '{arg_name}' must be of type "
                        f"{arg_type}, got {type(arg_value)} instead."
                    )

                for arg_validator_fn in arg_validator_funcs:
                    if callable(arg_validator_fn):
                        arg_validator_fn(arg_value, arg_name)

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
