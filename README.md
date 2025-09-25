# func-validator

[![Github](https://img.shields.io/badge/func--validator-000000?style=flat&logo=github&logoColor=white)](https://github.com/patrickboateng/func-validator)
[![PyPI Latest Release](https://img.shields.io/pypi/v/func-validator?style=flat&logo=pypi)](https://pypi.org/project/func-validator/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/func-validator.svg?logo=python&style=flat)](https://pypi.python.org/pypi/func-validator/)
[![Unit-Tests](https://github.com/patrickboateng/func-validator/actions/workflows/func-validator-unit-tests.yml/badge.svg)](https://github.com/patrickboateng/func-validator/actions/workflows/func-validator-unit-tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/patrickboateng/func-validator/badge.svg?branch=main)](https://coveralls.io/github/patrickboateng/func-validator?branch=main)
[![license](https://img.shields.io/pypi/l/func-validator?style=flat&logo=opensourceinitiative)](https://opensource.org/license/mit/)

MATLAB-style function argument validation for Python - clean, simple, and
reliable.

## Table of Contents

- [Installation](#installation)
- [Imports](#imports)
- [Usage](#usage)
- [Validators](#validators)
- [License](#license)

## Installation

```shell
pip install func-validator
```

## Imports

- Import for the function decorator

  ```python
  from func_validator import validate_func_args
  from func_validator import validate_func_args_at_runtime 
  ```

- Import for the validators

  ```python
  from func_validator import MustBeGreaterThan, MustMatchRegex 
  from func_validator.validators.numeric_arg_validators import MustBeGreaterThan
  ```

  There are 3 other modules you can import validators from, namely:

    - [collection_arg_validators](#collection-validators)
    - [datatype_arg_validators](#datatype-validators)
    - [text_arg_validators](#text-validators)

> [!NOTE]
> All validator objects (functions/callables) can be imported from the
> `func_validator` namespace

## Usage

```python

from typing import Annotated
from func_validator import validate_func_args
from func_validator.validators.numeric_arg_validators import ( MustBePositive, 
                                                               MustBeNegative)

@validate_func_args
def func(a: Annotated[int, MustBePositive], b: Annotated[float, MustBeNegative]):
    return (a, b)

func(10, -10)  # ✅ Correct

func(-10, -10)  # ❌ Wrong -10 is not positive and 10 is not negative
                # A validation error is raised with a message.

func(0, -10)    # ❌ Wrong 0 is not positive
                # A validation error is raised with a message.
                
func(20, 10)    # ❌ Wrong 10 is not negative
                # A validation error is raised with a message.
```

## Validators

This is not the exhaustive list for all validators, checkout
the [docs](https://func-validator.readthedocs.io/en/latest/)
for more examples.

### Collection Validators

<table>
    <tr>
        <td>MustBeMemberOf</td>
        <td>Validate that argument value is in a collection</td>
    </tr>
    <tr>
        <td>MustBeEmpty</td>
        <td>Validate that argument value is empty</td>
    </tr>
</table>

### DataType Validators

<table>
    <tr>
        <td>MustBeA</td>
        <td>Validates that the value is of the specified type</td>
    </tr>
</table>

### Numeric Validators

<table>
    <tr>
        <td>MustBePositive</td>
        <td>Validate that argument value is positive</td>
    </tr>
    <tr>
        <td>MustBeNegative</td>
        <td>Validate that argument value is negative</td>
    </tr>
</table>

### Text Validators

<table>
    <tr>
        <td>MustMatchRegex</td>
        <td>Validates that the value matches the provided regular expression.</td>
    </tr>
</table>

## License

MIT License
