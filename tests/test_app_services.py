# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     test_app_services.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/01 11:14:51
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from apps.domain.services.ui.app_services import CtripAppService

def test_select_special_flight():
    app = CtripAppService()
    app.start()
    app.select_special_flight(flight="MF8266")

def test_select_insecure():
    app = CtripAppService()
    app.start()
    app.select_insecure()


def test_get_tickect_actual_amount():
    app = CtripAppService()
    app.start()
    app.get_tickect_actual_amount()


def test_get_tickect_deduction_amount():
    app = CtripAppService()
    app.start()
    app.get_tickect_deduction_amount()

def test_get_pending_trip_order():
    app = CtripAppService()
    app.start()
    app.get_pending_trip_order()

def test_close_important_trip_guidelines():
    app = CtripAppService()
    app.start()
    app.close_important_trip_guidelines()

def test_get_flight_ticket_with_order_id():
    app = CtripAppService()
    app.start()
    print(app.get_flight_ticket_with_order_id())

def test_get_flight_ticket_with_itinerary_id():
    app = CtripAppService()
    app.start()
    print(app.get_flight_ticket_with_itinerary_id())

def test_select_more_payment():
    app = CtripAppService()
    app.start()
    app.select_more_payment()

def test_enter_payment_pass():
    app = CtripAppService()
    app.start()
    app.enter_payment_pass(payment_pass="0123456789")

def test_select_search_result_first_city():
    app = CtripAppService()
    app.start()
    app.select_search_result_first_city(select_value="PEK")

def test_check_user_login():
    app = CtripAppService()
    app.start()
    app.check_user_login(username="18600440822", password="ca161022")

def test_close_coupon_dialog():
    app = CtripAppService()
    app.start()
    app.close_coupon_dialog()

def test_expand_order_detail():
    app = CtripAppService()
    app.start()
    app.expand_order_detail()

def test_touch_order_detail():
    app = CtripAppService()
    app.start()
    app.touch_order_detail()

if __name__ == "__main__":
    # test_select_special_flight()
    # test_select_insecure()  
    # test_get_tickect_actual_amount()
    # test_get_tickect_deduction_amount()
    # test_get_pending_trip_order()
    # test_close_important_trip_guidelines()    
    # test_get_flight_ticket_with_order_id()
    # test_get_flight_ticket_with_itinerary_id()
    # test_select_more_payment()
    # test_enter_payment_pass()
    # test_select_search_result_first_city()
    # test_check_user_login()
    # test_close_coupon_dialog()
    # test_expand_order_detail()
    test_touch_order_detail()
