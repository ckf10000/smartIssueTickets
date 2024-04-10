# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     booking_services.py
# Description:  预订服务
# Author:       ckf10000
# CreateDate:   2024/03/23 13:09:38
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import time
import typing as t
from decimal import Decimal
from apps.common.annotation.log_service import logger
from apps.common.config.flight_ticket import airline_map
from apps.common.annotation.asynchronous import async_threading
from apps.domain.services.app_ui_services import CtripAppService
from apps.application.validators.booking_validators import FlightTicketValidator

__all__ = ["booking_flight_ser"]


class BookingFlightService(object):

    @classmethod
    def booking_ctrip_app_special_flight_ticket(
            cls,
            pre_order_id: str,  # 预售订单id
            departure_city: str,  # 离开城市编号
            arrive_city: str,  # 抵达城市编号
            departure_time: str,  # 起飞时间
            arrive_time: str,  # 抵达时间
            pre_sale_amount: str,  # 预售金额
            flight: str,  # 航班编号
            passenger: str,  # 乘客
            age_stage: str,  # 乘客年龄阶段，儿童/成人
            card_id: str,  # 身份证号
            internal_phone: str,  # 内部手机号码
            payment_pass: str,  # 支付密码
            ctrip_username: str,  # 携程账号
            user_pass: str,  # 携程账号密码
            departure_city_name: str = "",  # 离开城市名
            arrive_city_name: str = "",  # 抵达城市名
            passenger_phone: str = ""  # 乘客手机号码
    ) -> t.Dict:
        result = dict()
        ac = airline_map.get(flight[:2].upper())
        logger.info("本次要预定的航班：{}，为<{}>的航班，起飞时间为：{}".format(flight, ac, departure_time))
        app = CtripAppService()
        app.device.wake()
        app.restart()
        time.sleep(8)
        app.touch_home()
        app.touch_flight_ticket()
        app.touch_special_flight_ticket()
        app.select_departure_city()
        app.enter_search_value(search_value=departure_city)
        app.select_search_result_first_city(select_value=departure_city)
        app.sumbit_search_result()
        app.select_arrive_city()
        app.enter_search_value(search_value=arrive_city)
        app.select_search_result_first_city(select_value=arrive_city)
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
        special_flight_amount = app.get_special_flight_amount()
        if special_flight_amount <= Decimal(pre_sale_amount):
            is_direct_booking = app.is_direct_booking()
            if is_direct_booking is True:
                app.touch_direct_booking_button()
            else:
                app.touch_booking_the_second_button()
                app.touch_ordinary_booking_button()
            app.check_user_login(username=ctrip_username, password=user_pass)
            app.touch_more_passengers_button()
            app.touch_add_passengers_button()
            app.enter_passenger_username(passenger=passenger)
            app.enter_passenger_card_id(card_id=card_id)
            app.enter_passenger_phone_number(phone=internal_phone)
            app.submit_passenger_info()
            app.submit_passenger_info_confirm()
            app.add_passenger(passenger=passenger)
            app.select_insecure()
            app.touch_fill_order_next_step()
            is_duplicate_order = app.is_duplicate_order()
            if is_duplicate_order:
                logger.warning(is_duplicate_order)
            else:
                app.touch_select_service_no_need()  # 保障不需要
                app.touch_select_service_no_need()  # 预约不需要
                app.touch_to_payment()
                app.touch_insure_no()
                app.touch_read_agree()
                app.touch_payment_method()
                app.select_payment_method(payment_method="浦发银行储蓄卡(7397)")
                app.select_more_payment()
                app.select_point_deduction()
                tickect_actual_amount = app.get_tickect_actual_amount()
                tickect_deduction_amount = app.get_tickect_deduction_amount()
                do_validator = FlightTicketValidator.validator_payment_with_deduction(
                    pre_sale_amount=Decimal(pre_sale_amount),
                    actual_amount=tickect_actual_amount,
                    deduction_amount=tickect_deduction_amount,
                )
                if do_validator is True:
                    app.touch_bank_card_payment()
                    app.enter_payment_pass(payment_pass=payment_pass)
                    payment_amount = app.get_order_with_payment_amount()
                    payment_method = app.get_order_with_payment_method()
                    app.touch_payment_complete()
                    app.close_coupon_dialog()
                    app.expand_order_detail()
                    app.touch_order_detail()
                    app.close_important_trip_guidelines()
                    order_id = app.get_flight_ticket_with_order_id()
                    itinerary_id = app.get_flight_ticket_with_itinerary_id()
                    result = dict(
                        pre_order_id=pre_order_id,
                        departure_city=departure_city,
                        arrive_city=arrive_city,
                        departure_time=departure_time,
                        pre_sale_amount=pre_sale_amount,
                        flight=flight,
                        passenger=passenger,
                        age_stage=age_stage,
                        card_id=card_id,
                        internal_phone=internal_phone,
                        passenger_phone=passenger_phone,
                        order_id=order_id,
                        payment_amount=str(payment_amount),
                        payment_method=payment_method,
                        itinerary_id=itinerary_id,
                        departure_city_name=departure_city_name,
                        arrive_city_name=arrive_city_name,
                        arrive_time=arrive_time,
                        ctrip_username=ctrip_username
                    )
                    app.push_flight_ticket_order(message=result)
        else:
            logger.warning(
                "当前查询最低票价为：{}，高于航班订单票价：{}，本次预定即将结束。".format(
                    special_flight_amount, pre_sale_amount
                )
            )
        return result

    @classmethod
    @async_threading
    def asymc_booking_ctrip_app_special_flight_ticket(cls, **kwargs) -> None:
        cls.booking_ctrip_app_special_flight_ticket(**kwargs)


booking_flight_ser = BookingFlightService()
