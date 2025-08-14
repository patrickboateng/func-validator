# func-validator

<div>

[![PyPI Latest Release](https://img.shields.io/pypi/v/func-validator?style=flat&logo=pypi)](https://pypi.org/project/func-validator/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/func-validator.svg?logo=python&style=flat)](https://pypi.python.org/pypi/func-validator/)
[![license](https://img.shields.io/pypi/l/func-validator?style=flat&logo=opensourceinitiative)](https://opensource.org/license/mit/)

</div>

MATLAB-style function argument validation for Python.

## Installation

```sh

$ pip install func-validator

```

## Usage

```py

from typing import Annotated
from func_validator import (validate_func_args_at_runtime, MustBePositive,
                            MustBeNegative)


@validate_func_args_at_runtime
def func(a: Annotated[int, MustBePositive],
         b: Annotated[float, MustBeNegative]):
    pass


func(10, -10)  # ✅ Correct
func(-10, 10)  # ❌ Wrong -10 is not positive and 10 is not negative
func(0, -10)  # ❌ Wrong 0 is not positive

```

## License

MIT License
