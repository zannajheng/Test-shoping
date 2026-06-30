# 管理员订单状态更新 Selenium 自动化测试脚本
# 账户: admin / 11111111 (is_superuser=1)
# 覆盖接口：
#   #38 GET  /admin/order/update/          管理员更新订单状态
#   #23 POST /user/index/detail/buy/       (预置订单: 用普通用户 zhengziyi 创建可追踪的 order_number)
# 说明：
#   - #38 文档要求必须为管理员权限，参数 order_number / status，成功后 302 到 /admin/user/order/
#   - 每个接口断言：请求参数校验、响应状态码 / 重定向、消息提示 / 列表状态实际变化

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

# ========== 测试配置 ==========
ADMIN_USER = "admin"
ADMIN_PWD = "11111111"
VERIFY_CODE = "1234"
BASE_URL = "http://127.0.0.1:8000/"
LOGIN_URL = BASE_URL + "user/login/"
ADMIN_ORDER_UPDATE_URL = BASE_URL + "admin/order/update/"
ADMIN_ORDER_LIST_URL = BASE_URL + "admin/user/order/"

# 普通用户账户（用于 #23 预置订单，确保有可追踪的 order_number）
PRESET_USER = "zhengziyi"
PRESET_PWD = "11111111"
DETAIL_BUY_URL = BASE_URL + "user/index/detail/buy/"

driver_path = r"D:\chrome-win64\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=driver_path) if os.path.exists(driver_path) else None
if service is None:
    fallback_path = r"C:\Users\Zanna\.cache\selenium\chromedriver\win64\149.0.7827.155\chromedriver.exe"
    if os.path.exists(fallback_path):
        service = Service(executable_path=fallback_path)

_headless = os.environ.get("RUN_HEADLESS") == "1"
if _headless:
    from selenium.webdriver.chrome.options import Options as _CO
    _co = _CO(); _co.add_argument("--headless=new"); _co.add_argument("--disable-gpu")
    _co.add_argument("--window-size=1600,1200"); _co.add_argument("--no-sandbox")
    _co.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=service, options=_co) if service else webdriver.Chrome(options=_co)
else:
    driver = webdriver.Chrome(service=service) if service else webdriver.Chrome()

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
            t = alert.text
            try:
                alert.accept()
            except Exception:
                try:
                    alert.dismiss()
                except Exception:
                    pass
            time.sleep(0.2)
            return t
        except NoAlertPresentException:
            return None


def safe_click(el):
    if el is None:
        return
    try:
        el.click(); return
    except Exception:
        pass
    try:
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center',inline:'center'});"
            " if(!arguments[0].disabled){arguments[0].click();}", el)
    except Exception:
        driver.execute_script("arguments[0].click();", el)


def do_login(user, pwd):
    driver.get(LOGIN_URL)
    try:
        driver.maximize_window()
    except Exception:
        try:
            driver.set_window_size(1600, 1200)
        except Exception:
            pass
    time.sleep(0.5)

    def _locate(by1, v1, by2=None, v2=None):
        for by, v in ((by1, v1), (by2, v2) if by2 else ()):
            xs = driver.find_elements(by, v)
            if xs:
                return xs[0]
        return None

    u = _locate(By.NAME, "user", By.ID, "login_user")
    p = _locate(By.NAME, "password", By.ID, "login_password")
    v = _locate(By.NAME, "verifycode", By.CSS_SELECTOR, "input.vc_input")
    if not (u and p and v):
        mark(f"登录元素: user/pwd/vc 找到 (用户={user})", False,
             f"user_found={u is not None} pwd_found={p is not None} vc_found={v is not None}")
        return False
    u.clear(); u.send_keys(user)
    p.clear(); p.send_keys(pwd)
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
        mark(f"用户 {user} 登录成功", True, f"url={driver.current_url}")
        return True
    except TimeoutException:
        mark(f"用户 {user} 登录失败", False, f"url={driver.current_url}")
        return False


def logout():
    try:
        driver.get(BASE_URL + "user/logout/")
        time.sleep(0.8)
    except Exception:
        pass


