# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     order_services.py
# Description:  订单服务
# Author:       ckf10000
# CreateDate:   2024/03/23 13:09:38
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
class PhoneOrderService(object):

    @classmethod
    def booking_ctrip_flight_order(cls, package: str =None) -> str:
         if package is None:
              package = "ctrip.android.view"
         start_app(package)
