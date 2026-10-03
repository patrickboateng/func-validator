from typing import Optional, Type, Sequence
from collections import namedtuple

from ._core import T, ValidationError, Validator


__all__ = ["DependsOn"]


class DependsOn(Validator):

    """Class to indicate that a function argument depends on another
    argument.

    When an argument is marked as depending on another, it implies that the
    presence or value of one argument may influence the validation or necessity
    of the other.
    """

    DEFAULT_ERROR_MSG = ""
    args_metadata = namedtuple("ArgsMetadata",
                               "validator,err_msg,value",
                               defaults=[None])

    def __init__(
        self,
        *pos_args: str,
        pos_args_validators: tuple[Type[Validator]] = (),
        pos_args_err_msgs: tuple[str] = (),
        kw_args_validators: Optional[dict[str, Validator]] = None,
        kw_args_err_msgs: Optional[dict[str, str]] = None,
        extra_err_msg_args: Optional[dict] = None,
        **kw_args: T
    ):

        super().__init__(extra_err_msg_args=extra_err_msg_args)

        self.pos_args = pos_args
        self.pos_args_validators = pos_args_validators
        self.pos_args_err_msgs = pos_args_err_msgs
        self.kw_args_validators = (
            {} if kw_args_validators is None else kw_args_validators
        )
        self.kw_args_err_msgs = (
            {} if kw_args_err_msgs is None else kw_args_err_msgs
        )
        self.extra_err_msg_args = (
            {} if extra_err_msg_args is None else extra_err_msg_args
        )
        self.kw_args = kw_args

        # The arguments of the decorated function
        self.arguments = {}

    def __call__(self, arg_val: T, arg_name: str) -> None:
        if len(self.pos_args) > 0:
            self._pos_args_validation(arg_val, arg_name)
        if len(self.kw_args) > 0:
            self._kw_args_validation(arg_val, arg_name)

    @classmethod
    def _transform_pos_args(
            cls,
            pos_args: Sequence[str],
            pos_args_validators: Sequence[Type[Validator]],
            pos_args_err_msgs: Sequence[str],
    ) -> dict[str, tuple]:
        args_len = len(pos_args)
        validators_len = len(pos_args_validators)
        err_msgs_len = len(pos_args_err_msgs)

        if args_len != validators_len:
            err_msg = ("The length of the positional arguments (pos_args) "
                       "should be equal to the length of the positional "
                       "validators (pos_arg_validators)")
            raise ValidationError(err_msg)

        if err_msgs_len == 0:
            pos_args_err_msgs = (None,) * args_len
            err_msgs_len = args_len

        if args_len != err_msgs_len:
            err_msg = ("The length of the positional arguments (pos_args) "
                       "should be equal to the length of the positional "
                       "error messages (pos_args_err_msgs)")
            raise ValidationError(err_msg)

        _pos_args: dict[str, tuple] = {}
        args = zip(pos_args, pos_args_validators, pos_args_err_msgs)

        for pos_arg_name, pos_arg_validator, pos_arg_err_msg in args:
            _pos_args[pos_arg_name] = cls.args_metadata(pos_arg_validator,
                                                        pos_arg_err_msg)
        return _pos_args

    @classmethod
    def _transform_kw_args(
            cls,
            kw_args: dict[str, T],
            kw_args_validators: dict[str, Validator],
            kw_args_err_msgs: dict[str, str],
    ) -> dict[str, tuple]:
        _kw_args: dict[str, tuple] = {}

        if len(kw_args_err_msgs) == 0:
            for kw_arg_name in kw_args:
                kw_args_err_msgs[kw_arg_name] = None

        for kw_arg_name in kw_args:
            kw_arg_value = kw_args[kw_arg_name]
            kw_arg_validator = kw_args_validators[kw_arg_name]
            kw_arg_err_msg = kw_args_err_msgs[kw_arg_name]
            _kw_args[kw_arg_name] = cls.args_metadata(kw_arg_validator,
                                                      kw_arg_err_msg,
                                                      kw_arg_value)
        return _kw_args

    @classmethod
    def _get_parent_arg_value(cls, parent_arg_name: str, arguments: dict) -> T:
        if parent_arg_name in arguments:
            return arguments[parent_arg_name]

        instance = arguments.get("self")

        try:
            return getattr(instance, parent_arg_name)
        except AttributeError:
            err_msg = (f"Parent argument '{parent_arg_name}' was not found "
                       f"in function arguments or instance attributes.")
            raise ValidationError(err_msg)

    def _pos_args_validation(self, arg_val: T, arg_name: str) -> None:
        # positional arguments and metadata transformed
        pos_args_trfm = self._transform_pos_args(self.pos_args,
                                                 self.pos_args_validators,
                                                 self.pos_args_err_msgs)
        for parent_arg_name in pos_args_trfm:
            pos_arg = pos_args_trfm[parent_arg_name]
            pos_arg_value = self._get_parent_arg_value(parent_arg_name,
                                                       self.arguments)
            validator = pos_arg.validator
            err_msg = pos_arg.err_msg
            parent_arg_info = {'parent_arg_name': parent_arg_name,
                               'parent_arg_value': pos_arg_value}
            self.extra_err_msg_args |= parent_arg_info
            err_msg_args = self.extra_err_msg_args
            validator = validator(pos_arg_value,
                                  err_msg=err_msg,
                                  extra_err_msg_args=err_msg_args)
            validator(arg_val, arg_name)

    def _kw_args_validation(self, arg_val: T, arg_name: str) -> None:
        # keyword arguments and metadata transformed
        kw_args_trfm = self._transform_kw_args(self.kw_args,
                                               self.kw_args_validators,
                                               self.kw_args_err_msgs)
        for parent_arg_name in kw_args_trfm:
            kw_arg = kw_args_trfm[parent_arg_name]
            parent_arg_value = self._get_parent_arg_value(parent_arg_name,
                                                          self.arguments)
            provided_parent_arg_value = kw_arg.value
            if parent_arg_value == provided_parent_arg_value:
                parent_arg_info = {"parent_arg_name": parent_arg_name,
                                   "parent_arg_value": parent_arg_value}
                validator = kw_arg.validator
                err_msg = kw_arg.err_msg
                self.extra_err_msg_args |= parent_arg_info

                # The validator has already been created, so you need to
                # check the err_msg before making any modification to it.
                if err_msg:
                    validator.err_msg = err_msg

                validator.extra_err_msg_args.update(self.extra_err_msg_args)
                validator(arg_val, arg_name)
