# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     exception.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/03/23 14:32:50
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import traceback
from functools import wraps
from airtest.core.error import *



def airtest_exception_format(func):
    """
    airtest测试框架异常捕获格式化
    :param func:
    :return:
    """

    @wraps(func)
    def _deco(*args, **kwargs):
        try:
            result = func(*args, **kwargs) or None
        except (AdbError, AdbShellError) as e:
            result = (e.stdout + e.stderr).decode()
        except AirtestError as e:
            result = e
        return result

    return _deco
