# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     test_app_services.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/01 11:14:51
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from apps.domain.services.ui.app_services import CtripAppService

def test_select_special_flight():
    app = CtripAppService()
    app.start()
    app.select_special_flight(flight="MF8266")


if __name__ == "__main__":
    test_select_special_flight()
