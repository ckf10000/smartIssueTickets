# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     order_services.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/05 20:13:32
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import typing as t
from traceback import format_exc

from apps.common.annotation.log_service import logger
from apps.domain.services.message_services import MQMessageService
from apps.domain.services.qlv_request_services import OrderService
from apps.application.services.booking_services import booking_flight_ser
from apps.application.repository.qlv_repository import QlvConfigRepository
from apps.application.repository.ctrip_repository import CTripConfigRepository
from apps.application.converter.qlv_converter import QlvRequestParamsConverter

__all__ = ["out_ticket_ser"]


class QlvService(object):

    @classmethod
    def get_lock_order(cls, lock_rule: str) -> t.Dict:
        logger.info("根据政策匹配，开始获取劲旅系统被锁定的订单...")
        kwargs = QlvConfigRepository.get_request_base_params(
            inter_name="lock_order")
        policy_args = QlvConfigRepository.get_lock_order_params(
            lock_rule=lock_rule)
        kwargs.update(policy_args)
        order_ser = OrderService(**QlvConfigRepository.get_host_params())
        result = order_ser.lock_order(**kwargs)
        result["policy_args"] = policy_args
        result["data_info"] = result.pop("datainfojson", None)
        return result

    @classmethod
    def set_unlock_order(cls, order_id: int, oper: str, order_state: str, order_lose_type: str, remark: str) -> bool:
        logger.info("出票{}，开始解锁劲旅平台订单<{}>".format(
            "成功" if order_state == "1" else "失败", order_id))
        kwargs = QlvConfigRepository.get_request_base_params(
            inter_name="unlock_order")
        unlock_order_params = QlvConfigRepository.get_unlock_order_params(
            order_id=order_id, oper=oper, order_state=order_state, order_lose_type=order_lose_type, remark=remark)
        kwargs.update(unlock_order_params)
        order_ser = OrderService(**QlvConfigRepository.get_host_params())
        result = order_ser.unlock_order(**kwargs)
        if result.get("code") == 1:
            return True
        else:
            logger.error("劲旅平台订单<{}>解锁失败...".format(order_id))
            return False

    @classmethod
    def unlock_reason_with_flag(cls, flag: bool, order_id: int, oper: str) -> bool:
        unlock_reason_params = QlvConfigRepository.get_unlock_reason_params(
            flag=flag, order_id=order_id, oper=oper)
        return cls.set_unlock_order(**unlock_reason_params)

    @classmethod
    def loop_unlock_reason_with_flag(cls,  flag: bool, order_id: int, oper: str, attempts: int = 3):
        # 尝试3次解锁
        for i in range(attempts):
            is_succeed = QlvService.set_unlock_order(
                flag=flag, order_id=order_id, oper=oper)
            if is_succeed is True:
                break

    @classmethod
    def save_pay_info(cls, booking_info: t.Dict) -> None:
        logger.info("开始向劲旅系统回填采购信息...")
        kwargs = QlvConfigRepository.get_request_base_params(
            inter_name="save_order_pay_info")
        order_pay_info = QlvConfigRepository.get_order_pay_info(
            booking_info=booking_info)
        kwargs.update(order_pay_info)
        order_ser = OrderService(**QlvConfigRepository.get_host_params())
        result = order_ser.save_order_pay_info(**kwargs)
        if result.get("code") == 0:
            logger.error("向劲旅系统回填采购信息失败...")

    @classmethod
    def save_itinerary_info(cls, booking_info: t.Dict) -> None:
        logger.info("开始向劲旅系统回填乘客票单信息...")
        if booking_info.get("itinerary_id"):
            kwargs = QlvConfigRepository.get_request_base_params(
                inter_name="fill_order_itinerary_info")
            order_itinerary_info = QlvConfigRepository.get_order_itinerary_info(
                booking_info=booking_info)
            kwargs.update(order_itinerary_info)
            order_ser = OrderService(**QlvConfigRepository.get_host_params())
            result = order_ser.fill_order_itinerary_info(**kwargs)
            if result.get("code") == 0:
                logger.error("向劲旅系统回填乘客票单信息失败...")
        else:
            logger.warning("劲旅平台订单<{}>预计还在出票中，暂时需要人工回填乘客的票单信息...".format(
                booking_info.get("pre_order_id")))


class CTripService(object):

    @classmethod
    def booking_passenger_flight_ticket(cls, flight_info: t.Dict, passenger: t.Dict) -> t.Dict:
        passenger_info = CTripConfigRepository.get_passenger_info(
            qlv_passengers=passenger)
        flight_info.update(passenger_info)
        flight_info["payment_method"], payment_config = CTripConfigRepository.get_payment_group_config(
            group_name="group_1")
        ctrip_group_config = CTripConfigRepository.get_ctrip_group_config(
            group_name="group_1")
        flight_info.update(ctrip_group_config)
        booking_info = booking_flight_ser.booking_ctrip_app_special_flight_ticket(
            **flight_info)
        # 有预订信息，说明订票成功
        if booking_info:
            booking_info["user_pass"] = ctrip_group_config.get("user_pass")
            booking_info.update(payment_config)
        return booking_info


class OutTicketService(object):

    @classmethod
    def xc_app_auto_out_ticket(cls, lock_rule: str) -> None:
        # 1. 锁单
        lock_order_info = QlvService.get_lock_order(lock_rule=lock_rule)
        # 说明单已锁定，往下执行，如果未锁定，直接跳过
        if isinstance(lock_order_info.get("data_info"), dict):
            order_info = lock_order_info.get("data_info")
            oper = lock_order_info.get("policy_args").get("oper")
            order_id = order_info.get("ID")
            flights = order_info.get("Flights")
            passengers = order_info.get("Peoples")
            if len(flights) > 1 or len(passengers) > 1:
                logger.warning("当前不支持多航班或者多乘客下单...")
                QlvService.loop_unlock_reason_with_flag(
                    flag=False, order_id=order_id, oper=oper)
            else:
                logger.info(
                    "劲旅平台的订单<{}>已锁定，开启登录携程APP，进行下单操作...".format(order_id))
                try:
                    flight_info = QlvRequestParamsConverter.covert_flight_info(
                        order_id=order_id, flights=flights[0])
                    # 2. 携程app下单
                    booking_info = CTripService.booking_passenger_flight_ticket(
                        flight_info=flight_info, passenger=passengers[0])
                    if booking_info:
                        booking_info.update(dict(oper=oper))
                        logger.info(
                            "开始往MQ推送携程机票订单信息：<{}>".format(booking_info))
                        MQMessageService.push_flight_ticket_order(
                            message=booking_info)
                        # 3. 回填采购信息与票号
                        QlvService.save_pay_info(booking_info=booking_info)
                        QlvService.save_itinerary_info(
                            booking_info=booking_info)
                        # 4. 给订单解锁
                        QlvService.loop_unlock_reason_with_flag(
                            flag=True, order_id=order_id, oper=oper)
                    else:
                        QlvService.loop_unlock_reason_with_flag(
                            flag=False, order_id=order_id, oper=oper)
                except (Exception,):
                    logger.error(format_exc())
                    QlvService.loop_unlock_reason_with_flag(
                        flag=False, order_id=order_id, oper=oper)
        else:
            logger.error(lock_order_info.get("message"))


out_ticket_ser = OutTicketService()
