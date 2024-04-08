# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     mq.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/05 04:30:35
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import typing as t
from rabbitmq_plus.base.producer import Producer

from apps.common.annotation.log_service import logger
from apps.common.config.parameters import rabbitmq_default_config as cfg

def push_message_to_mq(message: t.Any) -> None:
    producer = Producer(**cfg)
    producer.publish(message=message)
    logger.info("消息已发送至MQ队列.")
