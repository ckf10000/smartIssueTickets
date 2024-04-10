# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     out_ticket_services.py
# Description:  场景机器人服务
# Author:       ckf10000
# CreateDate:   2024/04/10 21:08:58
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from copy import deepcopy
from apps.common.libs.parse_yaml import ProjectConfig
from apps.domain.services.qlv_request_services import OrderService


class CTripTicketService(object):
    qlv_config = getattr(ProjectConfig.get_object(), "qlv")
    interfaces = getattr(qlv_config, "interfaces")

    @classmethod
    def app_auto_out_ticket(cls) -> None:
        """
        携程app自动出票
        """
        lock_order_inter = getattr(cls.interfaces, "lock_order")
        kwargs = {
            "path": getattr(lock_order_inter, "path"),
            "method": getattr(lock_order_inter, "method"),
            "user_key": getattr(cls.qlv_config, "user_key"),
            "user_id": getattr(cls.qlv_config, "user_id"),
        }
        lock_order_args_list = getattr(cls.qlv_config, "lock_order_args")
        order_ser = OrderService(domain=getattr(cls.qlv_config, "domain"), protocol=getattr(cls.qlv_config, "protocol"))

        for lock_order_args in lock_order_args_list:
            kwargs_local = deepcopy(kwargs)
            kwargs_local.update(lock_order_args)
            result = order_ser.lock_order(**kwargs_local)
            print(result)
