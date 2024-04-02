# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     booking_bluesprints.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/03 01:54:20
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from flask import Blueprint
from apps.common.http.restfulApi import api_factory, anonymous_namespace_prefix
from apps.application.controllers.booking_controllers import BookingCtripAppSpecialFlightController

booking_blue_name = "booking"
booking_bp = Blueprint(booking_blue_name, __name__)

# 后端调用需要token认证，前端调用需要session认证，none为不加前缀，不认证，anonymous为不认证
booking_none_api = api_factory(blueprint=booking_bp, prefix=anonymous_namespace_prefix)

# 携程APP特价机票预订
booking_none_api.add_resource(BookingCtripAppSpecialFlightController, '/ctrip/specialFlight', 
                              endpoint='BookingCtripAppSpecialFlightController')
