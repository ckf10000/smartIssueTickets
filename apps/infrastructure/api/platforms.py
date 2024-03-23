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
from apps.infrastructure.api.mobile_terminals import Phone, DEFAULT_PLATFORM, WINDOWS_PLATFORM

class PlatformService(object):
    
    def __init__(self, device_config: dict = None) -> None:
        # 暂时支持Android和Windows平台
        self.device_config = device_config or self.get_default_andriod_device()
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
    
    @staticmethod
    def get_default_andriod_device() -> dict:
        # 公司LG G7手机
        return {
            "device_id": "LMG710N248c5b73",
            "device_conn": "android://127.0.0.1:5037/LMG710N248c5b73?cap_method=JAVACAP&touch_method=MAXTOUCH&",
            "platform": DEFAULT_PLATFORM,
            "enable_debug": True
        }

