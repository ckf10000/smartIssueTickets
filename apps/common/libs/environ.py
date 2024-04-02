# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     environ.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/02 14:41:40
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import os

__all__ = ["get_env"]

ENV_TYPE = ["production", "development", "sit", "pre", "uat"]
DEFAULT_ENV_TYPE = "development"

def get_env():
    # 操作系统需配置环境变量：ENV_TYPE，否则视为 development 环境
    env_type = os.getenv("ENV_TYPE")
    if not env_type:
        env_type = DEFAULT_ENV_TYPE
    return env_type
