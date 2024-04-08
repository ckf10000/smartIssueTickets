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
        departure_time="2024-04-12 18:45",
        departure_city="XNN",
        departure_city_name="西宁",
        arrive_time="2024-04-12 21:15",
        arrive_city="CSX",
        arrive_city_name="长沙",
        flight="A67254",
        passenger="舒钦",
        card_id="431281200002111617",
        pre_sale_amount="640.00",
        payment_pass="901127",
        # payment_pass="901129",
        phone="18569520328",
        age_stage="成人",
        pre_order_id="2888452"
    )


if __name__ == "__main__":
    test_booking_ctrip_app_special_flight_ticket()
