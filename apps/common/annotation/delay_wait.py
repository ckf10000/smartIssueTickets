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
from poco.exceptions import PocoNoSuchNodeException
from apps.common.annotation.log_service import logger


class SleepWait(object):

    def __init__(self, wait_time: int = 1) -> None:
        self.wait_time = wait_time

    def __call__(self, func: Callable) -> Any:
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs) or None
            sleep(self.wait_time)
            return result

        return wrapper
    
class LoopFindElement(object):

    def __init__(self, loop: int = 1) -> None:
        self.loop = loop

    def __call__(self, func: Callable) -> Any:
        def wrapper(*args, **kwargs):
            result = None
            for i in range(self.loop):
                # 1秒钟查找一次
                sleep(1)
                try:
                    result = func(*args, **kwargs) or None
                    break
                except PocoNoSuchNodeException as e:
                    logger.error("第{}次查找失败，失败原因：{}".format(i, str(e)))
            return result

        return wrapper
