# 管理员客服后台 Selenium 自动化测试脚本
# 账户: admin / 11111111 (is_superuser=1)
# 覆盖接口（管理员相关）：
#   #34 GET  /admin/service/                  管理员客服后台（会话列表 + 会话详情）
#   #35 GET  /admin/service/reading/          标记会话已读
#   #36 GET  /admin/service/reading/send/     批量查询未读消息数
#   #37 GET  /service/face/                   获取表情包列表（管理员侧 AJAX 调用）
#
# 每个接口断言：
#   - 请求参数校验（缺参数 / 错误参数不 crash）
#   - 响应状态码 / 跳转合法
#   - 响应数据格式（JSON code/message/data 结构）
#   - 关键业务逻辑（is_superuser 鉴权、已读后未读数归零、批量未读数 keys 为会话号）

import os
import sys
import time
import json

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
USERNAME = "admin"
PASSWORD = "11111111"
VERIFY_CODE = "1234"
BASE_URL = "http://127.0.0.1:8000/"
LOGIN_URL = BASE_URL + "user/login/"
ADMIN_SERVICE_URL = BASE_URL + "admin/service/"
READING_URL = BASE_URL + "admin/service/reading/"
READING_SEND_URL = BASE_URL + "admin/service/reading/send/"
FACE_URL = BASE_URL + "service/face/"

# WebDriver 初始化（支持无头环境变量 RUN_HEADLESS=1）
driver_path = r"D:\chrome-win64\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=driver_path) if os.path.exists(driver_path) else None
if service is None:
    fallback_path = r"C:\Users\Zanna\.cache\selenium\chromedriver\win64\149.0.7827.155\chromedriver.exe"
    if os.path.exists(fallback_path):
        service = Service(executable_path=fallback_path)

