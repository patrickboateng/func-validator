import inspect
from functools import wraps
from typing import Callable, ParamSpec, TypeVar, get_type_hints, get_args, \
    Annotated

P = ParamSpec('P')
R = TypeVar('R')


def validate(func=None, /,
             min_length: int | None = None,
             max_length: int | None = None,
             check_iterable_values=False):
    def dec(fn: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            sig = inspect.signature(fn)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            arguments = bound_args.arguments
            func_type_hints = get_type_hints(fn, include_extras=True)

            for arg_name, arg_annotation in func_type_hints.items():
                arg_metadata = get_args(arg_annotation)

                if arg_name == 'return' or len(arg_metadata) < 2:
                    continue

                _, *arg_validator_funcs = arg_metadata
                arg_value = arguments[arg_name]

                for arg_validator_fn in arg_validator_funcs:
                    if not callable(arg_validator_fn):
                        raise TypeError(f"Validator for argument '{arg_name}' "
                                        f"is not callable: {arg_validator_fn}")

                    if min_length is not None:
                        exc_msg = (f"Length of argument '{arg_name}' "
                                   f"must be at least {min_length}.")
                        if len(arg_value) < min_length:
                            raise ValueError(exc_msg)

                    if max_length is not None:
                        exc_msg = (f"Length of argument '{arg_name}' "
                                   f"must be at most {max_length}.")
                        if len(arg_value) > max_length:
                            raise ValueError(exc_msg)

                    if check_iterable_values:
                        for v in arg_value:
                            arg_validator_fn(v)
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


if __name__ == "__main__":
    # Example usage of the validate decorator
    @validate
    def example_function(
            arg1: list[int],
            # arg2: Annotated[str, lambda x: x]
    ):
        pass


    example_function("test")
