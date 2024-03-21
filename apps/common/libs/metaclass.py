# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     metaclass.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/03/21 10:24:17
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import typing as t
from enum import Enum

class EnumMetaClass(Enum):

    @classmethod
    def values(cls) -> t.List:
        return [x.value for x in cls]

    @classmethod
    def keys(cls) -> t.List:
        return [x.name for x in cls]

    @classmethod
    def get(cls, key: str) -> t.Any:
        if key.upper() in cls.keys():
            return getattr(cls, key.upper()).value
        elif key.lower() in cls.keys():
            return getattr(cls, key.lower()).value
        else:
            return None

    @classmethod
    def items(cls) -> t.List:
        return [(x.name, x.value) for x in cls]