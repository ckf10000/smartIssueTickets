# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     app_services.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/03/23 23:19:20
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import typing as t
from pandas import DataFrame
from apps.infrastructure.api.platforms import PlatformService

from apps.common.libs.dir import get_images_dir, is_exists, join_path


class CtripAppService(PlatformService):
    """
    携程APP
    """
    APP_NAME = "ctrip.android.view"
    IMAGE_DIR = get_images_dir()

    def __init__(self, device=None, app_name: str=None) -> None:
        self.device = device or PlatformService().device
        self.device.start_app(app_name or self.APP_NAME)
        
    def touch_home(self) -> None:
        """进入app后，点击【首页】"""
        file_name = join_path([get_images_dir(), "首页.png"])
        if is_exists(file_name):
            temp = self.device.get_cv_template(file_name=file_name)
        else:
            temp = (154, 2878) # LG g7手机上对应的坐标位置，其他型号手机可能不是这个值
        self.device.touch(temp)

    def touch_flight_ticket(self) -> None:
        """进入app后，点击【首页】，点击【机票】"""
        
    def touch_my(self) -> None:
        """进入app后，点击【我的】"""
        
    def get_flights(self, from_city: str, arrive_city: str, date: str) -> DataFrame:
        """查询航班"""
        pass
    
    def get_order(self, order_id: str) -> t.Dict:
        """查询订单"""
        pass
    
    def add_passenger(self, username: str, card_num: str, phone_num: str) -> None:
        """添加乘客/旅客"""
        pass

    def __del__(self) -> None:
        self.device.stop_app(app_name=self.APP_NAME)

if __name__ == "__main__":
    c = CtripAppService()
    c.touch_home()