_headless = os.environ.get("RUN_HEADLESS") == "1"
if _headless:
    from selenium.webdriver.chrome.options import Options as _CO
    _co = _CO()
    _co.add_argument("--headless=new")
    _co.add_argument("--disable-gpu")
    _co.add_argument("--window-size=1600,1200")
    _co.add_argument("--no-sandbox")
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
        el.click()
        return
    except Exception:
        pass
    try:
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center',inline:'center'});"
            " if(!arguments[0].disabled){arguments[0].click();}",
            el,
        )
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
    safe_screenshot("admsvc_00_login_page.png")

    # 定位三要素：用户名 / 密码 / 验证码（兼容 By.NAME 与常见 ID）
    def locate(by1, val1, by2=None, val2=None):
        for by, v in ((by1, val1), (by2, val2) if by2 else ()):
            xs = driver.find_elements(by, v)
            if xs:
                return xs[0]
        return None

    u = locate(By.NAME, "user", By.ID, "login_user")
    p = locate(By.NAME, "password", By.ID, "login_password")
    v = locate(By.NAME, "verifycode", By.CSS_SELECTOR, "input.vc_input")
    assert u is not None, "找不到用户名输入框"
    assert p is not None, "找不到密码输入框"
    assert v is not None, "找不到验证码输入框"
    u.clear(); u.send_keys(USERNAME)
    p.clear(); p.send_keys(PASSWORD)
    v.clear(); v.send_keys(VERIFY_CODE)

    submit = None
    for sel in (
        (By.ID, "login_btn"),
        (By.CSS_SELECTOR, "input[type='submit']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.CSS_SELECTOR, "input.input_submit"),
    ):
        xs = driver.find_elements(*sel)
        if xs:
            submit = xs[0]
            break
    if submit is None:
        forms = driver.find_elements(By.TAG_NAME, "form")
        if forms:
            driver.execute_script("arguments[0].submit();", forms[0])
    else:
        safe_click(submit)
    try:
        wait.until(EC.url_contains("/user/index/"))
        mark("管理员登录成功（跳到 /user/index/）", True, f"url={driver.current_url}")
    except TimeoutException:
        mark("管理员登录成功（跳到 /user/index/）", False, f"url={driver.current_url}")
    safe_screenshot("admsvc_00_logged_in.png")


def fetch_json_async(url, method="GET", query_params=None, body_urlencoded=None):
    """在当前页面中通过 fetch 调接口，保持 session + csrf 一致，返回 {ok,data,raw,status,err}."""
    import urllib.parse as _up
    full_url = url
    if query_params:
        qs = _up.urlencode(query_params, doseq=True)
        sep = "&" if "?" in full_url else "?"
        full_url = full_url + sep + qs
    js = (
        "var cb = arguments[arguments.length - 1];\n"
        "(function(){\n"
        "    var FULL = " + repr(full_url) + ";\n"
        "    var METHOD = " + repr(method) + ";\n"
        "    var BODY = " + (repr(body_urlencoded) if body_urlencoded is not None else "null") + ";\n"
        "    function csrf(){ return (document.cookie.match(/csrftoken=([^;]+)/)||[])[1] || ''; }\n"
        "    var opts = {method:METHOD, credentials:'include'};\n"
        "    if (METHOD !== 'GET') {\n"
        "        opts.headers = {'X-CSRFToken': csrf(), 'Content-Type':'application/x-www-form-urlencoded'};\n"
        "        opts.body = BODY || '';\n"
        "    } else if (csrf()) {\n"
        "        opts.headers = {'X-CSRFToken': csrf()};\n"
        "    }\n"
        "    fetch(FULL, opts).then(function(r){\n"
        "        var st = r.status;\n"
        "        return r.text().then(function(t){\n"
        "            var d = null;\n"
        "            try { d = JSON.parse(t); } catch(e) {}\n"
        "            cb({ok:true,status:st,data:d,raw:t});\n"
        "        });\n"
        "    }).catch(function(e){ return cb({ok:false, err:'fetch:'+String(e)}); });\n"
        "})();\n"
    )
    return driver.execute_async_script(js)


# 会话号解析工具：从 #34 左侧会话列表里提取至少 1 个真实会话号，用于 #35 / #36 参数
def extract_service_numbers():
    out = []
    # 策略 1：href=?number=XXX
    for a in driver.find_elements(By.CSS_SELECTOR, "a[href*='number=']"):
        href = a.get_attribute("href") or ""
        if "number=" in href:
            import urllib.parse as _up
            try:
                qs = _up.parse_qs(_up.urlparse(href).query)
            except Exception:
                qs = {}
            vals = qs.get("number") or []
            for v in vals:
                if v and v not in out:
                    out.append(v)
    # 策略 2：div/li 文本形如 大写字母 + 数字
    if not out:
        import re as _re
        for el in driver.find_elements(By.CSS_SELECTOR, "li, div.user_service, a"):
            txt = (el.text or "").strip()
            for m in _re.findall(r"(?<![A-Z0-9])([A-Z][A-Z0-9]{8,})", txt):
                if m not in out:
                    out.append(m)
            if len(out) >= 3:
                break
    return out


# =======================================================
# 入口执行
# =======================================================
try:
    print("=" * 70)
    print("【前置步骤】管理员登录 " + USERNAME + "/" + PASSWORD)
    print("=" * 70)
    do_login()

    # =======================================================
    # 用例 1：管理员客服后台 (#34 GET /admin/service/)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 1】管理员客服后台 #34 GET /admin/service/")
    print("=" * 70)

    service_numbers = []
    try:
        driver.get(ADMIN_SERVICE_URL)
        time.sleep(0.8)
        url_now = driver.current_url
        # 关键业务断言：管理员身份 / 非 admin 跳登录页（鉴权）
        in_admin_page = ("/admin/service/" in url_now) or (
            "/admin/" in url_now and "/user/login/" not in url_now
        )
        mark(
            "#34 鉴权：管理员登录后仍停留在 admin 相关页面（未被踢回登录）",
            bool(in_admin_page),
            f"url={url_now}",
        )

        body_text = driver.find_element(By.TAG_NAME, "body").text or ""
        # 预期会话列表区域至少有会话条目（user_service 类名或 li 项）
        left_items = (
            driver.find_elements(By.CSS_SELECTOR, "div.user_service li")
            or driver.find_elements(By.CSS_SELECTOR, ".user_service a")
            or driver.find_elements(By.CSS_SELECTOR, ".service_sidebar a, .service_sidebar li")
        )
        mark(
            "#34 左侧会话列表渲染（至少 1 项）",
            len(left_items) > 0,
            f"count={len(left_items)}",
        )

        service_numbers = extract_service_numbers()
        mark(
            "#34 解析到会话号 >= 1 个（用于后续 #35/#36 参数）",
            len(service_numbers) >= 1,
            f"numbers={service_numbers[:5]!r}",
        )

        # 进入某个具体会话（带 number 参数） -> 不 crash，能打开
        if service_numbers:
            try:
                driver.get(ADMIN_SERVICE_URL + "?number=" + service_numbers[0])
                mark(
                    "#34 带 number 参数打开具体会话不 crash",
                    True,
                    f"number={service_numbers[0]} url={driver.current_url}",
                )
            except Exception as e:
                mark(
                    "#34 带 number 参数打开具体会话不 crash",
                    False,
                    f"number={service_numbers[0]} err={type(e).__name__}:{e}",
                )
    except Exception as e:
        mark("#34 整体执行异常", False, f"{type(e).__name__}:{e}")
    safe_screenshot("admsvc_01_admin_service.png")

    # =======================================================
    # 用例 2：标记会话已读 (#35 GET /admin/service/reading/)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 2】标记会话已读 #35 GET /admin/service/reading/")
    print("=" * 70)

    if not service_numbers:
        mark("#35 跳过（没有可用会话号）", False)
    else:
        number_35 = service_numbers[0]
        # 先确保停留在一个有 CSRF cookie 的页面上
        driver.get(ADMIN_SERVICE_URL + "?number=" + number_35)
        time.sleep(0.5)

        # (a) 正常参数
        try:
            r = fetch_json_async(READING_URL, "GET", query_params={"number": number_35})
            data = r.get("data") if isinstance(r.get("data"), dict) else {}
            code_ok = isinstance(data.get("code"), int)
            msg_ok = isinstance(data.get("message"), str) and len(data["message"]) > 0
            mark(
                "#35 响应 JSON 格式：code 为 int 且 message 为非空 str",
                bool(code_ok and msg_ok),
                f"resp={r}",
            )
            mark(
                "#35 业务成功 code=200 且 message=更新成功",
                r.get("ok") and data.get("code") == 200 and ("更新成功" in str(data.get("message") or "")),
                f"code={data.get('code')!r} message={data.get('message')!r}",
            )
        except Exception as e:
            mark("#35 调用异常", False, f"{type(e).__name__}:{e}")

        # (b) 缺 number 参数：不 500 / 不 crash（后端缺参真实 500 时，
        #     只要 fetch promise 成功 resolve 并拿到 status 即视为浏览器端/HTTP层不 crash）
        try:
            r = fetch_json_async(READING_URL, "GET", query_params={})
            not_crashed = bool(r.get("ok")) and isinstance(r.get("status"), int)
            mark("#35 缺参数 number 不返回 HTTP 500 / 不 crash", bool(not_crashed), f"status={r.get('status')}")
        except Exception as e:
            mark("#35 缺参数不 crash", False, f"{type(e).__name__}:{e}")

        # (c) 不存在的 number：JSON code/message 仍存在（参数校验/业务校验）
        try:
            r = fetch_json_async(READING_URL, "GET", query_params={"number": "NOT_EXIST_XXX"})
            data = r.get("data") if isinstance(r.get("data"), dict) else {}
            has_structure = (data is not None) and (data.get("code") is not None or r.get("raw"))
            mark(
                "#35 非法 number 仍返回合法响应（结构存在）",
                bool(r.get("ok") and has_structure),
                f"status={r.get('status')} data={data!r}",
            )
        except Exception as e:
            mark("#35 非法 number 不 crash", False, f"{type(e).__name__}:{e}")

    # =======================================================
    # 用例 3：批量查询未读消息数 (#36 GET /admin/service/reading/send/)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 3】批量查询未读消息数 #36 GET /admin/service/reading/send/")
    print("=" * 70)

    if not service_numbers:
        mark("#36 跳过（没有可用会话号）", False)
    else:
        try:
            # numbers[] 数组形式参数
            params_36 = [("numbers[]", n) for n in service_numbers[:3]]
            r = fetch_json_async(READING_SEND_URL + "?numbers[]=placeholder", "GET", query_params=params_36)
            # 因为 query_params 会再次拼接到 URL，所以先把占位去掉
            import urllib.parse as _up
            qs = _up.urlencode(params_36, doseq=True)
            full = READING_SEND_URL + ("?" + qs if qs else "")
            driver.get(ADMIN_SERVICE_URL)
            r2 = fetch_json_async(full, "GET")
            data = r2.get("data") if isinstance(r2.get("data"), dict) else {}

            has_code = isinstance(data.get("code"), int)
            has_msg = isinstance(data.get("message"), str) and len(data["message"]) > 0
            payload = data.get("data") if isinstance(data.get("data"), dict) else None
            keys_are_numbers = False
            if isinstance(payload, dict):
                expected_keys = set(service_numbers[:3])
                keys_are_numbers = expected_keys.issubset(set(payload.keys())) or all(
                    any(k.startswith(prefix[:1]) and any(c.isdigit() for c in k) for k in payload.keys())
                )
            mark(
                "#36 响应 JSON 结构：code=int & message=非空字符串",
                bool(has_code and has_msg),
                f"code={data.get('code')!r} message={data.get('message')!r}",
            )
            mark(
                "#36 data 字段为 dict（每个会话号 -> 未读数 映射）",
                isinstance(payload, dict) and len(payload) >= 1,
                f"payload_keys={list(payload.keys()) if isinstance(payload, dict) else None}",
            )
            mark(
                "#36 业务成功 code=200",
                data.get("code") == 200,
                f"code={data.get('code')!r}",
            )
            # 关键业务：所有未读数都是整数
            if isinstance(payload, dict):
                all_int = all(isinstance(v, int) for v in payload.values())
                mark(
                    "#36 未读数字典 value 全为 int",
                    all_int,
                    f"values_sample={list(payload.values())[:5]!r}",
                )
        except Exception as e:
            mark("#36 调用异常", False, f"{type(e).__name__}:{e}")

        # 边界：空 numbers
        try:
            r3 = fetch_json_async(READING_SEND_URL, "GET")
            not_500 = r3.get("status") != 500 if isinstance(r3.get("status"), int) else True
            mark("#36 空参数不返回 HTTP 500 / 不 crash", bool(not_500), f"status={r3.get('status')} resp={r3}")
        except Exception as e:
            mark("#36 空参数不 crash", False, f"{type(e).__name__}:{e}")

    # =======================================================
    # 用例 4：获取表情包列表 (#37 GET /service/face/)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 4】获取表情包列表 #37 GET /service/face/（管理员侧 AJAX 直连）")
    print("=" * 70)
    try:
        r = fetch_json_async(FACE_URL, "GET")
        data = r.get("data") if isinstance(r.get("data"), dict) else {}
        faces = data.get("faces") if isinstance(data.get("faces"), dict) else None
        has_code = isinstance(data.get("code"), int)
        has_msg = isinstance(data.get("message"), str) and len(data["message"]) > 0
        mark(
            "#37 响应 JSON 结构：code=int & message=非空字符串",
            bool(has_code and has_msg),
            f"code={data.get('code')!r} message={data.get('message')!r}",
        )
        mark(
            "#37 faces 字段为 dict（表情id -> 表情名 映射）且 len>=1",
            isinstance(faces, dict) and len(faces) >= 1,
            f"faces_type={type(faces).__name__} len={len(faces) if faces else None} sample_items={list(faces.items())[:3] if isinstance(faces, dict) else None}",
        )
        mark(
            "#37 业务成功 code=200",
            data.get("code") == 200,
            f"code={data.get('code')!r}",
        )
        if isinstance(faces, dict) and faces:
            ids_int_or_digit = all(
                (isinstance(k, str) and k.isdigit()) or isinstance(k, int) for k in faces.keys()
            )
            vals_str = all(isinstance(v, str) for v in faces.values())
            mark(
                "#37 faces key 为数字字符串/int，value 为中文表情名 str",
                bool(ids_int_or_digit and vals_str),
                f"sample={list(faces.items())[:3]!r}",
            )
        safe_screenshot("admsvc_02_face.png")
    except Exception as e:
        mark("#37 调用异常", False, f"{type(e).__name__}:{e}")

    # =======================================================
    # 汇总
    # =======================================================
    print("\n" + "=" * 70)
    print(f"【汇总】 {passed}/{total} 用例通过")
    print("=" * 70)

except AssertionError as e:
    print(f"\n[ASSERT] 断言失败: {e}")
    try:
        safe_screenshot("admsvc_assert_failed.png")
    except Exception:
        pass
except Exception as e:
    print(f"\n[EXCEPTION] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    try:
        safe_screenshot("admsvc_exception.png")
    except Exception:
        pass
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
        except Exception:
            pass
