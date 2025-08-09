from typing import Callable


class validator:

    def __init__(self) -> None:
        pass

    def __call__(self, func: Callable) -> Callable:
        return func
