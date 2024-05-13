def gotype(args_info: dict, return_type: str):
    """
    A decorator that must be used if the function accepts or returns some data type.
    If the function does not accept or return data, the decorator is not required.
    :param args_info: The key is the name of the variable. The value is a data type from the Golang language.
    :param return_type: Data type from Golang language.
    """
    def decorator(func):
        for arg_name, arg_type in args_info.items():
            func.__annotations__[arg_name] = arg_type
        func.__annotations__['return'] = return_type
        return func
    return decorator
