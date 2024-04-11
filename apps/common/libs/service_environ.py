# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     service_environ.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/02 15:25:15
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import os
from flask import current_app

from apps.common.libs.environ import get_env
from apps.common.libs.dir import get_project_path
from apps.common.libs.context import is_current_app
from apps.common.libs.parse_yaml import ProjectConfig

__all__ = ["config", "configuration", "BaseConfig"]


class BaseConfig(object):
    """
    环境基类
    """
    # 获取项目根目录
    PROJECT_HOME = get_project_path()
    STATIC_PATH = os.path.join(PROJECT_HOME, "static")
    TEMPLATE_PATH = os.path.join(PROJECT_HOME, "templates")

    def __init__(self, env_type: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 获取项目根目录
        self.env_type = env_type
        self.CONFIG = ProjectConfig.get_object(env_type=self.env_type)


class DevelopmentConfig(BaseConfig):
    """
    开发环境
    """

    def __init__(self, env, *args, **kwargs):
        super().__init__(env, *args, **kwargs)

        # 是否开启Debug模式
        self.DEBUG = False


class SitConfig(BaseConfig):
    """
    集成环境
    """

    def __init__(self, env, *args, **kwargs):
        super().__init__(env, *args, **kwargs)

        # 是否开启Debug模式
        self.DEBUG = False


class UatConfig(BaseConfig):
    """
    用户验收环境
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 是否开启Debug模式
        self.DEBUG = False


class PreConfig(BaseConfig):
    """
    预发环境
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 是否开启Debug模式
        self.DEBUG = False


class ProductionConfig(BaseConfig):
    """
    生产环境
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 是否开启Debug模式
        self.DEBUG = False


config = {
    "development": DevelopmentConfig("development"),
    "production": ProductionConfig("production"),
    "sit": SitConfig("sit"),
    "uat": UatConfig("uat"),
    "pre": PreConfig("pre"),
}

if is_current_app():
    configuration = current_app.config["CONFIG"]
else:
    configuration = config[get_env()].CONFIG
