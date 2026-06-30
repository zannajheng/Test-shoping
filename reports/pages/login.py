from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os

# 优先使用本地 chromedriver（显式指定路径，跳过联网下载）
driver_path = r"D:\chrome-win64\chromedriver-win64\chromedriver.exe"

if os.path.exists(driver_path):
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
else:
    # 如果本地 driver 不存在，再退回 Selenium Manager 自动管理（需要能联网）
    driver = webdriver.Chrome()

# 打开了网页
driver.get("http://127.0.0.1:8000/")

#最大化
driver.maximize_window()

#保存快照
import time
time.sleep(3)
driver.save_screenshot("login.png")



#添加一行代码，仅仅为了让程序不结束
input()