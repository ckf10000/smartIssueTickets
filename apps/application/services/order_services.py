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
    def booking_ctrip_special_flight_ticket(
        cls,
        departure_city: str,
        arrive_city: str,
        departure_time: str,
        ac: str,
        lowest_price: float,
        flight: str,
        passenger: str,
        age_stage: str,
        card_id: str,
        phone: str
    ) -> None:
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
        app.touch_clear_filter()
        app.touch_filter_departure_time()
        app.select_filter_departure_time_area(date_str=departure_time)
        app.touch_filter_airline()
        app.select_filter_airline_company(ac)
        app.touch_filter_submit_button()
        app.select_special_flight(flight=flight)
        special_flight_price = app.get_special_flight_price()
        if special_flight_price <= lowest_price:
            app.touch_booking_the_second_button()
            app.touch_ordinary_booking_button()
            app.touch_more_passengers_button()
            app.touch_add_passengers_button()
            app.enter_passenger_username(passenger=passenger)
            app.enter_passenger_card_id(card_id=card_id)
            app.enter_passenger_phone_number(phone=phone)
            app.submit_passenger_info()
        else:
            print("当前查询最低票价为：{}，高于航班订单票价：{}，本次预定即将结束。".format(special_flight_price, lowest_price))
        


if __name__ == "__main__":
    PhoneOrderService.booking_ctrip_special_flight_ticket(
        departure_city="HGH", arrive_city="SZX", departure_time="2024-04-04 06:50", ac="厦门航空", flight="MF8383",
        lowest_price=940.00, passenger="徐佳伟", age_stage="成人", card_id="372301198901170336", phone="13861300264", 
     )
