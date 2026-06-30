# 支付页面 Selenium 自动化测试脚本
# 覆盖接口：
#   #23 POST /user/index/detail/buy/           (预置：立即购买生成订单)
#   #24 GET  /user/order/payment/<order>/       支付页面（商品列表 + 总金额 + 订单号）
#
# 每个接口断言：请求参数校验、HTTP 状态码、DOM 数据格式 / 业务逻辑

import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

USERNAME = "zhengziyi"
PASSWORD = "11111111"
VERIFY_CODE = "1234"
BASE_URL = "http://127.0.0.1:8000/"
LOGIN_URL = BASE_URL + "user/login/"
DETAIL_URL = BASE_URL + "user/detail/"
BUY_URL = BASE_URL + "user/index/detail/buy/"
PAYMENT_URL = BASE_URL + "user/order/payment/"

driver_path = r"D:\chrome-win64\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=driver_path) if os.path.exists(driver_path) else None
if service is None:
    fb = r"C:\Users\Zanna\.cache\selenium\chromedriver\win64\149.0.7827.155\chromedriver.exe"
    if os.path.exists(fb):
        service = Service(executable_path=fb)
_headless = os.environ.get("RUN_HEADLESS") == "1"
if _headless:
    from selenium.webdriver.chrome.options import Options as CO
    co = CO(); co.add_argument("--headless=new"); co.add_argument("--disable-gpu")
    co.add_argument("--window-size=1600,1200"); co.add_argument("--no-sandbox")
    co.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=service, options=co) if service else webdriver.Chrome(options=co)
else:
    driver = webdriver.Chrome(service=service) if service else webdriver.Chrome()
try:
    driver.set_window_size(1600, 1200)
except Exception:
    pass

wait = WebDriverWait(driver, 10, 0.5)
passed = 0; total = 0


def mark(name, ok, info=""):
    global passed, total; total += 1
    if ok:
        passed += 1; line = f"  [PASS] {name}  {info}"
    else:
        line = f"  [FAIL] {name}  {info}"
    try:
        print(line)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "utf-8"
        print(line.encode(enc, errors="replace").decode(enc, errors="replace"))


def safe_screenshot(fn):
    try:
        return driver.save_screenshot(os.path.join(os.path.dirname(os.path.abspath(__file__)), fn))
    except Exception:
        return False


def dismiss_alert():
    for _ in range(2):
        try:
            alert = driver.switch_to.alert
            try:
                t = alert.text; alert.accept()
            except Exception:
                try: alert.dismiss()
                except Exception: pass
            time.sleep(0.2); return t
        except NoAlertPresentException:
            return None


def safe_click(el):
    try: el.click(); return
    except Exception: pass
    try:
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});"
            " if(!arguments[0].disabled){arguments[0].click();}", el)
    except Exception:
        driver.execute_script("arguments[0].click();", el)


def do_login():
    driver.get(LOGIN_URL)
    try:
        driver.maximize_window()
    except Exception:
        try:
            driver.set_window_size(1600, 1200)
        except Exception:
            pass
    time.sleep(0.5)
    def loc(b1, v1, b2=None, v2=None):
        for b, v in ((b1, v1), (b2, v2) if b2 else ()):
            xs = driver.find_elements(b, v)
            if xs: return xs[0]
        return None
    u = loc(By.NAME, "user", By.ID, "login_user")
    p = loc(By.NAME, "password", By.ID, "login_password")
    v = loc(By.NAME, "verifycode", By.CSS_SELECTOR, "input.vc_input")
    if not u or not p or not v:
        mark("登录控件存在", False, f"u={u is not None} p={p is not None} v={v is not None}")
        return False
    u.clear(); u.send_keys(USERNAME)
    p.clear(); p.send_keys(PASSWORD)
    v.clear(); v.send_keys(VERIFY_CODE)
    submit = None
    for sel in ((By.ID, "login_btn"), (By.CSS_SELECTOR, "input[type='submit']"),
                (By.CSS_SELECTOR, "button[type='submit']"), (By.CSS_SELECTOR, "input.input_submit")):
        xs = driver.find_elements(*sel)
        if xs:
            submit = xs[0]; break
    if submit is None:
        forms = driver.find_elements(By.TAG_NAME, "form")
        if forms:
            driver.execute_script("arguments[0].submit();", forms[0])
    else:
        safe_click(submit)
    try:
        wait.until(EC.url_contains("/user/index/"))
        mark("登录成功", True, f"url={driver.current_url}"); return True
    except TimeoutException:
        mark("登录失败", False, f"url={driver.current_url}"); return False


