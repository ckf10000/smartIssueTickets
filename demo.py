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
from pprint import pprint
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from zhixing import get_webdriver


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



