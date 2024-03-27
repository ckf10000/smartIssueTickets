# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     order_services.py
# Description:  订单服务
# Author:       ckf10000
# CreateDate:   2024/03/23 13:09:38
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from time import sleep
from apps.domain.services.ui.app_services import CtripAppService

class PhoneOrderService(object):

    @classmethod
    def booking_ctrip_special_flight_ticket(cls, departure_city: str, arrive_city: str, departure_time: str, ac: str, lowest_price: float) -> None:
        app = CtripAppService()
        app.device.wake()
        sleep(8)
        app.touch_home()
        app.touch_flight_ticket()
        app.touch_special_flight_ticket()
        app.select_departure_city()
        app.enter_search_value(search_value=departure_city)
        app.select_search_result_first_city()
        app.sumbit_search_result()
        app.select_arrive_city()
        app.enter_search_value(search_value=arrive_city)
        app.select_search_result_first_city()
        app.sumbit_search_result()
        app.select_trip_date()
        app.select_trip_expect_month(date_str=departure_time)
        app.select_trip_expect_day(date_str=departure_time)
        app.touch_only_query_some_day()
        app.touch_query_special()
        app.touch_flight_inland_single_list_filter()
        app.touch_filter_departure_time()
        app.select_filter_departure_time_area(date_str=departure_time)
        app.touch_filter_airline()
        app.select_filter_airline_company(ac)
        app.touch_filter_submit_button()
        print(lowest_price)

if __name__ == "__main__":
    PhoneOrderService.booking_ctrip_special_flight_ticket(
        departure_city="HET", arrive_city="HLH", departure_time="2024-04-04 13:00", ac="华夏航空",
        lowest_price=300.00
     )
