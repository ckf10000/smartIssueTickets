# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     robot.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/10
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from time import sleep
from datetime import datetime
from traceback import print_exc
from apps.common.annotation.log_service import logger
from apps.application.services.order_services import out_ticket_ser


def xc_app_auto_out_ticket() -> None:
    while True:
        dt_start = datetime.now()
        try:
            out_ticket_ser.xc_app_auto_out_ticket(lock_rule="xc")
            dt_complete = datetime.now()
            st = dt_complete - dt_start
            # 空闲或者异常时平均间隔1分钟(60秒)``
            delta = 60 - st.total_seconds()
            if delta > 0:
                sleep(delta)
        except Exception as e:
            logger.error(str(e))
            logger.error(print_exc())
            dt_complete = datetime.now()
            # 空闲或者异常时平均间隔1分钟(60秒)
            delta = 60 - st.total_seconds()
            if delta > 0:
                sleep(delta)


if __name__ == "__main__":
    xc_app_auto_out_ticket()
