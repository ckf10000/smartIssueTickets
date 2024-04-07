# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     platforms.py
# Description:  所支持的平台
# Author:       ckf10000
# CreateDate:   2024/03/23 17:39:39
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from apps.common.config.device import default_andriod_device, default_minicap_device
from apps.infrastructure.api.mobile_terminals import Phone, DEFAULT_PLATFORM, WINDOWS_PLATFORM

class PlatformService(object):

    def __init__(self, device_config: dict = None) -> None:
        # 暂时支持Android和Windows平台
        self.device_config = device_config or default_andriod_device
        if self.device_config.get("platform") == DEFAULT_PLATFORM:
            self.device = Phone(
                device_id=self.device_config.get("device_id"),
                device_conn=self.device_config.get("device_conn"),
                platform=self.device_config.get("platform"),
                enable_debug=self.device_config.get("enable_debug")
            )
        elif self.device_config.get("platform") == WINDOWS_PLATFORM:
            pass
        else:
            raise ValueError("The platform configuration only supports Andriod and Windows.")

    @classmethod
    def minicap_device(cls, device_config: dict = None) -> Phone:
        config = device_config or default_minicap_device
        return Phone(
            device_id=config.get("device_id"),
            device_conn=config.get("device_conn"),
            platform=config.get("platform"),
            enable_debug=config.get("enable_debug"),
        )
