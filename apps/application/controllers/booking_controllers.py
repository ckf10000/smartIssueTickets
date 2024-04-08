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
from apps.common.annotation.log_service import logger
from apps.common.libs.base_controller import BaseArgumentController
from apps.application.services.booking_services import booking_flight_ser


class BookingCtripAppSpecialFlightController(BaseArgumentController):
    """携程特价机票预订"""

    def post(self):
        # location表示获取args中的关键字段进行校验，required表示必填不传报错，type表示字段类型
        self.parse.add_argument("pre_order_id", type=str, help="预售单参数<pre_order_id>校验错误",required=True, 
                                location='json', trim=True)
        self.parse.add_argument("departure_time", type=str, help="起飞时间参数<departure_time>校验错误，参数格式为：2024-04-07 12:10",required=True, 
                                location='json', trim=True)
        self.parse.add_argument("arrive_time", type=str, help="抵达时间参数<arrive_time>校验错误，参数格式为：2024-04-07 12:10",required=True, 
                                location='json', trim=True)
        self.parse.add_argument("flight", type=str, help="航班参数<flight>校验错误", required=True, location='json', trim=True)
        self.parse.add_argument("departure_city", type=str, help="起飞城市代号参数<departure_city>校验错误", required=True, 
                                location='json', trim=True)
        self.parse.add_argument("departure_city_name", type=str, help="起飞城市名参数<departure_city_name>校验错误", required=False, 
                                location='json', trim=True)
        self.parse.add_argument("arrive_city", type=str, help="抵达城市代号参数<arrive_city>校验错误", required=True, 
                                location='json', trim=True)
        self.parse.add_argument("arrive_city_name", type=str, help="抵达城市名参数<arrive_city_name>校验错误", required=False, 
                                location='json', trim=True)
        self.parse.add_argument("passenger", type=str, help="乘机人参数<passenger>校验错误", required=True, 
                                location='json', trim=True)
        self.parse.add_argument("age_stage", type=str, help="乘机人年龄阶段参数<age_stage>校验错误，只能是成人、儿童", required=True, 
                                location='json', trim=True, choices=["成人", "儿童"])
        self.parse.add_argument("card_id", type=str, help="身份证号参数<card_id>校验错误", required=True, 
                                location='json', trim=True)
        self.parse.add_argument("internal_phone", type=str, help="内部手机号参数<internal_phone>校验错误", required=True, 
                                location='json', trim=True)
        self.parse.add_argument("passenger_phone", type=str, help="乘客手机号参数<passenger_phone>校验错误", required=False, 
                                location='json', trim=True)
        self.parse.add_argument("pre_sale_amount", type=float, help="预售金额参数<pre_sale_amount>校验错误", required=True, 
                                location='json', trim=True)
        self.parse.add_argument("payment_pass", type=str, help="支付密码参数<payment_pass>校验错误", required=True, 
                                location='json', trim=True)
        self.parse.add_argument("ctrip_username", type=str, help="携程用户参数<ctrip_username>校验错误", required=True, 
                                location='json', trim=True)
        self.parse.add_argument("user_pass", type=str, help="用户密码参数<user_pass>校验错误", required=True, 
                                location='json', trim=True)
        # 获取传输的值/strict=True代表设置如果传以上未指定的参数主动报错
        kwargs = self.parse.parse_args(strict=True)
        booking_flight_ser.asymc_booking_ctrip_app_special_flight_ticket(**kwargs)
        logger.info(self.logger_formatter + " 成功...")
        return dict(code=200, message="执行成功", data=None), 200
