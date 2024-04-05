# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     order_services.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/05 20:13:32
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import time
import typing as t
from apps.common.annotation.log_service import logger
from apps.domain.services.ui.app_services import CtripAppService

__all__ = ["flight_ticket_order_ser"]

class FlightTicketOrderService(object):

    @classmethod
    def get_crtip_flight_ticket_order(cls, departure_time: str,  flight: str) -> t.Dict:
        """根据起飞时间，航班获取携程机票订单"""
        logger.info("本次要查询的航班为：{}，起飞时间在: {}".format(flight, departure_time))
        app = CtripAppService()
        app.device.wake()
        app.restart()
        time.sleep(8)
        app.touch_my()

flight_ticket_order_ser = FlightTicketOrderService()
