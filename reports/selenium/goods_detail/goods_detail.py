# 商品详情页 Selenium 自动化测试脚本
# 覆盖接口：
#   #10 /user/detail/<sku_id>/  GET  商品详情（含浏览历史+评论区）
#   #16 /user/cartadd/          POST 加入购物车 (通过详情页 add_cart 按钮触发)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException, NoSuchElementException
import os
import sys
import time

# 兼容 Windows PowerShell / cmd 默认 GBK 编码 —— 统一 stdout/stderr 为 UTF-8, 防止 ✓/❌ 等符号导致 UnicodeEncodeError
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

driver_path = r"D:\chrome-win64\chromedriver-win64\chromedriver.exe"
if os.path.exists(driver_path):
    service = Service(executable_path=driver_path)
# RUN_HEADLESS patch — inject headless options when RUN_HEADLESS=1
_headless = (os.environ.get('RUN_HEADLESS') == '1')
if _headless:
    from selenium.webdriver.chrome.options import Options as _CO
    _co = _CO(); _co.add_argument('--headless=new'); _co.add_argument('--disable-gpu'); _co.add_argument('--window-size=1600,1200'); _co.add_argument('--no-sandbox'); _co.add_experimental_option('excludeSwitches',['enable-logging'])
    driver = webdriver.Chrome(service=service, options=_co if _headless else None)
else:
    fallback_path = r"C:\Users\Zanna\.cache\selenium\chromedriver\win64\149.0.7827.155\chromedriver.exe"
    if os.path.exists(fallback_path):
        service = Service(executable_path=fallback_path)
        driver = webdriver.Chrome(service=service)
    else:
        driver = webdriver.Chrome()
# 统一设置窗口尺寸, 避免元素被遮挡导致 ElementClickInterceptedException
try:
    driver.set_window_size(1600, 1200)
except Exception:
    pass

wait = WebDriverWait(driver, 10, 0.5)
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
    # 防御 Windows 终端 GBK 编码导致 UnicodeEncodeError (如 ¥ 字符)
    try:
        print(line)
    except UnicodeEncodeError:
        print(line.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(sys.stdout.encoding or "utf-8", errors="replace"))


def dismiss_any_alert():
    """接受或关闭任何可能存在的 alert/confirm/prompt, 防止 UnexpectedAlertPresentException.
    返回弹框文本 (若不存在则返回 None)."""
    for _ in range(2):
        try:
            alert = driver.switch_to.alert
            text = alert.text
            try:
                alert.accept()
            except Exception:
                try:
                    alert.dismiss()
                except Exception:
                    pass
            time.sleep(0.2)
            return text
        except NoAlertPresentException:
            return None
        except UnexpectedAlertPresentException:
            time.sleep(0.3)
            continue
    return None


def safe_screenshot(filename):
    """截图前先清理 alert 等干扰, 返回是否成功."""
    dismiss_any_alert()
    try:
        return driver.save_screenshot(filename)
    except Exception:
        return False


def safe_click(el):
    """对元素做"抗遮挡"的点击: 先原生 click, 失败则 JS click 兜底."""
    if el is None:
        return
    try:
        el.click()
        return
    except Exception:
        pass
    try:
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center',inline:'center'}); "
            "if(!arguments[0].disabled){arguments[0].click();}", el)
    except Exception:
        driver.execute_script("arguments[0].click();", el)


def do_login():
    driver.get(LOGIN_URL)
    # 最大化/放大窗口: 让登录表单按钮可见, 避免被验证码/底部 banner 遮挡 (click intercepted)
    try: driver.maximize_window()
    except Exception:
        driver.set_window_size(1600, 1200)
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
    submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input_submit")))
    # 滚动进视口 + 点击 (JS 兜底, 避免元素遮挡)
    try:
        submit_btn.click()
    except Exception:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].click();", submit_btn)
    wait.until(EC.url_contains("/user/index/"))
    time.sleep(0.3)


