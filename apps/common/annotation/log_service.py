# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     log_service.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/02 14:46:04
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import traceback
import logging.config
from functools import wraps
import airtest.utils.logger as __logger__

from apps.common.libs.parse_yaml import ProjectConfig

logging_plus = getattr(ProjectConfig.get_object(), "logging")
logging.config.dictConfig(logging_plus)
logger = logging.getLogger("root")

def auto_log(func):
    """
    自动打印日志
    :param func:
    :return:
    """

    @wraps(func)
    def _deco(*args, **kwargs):
        try:
            real_func = func(*args, **kwargs)
            return real_func
        except Exception as e:
            logger.error(traceback.format_exc())
            raise Exception(e)
        
    return _deco


# 源码中的logger配置，写死为debug级别，需要重置源码配置，让配置文件接管，
def init_logging():
    # logger = logging.root
    # use 'airtest' as root logger name to prevent changing other modules' logger
    logger = logging.getLogger("airtest")
    # logger.setLevel(logging.INFO)
    # handler = logging.StreamHandler()
    # formatter = logging.Formatter(fmt='[%(asctime)s][%(levelname)s]<%(name)s> %(message)s', datefmt='%H:%M:%S')
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)

__logger__.init_logging = init_logging
__logger__.init_logging()
