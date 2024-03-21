# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     desk_form_services.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/03/21 11:10:58
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from selenium.webdriver.support.ui import WebDriverWait
from apps.infrastructure.api.crawlers import SeleniumFactory

class JinLvDeskService(object):

    def __init__(self, home_page: str=None) -> None:
        self.__home_page = home_page or "https://pekdazhicheng.qlv88.com/Home/Login"
        self.selenium = SeleniumFactory()

    def Login(self, username: str, password: str): 
        try:
            WebDriverWait(driver=self.driver, timeout=10)
            self.selenium.get(self.__home_page)
            self.selenium.input_text(selector="xpath", regx="/html/body/form/div/div[1]/div[1]/input[2]", value=username)
            self.selenium.input_text(selector="xpath", regx="/html/body/form/div/div[1]/div[2]/input", value=password)
            self.selenium.input_code(selector="xpath", regx="/html/body/form/div/div[1]/div[3]/img")
            self.selenium.submit_click(selector="xpath", regx="/html/body/form/div/div[2]/input")
        except Exception as e:
            print("登录劲旅系统失败，原因：", str(e))
            self.selenium.quit()


    def Logout(): pass


if __name__ == "__main__":
    JinLvDeskService().Login()