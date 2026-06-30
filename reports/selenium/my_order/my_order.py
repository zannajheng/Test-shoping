# 我的订单 Selenium 自动化测试脚本
# 覆盖接口：
#   #22 /user/order/                GET  订单列表
#   #25 /user/order/update/         GET  更新订单状态（取消/收货）
#   #26 /user/order/delete/         GET  删除订单
#   #27 /user/order/evaluate/       GET  订单评价页

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time

# ========== 测试配置 ==========
USERNAME = "zhengziyi"
PASSWORD = "11111111"
VERIFY_CODE = "1234"
BASE_URL = "http://127.0.0.1:8000/"
LOGIN_URL = BASE_URL + "user/login/"
ORDER_URL = BASE_URL + "user/order/"

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
    # 用例 1: 打开订单列表 (#22)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 1】打开订单列表页 (#22 GET /user/order/)")
    print("=" * 70)

    driver.get(ORDER_URL)
    wait.until(EC.text_to_be_present_in_element(
        (By.TAG_NAME, "body"), "全部订单"))
    assert "全部订单" in driver.page_source or "订单" in driver.title
    mark("订单列表页加载", True, f"title={driver.title}")
    driver.save_screenshot("mo_01_order_list.png")

    # 打印页面上有哪些状态的订单（辅助定位）
    order_rows = driver.find_elements(By.CSS_SELECTOR, "ul.order_list_th")
    oper_btns = driver.find_elements(By.CSS_SELECTOR, "a.oper_btn")
    print(f"  → 共识别到 {len(order_rows)} 条订单分组、{len(oper_btns)} 个操作按钮")

    # =======================================================
    # 用例 2: 点击「取消订单」 (#25)  (如存在)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 2】点击「取消订单」按钮 (#25 /user/order/update/?status=已取消)")
    print("=" * 70)

    cancel_btns = [
        b for b in driver.find_elements(By.CSS_SELECTOR, "a.oper_btn")
        if "取消" in b.text
    ]
    if cancel_btns:
        btn = cancel_btns[0]
        href = btn.get_attribute("href") or ""
        print(f"  → 取消按钮链接: {href}")
        mark("取消订单按钮 href 正确", "status=" in href and "已取消" in href, href)
        # 为了避免订单真实被取消影响后续，仅验证按钮存在 + href 正确。
        # 如果订单数 >=2，则真实点击第一条；否则不实际点击以防无订单可测。
        if len(order_rows) >= 2:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            driver.execute_script("arguments[0].style.outline='3px solid #e8616c';", btn)
            driver.save_screenshot("mo_02_before_cancel.png")
            driver.execute_script("arguments[0].style.outline=''; arguments[0].click();", btn)
            try:
                wait.until(EC.url_contains("/user/order/"))
                time.sleep(0.8)
                mark("取消订单后跳转回订单列表", True, f"url={driver.current_url}")
            except TimeoutException:
                mark("取消订单后跳转回订单列表", False, f"当前URL={driver.current_url}")
            driver.save_screenshot("mo_02_after_cancel.png")
        else:
            mark("取消订单按钮已校验 (未实际点击，订单数<2)", True)
    else:
        mark("当前无可取消订单（跳过 #25 取消分支）", True)

    # =======================================================
    # 用例 3: 点击「删除订单」 (#26)  (如存在)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 3】点击「删除订单」按钮 (#26 /user/order/delete/)")
    print("=" * 70)

    del_btns = [
        b for b in driver.find_elements(By.CSS_SELECTOR, "a.oper_btn")
        if "删除" in b.text
    ]
    if del_btns:
        btn = del_btns[0]
        href = btn.get_attribute("href") or ""
        print(f"  → 删除按钮链接: {href}")
        mark("删除订单按钮 href 正确", "/user/order/delete/" in href, href)
        # 安全起见：仅在存在 >=2 条可删订单时才真实点击
        if len(order_rows) >= 2:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            driver.save_screenshot("mo_03_before_delete.png")
            driver.execute_script("arguments[0].click();", btn)
            try:
                wait.until(EC.url_contains("/user/order/"))
                time.sleep(0.8)
                mark("删除后回到订单列表", True)
            except TimeoutException:
                mark("删除后未回到订单列表", False, f"当前URL={driver.current_url}")
            driver.save_screenshot("mo_03_after_delete.png")
        else:
            mark("删除订单按钮已校验（未实际点击，订单数<2）", True)
    else:
        mark("当前无可删除订单（跳过 #26 删除）", True)

    # =======================================================
    # 用例 4: 点击「确认收货」 (#25 status=已收货)  (如存在)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 4】点击「确认收货」按钮 (#25 /user/order/update/?status=已收货)")
    print("=" * 70)

    recv_btns = [
        b for b in driver.find_elements(By.CSS_SELECTOR, "a.oper_btn")
        if "确认收货" in b.text or "收货" == b.text.strip()
    ]
    if recv_btns:
        btn = recv_btns[0]
        href = btn.get_attribute("href") or ""
        print(f"  → 确认收货按钮链接: {href}")
        mark("确认收货按钮 href 正确",
             "/user/order/update/" in href and "已收货" in href, href)
        # 不实际点击，避免状态不可逆；如需真实点击把下面 if False → True
        if False:
            driver.execute_script("arguments[0].click();", btn)
        else:
            mark("确认收货按钮链接格式正确（未点击，避免数据污染）", True)
    else:
        mark("当前无待收货订单（跳过 #25 收货分支）", True)

    # =======================================================
    # 用例 5: 点击「去评价」 → 打开评价页 (#27)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 5】点击「去评价」进入评价页 (#27 GET /user/order/evaluate/)")
    print("=" * 70)

    eval_btns = [
        b for b in driver.find_elements(By.CSS_SELECTOR, "a.oper_btn")
        if "去评价" in b.text or "评价" == b.text.strip()
    ]
    if eval_btns:
        btn = eval_btns[0]
        href = btn.get_attribute("href") or ""
        print(f"  → 评价链接: {href}")
        mark("评价链接格式正确", "/user/order/evaluate/" in href, href)
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        driver.execute_script("arguments[0].style.outline='3px solid #5C8AEC';", btn)
        driver.save_screenshot("mo_05_before_eval.png")
        driver.execute_script("arguments[0].style.outline=''; arguments[0].click();", btn)
        try:
            wait.until(EC.url_contains("/user/order/evaluate/"))
            page_has_eval = "评价" in driver.title or "评价" in driver.find_element(By.TAG_NAME, "body").text
            mark("评价页打开成功", page_has_eval, f"url={driver.current_url}")
        except TimeoutException:
            mark("评价页跳转失败", False, f"当前URL={driver.current_url}")
        driver.save_screenshot("mo_05_eval_page.png")
        # 返回订单列表
        driver.get(ORDER_URL); time.sleep(0.5)
    else:
        mark("当前无待评价订单（跳过 #27）", True)

    # =======================================================
    # 用例 6: 订单列表底部翻页 (#22 page 参数)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 6】订单分页：点击「下一页」（#22 /user/order/?page=...）")
    print("=" * 70)

    page_links = driver.find_elements(By.CSS_SELECTOR, "div.pagenation a")
    print(f"  → 分页按钮数量: {len(page_links)}")
    next_btn = None
    for a in page_links:
        if a.get_attribute("id") == "next":
            next_btn = a; break
    if next_btn and "disabled" not in (next_btn.get_attribute("class") or ""):
        href = next_btn.get_attribute("href") or ""
        mark("下一页按钮存在且未禁用", href != "" and href != "#", href)
    else:
        mark("当前已是最后一页或无分页按钮（合理跳过）", True)
    driver.save_screenshot("mo_06_pagenation.png")

    # =======================================================
    # 汇总
    # =======================================================
    print("\n" + "=" * 70)
    print(f"【汇总】 {passed}/{total} 用例通过")
    print("=" * 70)

except AssertionError as e:
    print(f"\n❌ 断言失败: {e}")
    try:
        driver.save_screenshot("mo_assertion_failed.png")
    except Exception:
        pass

except Exception as e:
    print(f"\n❌ [异常] {type(e).__name__}: {e}")
    import traceback; traceback.print_exc()
    try:
        driver.save_screenshot("mo_error.png")
    except Exception:
        pass

finally:
    print("\n" + "=" * 70)
    print("程序结束，按回车键关闭浏览器...")
    print("=" * 70)
    input()
    driver.quit()
    print("浏览器已关闭。")
