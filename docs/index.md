# func-validator

[![PyPI Latest Release](https://img.shields.io/pypi/v/func-validator?logo=pypi)](https://pypi.org/project/func-validator/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/func-validator.svg?logo=python&style=flat)](https://pypi.python.org/pypi/func-validator/)
[![Unit-Tests](https://github.com/patrickboateng/func-validator/actions/workflows/func-validator-unit-tests.yml/badge.svg)](https://github.com/patrickboateng/func-validator/actions/workflows/func-validator-unit-tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/patrickboateng/func-validator/badge.svg?branch=main)](https://coveralls.io/github/patrickboateng/func-validator?branch=main)
[![license](https://img.shields.io/pypi/l/func-validator?style=flat&logo=opensourceinitiative)](https://opensource.org/license/mit/)

`func-validator` is a python package which provides MATLAB-style function 
argument validation for Python, which is clean, simple, and reliable.

## Installation

```shell
pip install func-validator 
```

## Imports

- Import for the function decorator

  ```python
  from func_validator import validate_params
  from func_validator import validate_func_args
  from func_validator import validate_func_args_at_runtime 
  ```

!!! note

    `validate_params` is a function decorator that validates function arguments
    at runtime. `validate_func_args` and `validate_func_args_at_runtime`
    are alias for `validate_params`.

- Import for the validators

  ```python
  from func_validator import MustBeGreaterThan, MustMatchRegex 
  ```

## Validators & Usage

!!! note

    This is not the exhaustive list for all validators, click on each heading 
    to checkout more examples.

### [Collection Validators](reference/collection_validators.md)

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

```python

>>> from typing import Annotated
>>> from func_validator import validate_func_args
>>> from func_validator.validators.collection_arg_validators import (MustBeMemberOf, 
...                                                                  MustBeEmpty)
>>> @validate_func_args
... def func(val_1: Annotated[int, MustBeMemberOf([1, 2, 3])]):
...        return val_1
>>> func(1)
1
>>> func(4)
Traceback (most recent call last):
...
ValidationError: val_1:4 must be in [1, 2, 3]

>>> @validate_func_args
... def func_2(val_2: Annotated[list, MustBeEmpty]):
...        return val_2
>>> func_2([])
[]
>>> func_2([1, 2, 3])
Traceback (most recent call last):
...
ValidationError: val_2:[1, 2, 3] must be empty.

```

### [DataType Validators](reference/datatype_validators.md)

<table>
    <tr>
        <td>MustBeA</td>
        <td>Validates that the value is of the specified type</td>
    </tr>
</table>

```python

>>> from typing import Annotated
>>> from func_validator import MustBeA, validate_func_args
>>> @validate_func_args
... def func(val_1: Annotated[list, MustBeA(list)]):
...     return val_1
>>> func([2, 3])
[2, 3]
>>> func((2, 3))
Traceback (most recent call last):
...
ValidationError: val_1 must be of type <class 'list'>, got <class 'tuple'> instead.

```

### [Numeric Validators](reference/numeric_validators.md)

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

```python

>>> from typing import Annotated
>>> from func_validator import (validate_func_args,
...                             MustBePositive,
...                             MustBeNegative)

>>> @validate_func_args  
... def func(a: Annotated[int, MustBePositive],
...          b: Annotated[float, MustBeNegative]):
...     return (a, b)

>>> func(10, -10)  # ✅ Correct
(10, -10)

>>> func(-10, -10)  # ❌ Wrong -10 is not positive and 10 is not negative
Traceback (most recent call last):
...
ValidationError: a:-10 must be > 0.0.

>>> func(0, -10)  # ❌ Wrong 0 is not positive
Traceback (most recent call last):
...
ValidationError: a:0 must be > 0.0.

>>> func(20, 10)  # ❌ Wrong 10 is not negative
Traceback (most recent call last):
...
ValidationError: b:10 must be < 0.0.

```


### [Text Validators](reference/text_validators.md)

<table>
    <tr>
        <td>MustMatchRegex</td>
        <td>Validates that the value matches the provided regular expression.</td>
    </tr>
</table>

```python
>>> from func_validator import validate_func_args
>>> from func_validator import MustMatchRegex, validate_func_args
>>> @validate_func_args
... def func(val_1: Annotated[str, MustMatchRegex(r"\d+")]):
...     return val_1
>>> func("123")
'123'
>>> func("abc")
Traceback (most recent call last):
...
ValidationError: val_1:abc does not match the regex pattern '\d+'.

```

## License

MIT License
