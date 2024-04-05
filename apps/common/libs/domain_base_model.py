# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     domain_base_model.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/05 21:14:05
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import inspect
import typing as t
from abc import abstractmethod


class DomainBaseModel(object):

    # 获取Parent类的所有子类
    @classmethod
    def get_subclasses(cls):
        subclasses = []
        for name, obj in inspect.getmembers(cls):
            if inspect.isclass(obj) and issubclass(obj, cls) and obj != cls:
                subclasses.append(obj)
        return subclasses

    def __get_dto_attributes(self) -> t.List:
        return inspect.getmembers(self, predicate=lambda a: not (inspect.isroutine(a)))

    def update_attributes(self, **kwargs):
        attrs = self.__get_dto_attributes()
        for attr_tuple in attrs:
            attr_name = attr_tuple[0]
            if isinstance(self.__class__.__dict__.get(attr_name), property) and attr_name in kwargs.keys():
                setattr(self, attr_name, kwargs.get(attr_name))
        return self

    def attributes(self) -> t.Dict:
        attrs = self.__get_dto_attributes()
        attrs_new = dict()
        for x in attrs:
            if x[0].startswith('_') or x[0].startswith('__') or x[0].endswith('_') or x[0].endswith('__'):
                continue
            else:
                if getattr(x[1], "attributes", None):
                    attr_value = x[1].attributes()
                else:
                    if isinstance(x[1], list) and len(x[1]) and getattr(x[1][0], "attributes", None):
                        attr_value = [y.attributes() for y in x[1]]
                    else:
                        attr_value = x[1]
                attrs_new.update({x[0]: attr_value})
        return attrs_new

    def __to_string(self) -> str:
        attrs = self.__get_dto_attributes()
        attrs_slice = list()
        for attr_tuple in attrs:
            attr_name = attr_tuple[0]
            if isinstance(self.__class__.__dict__.get(attr_name), property):
                if attr_tuple[1] and isinstance(attr_tuple[1], str):
                    attr_str = f"{attr_tuple[0]}='{attr_tuple[1]}'"
                else:
                    attr_str = f"{attr_tuple[0]}={attr_tuple[1]}"
                attrs_slice.append(attr_str)
        if attrs_slice:
            string = f"{self.__class__.__name__}(" + ", ".join(attrs_slice) + ")"
        else:
            string = f"{self.__class__.__name__}()"
        return string

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @staticmethod
    def has_attribute(obj: object, name: str):
        if name in obj.__slots__:
            return True
        else:
            return False

    @staticmethod
    def init_list_model(data_list: list, model: type, is_exist_primary_key: bool = True) -> list:
        new_list = list()
        for x in data_list:
            if isinstance(x, model):
                pass
            elif isinstance(x, dict):
                x = model(**x)
            else:
                continue
            if is_exist_primary_key is True and x.is_empty() is True:
                continue
            new_list.append(x)
        return new_list

    def __str__(self):
        return self.__to_string()

    def __repr__(self):
        return self.__to_string()


if __name__ == '__main__':
    one = DomainBaseModel()
    print(one)
    print(one.is_empty())
    print(DomainBaseModel.get_subclasses())
