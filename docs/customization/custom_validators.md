# Custom Validators

You can add a custom validator by creating a class and inheriting from
`Validator` (`from func_validator import Validator`) base class. Implement
the `__call__` method to accept arguments in the order `arg_value` and
`arg_name`. Raise a `ValidationError`
(`from func_validator import ValidationError`) if validation fails.

## Example custom validator

```python

from func_validator import Validator, ValidationError

# Validator
class MustBeEven(Validator):
    
    def __call__(self, arg_value, arg_name: str):
        if arg_value % 2 != 0:
            raise ValidationError(f"{arg_name}:{arg_value} must be even")

# Usage
from typing import Annotated
from func_validator import validate_params

@validate_params
def fn(param_1: Annotated[int, MustBeEven()]):
    return param_1 * param_1

```


