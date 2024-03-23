# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     andriods.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/03/23 13:56:52
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from apps.domain.services.platforms import PlatformService

class CtripAppService(PlatformService):
    """
    携程APP
    """
    def __init__(self, device_config: dict = None) -> None:
        super().__init__(device_config)
    