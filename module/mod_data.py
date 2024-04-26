import importlib
import inspect
import yef


class MethodParam:
    def __init__(self, name: str, param_type: type):
        self.name = name
        self.param_type = param_type

    def __repr__(self):
        return f"{self.name}: {self.param_type}"


class MethodInfo:
    def __init__(self, name: str, params: list[MethodParam], return_type: str):
        self.name = name
        self.params = params
        self.return_type = return_type

    def __repr__(self):
        f = ", ".join([p.__repr__() for p in self.params])
        return f"{self.name}({f})"


class ClassInfo:
    def __init__(self, cls, methods_info: dict[str, MethodInfo]):
        self.cls = cls
        self.methods_info = methods_info


class FuncInfo(MethodInfo):
    def __init__(self, name: str, params: list[MethodParam], return_type: str):
        super().__init__(name, params, return_type)


class Module:
    def __init__(self, name: str, gopkg: str, filename: str, imports: list[str]):
        self.Name = name
        self.Gopkg = gopkg
        self.Filename = filename
        self.Imports = imports


class ModuleInfo:
    def __init__(self, module: Module, classes: list[ClassInfo], functions: list[FuncInfo]):
        self.module = module
        self.classes = classes
        self.functions = functions


def get_classes(module) -> list:
    classes = []
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            classes.append(obj)
    return classes


def get_class_info(class_) -> ClassInfo:
    methods_info: dict[str, MethodInfo] = {}
    methods = [method for method in inspect.getmembers(class_) if method[0].startswith("_") == False and not method[1].
        __qualname__.startswith(yef.YefClass.__name__)]
    methods.append(("__init__", class_.__init__))
    for method in methods:
        class_methods = inspect.signature(method[1]).parameters
        method_params: list[MethodParam] = []
        for name, param in class_methods.items():
            method_params.append(MethodParam(name, param.annotation))
        methods_info[method[0]] = MethodInfo(method[0], method_params, inspect.signature(method[1]).return_annotation)
    return ClassInfo(class_, methods_info)


def get_module_functions_info(module) -> list[FuncInfo]:
    functions_info: list[FuncInfo] = []
    members = inspect.getmembers(module)
    functions = [func for _, func in members if inspect.isfunction(func) and inspect.getmodule(func) == module]
    for func in functions:
        func_params: list[MethodParam] = []
        for name, param in inspect.signature(func).parameters.items():
            func_params.append(MethodParam(name, param.annotation))
        functions_info.append(FuncInfo(func.__name__, func_params, inspect.signature(func).return_annotation))
    return functions_info


def get_modules_info(modules: list[Module]) -> list[ModuleInfo]:
    modules_info: list[ModuleInfo] = []
    for module in modules:
        module_classes_info: list[ClassInfo] = []
        imported_module = importlib.import_module(str(module.Name))
        members = inspect.getmembers(imported_module)
        local_classes = [member for name, member in members if inspect.getmodule(member) == imported_module]
        for lclass in local_classes:
            if inspect.isclass(lclass) and issubclass(lclass, yef.YefClass):
                clsInfo = get_class_info(lclass)
                module_classes_info.append(clsInfo)
        module_func_info = get_module_functions_info(imported_module)
        modules_info.append(ModuleInfo(module, module_classes_info, module_func_info))
    return modules_info
