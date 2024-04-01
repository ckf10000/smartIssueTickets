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


if __name__ == "__main__":
    PhoneOrderService.booking_ctrip_special_flight_ticket(
            departure_city="CGQ", arrive_city="XUZ", departure_time="2024-04-04 19:35", ac="长龙航空", flight="GJ8060",
            lowest_price=495.00, passenger="刘铁", age_stage="成人", card_id="220221199005106811", phone="18569520328", 
            payment_pass="901127"
        )
