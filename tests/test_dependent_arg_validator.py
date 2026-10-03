from typing import Annotated, Optional

import pytest

from func_validator import (
    must_be_truthy,
    must_be_positive,
    DependsOn,
    MustBeMemberOf,
    ValidationError,
    MustBeLessThan,
    MustBeGreaterThan,
    validate_params,
)


class TestDependsOnValidator:
    @classmethod
    def setup_class(cls):
        # Validators
        depends_on_vald_kw = DependsOn(
            arg__2="rectangle",
            kw_args_validators={"arg__2": must_be_truthy},
            kw_args_err_msgs={
                "arg__2": "arg__1 has to be provided if arg__2 is rectangle"
            }
        )
        depends_on_vald_kw_2 = DependsOn("arg__2",  # arg__2 does not exist
                                         pos_args_validators=(MustBeLessThan,))
        depends_on_vald_arg = DependsOn("arg__1",
                                        pos_args_validators=(MustBeLessThan,))
        depends_on_vald_arg_2 = DependsOn("arg__1", "arg__2",
                                          pos_args_validators=(MustBeGreaterThan,
                                                               MustBeLessThan),
                                          pos_args_err_msgs=("nan",))
        must_be_member_of_vald = MustBeMemberOf(["square", "rectangle"])

        # Testing object (function)
        @validate_params
        def _foo_fn(
            cls,
            arg__1: Annotated[Optional[float],
                              depends_on_vald_kw, must_be_positive] = None,
            arg__2: Annotated[Optional[str],
                              must_be_member_of_vald] = "square",
        ):
            pass

        # If positional arguments length is different from positional
        # arguments validators.
        @validate_params
        def _baz_fn(
                cls,
                arg__1: float,
                arg__2: Annotated[float, DependsOn("arg__1")]
        ):
            pass

        # If positional arguments length is different from positional error
        # message length.
        @validate_params
        def _foobar(
                cls,
                arg__1: float,
                arg__2: float,
                arg__3: Annotated[float, depends_on_vald_arg_2]):
            pass

        # Testing object (class)
        class Foo:

            def __init__(self, arg__1: int = 10, arg__2: int = 5):
                self.arg__1 = arg__1
                self.arg__2 = arg__2

            @property
            def arg__2(self):
                return self._arg__2

            @arg__2.setter
            @validate_params
            def arg__2(self, arg__2: Annotated[int, depends_on_vald_arg]):
                self._arg__2 = arg__2

        # If dependent argument does not exist.
        class Bar:

            def __init__(self, arg__1: int = 5):
                self.arg__1 = arg__1

            @property
            def arg__1(self):
                return self._arg__1

            @arg__1.setter
            @validate_params
            def arg__1(self, arg__1: Annotated[int, depends_on_vald_kw_2]):
                self._arg__1 = arg__1

        cls.foo_fn = _foo_fn  # function to test
        cls.baz_fn = _baz_fn  # function to test
        cls.foobar_fn = _foobar  # function to test
        cls.foo_cls = Foo()  # class to test
        cls.bar_cls = Bar    # class type to test

    def test_depends_on_validator_4_kw_args(self):
        self.foo_fn()
        self.foo_fn(arg__1=10)
        self.foo_fn(arg__1=10, arg__2="rectangle")

    def test_depends_on_validator_errors_4_kw_args(self):
        with pytest.raises(ValidationError):
            self.foo_fn(arg__2="rectangle")
            self.foo_fn(arg__1=-10)

    def test_depends_on_validator_4_pos_args(self):
        assert self.foo_cls.arg__2 == 5

    def test_depends_on_validator_errors_4_pos_args(self):
        with pytest.raises(ValidationError):
            self.bar_cls()

        with pytest.raises(ValidationError):
            self.baz_fn(arg__1=34, arg__2=45)

        with pytest.raises(ValidationError):
            self.foobar_fn(arg__1=24, arg__2=44, arg__3=33)

        # class TestDependsOnValidator:
        #     @validate_params
        #     def decorated_fn(
        #         self,
        #         arg__1: Annotated[
        #             Optional[float],
        #             DependsOn(arg__2="rectangle",
        #                       kw_args_validators={"arg__2": must_be_truthy},
        #                       kw_args_err_msgs={"arg__2": "arg__1 has to be provided if arg__2 is rectangle"}),
        #             MustBePositive(),
        #         ] = None,
        #         arg__2: Annotated[
        #             str, MustBeMemberOf(["square", "rectangle"])
        #         ] = "square",
        #     ):
        #         pass
        #
        #     def test_depends_on_validator_4_kw_args(self):
        #         self.decorated_fn()
        #         self.decorated_fn(arg__1=10)
        #         self.decorated_fn(arg__1=10, arg__2="rectangle")
        #
        #     def test_depends_on_validator_errors_4_kw_args(self):
        #         with pytest.raises(ValidationError):
        #             self.decorated_fn(arg__2="rectangle")
        #
        #         with pytest.raises(ValidationError):
        #             self.decorated_fn(arg__1=-10)
        #
        #     def test_depends_on_validator_4_pos_args(self):
        #         class A:
        #
        #             def __init__(self, arg__1: int = 10, arg__2: int = 5):
        #                 self.arg__1 = arg__1
        #                 self.arg__2 = arg__2
        #
        #             @property
        #             def arg__2(self):
        #                 return self._arg__2
        #
        #             @arg__2.setter
        #             @validate_params
        #             def arg__2(
        #                 self,
        #                 arg__2: Annotated[
        #                     int,
        #                     DependsOn("arg__1", pos_args_validators=(MustBeLessThan,))
        #                 ],
        #             ):
        #                 self._arg__2 = arg__2
        #
        #         a = A()
        #         assert a.arg__2 == 5
        #
        # If dependent argument does not exist.
        # class B:
        #
        #     def __init__(self, arg__1: int = 5):
        #         self.arg__1 = arg__1
        #
        #     @property
        #     def arg__1(self):
        #         return self._arg__1
        #
        #     @arg__1.setter
        #     @validate_params
        #     def arg__1(
        #         self,
        #         arg__1: Annotated[
        #             int, DependsOn("arg__2",
        #                            pos_args_validators=(MustBeLessThan,))
        #         ],
        #     ):
        #         self._arg__1 = arg__1
        #
        # with pytest.raises(ValidationError):
        #     B()
