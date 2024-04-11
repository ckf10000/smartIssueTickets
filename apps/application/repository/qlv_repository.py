# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     qlv_repository.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/11 15:03:50
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import typing as t
from apps.common.libs.parse_yaml import DictObject
from apps.common.libs.service_environ import configuration
from apps.common.libs.date_extend import current_datetime_str


class QlvConfigRepository(object):
    qlv_config = getattr(configuration, "qlv")
    interfaces = getattr(qlv_config, "interfaces")

    @classmethod
    def get_request_base_params(cls, inter_name: str) -> t.Dict:
        lock_order_inter = getattr(cls.interfaces, inter_name)
        return {
            "path": getattr(lock_order_inter, "path"),
            "method": getattr(lock_order_inter, "method"),
            "user_key": getattr(cls.qlv_config, "user_key"),
            "user_id": getattr(cls.qlv_config, "user_id"),
        }

    @classmethod
    def get_lock_order_params(cls, lock_rule: str) -> DictObject:
        return getattr(getattr(cls.qlv_config, "lock_order_args"), lock_rule)

    @classmethod
    def get_host_params(cls) -> t.Dict:
        return dict(domain=getattr(cls.qlv_config, "domain"), protocol=getattr(cls.qlv_config, "protocol"))

    @classmethod
    def get_unlock_order_params(cls, **kwargs) -> t.Dict:
        return {
            "order_id": kwargs.get("order_id"),
            "oper": kwargs.get("oper"),
            "order_state": kwargs.get("order_state"),
            "order_lose_type": kwargs.get("order_lose_type"),
            "remark": kwargs.get("remark")
        }

    @ classmethod
    def get_unlock_reason_params(cls, flag: bool, order_id: int, oper: str, remark: str) -> t.Dict:
        """flag 为 true时，出票成功，反之出票失败"""
        return dict(
            order_id=order_id,
            oper=oper,
            order_state="1" if flag is True else "0",
            order_lose_type="解锁订单",
            remark=remark
        )

    @ classmethod
    def get_order_pay_info(cls, booking_info: t.Dict) -> t.Dict:
        return {
            "order_id": booking_info.get("pre_order_id"),
            "pay_time": current_datetime_str(),
            "out_pf": booking_info.get("out_pf"),
            "out_ticket_account": booking_info.get("out_ticket_account"),
            "pay_account_type": booking_info.get("pay_account_type"),
            "pay_account": booking_info.get("pay_account"),
            "money": booking_info.get("payment_amount"),
            "serial_number": booking_info.get("order_id"),
            "air_co_order_id": booking_info.get("order_id"),
            "pnames": booking_info.get("passenger"),
            "oper": booking_info.get("oper"),
            "remark": "{}-{}".format(booking_info.get("ctrip_username"), booking_info.get("user_pass")),
            "d_type": 1
        }

    @ classmethod
    def get_order_itinerary_info(cls, booking_info: t.Dict) -> t.Dict:
        card_id = booking_info.get("card_id")
        passenger = booking_info.get("passenger")
        arrive_city = booking_info.get("arrive_city")
        itinerary_id = booking_info.get("itinerary_id")
        departure_city = booking_info.get("departure_city")
        return {
            "order_id": booking_info.get("pre_order_id"),
            "oper": booking_info.get("oper"),
            "ticket_infos": "#".join([passenger, card_id, itinerary_id, departure_city, arrive_city])
        }
