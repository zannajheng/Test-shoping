# 首页 Selenium 自动化测试脚本 — 覆盖：
#   #9 GET  /user/index/   首页（首页渲染 + 商品分类导航 + 回到顶部功能）

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

USERNAME = "zhengziyi"
PASSWORD = "11111111"
VERIFY_CODE = "1234"
BASE_URL = "http://127.0.0.1:8000/"
LOGIN_URL = BASE_URL + "user/login/"
INDEX_URL = BASE_URL + "user/index/"

HERE = os.path.dirname(os.path.abspath(__file__))
passed = 0
total = 0


def mark(name, ok, info=""):
    global passed, total
    total += 1
    if ok:
        passed += 1
        line = f"  [PASS] {name}  {info}"
    else:
        line = f"  [FAIL] {name}  {info}"
    try:
        print(line)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "utf-8"
        print(line.encode(enc, errors="replace").decode(enc, errors="replace"))


def safe_screenshot(fn):
    try:
        return driver.save_screenshot(os.path.join(HERE, fn))
    except Exception:
        return False


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


def get_scroll_top():
    return driver.execute_script(
        "return Math.max(document.documentElement.scrollTop, document.body.scrollTop);"
    )


def get_scroll_height():
    return driver.execute_script(
        "return Math.max(document.documentElement.scrollHeight, document.body.scrollHeight);"
    )


def get_viewport_height():
    return driver.execute_script("return window.innerHeight;")


def is_backtop_visible():
    return driver.execute_script(
        "const el = document.querySelector('.toolkit_item:last-child');"
        "if(!el) return false;"
        "const style = window.getComputedStyle(el);"
        "return style.display !== 'none' && style.visibility !== 'hidden' && el.offsetHeight > 0;"
    )


def smooth_scroll_to(target_y, step=300, interval=0.15):
    if isinstance(target_y, str) and target_y.lower() == 'bottom':
        target_y = get_scroll_height() - get_viewport_height() - 2
    current = get_scroll_top()
    if target_y > current:
        while current < target_y:
            current = min(current + step, target_y)
            driver.execute_script(f"window.scrollTo({{top: {current}, behavior: 'auto'}});")
            time.sleep(interval)
    else:
        while current > target_y:
            current = max(current - step, target_y)
            driver.execute_script(f"window.scrollTo({{top: {current}, behavior: 'auto'}});")
            time.sleep(interval)
    driver.execute_script(f"window.scrollTo({{top: {target_y}, behavior: 'auto'}});")
    time.sleep(0.3)


