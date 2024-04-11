# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     message_services.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/11 10:26:48
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import typing as t
from apps.common.annotation.log_service import logger
from apps.infrastructure.middleware.mq import push_message_to_mq


class MQMessageService(object):

    @classmethod
    def push_flight_ticket_order(cls, message: t.Dict) -> None:
        logger.info("开始往MQ推送携程机票订单信息：<{}>".format(message))
        push_message_to_mq(message=message)
