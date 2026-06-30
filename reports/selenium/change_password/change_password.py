# 修改密码页 Selenium 自动化测试脚本
# 覆盖接口：
#   #8 /user/password/   GET  渲染修改密码页
#   #8 /user/password/   POST 提交修改密码（仅做字段填充，不含真实提交，避免账号密码被改）

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
PASSWORD_URL = BASE_URL + "user/password/"

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
    # 用例 1: 打开修改密码页 (#8 GET /user/password/)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 1】打开修改密码页 (#8 GET /user/password/)")
    print("=" * 70)

    driver.get(PASSWORD_URL)
    try:
        wait.until(EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"), "修改密码"))
        mark("修改密码页加载成功", True, f"title={driver.title} URL={driver.current_url}")
    except TimeoutException:
        mark("修改密码页加载超时", False, f"URL={driver.current_url}")
    driver.save_screenshot("cp_01_page.png")

    # =======================================================
    # 用例 2: DOM 字段存在性 + name / id 对应
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 2】表单字段 DOM + name/id 对应 (#8 提交字段)")
    print("=" * 70)

    def check_input(el_id, expected_name, desc):
        el = driver.find_element(By.ID, el_id)
        name_ok = (el.get_attribute("name") == expected_name)
        mark(f"{desc} (id={el_id} name={expected_name})", name_ok,
             f"实际name={el.get_attribute('name')!r}")
        return el

    user = check_input("password_user", "user", "用户名输入框")
    pw1  = check_input("password_pw1",  "password",             "新密码输入框")
    pw2  = check_input("password_pw2",  "password_confirmation", "确认密码输入框")

    csrf = driver.find_elements(By.CSS_SELECTOR, "input[name='csrfmiddlewaretoken']")
    mark("CSRF token 存在", len(csrf) > 0, f"数量={len(csrf)}")
    driver.save_screenshot("cp_02_dom.png")

    # =======================================================
    # 用例 3: 字段填充（不真实点击 submit，避免改密）
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 3】字段值填充（不提交，仅验证可输入）")
    print("=" * 70)

    user.clear(); user.send_keys(USERNAME)
    pw1.clear();  pw1.send_keys("abc123!@#")
    pw2.clear();  pw2.send_keys("abc123!@#")
    mark("3 个字段值填充成功", True,
         f"user={user.get_attribute('value')!r}  "
         f"pw1_len={len(pw1.get_attribute('value'))}  "
         f"pw2_len={len(pw2.get_attribute('value'))}")
    driver.save_screenshot("cp_03_filled.png")

    # =======================================================
    # 用例 4: 页面登录链接跳转 (header <a> 登录)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 4】页面右上角「登录」链接 / reg_title 结构")
    print("=" * 70)

    try:
        title_h1 = driver.find_element(
            By.CSS_SELECTOR, ".reg_title h1").text
        login_a = driver.find_element(
            By.CSS_SELECTOR, ".reg_title a")
        mark(f"reg_title 标题={title_h1!r}  '登录' href",
             "修改密码" in title_h1 and "/user/login/" in (login_a.get_attribute("href") or ""),
             f"登录href={login_a.get_attribute('href')!r}")
    except Exception as e:
        mark("reg_title 结构错误", False, str(e))

    print("\n" + "=" * 70)
    print(f"【汇总】 {passed}/{total} 用例通过 (为防账号风险未实际点提交按钮)")
    print("=" * 70)

except AssertionError as e:
    print(f"\n❌ 断言失败: {e}")
    try:
        driver.save_screenshot("cp_assertion_failed.png")
    except Exception:
        pass

except Exception as e:
    print(f"\n❌ [异常] {type(e).__name__}: {e}")
    import traceback; traceback.print_exc()
    try:
        driver.save_screenshot("cp_error.png")
    except Exception:
        pass

finally:
    print("\n" + "=" * 70)
    print("程序结束，按回车键关闭浏览器...")
    print("=" * 70)
    input()
    driver.quit()
    print("浏览器已关闭。")
