from typing import Annotated

import pytest

from func_validator import (
    validate_func_args_at_runtime,
    MustBePositive,
    MustBeEmpty,
    MustBeNonEmpty,
    MustBeIn,
    MustHaveLengthEqual,
)


def test_validate_positive():
    @validate_func_args_at_runtime
    def foo(x: Annotated[float, MustBePositive]):
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


def test_validator_not_callable():
    with pytest.raises(TypeError):
        @validate_func_args_at_runtime
        def foo(x: Annotated[int, 123]):  # 123 is not callable
            return x

        foo(1)


def test_decorator_invalid_usage():
    with pytest.raises(TypeError):
        validate_func_args_at_runtime(123)  # Not a function or None


def test_MustBeEmpty():
    MustBeEmpty("")
    MustBeEmpty([])
    MustBeEmpty({})
    with pytest.raises(ValueError):
        MustBeEmpty("not empty")
    with pytest.raises(ValueError):
        MustBeEmpty([1, 2, 3])


def test_MustHaveLength():
    validator = MustHaveLengthEqual(3)
    validator([1, 2, 3])
    validator("abc")
    with pytest.raises(ValueError):
        validator([1, 2])
    with pytest.raises(ValueError):
        validator("")
