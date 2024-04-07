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
        departure_time="2024-04-22 12:30",
        departure_city="LZO",
        departure_city_name="泸州",
        arrive_time="2024-04-22 14:55",
        arrive_city="TNA",
        arrive_city_name="济南",
        flight="8L9649",
        passenger="蒲湘岚",
        card_id="510502200206277045",
        pre_sale_amount="420.00",
        # payment_pass="901127",
        payment_pass="901129",
        phone="18569520328",
        age_stage="成人",
        pre_order_id="2890007"
    )


if __name__ == "__main__":
    test_booking_ctrip_app_special_flight_ticket()