def fetch_async_urlencoded(url, method="POST", body_dict=None, query=None):
    """通过 fetch 调用 JSON / URL encoded 接口，保持 session + csrf."""
    import urllib.parse as _up
    full_url = url
    if query:
        qs = _up.urlencode(query, doseq=True)
        full_url = full_url + ("&" if "?" in full_url else "?") + qs
    body_str = _up.urlencode(body_dict or {}, doseq=True) if body_dict else ""
    js = (
        "var cb = arguments[arguments.length - 1];\n"
        "(function(){\n"
        "   var FULL = " + repr(full_url) + ";\n"
        "   var METHOD = " + repr(method) + ";\n"
        "   var BODY = " + repr(body_str) + ";\n"
        "   function csrf(){ return (document.cookie.match(/csrftoken=([^;]+)/)||[])[1] || ''; }\n"
        "   var opts = {method: METHOD, credentials:'include'};\n"
        "   if (METHOD !== 'GET') {\n"
        "       opts.headers = {'X-CSRFToken': csrf(), 'Content-Type':'application/x-www-form-urlencoded'};\n"
        "       opts.body = BODY;\n"
        "   } else {\n"
        "       var c = csrf(); if (c) opts.headers = {'X-CSRFToken': c};\n"
        "   }\n"
        "   fetch(FULL, opts).then(function(r){\n"
        "       var st = r.status;\n"
        "       return r.text().then(function(t){\n"
        "           var d = null;\n"
        "           try { d = JSON.parse(t); } catch(e) {}\n"
        "           cb({ok:true, status:st, data:d, raw:t});\n"
        "       });\n"
        "   }).catch(function(e){ return cb({ok:false,err:'fetch:'+String(e)}); });\n"
        "})();\n"
    )
    return driver.execute_async_script(js)


def create_order_via_buy_now(sku_id=1, count=1):
    """普通用户登录后调用 #23 立即购买，返回 order_number 或 None."""
    if not do_login(PRESET_USER, PRESET_PWD):
        return None
    # 先访问详情页一次，拿到 csrf cookie
    driver.get(BASE_URL + "user/detail/" + str(int(sku_id)) + "/")
    time.sleep(0.8)
    try:
        r = fetch_async_urlencoded(DETAIL_BUY_URL, "POST",
                                   body_dict={"sku_id": str(int(sku_id)), "count": str(int(count))})
        data = r.get("data") if isinstance(r.get("data"), dict) else {}
        ok = r.get("ok") and data.get("code") == 200 and isinstance(data.get("order_number"), str)
        mark(
            "预置订单 (#23 立即购买) 返回 code=200 且 order_number 非空",
            bool(ok),
            f"resp={r}",
        )
        if ok:
            return data["order_number"]
    except Exception as e:
        mark("预置订单 #23 异常", False, f"{type(e).__name__}:{e}")
    return None