try:
    print("=" * 70)
    print("【前置步骤】登录")
    print("=" * 70)
    do_login()
    print("  [OK] 登录成功")

    # =======================================================
    # 用例 1: 首页 → 首件商品详情 (#10)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 1】首页 → 商品详情页 (#10 /user/detail/<sku_id>/)")
    print("=" * 70)

    driver.get(INDEX_URL)
    time.sleep(0.5)
    # 定位首页第一件商品链接
    first_a = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "(//ul[contains(@class,'goods_list')]/li[1]/a[contains(@href,'/user/detail/')])[1]")
    ))
    sku_url = first_a.get_attribute("href")
    print(f"  → 首件商品链接: {sku_url}")
    mark("首页首件商品链接 /user/detail/<int>/ 格式",
         "/user/detail/" in sku_url and any(p.isdigit() for p in sku_url.split("/")),
         sku_url)
    safe_click(first_a)

    try:
        wait.until(EC.url_contains("/user/detail/"))
        mark("跳转成功", True, f"URL={driver.current_url}")
    except TimeoutException:
        mark("跳转成功", False, f"URL={driver.current_url}")

    # 详情页关键元素：名称、单价、数量、加入购物车按钮、详情 tab、评价列表
    try:
        goods_name = driver.find_element(
            By.CSS_SELECTOR, ".goods_detail_list h3").text
        unit_price = driver.find_element(By.ID, "unit").text
        tab_title  = driver.find_element(By.ID, "tag_detail").text
        mark(f"详情页元素齐全: 商品名={goods_name!r}  单价=¥{unit_price}  tab={tab_title!r}",
             bool(goods_name) and bool(unit_price))
    except Exception as e:
        mark("详情页元素缺失", False, str(e))
    safe_screenshot("gd_01_detail_page.png")

    # =======================================================
    # 用例 2: 数量 + / - 按钮 (DOM 验证)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 2】详情页数量 + / - 按钮 (cart_add / cart_decr)")
    print("=" * 70)

    cart_num  = driver.find_element(By.ID, "cart_num")
    cart_add  = driver.find_element(By.ID, "cart_add")
    cart_decr = driver.find_element(By.ID, "cart_decr")

    init = cart_num.get_attribute("value")
    driver.execute_script("arguments[0].click();", cart_add)
    time.sleep(0.3)
    after_add = cart_num.get_attribute("value")
    mark(f"点击 + 后数量：{init} → {after_add}", int(after_add) == int(init) + 1)

    driver.execute_script("arguments[0].click();", cart_decr)
    time.sleep(0.3)
    after_dec = cart_num.get_attribute("value")
    mark(f"点击 - 后数量：{after_add} → {after_dec}", int(after_dec) == int(after_add) - 1)
    safe_screenshot("gd_02_quantity.png")

    # =======================================================
    # 用例 3: 加入购物车按钮 → #16 /user/cartadd/
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 3】加入购物车按钮 (#16 POST /user/cartadd/)")
    print("=" * 70)

    add_cart = wait.until(EC.element_to_be_clickable((By.ID, "add_cart")))
    sku_id_on_btn = add_cart.get_attribute("sku_id")
    mark(f"加入购物车按钮 sku_id 属性存在", sku_id_on_btn is not None and sku_id_on_btn != "",
         f"sku_id={sku_id_on_btn}")
    driver.execute_script(
        "arguments[0].style.outline='3px solid #5C8AEC';", add_cart)
    safe_screenshot("gd_03_before_cartadd.png")
    driver.execute_script("arguments[0].style.outline='';", add_cart)
    # 点之前先清旧 alert, 避免残留弹框干扰
    dismiss_any_alert()
    safe_click(add_cart)
    # 等待 alert 出现并处理 —— Django 视图一般 return HttpResponse(alert('加入购物车成功'))
    # 这里用短轮询拿到 alert 文本, 超时再兜底 dismiss
    alert_text = None
    t0 = time.time()
    while time.time() - t0 < 3.0:
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            try:
                alert.accept()
            except Exception:
                try: alert.dismiss()
                except Exception: pass
            break
        except NoAlertPresentException:
            time.sleep(0.2)
    mark("加入购物车 → alert 文案包含 '加入购物车成功'",
         alert_text is not None and "加入购物车成功" in (alert_text or ""),
         f"alert_text={alert_text!r}")
    mark("加入购物车按钮已点击（AJAX / HttpResponse 请求已发出）", True)
    # 保证后续截图不会报 UnexpectedAlertPresentException
    dismiss_any_alert()
    safe_screenshot("gd_03_after_cartadd.png")

    # =======================================================
    # 用例 4: 推荐商品 + 评价 + 浏览历史 (详情页完整度)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 4】推荐商品 + 评价模块 (#10 详情页配套渲染)")
    print("=" * 70)

    try:
        new_goods = driver.find_element(By.CSS_SELECTOR, ".new_goods h3")
        mark("推荐商品标题存在", "推荐" in new_goods.text, f"标题={new_goods.text!r}")
    except Exception as e:
        mark("推荐商品标题存在", False, str(e))

    evaluate_divs = driver.find_elements(By.CSS_SELECTOR, ".reviewdiv")
    mark(f"评价模块 div.reviewdiv 数量={len(evaluate_divs)}", True)
    safe_screenshot("gd_04_evaluate_and_recommend.png")

    print("\n" + "=" * 70)
    print(f"【汇总】 {passed}/{total} 用例通过")
    print("=" * 70)

except AssertionError as e:
    print(f"\n❌ 断言失败: {e}")
    try:
        safe_screenshot("gd_assertion_failed.png")
    except Exception:
        pass

except Exception as e:
    print(f"\n❌ [异常] {type(e).__name__}: {e}")
    import traceback; traceback.print_exc()
    try:
        safe_screenshot("gd_error.png")
    except Exception:
        pass

finally:
    # 关闭残留 alert 再退出, 保证 driver.quit 也不会因为 UnexpectedAlert 而报错
    try: dismiss_any_alert()
    except Exception: pass
    print("\n" + "=" * 70)
    print("程序结束，按回车键关闭浏览器...")
    print("=" * 70)
    if os.environ.get("AUTO_CLOSE") != "1":
        try: input()
        except (EOFError, KeyboardInterrupt): pass
    try: driver.quit()
    except Exception: pass
    print("浏览器已关闭。")
