# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     crawlers.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/03/21 09:39:32
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import os
import ddddocr
from PIL import Image
from io import BytesIO
from traceback import format_exc
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
# expected_conditions 类负责条件
from selenium.webdriver.support import expected_conditions as EC

from apps.common.libs.selector import Selector
from apps.infrastructure.api.browsers import ChromeBrowser, FirefoxBrowser

class Selenium(object):

    def __init__(self) -> None:
        # self.browser = ChromeBrowser.get_browser()
        self.browser, self.wait, self.browser_name = FirefoxBrowser.get_browser()
    
    def input_text(self, selector: str, regx: str, value: str) -> None:
        """
        selector 选择器
        regx 选择器所要匹配的表达式
        value 文本框输入值
        """
        try:
            input = self.wait.until(
                # EC.presence_of_all_elements_located 参数为元组
                EC.presence_of_element_located((Selector.get(selector), regx))
            )
            input.send_keys('{}'.format(value))
            # self.browser.find_element(Selector.get(selector), regx).send_keys(value)
        except Exception as e:
            print(format_exc())
            err_str = "通过选择器：{}，捕获输入框设置文本<{}>失败，error：{}".format(selector, value, e)
            raise AttributeError(err_str)
        
    def submit_click(self, selector: str, regx: str) -> None:
        """
        selector 选择器
        regx 选择器所要匹配的表达式
        value 文本框输入值
        """
        try:
            submit = self.wait.until(
                EC.element_to_be_clickable((Selector.get(selector), regx))
            )
            submit.click()
            # self.browser.find_element(Selector.get(selector), regx).click()
        except Exception as e:
            print(format_exc())
            err_str = "通过选择器：{}，捕获按钮并提交失败，error：{}".format(selector, e)
            raise AttributeError(err_str)
 
    def get_code(self, selector: str, regx: str) -> str:
        print("开始获取验证码...")
        try:
            selector = Selector.get(selector)
            captcha = self.browser.find_element(selector, regx)
            code_image = Image.open(BytesIO(captcha.screenshot_as_png))
            #1.初始化一个实例，配置识别模式默认为OCR识别
            ocr = ddddocr.DdddOcr(show_ad=False)
            ocr_result = ocr.classification(code_image)
            print("识别到的验证码为：", ocr_result)
            return ocr_result
        except Exception as e:
            print(format_exc())
            err_str = "通过选择器：{}，识别验证码失败，error：{}".format(selector, e)
            raise AttributeError(err_str)
    
    def alert_accept(self) -> None:
        # 等待弹框出现
        try:
            alert = self.wait.until(EC.alert_is_present())
            print("弹框已出现")
            # 处理弹框，点击确定按钮
            alert.accept()
        except Exception as e:
            del e
            print("未出现弹框，无需处理。")

    def get_element_text(self, selector: str, regx: str) -> str:
        try:
            # 根据实际情况定位按钮元素
            element = self.browser.find_element(selector, regx)
            # 获取按钮元素的文本信息
            element_text = element.text.strip()
            print("获取元素的文字信息为:", element_text)
            return element_text
        except Exception as e:
            print(format_exc())
            err_str = "通过选择器：{}，识别验证码失败，error：{}".format(selector, e)
            raise AttributeError(err_str)
    
    def quit(self) -> None:
        self.browser.quit()

    def get(self, url: str) -> None:
        print(url)
        self.browser.get(url)


if __name__ == "__main__":
    s = Selenium()
    s.get("https://www.baidu.com")
    s.quit()