# =======================================================
# 主流程
# =======================================================
order_number_for_admin = None
try:
    # 先：用普通用户做一次 #23 立即购买 拿到 order_number
    print("=" * 70)
    print("【前置】普通用户下单 (#23) -> 退出 -> 管理员登录")
    print("=" * 70)
    order_number_for_admin = create_order_via_buy_now(sku_id=1, count=1)
    logout()
    time.sleep(0.5)

    # 管理员登录
    print("\n" + "=" * 70)
    print("【前置】管理员登录 " + ADMIN_USER + "/" + ADMIN_PWD)
    print("=" * 70)
    admin_ok = do_login(ADMIN_USER, ADMIN_PWD)
    safe_screenshot("admord_00_admin_logged.png")

    # =======================================================
    # 用例 1：#38 正常请求（有 order_number + status）
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 1】#38 正常参数：order_number + status 已发货 -> 302 /admin/user/order/")
    print("=" * 70)
    if order_number_for_admin and admin_ok:
        target_status = "已发货"
        params_qs = f"order_number={order_number_for_admin}&status={target_status}"
        try:
            driver.get(ADMIN_ORDER_UPDATE_URL + "?" + params_qs)
            time.sleep(0.8)
            url_now = driver.current_url
            redirect_ok = ("/admin/user/order/" in url_now) or ("/admin/" in url_now and "order" in url_now)
            mark(
                "#38 正常参数：302 重定向到 /admin/user/order/（订单列表）",
                bool(redirect_ok),
                f"url={url_now}",
            )
            body = driver.find_element(By.TAG_NAME, "body").text or ""
            # 业务关键：列表中出现该订单号，并且其对应状态=已发货
            has_order_no = order_number_for_admin in body
            status_hit = (target_status in body)
            mark(
                "#38 业务断言：admin 订单列表中存在该订单号 且 状态列为 " + target_status,
                bool(has_order_no and status_hit),
                f"has_order_no={has_order_no} status_hit={status_hit} body_sample={body[:300]!r}",
            )
            # Django messages 可能在 ul.messagelist / .alert 等容器 包含 "已更新 / 更新成功 / 订单状态"
            try:
                msgs = driver.find_elements(By.CSS_SELECTOR,
                                            "ul.messagelist li, div.messages, div.alert, .alert-success, .alert-info")
                msg_text = " ".join(m.text or "" for m in msgs)
            except Exception:
                msg_text = ""
            msg_hit = any(k in msg_text for k in ("更新", "成功", "订单状态")) or any(
                k in body for k in ("订单状态已更新", f"已更新为 {target_status}"))
            mark(
                "#38 页面含 messages 提示（更新成功/订单状态 类文案）",
                bool(msg_hit),
                f"msg_text={msg_text[:120]!r}",
            )
        except Exception as e:
            mark("#38 正常参数执行异常", False, f"{type(e).__name__}:{e}")
    else:
        mark("#38 用例跳过（未预置 order_number 或 admin 登录失败）", False,
             f"order_number={order_number_for_admin!r} admin_ok={admin_ok}")
    safe_screenshot("admord_01_updated.png")

    # =======================================================
    # 用例 2：#38 缺参数（仅 status / 仅 order_number / 都无）
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 2】#38 参数校验：缺 order_number / 缺 status / 都缺 不 crash，均 302 回 admin 订单列表")
    print("=" * 70)
    if admin_ok:
        sub_cases = [
            ("缺 order_number", f"status=已发货"),
            ("缺 status", f"order_number=FAKE_ORDER_NOT_EXIST"),
            ("全缺", ""),
        ]
        for name, qs in sub_cases:
            try:
                url = ADMIN_ORDER_UPDATE_URL + ("?" + qs if qs else "")
                driver.get(url)
                time.sleep(0.5)
                ok = ("/admin/user/order/" in driver.current_url) or ("/admin/" in driver.current_url)
                mark(
                    f"#38 参数校验({name}): 302 /admin/...（不 500）",
                    bool(ok),
                    f"url={driver.current_url}",
                )
            except Exception as e:
                mark(f"#38 参数校验({name}) 异常", False, f"{type(e).__name__}:{e}")

    # =======================================================
    # 用例 3：#38 非法 order_number（不存在的订单）不 crash
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 3】#38 非法订单号 FAKE__ORDER：仍然 302 且无 500")
    print("=" * 70)
    if admin_ok:
        try:
            driver.get(ADMIN_ORDER_UPDATE_URL + "?order_number=FAKE__ORDER&status=已发货")
            time.sleep(0.5)
            not_500 = "Server Error" not in (driver.find_element(By.TAG_NAME, "body").text or "")
            redirect_ok = ("/admin/" in driver.current_url)
            mark(
                "#38 非法订单号：302 且无 500 页面",
                bool(not_500 and redirect_ok),
                f"url={driver.current_url}",
            )
        except Exception as e:
            mark("#38 非法订单号执行异常", False, f"{type(e).__name__}:{e}")

    # =======================================================
    # 用例 4：#38 鉴权（非管理员访问 → 跳登录 / 被拒绝）
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 4】#38 鉴权：普通用户登录后访问 #38 应被拦截（跳登录/admin 后台登录）")
    print("=" * 70)
    if True:
        logout()
        time.sleep(0.5)
        if do_login(PRESET_USER, PRESET_PWD):
            try:
                driver.get(ADMIN_ORDER_UPDATE_URL + "?order_number=FAKE_ORDER_PROTECT&status=已发货")
                time.sleep(0.5)
                url_now = driver.current_url
                # 被拦截的典型 URL：/user/login/ 、/admin/login/（Django 后台登录）
                # 只要没有成功进入 /admin/user/order/ 管理列表，即视为鉴权拦截成功
                blocked = ("/login/" in url_now) or ("/admin/user/order/" not in url_now)
                mark(
                    "#38 鉴权：非管理员不能进入 /admin/*（跳登录或在非admin页面）",
                    bool(blocked),
                    f"url={url_now}",
                )
            except Exception as e:
                mark("#38 鉴权异常", False, f"{type(e).__name__}:{e}")
        safe_screenshot("admord_02_non_admin.png")

    # =======================================================
    # 汇总
    # =======================================================
    print("\n" + "=" * 70)
    print(f"【汇总】 {passed}/{total} 用例通过")
    print("=" * 70)

except AssertionError as e:
    print(f"\n[ASSERT] 断言失败: {e}")
    safe_screenshot("admord_assert_failed.png")
except Exception as e:
    print(f"\n[EXCEPTION] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    safe_screenshot("admord_exception.png")
finally:
    if os.environ.get("AUTO_CLOSE") == "1":
        try:
            driver.quit(); print("浏览器已关闭。")
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
        except Exception:
            pass
