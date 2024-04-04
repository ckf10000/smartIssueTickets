# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     maintain_controllers.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/03 02:04:00
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from apps.common.annotation.log_service import logger
from apps.application.services.maintain_services import main_ser
from apps.common.libs.base_controller import BaseArgumentController


class HealthStatusController(BaseArgumentController):

    def get(self):
        """
        服务健康状态
        """
        # 获取传输的值/strict=True代表设置如果传以上未指定的参数主动报错
        kwargs = self.parse.parse_args(strict=True)
        kwargs.clear()
        result = main_ser.test_service_status()
        logger.info(self.logger_formatter + " 成功...")
        return result, 200


class UrlMapController(BaseArgumentController):

    def get(self):
        """
        当前服务所有的url摘要信息
        """
        # 获取传输的值/strict=True代表设置如果传以上未指定的参数主动报错
        kwargs = self.parse.parse_args(strict=True)
        kwargs.clear()
        result = main_ser.get_instances_brief()
        logger.info(self.logger_formatter + " 成功...")
        return result, 200


class UrlsController(BaseArgumentController):

    def get(self):
        """
        当前服务所有的url
        """
        # 获取传输的值/strict=True代表设置如果传以上未指定的参数主动报错
        kwargs = self.parse.parse_args(strict=True)
        kwargs.clear()
        result = main_ser.get_urls()
        logger.info(self.logger_formatter + " 成功...")
        return result, 200
