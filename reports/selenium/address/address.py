# 收货地址页 Selenium 自动化测试脚本
# 覆盖接口：
#   #30 /user/address/  GET  收货地址页

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time

USERNAME = "zhengziyi"
PASSWORD = "11111111"
VERIFY_CODE = "1234"
BASE_URL = "http://127.0.0.1:8000/"
LOGIN_URL = BASE_URL + "user/login/"
CENTER_URL = BASE_URL + "user/center/"
ADDRESS_URL = BASE_URL + "user/address/"

driver_path = r"D:\chrome-win64\chromedriver-win64\chromedriver.exe"
if os.path.exists(driver_path):
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
else:
    fallback_path = r"C:\Users\Zanna\.cache\selenium\chromedriver\win64\149.0.7827.155\chromedriver.exe"
    if os.path.exists(fallback_path):
        service = Service(executable_path=fallback_path)
        driver = webdriver.Chrome(service=service)
    else:
        driver = webdriver.Chrome()

wait = WebDriverWait(driver, 10, 0.5)
passed = 0
total = 0


def mark(name, ok, info=""):
    global passed, total
    total += 1
    if ok:
        passed += 1
        print(f"  [PASS] {name}  {info}")
    else:
        print(f"  [FAIL] {name}  {info}")


def do_login():
    driver.get(LOGIN_URL)
    driver.maximize_window()
    wait.until(EC.presence_of_element_located((By.ID, "login_user")))
    driver.find_element(By.ID, "login_user").clear()
    driver.find_element(By.ID, "login_user").send_keys(USERNAME)
    driver.find_element(By.ID, "login_password").clear()
    driver.find_element(By.ID, "login_password").send_keys(PASSWORD)
    try:
        vc = driver.find_element(By.CSS_SELECTOR, "input.vc_input")
        vc.clear(); vc.send_keys(VERIFY_CODE)
    except Exception:
        pass
    driver.find_element(By.CSS_SELECTOR, "input.input_submit").click()
    wait.until(EC.url_contains("/user/index/"))
    time.sleep(0.3)


try:
    print("=" * 70)
    print("【前置步骤】登录")
    print("=" * 70)
    do_login()
    print("  ✓ 登录成功")

    # =======================================================
    # 用例 1: 直接访问 /user/address/  (#30 GET)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 1】直接打开地址页 (#30 GET /user/address/)")
    print("=" * 70)

    driver.get(ADDRESS_URL)
    try:
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "h3.common_title2"), "收货地址"))
        mark("收货地址页加载成功", True, f"url={driver.current_url}")
    except TimeoutException:
        mark("收货地址页加载超时", False, f"url={driver.current_url}")
    driver.save_screenshot("addr_01_direct.png")

    # =======================================================
    # 用例 2: 当前地址区 + 编辑地址表单 DOM 完整性
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 2】当前地址 + 编辑表单 DOM 完整性")
    print("=" * 70)

    try:
        site_cons = driver.find_elements(By.CSS_SELECTOR, ".site_con")
        mark(f".site_con 容器数量 = {len(site_cons)}", len(site_cons) >= 2,
             "（至少：当前地址 + 编辑地址）")
    except Exception as e:
        mark(".site_con 容器", False, str(e))

    try:
        cur_dt = driver.find_element(By.CSS_SELECTOR, ".site_con dl dt")
        cur_dd = driver.find_element(By.CSS_SELECTOR, ".site_con dl dd")
        mark(f"当前地址区 dt={cur_dt.text!r}", "当前地址" in cur_dt.text,
             f"dd 内容示例={cur_dd.text[:20]!r}")
    except Exception as e:
        mark("当前地址区 dt/dd 校验失败", False, str(e))

    # 编辑地址表单
    labels = ["收件人：", "详细地址：", "邮编：", "手机："]
    input_by_label = {}
    form_groups = driver.find_elements(By.CSS_SELECTOR, "form .form_group")
    mark(f"编辑地址 form_group 数量={len(form_groups)}", len(form_groups) >= 4)

    for label, group in zip(labels, form_groups[:4]):
        try:
            lab = group.find_element(By.TAG_NAME, "label").text
        except Exception:
            lab = ""
        if label in lab:
            if "详细" in label:
                inp = group.find_element(By.CSS_SELECTOR, "textarea.site_area")
            else:
                inp = group.find_element(By.TAG_NAME, "input")
            input_by_label[label] = inp
            mark(f"编辑字段 {label!r} 存在", True)
        else:
            mark(f"编辑字段 {label!r} 缺失", False, f"实际 label={lab!r}")

    submit = driver.find_element(By.CSS_SELECTOR, "form input.info_submit[type='submit']")
    mark("提交按钮 info_submit 存在", submit.get_attribute("value") == "提交")
    driver.save_screenshot("addr_02_dom.png")

    # =======================================================
    # 用例 3: 字段填充（不提交，仅验证可输入）
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 3】编辑地址字段可输入性（不真实提交）")
    print("=" * 70)

    sample = {"收件人：": "测试用户",
              "详细地址：": "北京市海淀区学院路 100 号 测试小区 1-1-101",
              "邮编：": "100083",
              "手机：": "13900001111"}
    for label, val in sample.items():
        if label in input_by_label:
            try:
                el = input_by_label[label]
                try:
                    el.clear()
                except Exception:
                    pass
                el.send_keys(val)
                actual = (el.get_attribute("value") if el.tag_name == "input"
                          else el.get_attribute("value") or el.text)
                mark(f"填充 {label!r} → {val!r}", True,
                     f"实际读取长度={len(actual)}")
            except Exception as e:
                mark(f"填充 {label!r}", False, str(e))
    driver.save_screenshot("addr_03_filled.png")

    print("\n" + "=" * 70)
    print(f"【汇总】 {passed}/{total} 用例通过")
    print("=" * 70)

except AssertionError as e:
    print(f"\n❌ 断言失败: {e}")
    try:
        driver.save_screenshot("addr_assertion_failed.png")
    except Exception:
        pass

except Exception as e:
    print(f"\n❌ [异常] {type(e).__name__}: {e}")
    import traceback; traceback.print_exc()
    try:
        driver.save_screenshot("addr_error.png")
    except Exception:
        pass

finally:
    print("\n" + "=" * 70)
    print("程序结束，按回车键关闭浏览器...")
    print("=" * 70)
    input()
    driver.quit()
    print("浏览器已关闭。")