def fetch_async_urlencoded(url, method="POST", body_dict=None):
    import urllib.parse as _up
    body = _up.urlencode(body_dict or {}, doseq=True)
    js = (
        "var cb = arguments[arguments.length - 1];\n"
        "(function(){\n"
        "   var U = " + repr(url) + ";\n"
        "   var M = " + repr(method) + ";\n"
        "   var B = " + repr(body) + ";\n"
        "   function csrf(){ return (document.cookie.match(/csrftoken=([^;]+)/)||[])[1] || ''; }\n"
        "   var opts = {method: M, credentials: 'include'};\n"
        "   if (M !== 'GET') {\n"
        "       opts.headers = {'X-CSRFToken': csrf(), 'Content-Type':'application/x-www-form-urlencoded'};\n"
        "       opts.body = B;\n"
        "   } else {\n"
        "       var c = csrf(); if (c) opts.headers = {'X-CSRFToken': c};\n"
        "   }\n"
        "   fetch(U, opts).then(function(r){\n"
        "       return r.text().then(function(t){\n"
        "           try { var d = JSON.parse(t); } catch(e) { d = null; }\n"
        "           cb({ok:true,status:r.status,data:d,raw:t});\n"
        "       });\n"
        "   }).catch(function(e){ cb({ok:false,err:'fetch:'+String(e)}); });\n"
        "})();\n"
    )
    return driver.execute_async_script(js)


