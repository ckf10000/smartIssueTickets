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
        ac="鹰联航空",
        departure_time="2024-04-04 21:45",
        flight="EU1854",
        departure_city="NNG",
        arrive_city="CSX",
        passenger="吴盼盼",
        age_stage="成人",
        card_id="450802200509094326",
        phone="18569520328",
        lowest_price=200.00,
        payment_pass="901127",
    )

if __name__ == "__main__":
    test_booking_ctrip_special_flight_ticket()
