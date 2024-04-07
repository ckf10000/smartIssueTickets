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
        departure_time="2024-04-11 17:35",
        departure_city="NKG",
        departure_city_name="南京",
        arrive_time="2024-04-11 19:50",
        arrive_city="HZG",
        arrive_city_name="汉中",
        flight="UQ2542",
        passenger="邢诒森",
        card_id="460022194808080050",
        pre_sale_amount="412.00",
        # payment_pass="901127",
        payment_pass="901129",
        phone="18569520328",
        age_stage="成人",
        pre_order_id="2887983",
    )


if __name__ == "__main__":
    test_booking_ctrip_app_special_flight_ticket()
