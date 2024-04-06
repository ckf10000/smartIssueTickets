# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     test_middlewares.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/07 01:58:40
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from apps.infrastructure.middleware.mq import push_message_to_mq

def test_push_message_to_mq():
    message = dict(code=200, message="这是第一个消息", data=dict())
    push_message_to_mq(message=message)


if __name__ == "__main__":
    test_push_message_to_mq()
