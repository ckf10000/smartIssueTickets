# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     robot.py.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/10
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from time import sleep
from traceback import print_exc
from apps.common.annotation.log_service import logger
from apps.application.services.out_ticket_services import CTripTicketService


def xc_app_out_ticket() -> None:
    while True:
        try:
            CTripTicketService.app_auto_out_ticket()
            sleep(10)  # 休眠10秒
        except (Exception,):
            logger.error(print_exc())


if __name__ == "__main__":
    xc_app_out_ticket()
