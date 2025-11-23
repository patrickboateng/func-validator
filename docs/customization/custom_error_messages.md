# Custom Error Messages

You can add custom error message to validators via the `err_msg` parameter.
If you would like to interpolate the argument names and values into your 
message, you can do that using the following syntax:

- `${arg_name}`: To interpolate the name of the argument
- `${arg_value}`: To interpolate the value of the argument

If you are using the `DependsOn` validator, you can further customize your
error message using two extra interpolated values as follows:

- `${dep_arg_name}`: To interpolate the name of the dependent argument
- `${dep_arg_value}`: To interpolate the value of the dependent argument