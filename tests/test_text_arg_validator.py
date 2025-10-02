import re
from typing import Annotated

import pytest

from func_validator import validate_params, MustMatchRegex, ValidationError


def test_must_match_regex_match():
    @validate_params
    def func(x: Annotated[str, MustMatchRegex(r"\d+")]):
        return x

    assert func("123") == "123"

    with pytest.raises(ValidationError):
        func("abc")


def test_must_match_regex_fullmatch():
    @validate_params
    def func(
        x: Annotated[str, MustMatchRegex(r"\d+", match_type="fullmatch")],
    ):
        return x

    assert func("456") == "456"

    with pytest.raises(ValidationError):
        func("456abc")


def test_must_match_regex_search():
    @validate_params
    def func(x: Annotated[str, MustMatchRegex(r"\d+", match_type="search")]):
        return x

    assert func("abc789xyz") == "abc789xyz"


def test_must_match_regex_with_flags():
    @validate_params
    def func(x: Annotated[str, MustMatchRegex(r"abc", flags=re.IGNORECASE)]):
        return x

    assert func("ABC") == "ABC"


def test_must_match_regex_type_error_non_string():
    @validate_params
    def func(x: Annotated[str, MustMatchRegex(r"\d+")]):
        return x

    with pytest.raises(TypeError):
        func(123)  # Passing an int should raise TypeError


def test_must_match_regex_error_message_contains_pattern():
    pattern = r"\d+"

    @validate_params
    def func(x: Annotated[str, MustMatchRegex(pattern)]):
        return x

    with pytest.raises(ValidationError):
        func("abc")


def test_must_match_regex_precompiled_pattern():
    compiled_pattern = re.compile(r"\d{3}")

    @validate_params
    def func(x: Annotated[str, MustMatchRegex(compiled_pattern)]):
        return x

    # Matching input should pass
    assert func("123") == "123"

    # Non-matching input should raise ValidationError
    with pytest.raises(ValidationError):
        func("12")


def test_must_match_regex_invalid_match_type():
    with pytest.raises(ValidationError):

        @validate_params
        def func(
            x: Annotated[
                str,
                MustMatchRegex(
                    r"abc", flags=re.IGNORECASE, match_type="invalid"
                ),
            ],
        ): ...
