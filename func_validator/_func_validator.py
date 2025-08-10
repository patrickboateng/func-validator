import inspect
from functools import wraps
from typing import (Callable, ParamSpec, List, Tuple, Set,
                    TypeVar, get_type_hints, get_args)

P = ParamSpec('P')
R = TypeVar('R')


def validate(func=None, /):
    def dec(fn: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            sig = inspect.signature(fn)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            arguments = bound_args.arguments
            func_type_hints = get_type_hints(func, include_extras=True)

            for arg_name, arg_annotation in func_type_hints.items():
                if arg_name == 'return':
                    continue

                _, *arg_validators_fn = get_args(arg_annotation)
                arg_value = arguments[arg_name]

                for arg_validator_fn in arg_validators_fn:
                    if not callable(arg_validator_fn):
                        raise TypeError(
                            f"Validator for argument '{arg_name}' is not callable: {arg_validator_fn}"
                        )

                    if isinstance(arg_value, List | Tuple | Set):
                        for v in arg_value:
                            arg_validator_fn(v)
                    else:
                        arg_validator_fn(arg_value)

            return fn(*args, **kwargs)

        return wrapper

    # If no function is provided, return the decorator
    if func is None:
        return dec

    # If a function is provided, apply the decorator directly
    if callable(func):
        return dec(func)

    raise TypeError("The first argument must be a callable function or None.")
