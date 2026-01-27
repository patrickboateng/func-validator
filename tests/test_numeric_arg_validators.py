from typing import Annotated

import pytest

from func_validator import (
    MustBeAlmostEqual,
    MustBeBetween,
    MustBeEqual,
    MustBeGreaterThan,
    MustBeGreaterThanOrEqual,
    MustBeLessThan,
    MustBeLessThanOrEqual,
    MustBeNegative,
    MustBeNonNegative,
    MustBeNonPositive,
    MustBePositive,
    MustNotBeEqual,
    ValidationError,
    validate_params,
)


class TestNumericValidator:

    def test_must_be_positive_validator(self):
        @validate_params
        def fn(arg__1: Annotated[int, MustBePositive()]) -> int:
            return arg__1

        assert fn(10) == 10

        with pytest.raises(ValidationError):
            fn(0)
            fn(-10)


    def test_must_be_non_positive_validator(self):
        @validate_params
        def fn(arg__1: Annotated[int, MustBeNonPositive()]):
            return arg__1

        assert fn(-2) == -2
        assert fn(0) == 0

        with pytest.raises(ValidationError):
            fn(10)

    def test_must_be_negative_validator(self):
        @validate_params
        def fn(arg__1: Annotated[int, MustBeNegative()]):
            return arg__1

        assert fn(-10) == -10

        with pytest.raises(ValidationError):
            fn(10)

    def test_must_be_non_negative_validator(self):
        @validate_params
        def fn(arg__1: Annotated[int, MustBeNonNegative()]):
            return arg__1

        assert fn(10) == 10
        assert fn(0) == 0

        with pytest.raises(ValidationError):
            fn(-10)

    def test_must_be_between_validator__1(self):
        @validate_params
        def fn(
            arg__1: Annotated[int, MustBeBetween(min_value=2, max_value=4)],
        ):
            return arg__1

        assert fn(2) == 2
        assert fn(3) == 3
        assert fn(4) == 4

        with pytest.raises(ValidationError):
            fn(1)
            fn(5)


    def test_must_be_between_validator__2(self):
        @validate_params
        def fn(
            arg__1: Annotated[
                int,
                MustBeBetween(
                    min_value=2,
                    max_value=4,
                    min_inclusive=False,
                    max_inclusive=False,
                ),
            ],
        ):
            return arg__1

        assert fn(3) == 3

        with pytest.raises(ValidationError):
            fn(2)
            fn(4)

    def test_must_be_equal_validator(self):
        @validate_params
        def fn(arg__1: Annotated[int, MustBeEqual(10)]):
            return arg__1

        assert fn(10) == 10

        with pytest.raises(ValidationError):
            fn(9)

    def test_must_be_not_equal_validator(self):
        @validate_params
        def fn(x_1: Annotated[int, MustNotBeEqual(10)]):
            return x_1

        assert fn(4) == 4

        with pytest.raises(ValidationError):
            fn(10)

    def test_must_be_greater_than_validator(self):
        @validate_params
        def fn(arg__1: Annotated[int, MustBeGreaterThan(5)]):
            return arg__1

        assert fn(6) == 6

        with pytest.raises(ValidationError):
            fn(4)
            fn(5)

    def test_must_be_greater_than_or_equal_validator(self):
        @validate_params
        def fn(arg__1: Annotated[int, MustBeGreaterThanOrEqual(5)]):
            return arg__1

        assert fn(6) == 6
        assert fn(5) == 5

        with pytest.raises(ValidationError):
            fn(4)

    def test_must_be_less_than_validator(self):
        @validate_params
        def fn(arg__1: Annotated[int, MustBeLessThan(5)]):
            return arg__1

        assert fn(4) == 4

        with pytest.raises(ValidationError):
            fn(6)
            fn(5)

    def test_must_be_less_than_or_equal_validator(self):
        @validate_params
        def fn(arg__1: Annotated[int, MustBeLessThanOrEqual(5)]):
            return arg__1

        assert fn(4) == 4
        assert fn(5) == 5

        with pytest.raises(ValidationError):
            fn(6)

    def test_must_be_almost_equal(self):
        @validate_params
        def fn(
            arg__1: Annotated[float, MustBeAlmostEqual(5.39, rel_tol=0.01)],
        ):
            return arg__1

        assert fn(5.4) == pytest.approx(5.4)

        with pytest.raises(ValidationError):
            fn(6)
