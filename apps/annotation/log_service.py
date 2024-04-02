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
