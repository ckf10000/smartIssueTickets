# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     robot_services.py
# Description:  场景机器人服务
# Author:       ckf10000
# CreateDate:   2024/04/10 21:08:58
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from apps.common.libs.parse_yaml import ProjectConfig
from apps.domain.services.qlv_request_services import OrderService


class CtripTicketService(object):
    qlv_config = ProjectConfig.get_object()
    interfaces = getattr(qlv_config, "interfaces")

    @classmethod
    def app_auto_out_ticket(cls) -> None:
        """
        携程app自动出票
        """
        lock_order_intf = getattr(cls.interfaces, "lock_order")
        kwargs = {
            "path": getattr(lock_order_intf, "path"),
            "method": getattr(lock_order_intf, "method"),
            "user_key": "9a68295ec90b1fc10ab94331c882bab9",
            "user_id": 186,
            "policy_name": "测试-XC",
            "oper": "robot-XC",
            "air_cos": "",
            "order_pk": "",
            "order_src_cat": "国内"
        }
        OrderService(domain=getattr(cls.qlv_config, "domain"), protocol=getattr(cls.qlv_config, "protocol")).lock_order(
            **kwargs)
