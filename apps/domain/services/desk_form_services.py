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
from apps.infrastructure.api.crawlers import Selenium
from apps.infrastructure.api.browsers import ChromeBrowser, FirefoxBrowser

class JinLvDeskService(object):

    def __init__(self, home_page: str=None) -> None:
        self.__home_page = home_page or "https://pekdazhicheng.qlv88.com/Home/Login"
        self.selenium = Selenium()

    def login(self, username: str, password: str, is_logout: bool = True) -> None:
        # 设置最大尝试次数
        max_attempts = 3
        for i in range(3):
            self.__login(username=username, password=password)
            element_text = self.selenium.get_element_text(selector="xpath", regx="/html/body/div[1]/div[1]/div[4]/div[2]/span")
            if element_text == username:
                break
            else:
                self.__login(username=username, password=password)
        if is_logout is True:
            self.logout()
            self.selenium.quit()

    def __login(self, username: str, password: str): 
        try:
            print("准备登录...")
            self.selenium.get(self.__home_page)
            # 输入用户名
            self.selenium.input_text(selector="xpath", regx="/html/body/form/div/div[1]/div[1]/input[2]", value=username)
            # 输入密码
            self.selenium.input_text(selector="xpath", regx="/html/body/form/div/div[1]/div[2]/input", value=password)
            # 识别验证码
            ocr_result = self.selenium.get_code(selector="xpath", regx="/html/body/form/div/div[1]/div[3]/img")
            # 输入验证码
            self.selenium.input_text(selector="xpath", regx="/html/body/form/div/div[1]/div[3]/input", value=ocr_result)
            # 点击登录
            self.selenium.submit_click(selector="xpath", regx="/html/body/form/div/div[2]/input")
            print("劲旅系统登录成功。")
            # 判断如果有强制下线提示框，则需要消除提示框
            self.selenium.alert_accept()
        except Exception as e:
            print("登录劲旅系统失败，详细日志请关注下面异常...")
            print(e)

    def logout(self): 
        try:
            # 退出系统
            self.selenium.submit_click(selector="xpath", regx="/html/body/div[1]/div[1]/div[4]/div[1]/ul/li[4]/a")
        except Exception as e:
            print("退出劲旅系统失败，详细日志请关注下面异常...")
            print(e)
            self.selenium.quit()


if __name__ == "__main__":
    JinLvDeskService().login(username="周汗林", password="ca123456")