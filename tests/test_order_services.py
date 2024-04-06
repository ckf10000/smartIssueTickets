# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     test_order_services.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/05 20:25:15
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from apps.application.services.order_services import flight_ticket_order_ser

def test_get_crtip_pending_trip_order():
    flight_ticket_order_ser.get_crtip_pending_trip_order(
        departure_time="2024-04-08 19:20",
        flight="G54489"
    )


if __name__ == "__main__":
    test_get_crtip_pending_trip_order()
