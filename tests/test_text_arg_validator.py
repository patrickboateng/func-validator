import re
from typing import Annotated

import pytest

from func_validator import MustMatchRegex, ValidationError, validate_params


class TestTextValidator:

    def test_must_match_regex_match(self):
        @validate_params
        def fn(arg__1: Annotated[str, MustMatchRegex(r"\d+")]):
            return arg__1

        assert fn("123") == "123"

        with pytest.raises(ValidationError):
            fn("abc")

    def test_must_match_regex_fullmatch(self):
        @validate_params
        def fn(
            arg__1: Annotated[
                str, MustMatchRegex(r"\d+", match_type="fullmatch")
            ],
        ):
            return arg__1

        assert fn("456") == "456"

        with pytest.raises(ValidationError):
            fn("456abc")

    def test_must_match_regex_search(self):
        @validate_params
        def fn(
            arg__1: Annotated[
                str, MustMatchRegex(r"\d+", match_type="search")
            ],
        ):
            return arg__1

        assert fn("abc789xyz") == "abc789xyz"

    def test_must_match_regex_with_flags(self):
        @validate_params
        def fn(
            arg__1: Annotated[
                str, MustMatchRegex(r"abc", flags=re.IGNORECASE)
            ],
        ):
            return arg__1

        assert fn("ABC") == "ABC"

    def test_must_match_regex_errors(self):
        @validate_params
        def fn__1(arg__1: Annotated[str, MustMatchRegex(r"\d+")]):
            return arg__1

        with pytest.raises(TypeError):
            fn__1(123)

        @validate_params
        def fn__2(arg__1: Annotated[str, MustMatchRegex(r"\d+")]):
            return arg__1

        with pytest.raises(ValidationError):
            fn__2("abc")

        with pytest.raises(ValidationError):
            @validate_params
            def fn__3(
                arg__1: Annotated[
                    str, MustMatchRegex(r"\d+", match_type="invalid")
                ],
            ):
                return arg__1



