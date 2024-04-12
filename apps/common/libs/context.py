# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     context.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/02 14:47:23
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from typing import Any
from flask import current_app


def is_current_app() -> Any:
    try:
        with current_app.app_context():
            return True
    except RuntimeError:
        return False
