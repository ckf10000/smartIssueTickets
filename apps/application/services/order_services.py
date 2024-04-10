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
from decimal import Decimal
from traceback import format_exc
from apps.common.libs.parse_yaml import ProjectConfig
from apps.common.annotation.log_service import logger
from apps.domain.services.qlv_request_services import OrderService
from apps.application.services.booking_services import booking_flight_ser

__all__ = ["out_ticket_ser"]


class QlvService(object):
    qlv_config = getattr(ProjectConfig.get_object(), "qlv")
    interfaces = getattr(qlv_config, "interfaces")

    @classmethod
    def get_lock_order(cls, lock_rule: str) -> t.Dict:
        lock_order_inter = getattr(cls.interfaces, "lock_order")
        kwargs = {
            "path": getattr(lock_order_inter, "path"),
            "method": getattr(lock_order_inter, "method"),
            "user_key": getattr(cls.qlv_config, "user_key"),
            "user_id": getattr(cls.qlv_config, "user_id"),
        }
        policy_args = getattr(getattr(cls.qlv_config, "lock_order_args"), lock_rule)
        kwargs.update(policy_args)
        order_ser = OrderService(domain=getattr(cls.qlv_config, "domain"), protocol=getattr(cls.qlv_config, "protocol"))
        result = order_ser.lock_order(**kwargs)
        return dict(
            policy_args=policy_args,
            data_info=result.get("DataInfoJson")
        ) if isinstance(result.get("DataInfoJson"), t.Dict) else dict()

    @classmethod
    def set_unlock_order(cls, order_id: int, oper: str, order_state: str, order_lose_type: str, remark: str) -> bool:
        lock_order_inter = getattr(cls.interfaces, "unlock_order")
        kwargs = {
            "path": getattr(lock_order_inter, "path"),
            "method": getattr(lock_order_inter, "method"),
            "user_key": getattr(cls.qlv_config, "user_key"),
            "user_id": getattr(cls.qlv_config, "user_id"),
            "order_id": order_id,
            "oper": oper,
            "order_state": order_state,
            "order_lose_type": order_lose_type,
            "remark": remark
        }
        order_ser = OrderService(domain=getattr(cls.qlv_config, "domain"), protocol=getattr(cls.qlv_config, "protocol"))
        result = order_ser.unlock_order(**kwargs)
        if result.get("code") == 1:
            return True
        else:
            return False


class CTripService(object):
    ctrip_config = getattr(ProjectConfig.get_object(), "ctrip")

    @classmethod
    def get_group_config(cls, group_name: str) -> t.Dict:
        group_config = getattr(cls.ctrip_config, group_name)
        return dict(
            ctrip_username=getattr(group_config, "account"),
            user_pass=getattr(group_config, "sec_key"),
            payment_pass=getattr(group_config, "pay_key"),
            internal_phone=getattr(group_config, "internal_phone")
        )

    @classmethod
    def booking_passenger_flight_ticket(cls, flight_info: t.Dict, passenger: t.Dict) -> t.Dict:
        flight_info["passenger"] = passenger.get("PName")
        flight_info["card_id"] = passenger.get("IDNo")
        flight_info["passenger_phone"] = passenger.get("Mobile")
        flight_info["age_stage"] = passenger.get("PType")
        flight_info["card_type"] = passenger.get("IDType")
        flight_info.update(cls.get_group_config("group_1"))
        return booking_flight_ser.booking_ctrip_app_special_flight_ticket(**flight_info)


class OutTicketService(object):

    @classmethod
    def xc_app_auto_out_ticket(cls, lock_rule: str) -> None:
        lock_order_info = QlvService.get_lock_order(lock_rule=lock_rule)
        # 说明单已锁定
        if lock_order_info:
            order_info = lock_order_info.get("data_info")
            policy_args = lock_order_info.get("policy_args")
            order_id = order_info.get("ID")
            flights = order_info.get("Flights")
            passengers = order_info.get("Peoples")
            if len(flights) > 1 or len(passengers) > 1:
                raise ValueError("当前不支持多航班或者多乘客下单...")
            logger.info("劲旅平台的订单<{}>已锁定，开启登录携程APP，进行下单操作...".format(order_id))
            try:
                flight_info = dict(
                    pre_order_id=order_id,
                    departure_time=flights[0].get("DatDep"),
                    departure_city=flights[0].get("CodeDep"),
                    departure_city_name=flights[0].get("CityDep"),
                    arrive_time=flights[0].get("DatArr"),
                    arrive_city=flights[0].get("CodeArr"),
                    arrive_city_name=flights[0].get("CityArr"),
                    flight=flights[0].get("FlightNo"),
                    pre_sale_amount=str(Decimal(flights[0].get("PriceStd")))
                )
                CTripService.booking_passenger_flight_ticket(flight_info=flight_info, passenger=passengers[0])

            except (Exception,):
                logger.error(format_exc())
                kwargs = dict(
                    order_id=lock_order_info.get("ID"),
                    oper=policy_args.get("oper"),
                    order_state="0",
                    order_lose_type="系统",
                    remark="机器人运行过程中出现异常"
                )
                # 尝试3次解锁
                for i in range(3):
                    is_succeed = QlvService.set_unlock_order(**kwargs)
                    if is_succeed is True:
                        break


out_ticket_ser = OutTicketService()
