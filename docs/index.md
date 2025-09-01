# func-validator

<p align="left">
  <a href="https://pypi.org/project/func-validator/">
    <img src="https://img.shields.io/pypi/v/func-validator?style=flat&logo=pypi" alt="PyPI Latest Release">
  </a>
  <a href="https://pypi.python.org/pypi/func-validator/">
    <img src="https://img.shields.io/pypi/pyversions/func-validator.svg?logo=python&style=flat" alt="PyPI pyversions">
  </a>
  <a href="https://opensource.org/license/mit/">
    <img src="https://img.shields.io/pypi/l/func-validator?style=flat&logo=opensourceinitiative" alt="license">
  </a>
</p>

`func-validator` is a python package which provides MATLAB-style function 
argument validation for Python, which is clean, simple, and reliable.

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
  ```

## Usage

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

## Validators

This is not the exhaustive list for all validators, click on each heading to
checkout more examples.

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

### [DataType Validators](reference/datatype_validators.md)

<table>
    <tr>
        <td>MustBeA</td>
        <td>Validates that the value is of the specified type</td>
    </tr>
</table>



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

### [Text Validators](reference/text_validators.md)

<table>
    <tr>
        <td>MustMatchRegex</td>
        <td>Validates that the value matches the provided regular expression.</td>
    </tr>
</table>

## License

MIT License
