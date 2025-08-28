from typing import Annotated

import pytest

from func_validator import (
    validate_func_args,
    MustBeMemberOf,
    MustBeEmpty,
    MustBeNonEmpty,
    MustHaveLengthEqual,
    MustHaveLengthGreaterThan,
    MustHaveLengthGreaterThanOrEqual,
    MustHaveLengthLessThan,
    MustHaveLengthLessThanOrEqual,
    MustHaveLengthBetween,
    MustHaveValuesGreaterThan,
    MustHaveValuesGreaterThanOrEqual,
    MustHaveValuesLessThan,
    MustHaveValuesLessThanOrEqual,
    MustHaveValuesBetween,
    ValidationError,
)


# Membership and range validation tests


def test_must_be_a_member_of_validator():
    @validate_func_args
    def func(x_1: Annotated[int, MustBeMemberOf([1, 2, 3])]):
        return x_1

    assert func(1) == 1
    assert func(2) == 2
    assert func(3) == 3

    with pytest.raises(ValidationError):
        func(4)

    with pytest.raises(ValidationError):
        func(0)


def test_must_be_empty_validator():
    @validate_func_args
    def func(x_1: Annotated[list, MustBeEmpty]):
        return x_1

    assert func([]) == []

    with pytest.raises(ValidationError):
        func([1, 2])


def test_must_be_non_empty_validator():
    @validate_func_args
    def func(x_1: Annotated[list, MustBeNonEmpty]):
        return x_1

    assert func([1, 2]) == [1, 2]

    with pytest.raises(ValidationError):
        func([])


def test_must_have_length_equal():
    @validate_func_args
    def func(x_1: Annotated[list, MustHaveLengthEqual(3)]):
        return x_1

    assert func([1, 2, 3]) == [1, 2, 3]

    with pytest.raises(ValidationError):
        func([1, 2, 3, 4])


def test_must_have_length_greater_than_validator():
    @validate_func_args
    def func(x_1: Annotated[list, MustHaveLengthGreaterThan(2)]):
        return x_1

    assert func([1, 2, 3]) == [1, 2, 3]

    with pytest.raises(ValidationError):
        func([1, 2])


def test_must_have_length_greater_than_or_equal_validator():
    @validate_func_args
    def func(x_1: Annotated[list, MustHaveLengthGreaterThanOrEqual(3)]):
        return x_1

    assert func([1, 2, 3]) == [1, 2, 3]

    with pytest.raises(ValidationError):
        func([1, 2])


def test_must_have_length_less_than_validator():
    @validate_func_args
    def func(x_1: Annotated[list, MustHaveLengthLessThan(3)]):
        return x_1

    assert func([1, 2]) == [1, 2]

    with pytest.raises(ValidationError):
        func([1, 2, 3])


def test_must_have_length_less_than_or_equal_validator():
    @validate_func_args
    def func(x_1: Annotated[list, MustHaveLengthLessThanOrEqual(4)]):
        return x_1

    assert func([1, 2]) == [1, 2]
    assert func([1, 2, 3, 4]) == [1, 2, 3, 4]

    with pytest.raises(ValidationError):
        func([1, 2, 3, 4, 5])


def test_must_have_length_between_validator():
    @validate_func_args
    def func(x_1: Annotated[list, MustHaveLengthBetween(min_value=2, max_value=4)]):
        return x_1

    assert func([1, 2]) == [1, 2]
    assert func([1, 2, 3]) == [1, 2, 3]
    assert func([1, 2, 3, 4]) == [1, 2, 3, 4]

    with pytest.raises(ValidationError):
        func([1])

    with pytest.raises(ValidationError):
        func([1, 2, 3, 4, 5])

    @validate_func_args
    def func_2(
        x_1: Annotated[
            list, MustHaveLengthBetween(min_value=2, max_value=4, min_inclusive=False)
        ],
    ):
        return x_1

    assert func_2([1, 2, 3]) == [1, 2, 3]
    assert func_2([1, 2, 3, 4]) == [1, 2, 3, 4]

    with pytest.raises(ValidationError):
        func_2([1, 2])

    @validate_func_args
    def func_3(
        x_1: Annotated[
            list, MustHaveLengthBetween(min_value=2, max_value=4, max_inclusive=False)
        ],
    ):
        return x_1

    assert func_3([1, 2]) == [1, 2]
    assert func_3([1, 2, 3]) == [1, 2, 3]

    with pytest.raises(ValidationError):
        func_3([1, 2, 3, 4])

    @validate_func_args
    def func_4(
        x_1: Annotated[
            list,
            MustHaveLengthBetween(
                min_value=2, max_value=4, min_inclusive=False, max_inclusive=False
            ),
        ],
    ):
        return x_1

    assert func_4([1, 2, 3]) == [1, 2, 3]

    with pytest.raises(ValidationError):
        func_4([1, 2])

    with pytest.raises(ValidationError):
        func_4([1, 2, 3, 4])


def test_must_have_values_greater_than_validator():
    @validate_func_args
    def func(x_1: Annotated[list, MustHaveValuesGreaterThan(3)]):
        return x_1

    assert func([4, 5, 6]) == [4, 5, 6]

    with pytest.raises(ValidationError):
        func([1, 2, 3])


def test_must_have_values_greater_than_or_equal_validator():
    @validate_func_args
    def func(x_1: Annotated[list, MustHaveValuesGreaterThanOrEqual(3)]):
        return x_1

    assert func([3, 4, 5]) == [3, 4, 5]

    with pytest.raises(ValidationError):
        func([1, 2])


def test_must_have_values_less_than_validator():
    @validate_func_args
    def func(x_1: Annotated[list, MustHaveValuesLessThan(5)]):
        return x_1

    assert func([2, 3, 4]) == [2, 3, 4]

    with pytest.raises(ValidationError):
        func([5, 6, 7])


def test_must_have_values_less_than_or_equal_validator():
    @validate_func_args
    def func(x_1: Annotated[list, MustHaveValuesLessThanOrEqual(5)]):
        return x_1

    assert func([2, 3, 4, 5]) == [2, 3, 4, 5]

    with pytest.raises(ValidationError):
        func([6, 7, 8])


def test_must_have_values_between_validator():
    @validate_func_args
    def func(x_1: Annotated[list, MustHaveValuesBetween(min_value=2, max_value=5)]):
        return x_1

    assert func([2, 3, 4, 5]) == [2, 3, 4, 5]

    with pytest.raises(ValidationError):
        func([0, 1])

    @validate_func_args
    def func_2(
        x_1: Annotated[
            list, MustHaveValuesBetween(min_value=2, max_value=5, min_inclusive=False)
        ],
    ):
        return x_1

    assert func_2([3, 4, 5]) == [3, 4, 5]

    with pytest.raises(ValidationError):
        func_2([2, 3])

    @validate_func_args
    def func_3(
        x_1: Annotated[
            list, MustHaveValuesBetween(min_value=2, max_value=5, max_inclusive=False)
        ],
    ):
        return x_1

    assert func_3([2, 3, 4]) == [2, 3, 4]

    with pytest.raises(ValidationError):
        func_3([2, 3, 4, 5])

    @validate_func_args
    def func_4(
        x_1: Annotated[
            list,
            MustHaveValuesBetween(
                min_value=2, max_value=5, min_inclusive=False, max_inclusive=False
            ),
        ],
    ):
        return x_1

    assert func_4([3, 4]) == [3, 4]

    with pytest.raises(ValidationError):
        func_4([2, 3])

    with pytest.raises(ValidationError):
        func_4([4, 5])
