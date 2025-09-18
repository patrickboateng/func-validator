from typing import Annotated
import pytest
from func_validator import (
    validate_func_args,
    MustBePositive,
    MustBeNonPositive,
    MustBeNonNegative,
    MustBeNegative,
    MustBeBetween,
    MustBeEqual,
    MustBeNotEqual,
    MustBeGreaterThan,
    MustBeLessThan,
    MustBeGreaterThanOrEqual,
    MustBeAlmostEqual,
    MustBeLessThanOrEqual,
    ValidationError,
)


# Numeric validation tests


def test_must_be_positive_validator():
    @validate_func_args
    def func(x_1: Annotated[int, MustBePositive]):
        return x_1

    assert func(1) == 1

    with pytest.raises(ValidationError):
        func(0)

    with pytest.raises(ValidationError):
        func(-10)


def test_must_be_non_positive_validator():
    @validate_func_args
    def func(x_1: Annotated[int, MustBeNonPositive]):
        return x_1

    assert func(-2) == -2
    assert func(0) == 0

    with pytest.raises(ValidationError):
        func(4)


def test_must_be_negative_validator():
    @validate_func_args
    def func(x_1: Annotated[int, MustBeNegative]):
        return x_1

    assert func(-10) == -10

    with pytest.raises(ValidationError):
        func(5.0)


def test_must_be_non_negative_validator():
    @validate_func_args
    def func(x_1: Annotated[int, MustBeNonNegative]):
        return x_1

    assert func(10) == 10
    assert func(0) == 0

    with pytest.raises(ValidationError):
        func(-10)


def test_must_be_between_validator():
    @validate_func_args
    def func(x_1: Annotated[int, MustBeBetween(min_value=2, max_value=4)]):
        return x_1

    assert func(2) == 2
    assert func(3) == 3
    assert func(4) == 4

    with pytest.raises(ValidationError):
        func(1)

    with pytest.raises(ValidationError):
        func(5)

    @validate_func_args
    def func_2(
        x_1: Annotated[
            int, MustBeBetween(min_value=2, max_value=4, min_inclusive=False)
        ],
    ):
        return x_1

    assert func_2(3) == 3
    assert func_2(4) == 4

    with pytest.raises(ValidationError):
        func_2(2)

    @validate_func_args
    def func_3(
        x_1: Annotated[
            int, MustBeBetween(min_value=2, max_value=4, max_inclusive=False)
        ],
    ):
        return x_1

    assert func_3(2) == 2
    assert func_3(3) == 3

    with pytest.raises(ValidationError):
        func_3(4)

    @validate_func_args
    def func_4(
        x_1: Annotated[
            int,
            MustBeBetween(
                min_value=2,
                max_value=4,
                min_inclusive=False,
                max_inclusive=False,
            ),
        ],
    ):
        return x_1

    assert func_4(3) == 3

    with pytest.raises(ValidationError):
        func_4(2)

    with pytest.raises(ValidationError):
        func_4(4)


# Comparison validation tests
def test_must_be_equal_validator():
    @validate_func_args
    def func(x_1: Annotated[int, MustBeEqual(5)]):
        return x_1

    assert func(5) == 5

    with pytest.raises(ValidationError):
        func(4)


def test_must_be_not_equal_validator():
    @validate_func_args
    def func(x_1: Annotated[int, MustBeNotEqual(5)]):
        return x_1

    assert func(4) == 4

    with pytest.raises(ValidationError):
        func(5)


def test_must_be_greater_than_validator():
    @validate_func_args
    def func(x_1: Annotated[int, MustBeGreaterThan(5)]):
        return x_1

    assert func(6) == 6

    with pytest.raises(ValidationError):
        func(4)

    with pytest.raises(ValidationError):
        func(5)


def test_must_be_greater_than_or_equal_validator():
    @validate_func_args
    def func(x_1: Annotated[int, MustBeGreaterThanOrEqual(5)]):
        return x_1

    assert func(6) == 6
    assert func(5) == 5

    with pytest.raises(ValidationError):
        func(4)


def test_must_be_less_than_validator():
    @validate_func_args
    def func(x_1: Annotated[int, MustBeLessThan(5)]):
        return x_1

    assert func(4) == 4

    with pytest.raises(ValidationError):
        func(6)

    with pytest.raises(ValidationError):
        func(5)


def test_must_be_less_than_or_equal_validator():
    @validate_func_args
    def func(x_1: Annotated[int, MustBeLessThanOrEqual(5)]):
        return x_1

    assert func(4) == 4
    assert func(5) == 5

    with pytest.raises(ValidationError):
        func(6)


def test_must_be_almost_equal():
    @validate_func_args
    def func(x_1: Annotated[float, MustBeAlmostEqual(5.39, rel_tol=0.01)]):
        return x_1

    assert func(5.4) == pytest.approx(5.4)

    with pytest.raises(ValidationError):
        func(6)
