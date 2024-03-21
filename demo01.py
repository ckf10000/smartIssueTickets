
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


driver = webdriver.Chrome()

driver.fullscreen_window()

wait = WebDriverWait(driver=driver, timeout=10)
try:
    driver.get("https://www.baidu.com")
except Exception as e:
    print(e)
driver.quit()