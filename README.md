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
from func_validator import (validate_func_args_at_runtime, 
                            MustBePositive,
                            MustBeNegative)


@validate_func_args_at_runtime
def func(a: Annotated[int, MustBePositive],
         b: Annotated[float, MustBeNegative]):
    pass


func(10, -10)  # ✅ Correct
func(-10, 10)  # ❌ Wrong -10 is not positive and 10 is not negative
func(0, -10)  # ❌ Wrong 0 is not positive

```

## Validators

### Numeric Value Validation

<table>
    <tr>
        <td>MustBePositive</td>
        <td>Validate that value is positive</td>
    </tr>
    <tr>
        <td>MustBeNonPositive</td>
        <td>Validate that value is non-positive</td>
    </tr>
    <tr>
        <td>MustBeNegative</td>
        <td>Validate that value is negative</td>
    </tr>
    <tr>
        <td>MustBeNonNegative</td>
        <td>Validate that value is non-negative</td>
    </tr>
</table>

### Comparison Validation

<table>
    <tr>
        <td>MustBeEqual</td>
        <td>Validate that value is equal to another value</td>
    </tr>
    <tr>
        <td>MustBeNotEqual</td>
        <td>Validate that value is not equal to another value</td>
    </tr>
    <tr>
        <td>MustBeGreaterThan</td>
        <td>Validate that value is greater than another value</td>
    </tr>
    <tr>
        <td>MustBeGreaterThanOrEqual</td>
        <td>Validate that value is greater than or equal to another value</td>
    </tr>
    <tr>
        <td>MustBeLessThan</td>
        <td>Validate that value is less than another value</td>
    </tr>
    <tr>
        <td>MustBeLessThanOrEqual</td>
        <td>Validate that value is less than or equal to another value</td>
    </tr>
</table>

### Membership Validation

<table>
    <tr>
        <td>MustBeIn</td>
        <td>Validate that value is in a collection</td>
    </tr>
    <tr>
        <td>MustBeBetween</td>
        <td>Validate that value is between two other values</td>
    </tr>
</table>

### Size Validation

<table>
    <tr>
        <td>MustBeEmpty</td>
        <td>Validate that a collection is empty</td>
    </tr>
    <tr>
        <td>MustBeNonEmpty</td>
        <td>Validate that a collection is non-empty</td>
    </tr>
    <tr>
        <td>MustHaveLength</td>
        <td>Validate that a collection has a specific length</td>
    </tr>
</table>


## License

MIT License
