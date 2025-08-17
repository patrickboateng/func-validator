import pytest
from func_validator import (
    MustBeIn,
    MustBeBetween,
    MustBeNonEmpty,
    MustHaveValuesBetween,
)


# Membership and range validation tests


def test_must_be_in():
    validator = MustBeIn([1, 2, 3])
    validator(2)
    with pytest.raises(ValueError):
        validator(4)


def test_must_be_between():
    validator = MustBeBetween(min_value=1, max_value=5)
    validator(1)
    validator(3)
    validator(5)
    with pytest.raises(ValueError):
        validator(0)
    with pytest.raises(ValueError):
        validator(6)


def test_must_be_non_empty():
    MustBeNonEmpty("a")
    MustBeNonEmpty([1])
    with pytest.raises(ValueError):
        MustBeNonEmpty("")
    with pytest.raises(ValueError):
        MustBeNonEmpty([])


def test_must_have_values_between():
    fn = MustHaveValuesBetween(min_value=1, max_value=3)
    fn([1, 2, 3])


def test_must_have_length_between():
    fn = MustHaveValuesBetween(min_value=1, max_value=3)
    fn([1, 2, 3])

    with pytest.raises(ValueError):
        fn([0, 4])

    with pytest.raises(ValueError):
        fn([1, 2, 3, 4])
