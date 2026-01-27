from typing import Annotated, Optional

import pytest

from func_validator import (
    validate_params,
    MustBeA,
    ValidationError,
    MustBePositive,
)


class TestDecoratorFn:

    def test_decorator_fn(self):
        @validate_params
        def fn__1(arg__1: int, arg__2: Annotated[int, "Just a Metadata"]):
            return arg__1, arg__2

        assert fn__1(2, 3) == (2, 3)

        @validate_params(check_arg_types=True)
        def fn__2(arg__1: Annotated[Optional[int], MustBePositive()]):
            return arg__1

        assert fn__2(2) == 2

        with pytest.raises(ValidationError):
            fn__2("2")

    def test_decorator_fn_errors(self):
        with pytest.raises(TypeError):
            validate_params("invalid_decorator_arg")
