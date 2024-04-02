# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     order_services_test.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/01 10:11:15
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from apps.application.services.order_services import PhoneOrderService


def test_booking_ctrip_special_flight_ticket():
    PhoneOrderService.booking_ctrip_special_flight_ticket(
        departure_time="2024-04-07 12:10",
        flight="MF8358",
        departure_city="WUH",
        arrive_city="XMN",
        passenger="罗杨",
        age_stage="成人",
        card_id="420684198710130016",
        phone="18569520328",
        lowest_price=647.00,
        payment_pass="901127",
    )

if __name__ == "__main__":
    test_booking_ctrip_special_flight_ticket()
