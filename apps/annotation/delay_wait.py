# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     delay_wait.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/03/26 10:23:32
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from time import sleep
from typing import Any, Callable


class SleepWait(object):

    def __init__(self, wait_time: int = 1) -> None:
        self.wait_time = wait_time

    def __call__(self, func: Callable) -> Any:
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs) or None
            sleep(self.wait_time)
            return result

        return wrapper
