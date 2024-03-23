# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     browsers.py
# Description:  浏览器驱动
# Author:       ckf10000
# CreateDate:   2024/03/21 15:14:01
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import os
import typing as t
from selenium import webdriver
from abc import abstractclassmethod
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from apps.common.libs.utils import get_project_path

class Browser(object):
    TIMEOUT = 10
    LOG_LEVEL = "DEBUG"
    BROWSER_NAME = None
    PROECT_PATH = get_project_path()

    @abstractclassmethod
    def get_browser(): pass

    @abstractclassmethod
    def get_options(): pass

    @abstractclassmethod
    def get_service(): pass


class ChromeBrowser(Browser):
    BROWSER_NAME = "Chrome"

    @staticmethod
    def get_options() -> ChromiumOptions:
        # 支持的浏览器有: Firefox, Chrome, Ie, Edge, Opera, Safari, BlackBerry, Android, PhantomJS等
        chrome_options = webdriver.ChromeOptions()
        # 谷歌浏览器后台运行模式
        # chrome_options.add_argument('--headless')
        # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--disable-gpu')
        # 隐身模式（无痕模式）
        chrome_options.add_argument('--incognito')
        # 隐藏"Chrome正在受到自动软件的控制"
        # chrome_options.add_argument('disable-infobars')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 设置中文
        chrome_options.add_argument('lang=zh_CN.UTF-8')
        # 指定浏览器分辨率
        # chrome_options.add_argument('window-size=1920x1080')
        # 浏览器最大化
        chrome_options.add_argument('--start-maximized')
        # 隐藏滚动条, 应对一些特殊页面
        # chrome_options.add_argument('--hide-scrollbars')
        # chrome_options.add_argument('--remote-debugging-port=9222')
        # 手动指定使用的浏览器位置，如果谷歌浏览器的安装目录配置在系统的path环境变量中，那么此处可以不传路径
        chrome_options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

        pre = dict()
        # 设置这两个参数就可以避免密码提示框的弹出
        pre["credentials_enable_service"] = False
        pre["profile.password_manager_enabled"] = False

        # 禁止加载图片
        # pre["profile.managed_default_content_settings.images"] = 2
        # 或者使用下面的设置, 提升速度
        # chrome_options.add_argument('blink-settings=imagesEnabled=false')
        chrome_options.add_experimental_option("prefs", pre)
        # 关闭devtools工具
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        return chrome_options
    
    @staticmethod
    def get_proxy(proxy_url: str = None)-> dict:
        if proxy_url:
            # 添加代理
            # 域\用户:密码@代理主机或者域名:端口号
            # proxy_url = r"CHINA\zwx400423:password123@172.16.30.161:8080"
            desired_capabilities['proxy'] = {
                "httpProxy": proxy_url,
                "ftpProxy": proxy_url,
                "sslProxy": proxy_url,
                "noProxy": None,
                "proxyType": "MANUAL",
                "class": "org.openqa.selenium.Proxy",
                "autodetect": False
            }
        else:
            desired_capabilities = dict()
        return desired_capabilities

    @classmethod
    def get_service(cls) -> ChromeService:
        # 指定chrome_driver路径
        # chrome_driver = r"C:\Python\spiderStudyProject\driver\chromedriver.exe"
        # 指定chrome_driver记录的日志信息
        log_file = os.path.join(cls.PROECT_PATH, "logs", "chrome.log")
        # 如果selenium的版本高于4.6，则不需要配置executable_path参数
        service = ChromeService(
            # executable_path=chrome_driver,
            service_args=['--log-level={}'.format(cls.LOG_LEVEL),'--append-log', '--readable-timestamp'], 
            log_output=log_file
        )
        return service

    @classmethod
    def get_browser(cls) -> t.Tuple: 
        options = cls.get_options()
        service = cls.get_service()
        browser = Chrome(service=service, options=options)
        wait = WebDriverWait(driver=browser, timeout=cls.TIMEOUT)
        return browser, wait, cls.BROWSER_NAME
    

class FirefoxBrowser(Browser):
    BROWSER_NAME = "FireFfox"

    @staticmethod
    def get_options() -> FirefoxOptions:
        options = FirefoxOptions()
        # 在无头模式下运行 Firefox
        # options.headless = True  
        # 设置代理
        # options.add_argument('--proxy-server=http://proxy.example.com:8080') 
        options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        return options
    
    @classmethod
    def get_service(cls) -> FirefoxService:
        # geckodriver 驱动路径
        # gecko_driver_path = '/path/to/geckodriver'
        # 指定gecko_driver记录的日志信息
        log_file = os.path.join(cls.PROECT_PATH, "logs", "firefox.log")
        # 如果selenium的版本高于4.6，则不需要配置executable_path参数
        service = FirefoxService(
            # executable_path=gecko_driver_path,
            service_args=['--log={}'.format(cls.LOG_LEVEL.lower())], 
            log_output=log_file
        )
        return service

    @classmethod
    def get_browser(cls) -> t.Tuple: 
        options = cls.get_options()
        service = cls.get_service()
        browser = Firefox(service=service, options=options)
        wait = WebDriverWait(driver=browser, timeout=cls.TIMEOUT)
        return browser, wait, cls.BROWSER_NAME