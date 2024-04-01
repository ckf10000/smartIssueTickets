# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     desktop_services.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/03/21 11:10:58
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from time import sleep
from apps.infrastructure.api.crawlers import Selenium

from apps.common.libs.calc import calc_text_equation

class JinLvDesktopService(object):

    def __init__(self, home_page: str=None) -> None:
        self.__home_page = home_page or "https://pekdazhicheng.qlv88.com/Home/Login"
        self.selenium = Selenium()
        self.online_flag = False

    def get_login_username(self) -> str:
        try:
            return self.selenium.get_element_text(selector="xpath", regx="/html/body/div[1]/div[1]/div[4]/div[2]/span")
        except Exception as e:
            del e
            return ""
        
    def get_force_offline_alert_msg(self) -> str:
        """用户登录系统后，如果是已登录的用户，则会出现JS弹框，提示已登录的用户强制下线"""
        try:
            # alert_msg = self.selenium.get_element_text(selector="xpath", regx="/html/body/div[5]/a/cite")
            alert_msg = self.selenium.get_element_text(selector="xpath", regx="//a[@id='alertMsg_btnConfirm']/cite[text()='确 定']")
            return alert_msg
        except Exception as e:
            del e
            return ""

    def login(self, username: str, password: str, is_logout: bool = True) -> None:
        print("准备登录...")
        self.selenium.get(self.__home_page)
        # 设置最大尝试次数 5次
        for i in range(5):
            self.__login(username=username, password=password)
            sleep(5)
            # element_text = self.get_login_username()
            alert_msg = self.get_force_offline_alert_msg()
            print("************************************")
            # print(element_text)
            print(alert_msg)
            print("####################################")
            # if alert_msg == "确 定" or element_text == username:
            if alert_msg == "确 定":
                self.online_flag = True
                print("劲旅系统登录成功。")
                if alert_msg == "确 定":
                    # 判断如果有强制下线提示框，则需要消除提示框
                    # self.selenium.alert_accept()
                    self.selenium.submit_click(selector="xpath", regx="/html/body/div[5]/a/cite")
                break
            else:
                self.__retry_login()
        if is_logout is True:
            self.logout()

    def __login(self, username: str, password: str): 
        try:
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
        except Exception as e:
            print("登录劲旅系统失败，详细日志请关注下面异常...")
            print(e)

    def __retry_login(self) -> None:
        try:
            # 识别验证码
            ocr_result = self.selenium.get_code(selector="xpath", regx="/html/body/form/div/div[1]/div[3]/img")
            if ocr_result:
                ocr_result = calc_text_equation(text=ocr_result)
            # 输入验证码
            self.selenium.input_text(selector="xpath", regx="/html/body/form/div/div[1]/div[3]/input", value=ocr_result)
            # 点击登录
            self.selenium.submit_click(selector="xpath", regx="/html/body/form/div/div[2]/input")
        except Exception as e:
            print("登录劲旅系统失败，详细日志请关注下面异常...")
            print(e)

    def logout(self): 
        if self.online_flag is True:
            try:
                # 退出系统
                self.selenium.submit_click(selector="xpath", regx="/html/body/div[1]/div[1]/div[4]/div[1]/ul/li[4]/a")
                # 会弹出确认提示框，需要点击确认才能退出
                # self.selenium.alert_accept()
                self.selenium.submit_click(selector="xpath", regx="/html/body/div[5]/a[1]/cite")
                # self.selenium.submit_click(selector="xpath", regx="/html/body/div[6]/a[1]")
                sleep(3)
                print("劲旅系统退出成功。")
            except Exception as e:
                print("退出劲旅系统失败，详细日志请关注下面异常...")
                print(e)
        self.selenium.quit()

    def __switch_left_level_1_navigation(self, selector: str, regx: str) -> None:
        # 先判断左侧一级导航栏是否已展开，可以根据导航栏的背景颜色区分
        background_color = self.selenium.get_background_color(selector=selector, regx=regx)
        if background_color == "rgb(37, 110, 188)":  # 展开时的背景颜色
            print("导航栏已展开，无需切换。")
        else:
            print("导航栏还未展开，需要进行展开操作")
            self.selenium.submit_click(selector=selector, regx=str)

    def __switch_left_level_2_navigation(self, level_1_selector: str, level_1_regx: str, level_2_selector: str, level_2_regx: str) -> None:
        # 先切换一级导航栏
        self.__switch_left_level_1_navigation(selector=level_1_selector, regx=level_1_regx)
        sleep(1)
        # 再切换二级导航栏
        self.selenium.submit_click(selector=level_2_selector, regx=level_2_regx)
        sleep(3)

    # 国内未出票
    def show_internal_unissue_tickets(self) -> None:
        level_1_selector = level_2_selector = "xpath"
        level_1_regx = "/html/body/div[1]/div[2]/ul/li[5]/div/span"
        level_2_regx="/html/body/div[1]/div[2]/ul/li[5]/ul/li[12]/a"
        self.__switch_left_level_2_navigation(
            level_1_selector=level_1_selector, level_1_regx=level_1_regx, level_2_selector=level_2_selector, level_2_regx=level_2_regx
        )


if __name__ == "__main__":
    JimLv = JinLvDesktopService() 
    JimLv.login(username="周汗林", password="ca123456", is_logout=False)
    JimLv.show_internal_unissue_tickets()