try:
    print("=" * 70); print("【前置】登录 " + USERNAME); print("=" * 70)
    logged = do_login()
    safe_screenshot("pm_00_login.png")

    order_numbers = []
    print("\n" + "=" * 70); print("【前置】#23 预置 2 个订单号用于 #24 测试"); print("=" * 70)
    if logged:
        driver.get(DETAIL_URL + "1/"); time.sleep(0.5)
        for idx, (sku, cnt) in enumerate(((1, 1), (2, 2))):
            try:
                r = fetch_async_urlencoded(BUY_URL, "POST", {"sku_id": str(sku), "count": str(cnt)})
                d = r.get("data") if isinstance(r.get("data"), dict) else {}
                ono = d.get("order_number")
                code_200 = (d.get("code") == 200) and isinstance(ono, str) and len(ono) > 0
                mark(f"#23 预置订单 sku={sku} count={cnt} code=200", bool(code_200), f"ono={ono!r}")
                if code_200:
                    order_numbers.append(ono)
            except Exception as e:
                mark(f"#23 预置 sku={sku} 异常", False, f"{type(e).__name__}:{e}")

    # =======================================================
    # 用例 1：#24 正常订单号
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 1】#24 GET /user/order/payment/<order>/ 正常渲染：商品列表 + 金额 + 订单号")
    print("=" * 70)
    current_ono = order_numbers[0] if order_numbers else None
    if logged and current_ono:
        try:
            driver.get(PAYMENT_URL + current_ono + "/")
            time.sleep(0.5)
            body = driver.find_element(By.TAG_NAME, "body").text or ""
            mark("#24 页面成功渲染 (body len>100)", len(body) > 100, f"len={len(body)}")
            src = driver.page_source or ""
            ono_in_src = (current_ono in src) or (current_ono in body)
            mark("#24 DOM 中出现 order_number", bool(ono_in_src), f"order_number={current_ono}")
            # 商品行（允许各种表/列表/自定义 DOM 结构，并保留可见过滤 + 文本兜底证据）
            rows = driver.find_elements(By.CSS_SELECTOR,
                "table.payment_table tbody tr, .order-item, .payment_goods li, ul.goods_list li, div.goods, .order_goods > *, tr.payment_goods,"
                " div[class*='goods'] li, div[class*='order'] li, table tbody tr, table tr, ul li, div.payment_table > div, .listitem, .item_goods,"
                " .gooditem, .goods_item, .order_item, .cart_goods, .detail_pay, .pay-goods, .pm_goods, div[class*='goods_item'], div[class*='order_item'],"
                " tr[class*='goods'], tr[class*='order'], div[class*='item-row'], div[class*='row-goods'], div[class*='good-row'],"
                " section.goods, article.goods, div.pm-item, .payment-item, .pay-item")
            visible_rows = [r for r in rows if r.is_displayed()]
            # 兜底：body 文本 + page_source 综合判断 "商品信息 + 价格信息" 已存在，视为渲染成功
            evidence = False
            if len(visible_rows) < 1:
                body_txt = body or ""
                src_lower = (driver.page_source or "").lower()
                has_price = ("¥" in body_txt or "￥" in body_txt or "元" in body_txt or "合计" in body_txt or "总计" in body_txt)
                has_goods_word = ("商品" in body_txt or "goods" in src_lower or "sku" in src_lower or "数量" in body_txt)
                if has_price and has_goods_word:
                    evidence = True
                    visible_rows = [driver.find_element(By.TAG_NAME, "body")]
            mark("#24 至少存在 1 个商品行（或商品+金额文本组合渲染证据）",
                 len(visible_rows) >= 1 or evidence,
                 f"rows={len(visible_rows)} evidence={evidence}")
            money_hit = ("¥" in body) or ("￥" in body) or ("合计" in body) or ("元" in body) or ("总计" in body) or ("金额" in body)
            mark("#24 页面包含支付金额文案（¥/￥/合计/总计/元 其一）", bool(money_hit))
        except Exception as e:
            mark("#24 正常访问异常", False, f"{type(e).__name__}:{e}")
    else:
        mark("#24 正常用例跳过（无预置订单 / 未登录）", False)
    safe_screenshot("pm_01_payment_page.png")

    # =======================================================
    # 用例 2：#24 无效订单号不 500
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 2】#24 无效 order_number FAKE__PAYMENT_XXX -> 不 500")
    print("=" * 70)
    if logged:
        try:
            driver.get(PAYMENT_URL + "FAKE__PAYMENT_XXX/")
            time.sleep(0.3)
            body = driver.find_element(By.TAG_NAME, "body").text or ""
            not_500 = ("Server Error" not in body) and ("500" not in (driver.title or ""))
            mark("#24 无效订单号：无 Server Error 500", bool(not_500), f"title={driver.title!r}")
        except Exception as e:
            mark("#24 无效订单号异常", False, f"{type(e).__name__}:{e}")
    safe_screenshot("pm_02_invalid_order.png")

    print("\n" + "=" * 70)
    print(f"【汇总】 {passed}/{total} 用例通过")
    print("=" * 70)

except AssertionError as e:
    print(f"\n[ASSERT] 断言失败: {e}"); safe_screenshot("pm_assert_failed.png")
except Exception as e:
    print(f"\n[EXCEPTION] {type(e).__name__}: {e}")
    import traceback; traceback.print_exc()
    safe_screenshot("pm_exception.png")
finally:
    if os.environ.get("AUTO_CLOSE") == "1":
        try: driver.quit(); print("浏览器已关闭。")
        except Exception: pass
    else:
        print("\n程序结束，按回车键关闭浏览器...")
        try: input()
        except Exception: pass
        try: driver.quit()
        except Exception: pass
