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

def test_get_crtip_flight_ticket_order():
    flight_ticket_order_ser.get_crtip_flight_ticket_order(
        departure_time="2024-04-13 09:15",
        flight="EU1805"
    )


if __name__ == "__main__":
    test_get_crtip_flight_ticket_order()
