# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     booking_controllers.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/02 11:52:39
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import asyncio
from apps.common.libs.base_controller import BaseArgumentController
from apps.application.services.booking_services import booking_flight_ser


class BookingCtripAppSpecialFlightController(BaseArgumentController):
    """携程特价机票预订"""

    async def post(self):
        # location表示获取args中的关键字段进行校验，required表示必填不传报错，type表示字段类型
        self.parse.add_argument("departure_time", type=str, help="起飞时间参数<departure_time>校验错误，参数格式为：2024-04-07 12:10",required=True, 
                                location='json', trim=True)
        self.parse.add_argument("flight", type=str, help="航班参数<flight>校验错误", required=True, location='json', trim=True)
        self.parse.add_argument("departure_city", type=str, help="起飞城市代号参数<departure_city>校验错误", required=True, 
                                location='json', trim=True)
        self.parse.add_argument("arrive_city", type=str, help="抵达城市参数<arrive_city>校验错误", required=True, 
                                location='json', trim=True)
        self.parse.add_argument("passenger", type=str, help="乘机人参数<passenger>校验错误", required=True, 
                                location='json', trim=True)
        self.parse.add_argument("age_stage", type=str, help="乘机人年龄阶段参数<age_stage>校验错误，只能是成人、儿童", required=True, 
                                location='json', trim=True, choices=["成人", "儿童"])
        self.parse.add_argument("card_id", type=str, help="身份证号参数<card_id>校验错误", required=True, 
                                location='json', trim=True)
        self.parse.add_argument("phone", type=str, help="手机号参数<phone>校验错误", required=True, 
                                location='json', trim=True, default="18569520328")
        self.parse.add_argument("lowest_price", type=float, help="最低售价参数<lowest_price>校验错误", required=True, 
                                location='json', trim=True)
        self.parse.add_argument("payment_pass", type=str, help="支付密码参数<payment_pass>校验错误", required=True, 
                                location='json', trim=True)
        # 获取传输的值/strict=True代表设置如果传以上未指定的参数主动报错
        kwargs = self.parse.parse_args(strict=True)
        asyncio.create_task(booking_flight_ser.booking_ctrip_app_special_flight_ticket(**kwargs)) 
        return dict(code=200, message="执行成功", data=None), 200
