from ._core import T


class MustBeA:
    """Validates that the value is of the specified type."""

    def __init__(self, arg_type=None, infer=True):
        """
        :param arg_type: The type to validate against. If None and infer
                         is True, the type will be inferred from the value
                         at runtime. Default is None.

        :param infer: Whether to infer the type from the typehint from
                      `typing.Annotated`. If infer is true, `arg_type` is
                       ignored. Default is True.

        :raises TypeError: If the value is not of the specified type.
        :raises ValueError: If arg_type is None and infer is False.
        """
        if arg_type is None and not infer:
            raise ValueError("arg_type must be provided if infer is False.")
        self.arg_type = arg_type
        self.infer = infer

    def __call__(self, value: T) -> None:
        if not isinstance(value, self.arg_type):
            exc_msg = (
                f"Value must be of type {self.arg_type}, got {type(value)} instead."
            )
            raise TypeError(exc_msg)
