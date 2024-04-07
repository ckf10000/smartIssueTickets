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
        departure_time="2024-04-11 15:15",
        departure_city="CAN",
        departure_city_name="广州",
        arrive_time="2024-04-11 18:15",
        arrive_city="PEK",
        arrive_city_name="北京",
        flight="HU7810",
        passenger="王世芳",
        card_id="110105196503082125",
        pre_sale_amount="716.00",
        # payment_pass="901127",
        payment_pass="901129",
        phone="18569520328",
        age_stage="成人",
        pre_order_id="2885807",
    )


if __name__ == "__main__":
    test_booking_ctrip_app_special_flight_ticket()
