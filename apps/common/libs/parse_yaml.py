# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     parse_yaml.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/02 12:11:08
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import os
import yaml
import importlib
import typing as t
from pathlib import Path

from apps.common.libs.dir import get_project_path, is_file
from apps.common.libs.environ import ENV_TYPE, DEFAULT_ENV_TYPE

__all__ = ["DictObject", "ProjectConfig"]


class ParseYaml(object):

    def __init__(self, file_path):
        self.path = Path(file_path)
        if not is_file(file_path=self.path):
            raise ValueError("<{}>文件不存在，或者它不是一个文件.".format(self.path))

    @property
    def dict(self):
        with open(self.path, "r", encoding="utf-8") as f:
            y = yaml.load(f, Loader=yaml.FullLoader)
            return y


class DictObject(dict):
    def __init__(self, *args, **kwargs):
        super(DictObject, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        value = self.get(key)
        if isinstance(value, dict):
            value = DictObject(value)
        return value


class ProjectConfig(object):

    @classmethod
    def create_class(
        cls, class_name: str, class_attr: dict = None, class_parents: tuple = None
    ) -> type:
        # 遍历属性字典，把不是__开头的属性名字变为大写
        new_attr = dict()
        class_name = class_name.title()
        if class_attr:
            for name, value in class_attr.items():
                if not name.startswith("__"):
                    new_attr[name] = value

        # 调用type来创建一个类
        if class_parents:
            for c in class_parents:
                if type(c).__name__ != "type":
                    raise ValueError("<>它不是一个自定义类型.".format(c))
            new_class = type(class_name, class_parents, new_attr)
        else:
            new_class = type(class_name, (object,), new_attr)
        return new_class

    @staticmethod
    def set_class_attribute(cls: type, **kwargs):
        for key, value in kwargs.items():
            setattr(cls, key, value)
        return cls

    @classmethod
    def get_all_file(cls, config_root: Path):
        all_file_dict = dict()
        for d_ex in config_root.iterdir():
            if d_ex.is_dir():
                sub_file_list = list()
                for d_in in d_ex.iterdir():
                    if d_in.is_file() and d_in.name.endswith(".yaml"):
                        sub_file_list.append({d_in.stem: d_in})
                all_file_dict[d_ex.name] = sub_file_list
            else:
                if d_ex.is_file() and d_ex.name.endswith(".yaml"):
                    all_file_dict[d_ex.stem] = d_ex

        return all_file_dict

    @classmethod
    def iterator(cls, value: dict) -> iter:
        if isinstance(value, dict):
            for key, val in value.items():
                yield (key, val)

    @classmethod
    def iterator_plus(cls, value: dict) -> iter:
        for key, val in cls.iterator(value):
            if isinstance(val, (dict, list)):
                for k, v in cls.iterator_plus(val):
                    k = "{}.{}".format(key, k)
                    yield (k, v)
            else:
                yield (key, val)

    @classmethod
    def get_attr_class(cls, conf: dict) -> dict:
        """
        多层嵌套字典转成标准字典格式，转化格式如：key1.key2.key3.key4: value
        :param conf:
        :return:
        """
        base_dict = dict()
        for x, y in cls.iterator_plus(conf):
            base_dict[x] = y
        return base_dict

    @classmethod
    def convert_tuple(cls, prefix: str, value: str) -> tuple:
        obj = value.split(prefix)[-1].strip()
        if (
            obj.startswith("[")
            and obj.endswith("]")
            or obj.startswith("(")
            and obj.endswith(")")
        ):
            if obj[1:-1].endswith(","):
                obj = tuple(obj[1:-2].split(","))
            else:
                obj = tuple(obj[1:-1].split(","))
        else:
            if value.endswith(","):
                pass
            else:
                obj = tuple(value.split(","))
        return obj

    @classmethod
    def convert_sys_module(cls, prefix: str, value: str) -> tuple:
        obj = value.split(prefix)[-1].strip()
        module = ".".join(obj.split(".")[:-1])
        attr = obj.split(".")[-1]
        # 导入的就是需要导入的那个metaclass, 存在需要导入的模块，例如sys，os，socket等
        metaclass = importlib.import_module(module)
        return getattr(metaclass, attr)

    @classmethod
    def convert_abspath(
        cls, yaml_name: str, prefix: str, relative_path: str, project_home: str
    ) -> str:
        relative_path = relative_path.split(prefix)[-1].strip()
        if relative_path.startswith("./"):
            relative_path = relative_path.strip("./")
            relative_path_list = relative_path.split("/")
            relative_path = f"{os.sep}".join(relative_path_list)
            abspath = Path(project_home, relative_path)
            if abspath.parent.is_dir():
                pass
            else:
                os.makedirs(abspath.parent)
            return abspath
        else:
            raise ValueError("<{}>路径存在问题.".format(yaml_name))

    @classmethod
    def convert(
        cls, yaml_name: str, conf: t.Union[dict, DictObject], project_home: str
    ):
        prefix_object = "~~object"
        prefix_tuple = "~~tuple"
        prefix_abspath = "~~abspath"
        prefix_sys_module = "~~sys_module"
        # 使用isinstance检测数据类型
        if isinstance(conf, dict) or isinstance(conf, DictObject):
            for x in range(len(conf)):
                temp_key = list(conf.keys())[x]
                temp_value = conf[temp_key]
                if isinstance(temp_value, str):
                    if temp_value.startswith(prefix_object):
                        obj = eval(temp_value.split(prefix_object)[-1].strip())
                    elif temp_value.startswith(prefix_tuple):
                        obj = cls.convert_tuple(prefix=prefix_tuple, value=temp_value)
                    elif temp_value.startswith(prefix_abspath):
                        obj = cls.convert_abspath(
                            yaml_name=yaml_name,
                            prefix=prefix_abspath,
                            relative_path=temp_value,
                            project_home=project_home,
                        )
                    elif temp_value.startswith(prefix_sys_module):
                        obj = cls.convert_sys_module(
                            prefix=prefix_sys_module, value=temp_value
                        )
                    else:
                        obj = temp_value
                    if isinstance(conf, DictObject):
                        setattr(conf, temp_key, obj)
                    elif isinstance(conf, dict):
                        conf[temp_key] = obj
                # 自我调用实现无限遍历
                cls.convert(
                    yaml_name=yaml_name, conf=temp_value, project_home=project_home
                )

    @classmethod
    def get_object(cls, env_type: str = None, configuration_path: str = None) -> object:
        object_dict = dict()
        if configuration_path:
            configuration_path = Path(configuration_path)
            if configuration_path.is_dir():
                all_config = cls.get_all_file(configuration_path)
            else:
                raise ValueError("<{}>它不是一个目录.".format(configuration_path))
        else:
            config_root = Path(get_project_path(), "configuration")
            all_config = cls.get_all_file(config_root)
        for key, value in all_config.items():
            file_object_dict = dict()
            if isinstance(value, list):
                for file_dict in value:
                    for k, v in file_dict.items():
                        file_config = ParseYaml(v).dict
                        intersection = [i for i in file_config.keys() if i in ENV_TYPE]
                        if intersection:
                            if env_type:
                                if env_type in ENV_TYPE:
                                    file_config = file_config.get(env_type, dict())
                                else:
                                    raise ValueError(
                                        "<{}>无效的环境类型.".format(env_type)
                                    )
                            else:
                                if os.getenv("ENV_TYPE"):
                                    file_config = file_config.get(
                                        os.getenv("ENV_TYPE"), dict()
                                    )
                                else:
                                    file_config = file_config.get(
                                        DEFAULT_ENV_TYPE, dict()
                                    )
                        # 将文件转成字典对象
                        file_config_object = DictObject(file_config)
                        cls.convert(
                            yaml_name=str(v),
                            conf=file_config_object,
                            project_home=get_project_path(),
                        )
                        # 将字典对象放入目录列表
                        file_object_dict[k] = file_config_object
                object_dict[key] = cls.create_class(key, file_object_dict)
            else:
                file_config = ParseYaml(value).dict
                intersection = [i for i in file_config.keys() if i in ENV_TYPE]
                if intersection:
                    if env_type:
                        if env_type in ENV_TYPE:
                            file_config = file_config.get(env_type, dict())
                        else:
                            raise ValueError("<{}>无效的环境类型.".format(env_type))
                    else:
                        if os.getenv("ENV_TYPE"):
                            file_config = file_config.get(os.getenv("ENV_TYPE"), dict())
                        else:
                            file_config = file_config.get(DEFAULT_ENV_TYPE, dict())
                file_config_object = DictObject(file_config)
                cls.convert(
                    yaml_name=str(value),
                    conf=file_config_object,
                    project_home=get_project_path(),
                )
                object_dict[key] = file_config_object
        return cls.create_class("configuration", object_dict)
