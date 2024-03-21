# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     selectorVO.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/03/21 10:20:32
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from selenium.webdriver.common.by import By
from apps.common.libs.metaclass import EnumMetaClass

class Selector(EnumMetaClass):

    id = By.ID
    name = By.NAME
    xpath = By.XPATH
    tag_name = By.TAG_NAME
    link_text = By.LINK_TEXT
    class_name = By.CLASS_NAME
    css_selector = By.CSS_SELECTOR
    partial_link_text = By.PARTIAL_LINK_TEXT