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
        departure_time="2024-04-07 22:35",
        flight="UQ3558",
        departure_city="CKG",
        arrive_city="ZHA",
        passenger="何斯蕙",
        age_stage="成人",
        card_id="440902199406301247",
        phone="18569520328",
        lowest_price=480.00,
        payment_pass="901127",
    )

if __name__ == "__main__":
    test_booking_ctrip_special_flight_ticket()
