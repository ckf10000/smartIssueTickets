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
import ddddocr
from PIL import Image
from io import BytesIO
from traceback import format_exc
# expected_conditions 类负责条件
from selenium.webdriver.support import expected_conditions as ec

from apps.common.libs.selector import Selector
from apps.common.annotation.log_service import logger
from apps.infrastructure.api.desktop_browsers import FirefoxBrowser


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
            input_1 = self.wait.until(
                # EC.presence_of_all_elements_located 参数为元组
                ec.presence_of_element_located((Selector.get(selector), regx))
            )
            # 判断输入框是否有数据
            if input_1.get_attribute("value"):
                # 清除输入框数据
                input_1.clear()
            input_1.send_keys('{}'.format(value))
            # self.browser.find_element(Selector.get(selector), regx).send_keys(value)
        except Exception as e:
            logger.error(format_exc())
            err_str = "通过选择器：{}，表达式: {}，捕获输入框设置文本<{}>失败，error：{}".format(selector, regx, value, e)
            raise AttributeError(err_str)

    def submit_click(self, selector: str, regx: str) -> None:
        """
        selector 选择器
        regx 选择器所要匹配的表达式
        value 文本框输入值
        """
        try:
            submit = self.wait.until(
                ec.element_to_be_clickable((Selector.get(selector), regx))
            )
            submit.click()
            # self.browser.find_element(Selector.get(selector), regx).click()
        except Exception as e:
            logger.error(format_exc())
            err_str = "通过选择器：{}，表达式: {}，捕获点击对象并点击失败，error：{}".format(selector, regx, e)
            raise AttributeError(err_str)

    def get_code(self, selector: str, regx: str) -> str:
        logger.info("开始获取验证码...")
        try:
            selector = Selector.get(selector)
            captcha = self.browser.find_element(Selector.get(selector), regx)
            code_image = Image.open(BytesIO(captcha.screenshot_as_png))
            # 1.初始化一个实例，配置识别模式默认为OCR识别
            ocr = ddddocr.DdddOcr(show_ad=False)
            ocr_result = ocr.classification(code_image)
            logger.info("识别到的验证码为：", ocr_result)
            return ocr_result
        except Exception as e:
            logger.error(format_exc())
            err_str = "通过选择器：{}，表达式: {}，识别验证码失败，error：{}".format(selector, regx, e)
            raise AttributeError(err_str)

    def alert_accept(self) -> None:
        # 等待弹框出现
        try:
            alert = self.wait.until(ec.alert_is_present())
            logger.info("弹框已出现")
            # 处理弹框，点击确定按钮
            alert.accept()
        except (Exception,):
            logger.warning("未出现弹框，无需处理。")

    def get_element_text(self, selector: str, regx: str) -> str:
        try:
            # 根据实际情况定位按钮元素
            element = self.browser.find_element(Selector.get(selector), regx)
            # 获取按钮元素的文本信息
            element_text = element.text.strip() if isinstance(element.text, str) else ""
            logger.info("获取元素的文字信息为:", element_text)
            return element_text
        except Exception as e:
            logger.error(format_exc())
            err_str = "通过选择器：{}，表达式: {}，获取元素文本信息失败，error：{}".format(selector, regx, e)
            raise AttributeError(err_str)

    def get_background_color(self, selector: str, regx: str) -> str:
        try:
            # 根据实际情况定位按钮元素
            element = self.browser.find_element(Selector.get(selector), regx)
            # 获取选项的背景颜色
            background_color = element.value_of_css_property("background-color")
            return background_color.strip() if isinstance(background_color, str) else ""
        except Exception as e:
            logger.error(format_exc())
            err_str = "通过选择器：{}，表达式: {}，获取背景颜色失败，error：{}".format(selector, regx, e)
            raise AttributeError(err_str)

    def quit(self) -> None:
        self.browser.quit()

    def get(self, url: str) -> None:
        self.browser.get(url)


if __name__ == "__main__":
    s = Selenium()
    s.get("https://www.baidu.com")
    s.quit()
