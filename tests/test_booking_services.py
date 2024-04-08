# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     test_booking_services.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/01 10:11:15
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from apps.application.services.booking_services import booking_flight_ser


def test_booking_ctrip_app_special_flight_ticket():
    booking_flight_ser.booking_ctrip_app_special_flight_ticket(
        departure_time="2024-04-13 21:50",
        departure_city="NKG",
        departure_city_name="南京",
        arrive_time="2024-04-13 23:30",
        arrive_city="CSX",
        arrive_city_name="长沙",
        flight="MF8036",
        passenger="李成浩",
        card_id="321284199803018015",
        pre_sale_amount="240.00",
        payment_pass="901127",
        phone="18569520328",
        age_stage="成人",
        pre_order_id="2891160"
    )


if __name__ == "__main__":
    test_booking_ctrip_app_special_flight_ticket()
