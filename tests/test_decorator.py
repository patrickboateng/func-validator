import pytest
from typing import Annotated
from func_validator import (
    validate_func_args_at_runtime,
    MustBePositive,
    MustBeNonEmpty,
    MustBeIn,
)


def test_validate_positive():
    @validate_func_args_at_runtime
    def foo(x: Annotated[int, MustBePositive]):
        return x * 2

    assert foo(5) == 10
    with pytest.raises(ValueError):
        foo(-1)


def test_validate_nonempty():
    @validate_func_args_at_runtime
    def bar(s: Annotated[str, MustBeNonEmpty]):
        return s.upper()

    assert bar("abc") == "ABC"
    with pytest.raises(ValueError):
        bar("")


def test_validate_in():
    @validate_func_args_at_runtime
    def baz(x: Annotated[int, MustBeIn([1, 2, 3])]):
        return x

    assert baz(2) == 2
    with pytest.raises(ValueError):
        baz(5)


def test_validate_min_length():
    @validate_func_args_at_runtime(min_length=2)
    def qux(s: Annotated[str, MustBeNonEmpty]):
        return s

    assert qux("ab") == "ab"
    with pytest.raises(ValueError):
        qux("a")


def test_validate_max_length():
    @validate_func_args_at_runtime(max_length=3)
    def quux(s: Annotated[str, MustBeNonEmpty]):
        return s

    assert quux("abc") == "abc"
    with pytest.raises(ValueError):
        quux("abcd")


def test_validator_not_callable():
    with pytest.raises(TypeError):

        @validate_func_args_at_runtime
        def foo(x: Annotated[int, 123]):  # 123 is not callable
            return x

        foo(1)


def test_decorator_invalid_usage():
    with pytest.raises(TypeError):
        validate_func_args_at_runtime(123)  # Not a function or None


def test_check_iterable_values():
    class MustBeEven:
        def __call__(self, x):
            if x % 2 != 0:
                raise ValueError("Not even")

    @validate_func_args_at_runtime(check_iterable_values=True)
    def foo(xs: Annotated[list[int], MustBeEven()]):
        return sum(xs)

    assert foo([2, 4]) == 6
    with pytest.raises(ValueError):
        foo([2, 3])


def test_length_check_on_non_iterable():
    @validate_func_args_at_runtime(min_length=2)
    def foo(x: Annotated[int, lambda x: None]):
        return x

    with pytest.raises(TypeError):
        foo(1)
