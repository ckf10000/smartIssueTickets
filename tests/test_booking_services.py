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
        arrive_city="CTU",
        card_id="412924196807203155",
        departure_city="SZX",
        departure_time="2024-04-09 11:35",
        flight="EU2218",
        pre_sale_amount=600.00,
        passenger="曹文全",
        payment_pass="901127",
        phone="18569520328",
        age_stage="成人",
        pre_order_id="2885578",
    )


if __name__ == "__main__":
    test_booking_ctrip_app_special_flight_ticket()
