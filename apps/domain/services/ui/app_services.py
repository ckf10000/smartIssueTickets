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


class CtripAppService(PlatformService):
    """
    携程APP
    """

    def __init__(self) -> None:
        self.device = PlatformService().device
        
    def touch_home(self) -> None:
        """进入app后，点击【首页】"""
        
    def touch_my(self) -> None:
        """进入app后，点击【我的】"""
        
    def touch_flight_ticket(self) -> None:
        """进入app后，点击【首页】，点击【机票】"""
        
    def get_flights(self, from_city: str, arrive_city: str, date: str) -> DataFrame:
        """查询航班"""
        pass
    
    def get_order(self, order_id: str) -> t.Dict:
        """查询订单"""
        pass
    
    def add_passenger(self, username: str, card_num: str, phone_num: str) -> None:
        """添加乘客/旅客"""
        pass