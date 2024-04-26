def gotype(args_info: dict, return_type: str):
    def decorator(func):
        for arg_name, arg_type in args_info.items():
            func.__annotations__[arg_name] = arg_type
        func.__annotations__['return'] = return_type
        return func
    return decorator
