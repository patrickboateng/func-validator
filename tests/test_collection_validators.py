from typing import Annotated

import pytest

from func_validator import (
    MustBeEmpty,
    MustBeMemberOf,
    MustBeNonEmpty,
    MustHaveLengthBetween,
    MustHaveLengthEqual,
    MustHaveLengthGreaterThan,
    MustHaveLengthGreaterThanOrEqual,
    MustHaveLengthLessThan,
    MustHaveLengthLessThanOrEqual,
    MustHaveValuesBetween,
    MustHaveValuesGreaterThan,
    MustHaveValuesGreaterThanOrEqual,
    MustHaveValuesLessThan,
    MustHaveValuesLessThanOrEqual,
    ValidationError,
    validate_params,
)

# Membership and range validation tests


class TestCollectionValidator:

    def test_must_be_a_member_of_validator(self):
        @validate_params
        def fn(arg__1: Annotated[int, MustBeMemberOf([1, 2, 3])]):
            return arg__1

        assert fn(1) == 1
        assert fn(2) == 2
        assert fn(3) == 3

        with pytest.raises(ValidationError):
            fn(4)
            fn(0)

    def test_must_be_empty_validator(self):
        @validate_params
        def fn(arg__1: Annotated[list, MustBeEmpty()]):
            return arg__1

        assert fn([]) == []

        with pytest.raises(ValidationError):
            fn([1, 2])

    def test_must_be_non_empty_validator(self):
        @validate_params
        def fn(arg__1: Annotated[list, MustBeNonEmpty()]):
            return arg__1

        assert fn([1, 2]) == [1, 2]

        with pytest.raises(ValidationError):
            fn([])

    def test_must_have_length_equal_validator(self):
        @validate_params
        def fn(arg__1: Annotated[list, MustHaveLengthEqual(3)]):
            return arg__1

        assert fn([1, 2, 3]) == [1, 2, 3]

        with pytest.raises(ValidationError):
            fn([1, 2, 3, 4])

    def test_must_have_length_greater_than_validator(self):
        @validate_params
        def fn(arg__1: Annotated[list, MustHaveLengthGreaterThan(2)]):
            return arg__1

        assert fn([1, 2, 3]) == [1, 2, 3]

        with pytest.raises(ValidationError):
            fn([1, 2])

    def test_must_have_length_greater_than_or_equal_validator(self):
        @validate_params
        def fn(arg__1: Annotated[list, MustHaveLengthGreaterThanOrEqual(3)]):
            return arg__1

        assert fn([1, 2, 3]) == [1, 2, 3]

        with pytest.raises(ValidationError):
            fn([1, 2])

    def test_must_have_length_less_than_validator(self):
        @validate_params
        def fn(arg__1: Annotated[list, MustHaveLengthLessThan(3)]):
            return arg__1

        assert fn([1, 2]) == [1, 2]

        with pytest.raises(ValidationError):
            fn([1, 2, 3])

    def test_must_have_length_less_than_or_equal_validator(self):
        @validate_params
        def fn(arg__1: Annotated[list, MustHaveLengthLessThanOrEqual(4)]):
            return arg__1

        assert fn([1, 2]) == [1, 2]
        assert fn([1, 2, 3, 4]) == [1, 2, 3, 4]

        with pytest.raises(ValidationError):
            fn([1, 2, 3, 4, 5])

    def test_must_have_length_between_validator(self):
        @validate_params
        def fn__1(
            arg__1: Annotated[
                list, MustHaveLengthBetween(min_value=2, max_value=4)
            ],
        ):
            return arg__1

        assert fn__1([1, 2]) == [1, 2]
        assert fn__1([1, 2, 3]) == [1, 2, 3]
        assert fn__1([1, 2, 3, 4]) == [1, 2, 3, 4]

        with pytest.raises(ValidationError):
            fn__1([1])
            fn__1([1, 2, 3, 4, 5])

        @validate_params
        def fn__2(
            arg__1: Annotated[
                list,
                MustHaveLengthBetween(
                    min_value=2,
                    max_value=4,
                    min_inclusive=False,
                    max_inclusive=False,
                ),
            ],
        ):
            return arg__1

        assert fn__2([1, 2, 3]) == [1, 2, 3]

        with pytest.raises(ValidationError):
            fn__2([1, 2])
            fn__2([1, 2, 3, 4])

    def test_must_have_values_greater_than_validator(self):
        @validate_params
        def fn(arg__1: Annotated[list, MustHaveValuesGreaterThan(3)]):
            return arg__1

        assert fn([4, 5, 6]) == [4, 5, 6]

        with pytest.raises(ValidationError):
            fn([1, 2, 3])

    def test_must_have_values_greater_than_or_equal_validator(self):
        @validate_params
        def fn(arg__1: Annotated[list, MustHaveValuesGreaterThanOrEqual(3)]):
            return arg__1

        assert fn([3, 4, 5]) == [3, 4, 5]

        with pytest.raises(ValidationError):
            fn([1, 2])

    def test_must_have_values_less_than_validator(self):
        @validate_params
        def fn(arg__1: Annotated[list, MustHaveValuesLessThan(5)]):
            return arg__1

        assert fn([2, 3, 4]) == [2, 3, 4]

        with pytest.raises(ValidationError):
            fn([5, 6, 7])

    def test_must_have_values_less_than_or_equal_validator(self):
        @validate_params
        def fn(arg__1: Annotated[list, MustHaveValuesLessThanOrEqual(5)]):
            return arg__1

        assert fn([2, 3, 4, 5]) == [2, 3, 4, 5]

        with pytest.raises(ValidationError):
            fn([6, 7, 8])

    def test_must_have_values_between_validator(self):
        @validate_params
        def fn__1(
            arg__1: Annotated[
                list, MustHaveValuesBetween(min_value=2, max_value=5)
            ],
        ):
            return arg__1

        assert fn__1([2, 3, 4, 5]) == [2, 3, 4, 5]

        with pytest.raises(ValidationError):
            fn__1([0, 1])

        @validate_params
        def fn__2(
            x_1: Annotated[
                list,
                MustHaveValuesBetween(
                    min_value=2,
                    max_value=5,
                    min_inclusive=False,
                    max_inclusive=False,
                ),
            ],
        ):
            return x_1

        assert fn__2([3, 4]) == [3, 4]

        with pytest.raises(ValidationError):
            fn__2([2, 3])
            fn__2([4, 5])
