# Adding custom validators


You can add a custom validator by creating a function that takes two
parameters, `arg_value` (type depends on what you are testing), and 
`arg_name` (type `str`). Your function should return a tuple containing two
elements, a `bool` indicating if the validation passed, and a `str` containing
an error message if the validation failed (or an empty string if it passed).
`arg_name` is provided so that you can include it in your error message.
You should decorate your function with the `@validator` decorator from the
`func_validator` package. See the example below.

!!! note

    Argument values will be passed to your validator in the order `arg_value`,
    `arg_name`, so make sure your function signature matches this order. The 
    specific parameter name does not matter, only the order matters since
    it is positional.

## Example custom validator

```python
from func_validator import validator

@validator
def must_be_even(arg_val: int, arg_name: str) -> tuple[bool, str]:
    check = arg_val % 2 == 0
    if check:
        return check, ""

    return check, f"{arg_name}:{arg_val} must be even"
```

