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
from apps.domain.services.app_ui_services import CtripAppService

__all__ = ["flight_ticket_order_ser"]

class FlightTicketOrderService(object):

    @classmethod
    def get_crtip_pending_trip_order(cls) -> t.Dict:
        """获取携程未出行订单"""
        logger.info("开始获取携程未出行的订单.")
        app = CtripAppService()
        app.device.wake()
        app.restart()
        time.sleep(8)
        app.touch_my()
        app.touch_pending_trip_order()
        app.get_pending_trip_order()

flight_ticket_order_ser = FlightTicketOrderService()
