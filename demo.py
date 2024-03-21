# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     demo.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/03/20 17:37:00
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import ddddocr
from time import sleep
from PIL import Image
from io import BytesIO
import os
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
# 超时的异常
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import ChromiumDriver
from selenium.webdriver.chromium.options import ChromiumOptions

from apps.common.libs.utils import get_project_path


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
    # 浏览器最大化
    chrome_options.add_argument('--start-maximized')
    # 指定浏览器分辨率
    chrome_options.add_argument('window-size=1920x1080')
    # 隐藏滚动条, 应对一些特殊页面
    # chrome_options.add_argument('--hide-scrollbars')
    # chrome_options.add_argument('--remote-debugging-port=9222')
    # 手动指定使用的浏览器位置，如果谷歌浏览器的安装目录配置在系统的path环境变量中，那么此处可以不传路径
    # chrome_options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    pre = dict()
    # 设置这两个参数就可以避免密码提示框的弹出
    pre["credentials_enable_service"] = False
    pre["profile.password_manager_enabled"] = False

    # 禁止加载图片
    # pre["profile.managed_default_content_settings.images"] = 2
    # 或者使用下面的设置, 提升速度
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_experimental_option("prefs", pre)
    # 关闭devtools工具
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
    return chrome_options

def get_proxy(desired_capabilities: dict)-> dict:
    if desired_capabilities:
        # 添加代理
        # 域\用户:密码@代理主机或者域名:端口号
        PROXY = r"CHINA\zwx400423:password123@172.16.30.161:8080"
        desired_capabilities['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,
            "noProxy": None,
            "proxyType": "MANUAL",
            "class": "org.openqa.selenium.Proxy",
            "autodetect": False
        }
    else:
        desired_capabilities = dict()
    return desired_capabilities

def get_webdriver() -> ChromiumDriver:
    # 指定chrome_driver路径
    # chrome_driver = r"F:\SoftwareDeveloper\Python\spiderStudyProject\driver\chromedriver.exe"
    # 指定chrome_driver记录的日志信息
    log_file = os.path.join(get_project_path(), "logs", "chrome.log")
    chrome_options = get_options()
    # desired_capabilities = get_proxy(desired_capabilities=chrome_options.to_capabilities())
    # 如果selenium的版本高于4.6，则不需要配置executable_path参数
    service = webdriver.ChromeService(
        # executable_path=chrome_driver
        service_args=['--log-level=DEBUG','--append-log', '--readable-timestamp'], log_output=log_file
    )
    # desired_capabilities = webdriver.DesiredCapabilities()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # driver = webdriver.Chrome(service=service)
    # with open(log_file, 'r') as f:
        # assert re.match(r"\[\d\d-\d\d-\d\d\d\d", f.read())
    # 无界面浏览器
    # driver  = webdriver.PhantomJS(executable_path=r"C:\Program Files (x86)\phantomjs-2.1.1\bin\phantomjs.exe")
    # 浏览器显示最大化
    driver.maximize_window()
    return driver

driver = get_webdriver()
wait = WebDriverWait(driver=driver, timeout=10)
url = "https://pekdazhicheng.qlv88.com/Home/Login"
print("开始登录：", url)
driver.get(url)

try:
    # 输入用户名
    # input_username = wait.until(
        # EC.presence_of_all_elements_located 参数为元组
        # EC.presence_of_element_located((By.XPATH, '/html/body/form/div/div[1]/div[1]/input[2]'))
    # )
    # input_username.send_keys(r'{}'.format("周汗林"))
    # 输入用户名
    # input_password = wait.until(
        # EC.presence_of_all_elements_located 参数为元组
        # EC.presence_of_element_located((By.XPATH, '/html/body/form/div/div[1]/div[2]/input'))
    # )
    # input_username.send_keys(r'{}'.format("ca123456"))
    driver.find_element(By.XPATH, '/html/body/form/div/div[1]/div[1]/input[2]').send_keys("周汗林")
    driver.find_element(By.XPATH, '/html/body/form/div/div[1]/div[2]/input').send_keys("ca123456")
    print("开始获取验证码...")
    captcha = driver.find_element(By.XPATH, '/html/body/form/div/div[1]/div[3]/img')
    code_image = Image.open(BytesIO(captcha.screenshot_as_png))
    #1.初始化一个实例，配置识别模式默认为OCR识别
    ocr = ddddocr.DdddOcr(show_ad=False)
    ocr_result = ocr.classification(code_image)
    print("识别到的验证码为：", ocr_result)
    driver.find_element(By.XPATH, '/html/body/form/div/div[1]/div[3]/input').send_keys(ocr_result)
    driver.find_element(By.XPATH, '/html/body/form/div/div[2]/input').click()
    sleep(5)
    driver.quit()
except TimeoutException:
    pprint("failed...")



