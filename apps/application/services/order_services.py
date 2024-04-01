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
        departure_city: str,  # 离开城市
        arrive_city: str,  # 抵达城市
        departure_time: str,  # 起飞时间
        ac: str,  # 航司
        lowest_price: float,  # 最低票价
        flight: str,  # 航班编号
        passenger: str,  # 乘客
        age_stage: str,  # 乘客年龄阶段，儿童/成人
        card_id: str,  # 身份证号
        phone: str,  # 手机号码
        payment_pass: str,
    ) -> None:
        app = CtripAppService()
        app.device.wake()
        app.restart()
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
        is_exist_flight = app.is_exist_flight_in_screen(flight=flight)
        if is_exist_flight is False:
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
            is_direct_booking = app.is_direct_booking()
            if is_direct_booking is True:
                app.touch_direct_booking_button()
            else:
                app.touch_booking_the_second_button()
                app.touch_ordinary_booking_button()
            app.touch_more_passengers_button()
            app.touch_add_passengers_button()
            app.enter_passenger_username(passenger=passenger)
            app.enter_passenger_card_id(card_id=card_id)
            app.enter_passenger_phone_number(phone=phone)
            app.submit_passenger_info()
            app.submit_passenger_info_confirm()
            app.add_passenger(passenger=passenger)
            app.select_insecure()
            app.touch_fill_order_next_step()
            is_duplicate_order = app.is_duplicate_order()
            if is_duplicate_order:
                print(is_duplicate_order)
            else:
                app.touch_select_service_no_need()  # 保障不需要
                app.touch_select_service_no_need()  # 预约不需要
                app.touch_to_payment()
                app.touch_insure_no()
                app.touch_read_agree()
                app.select_more_payment()
                app.select_point_deduction()
                app.touch_bank_card_payment()
                app.enter_payment_pass(payment_pass=payment_pass)
        else:
            print(
                "当前查询最低票价为：{}，高于航班订单票价：{}，本次预定即将结束。".format(
                    special_flight_price, lowest_price
                )
            )
