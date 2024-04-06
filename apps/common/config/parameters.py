# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     parameters.py
# Description:  各类中间件的连接参数
# Author:       ckf10000
# CreateDate:   2024/04/07 01:36:20
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""

rabbitmq_default_config = {
    "port": 5672,
    "app_id": "smartIssueTickets",
    "host": "192.168.3.232",
    "username": "ticket",
    "password": "Admin@123",
    "virtual_host": "smartIssueTickets",
    # "queue": "order.flight.ctrip",
    "exchange": "amq.fanout",
    "exchange_type": "fanout",
    "routing_key": ''
}