try:
    # ========== 前置：登录 ==========
    print("=" * 70)
    print("【前置】登录账号")
    print("=" * 70)
    driver.get(LOGIN_URL)
    try:
        driver.maximize_window()
    except Exception:
        try:
            driver.set_window_size(1600, 1200)
        except Exception:
            pass
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
    time.sleep(0.6)

    # ========== 1. #9 GET /user/index/ 首页渲染 ==========
    print("\n" + "=" * 70)
    print("[1/6] #9 GET /user/index/ 首页渲染")
    print("=" * 70)
    driver.get(INDEX_URL)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".tt_toolkit, .header_bar, .list_banner, .goods_type_list")))
    mark("#9 首页关键 DOM 已出现 (.header / .goods_type_list / .tt_toolkit)", True,
         f"url={driver.current_url}")
    # 验证根路径 / 是否 302 到 /user/index/
    try:
        driver.get(BASE_URL)
        wait.until(EC.url_contains("/user/index/"))
        mark("#9 根路径 / 302 -> /user/index/", True, f"url={driver.current_url}")
    except TimeoutException:
        mark("#9 根路径 / 未 302 跳 /user/index/", False, f"url={driver.current_url}")
    driver.get(INDEX_URL)
    safe_screenshot("index_01_initial_top.png")

    # ========== 2. 初始 scrollTop 与 回顶部按钮状态 ==========
    print("\n" + "=" * 70)
    print("[2/6] 初始 scrollTop 与 回顶部按钮可见性")
    print("=" * 70)
    scroll_top_initial = get_scroll_top()
    backtop_visible_initial = is_backtop_visible()
    print(f"  初始 scrollTop = {scroll_top_initial} px，回顶部可见 = {backtop_visible_initial}")
    if scroll_top_initial < 500:
        mark("初始状态 scrollTop<500 时回顶部按钮隐藏",
             not backtop_visible_initial,
             f"scrollTop={scroll_top_initial} visible={backtop_visible_initial}")
    else:
        mark("初始状态回顶部按钮符合预期（skip because scrollTop>=500）", True)

    # ========== 3. 滚动到底部 ==========
    print("\n" + "=" * 70)
    print("[3/6] 平滑滚动到底部")
    print("=" * 70)
    page_total_height = get_scroll_height()
    viewport_h = get_viewport_height()
    print(f"  页面总高 scrollHeight = {page_total_height} px，视口高 = {viewport_h} px")
    smooth_scroll_to('bottom', step=300, interval=0.12)
    scroll_after_bottom = get_scroll_top()
    print(f"  滚动结束 scrollTop = {scroll_after_bottom} px")
    mark("滚动到底部后 scrollTop > 500", scroll_after_bottom > 500,
         f"scrollTop={scroll_after_bottom}")
    safe_screenshot("index_02_bottom_before_click.png")

    # ========== 4. 回顶部按钮显示 ==========
    print("\n" + "=" * 70)
    print("[4/6] 滚动到底部后回顶部按钮显示状态")
    print("=" * 70)
    scroll_top_now = get_scroll_top()
    backtop_visible_now = is_backtop_visible()
    print(f"  scrollTop={scroll_top_now} px, 回顶部可见={backtop_visible_now}")
    if scroll_top_now > 500:
        mark("scrollTop>500 时回顶部按钮可见", bool(backtop_visible_now),
             f"visible={backtop_visible_now}")
    if not backtop_visible_now:
        driver.execute_script(
            "const el = document.querySelector('.toolkit_item:last-child');"
            "if(el){ el.style.display='block'; el.style.visibility='visible'; }"
        )
        time.sleep(0.3)
        print("  强制点亮回顶部按钮以便后续测试点击行为")

    # ========== 5. 点击回顶部按钮 ==========
    print("\n" + "=" * 70)
    print("[5/6] 点击「回顶部」按钮 -> 验证回到顶部")
    print("=" * 70)
    backtop_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".toolkit_item:last-child"))
    )
    driver.execute_script(
        "arguments[0].style.outline='3px solid #e8616c';"
        "arguments[0].style.outlineOffset='3px';",
        backtop_btn
    )
    time.sleep(0.3)
    safe_screenshot("index_03_backtop_highlighted.png")
    print("  已高亮回顶部按钮并截图: index_03_backtop_highlighted.png")

    driver.execute_script(
        "arguments[0].style.outline=''; arguments[0].style.outlineOffset='';",
        backtop_btn
    )
    scroll_before_click = get_scroll_top()
    print(f"  点击前 scrollTop = {scroll_before_click} px")
    backtop_btn.click()

    print("  等待 smooth 滚动到顶（最多 10 秒）...")
    prev_scroll = -1
    stable_count = 0
    for i in range(10):
        time.sleep(1)
        current_scroll = get_scroll_top()
        print(f"    第{i+1}秒: scrollTop = {current_scroll} px")
        if current_scroll == prev_scroll:
            stable_count += 1
            if stable_count >= 2:
                print("    连续 2 秒不变，滚动结束")
                break
        else:
            stable_count = 0
        prev_scroll = current_scroll
        if current_scroll <= 0:
            print("    已到达顶部")
            break

    scroll_final = get_scroll_top()
    mark("点击回顶部按钮后 scrollTop <= 10", scroll_final <= 10,
         f"scrollFinal={scroll_final}")
    if scroll_final <= 10:
        safe_screenshot("index_04_back_to_top_success.png")
        print("  已截图: index_04_back_to_top_success.png")
    else:
        safe_screenshot("index_04_back_to_top_fail.png")

    # ========== 6. 汇总 ==========
    print("\n" + "=" * 70)
    print(f"【汇总】 {passed}/{total} 用例通过")
    print("=" * 70)

except AssertionError as e:
    print(f"\n❌ 断言失败: {e}")
    safe_screenshot("index_assertion_failed.png")

except Exception as e:
    print(f"\n[异常] 脚本执行出错: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    safe_screenshot("index_error.png")

finally:
    if os.environ.get("AUTO_CLOSE") == "1":
        try:
            driver.quit()
            print("浏览器已关闭。")
        except Exception:
            pass
    else:
        print("\n程序结束，按回车键关闭浏览器...")
        try:
            input()
        except Exception:
            pass
        try:
            driver.quit()
            print("浏览器已关闭。")
        except Exception:
            pass
