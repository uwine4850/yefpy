import inspect
import os
from typing import List

from ruamel.yaml import YAML
import yef
from module.mod_data import MethodInfo, ClassInfo, Module, ModuleInfo, FuncInfo

yaml = YAML()


class YamlClassData:
    def __init__(self):
        self.class_name: str = ""
        self.methods_info: dict[str, MethodInfo] = {}


class YamlFuncData:
    def __init__(self, name: str, func_info: FuncInfo):
        self.name = name
        self.func_info = func_info


class YamlModData:
    def __init__(self, mod_info: ModuleInfo, classes: list[YamlClassData], functions: list[YamlFuncData]):
        self.mod_info = mod_info
        self.classes = classes
        self.functions = functions


def get_yaml_modules_data(modules_info: list[ModuleInfo]) -> list[YamlModData]:
    # yaml_modules: dict[Module, list[YamlClassData]] = {}
    mod_data: list[YamlModData] = []
    for mod_info in modules_info:
        yaml_class_data: list[YamlClassData] = []
        yaml_func_data: list[YamlFuncData] = []
        for class_info in mod_info.classes:
            yaml_class = YamlClassData()
            cls: yef.YefClass = class_info.cls
            yaml_class.class_name = cls.get_class_name()
            yaml_class.methods_info = class_info.methods_info
            yaml_class_data.append(yaml_class)
        for func_info in mod_info.functions:
            yaml_func = YamlFuncData(func_info.name, func_info)
            yaml_func_data.append(yaml_func)
        mod_data.append(YamlModData(mod_info, yaml_class_data, yaml_func_data))
        # yaml_modules[mod_info] = yaml_class_data
    # return yaml_modules
    return mod_data


class ArgTypeIsEmpty(Exception):
    def __init__(self, arg_name):
        super().__init__(f'{arg_name} argument has no type')


def _handle_init(cls: YamlClassData) -> list[dict[str, str]]:
    init_args: list[dict[str, str]] = []
    for arg in cls.methods_info["__init__"].params:
        if arg.param_type is inspect._empty and arg.name != "self":
            raise ArgTypeIsEmpty(arg.name)
        if arg.name != "self":
            init_args.append({"name": arg.name, "type": arg.param_type})
    return init_args


def _handle_class_method(cls: YamlClassData) -> dict:
    class_methods_data = {}
    for method_name, method in cls.methods_info.items():
        if method_name == "__init__":
            continue
        class_method_args = []
        class_method_type = "class"
        has_type = False
        for method_arg in method.params:
            if method_arg.name == "self":
                class_method_type = "instance"
                has_type = True
                continue
            elif not has_type:
                class_method_type = "class"
            class_method_args.append({'name': method_arg.name, 'type': method_arg.param_type})
        class_methods_data[method_name] = {'type': class_method_type, 'args': class_method_args,
                                           'output': method.return_type}
    return class_methods_data


def _handle_module_func(func: YamlFuncData) -> dict:
    args = []
    for param in func.func_info.params:
        args.append({"name": param.name, "type": param.param_type})
    return {"name": func.name, "args": args, "output": func.func_info.return_type}


def generate_yaml(ymd: list[YamlModData], filename: str, gen_dir_path: str):
    yaml_data: dict = {'modules': {}}
    for module_data in ymd:
        module = module_data.mod_info.module
        mn = module.Name
        modules = yaml_data["modules"]
        modules[mn] = {"gopkg": module.Gopkg, "filename": module.Filename,
                       "import": module.Imports, "classes": [], "functions": []}
        for cls in module_data.classes:
            class_data = {"name": cls.class_name, "args": _handle_init(cls), "methods": _handle_class_method(cls)}
            modules[mn]["classes"].append(class_data)
        for func in module_data.functions:
            modules[mn]["functions"].append(_handle_module_func(func))
        yaml_data["modules"] = modules
    if not os.path.exists(gen_dir_path):
        os.makedirs(gen_dir_path)
    with open(os.path.join(gen_dir_path, filename), 'w') as file:
        yaml.dump(yaml_data, file)
