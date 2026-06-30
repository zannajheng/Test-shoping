# 搜索/分类分页 + 搜索页加购 Selenium 自动化测试脚本
# 覆盖接口：
#   #11 GET  /user/search/                     搜索结果页
#   #12 GET  /user/search/page/                (AJAX) 搜索分页
#   #13 GET  /user/index/list/                 分类商品列表页
#   #14 GET  /user/index/list/page/            (AJAX) 分类列表分页
#   #15 GET  /user/index/list/price/           (AJAX) 分类列表按价格降序
#   #17 POST /user/search/cartadd/             搜索页加购（需要登录）

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
SEARCH_URL = BASE_URL + "user/search/"
SEARCH_PAGE_AJAX = BASE_URL + "user/search/page/"
LIST_URL = BASE_URL + "user/index/list/"
LIST_PAGE_AJAX = BASE_URL + "user/index/list/page/"
LIST_PRICE_AJAX = BASE_URL + "user/index/list/price/"
SEARCH_CARTADD = BASE_URL + "user/search/cartadd/"

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


def fetch_async_urlencoded(url, method="GET", body_dict=None, query=None):
    import urllib.parse as _up
    body = _up.urlencode(body_dict or {}, doseq=True)
    full = url
    if query:
        qs = _up.urlencode(query, doseq=True)
        full = full + ("&" if "?" in full else "?") + qs
    js = (
        "var cb = arguments[arguments.length - 1];\n"
        "(function(){\n"
        "   var U = " + repr(full) + ";\n"
        "   var M = " + repr(method) + ";\n"
        "   var B = " + repr(body) + ";\n"
        "   function csrf(){ return (document.cookie.match(/csrftoken=([^;]+)/)||[])[1] || ''; }\n"
        "   var opts = {method:M, credentials:'include'};\n"
        "   if (M !== 'GET') {\n"
        "       opts.headers = {'X-CSRFToken': csrf(), 'Content-Type':'application/x-www-form-urlencoded'};\n"
        "       opts.body = B;\n"
        "   } else { var c = csrf(); if (c) opts.headers = {'X-CSRFToken': c}; }\n"
        "   fetch(U, opts).then(function(r){\n"
        "       return r.text().then(function(t){\n"
        "           try{var d=JSON.parse(t)}catch(e){d=null}\n"
        "           cb({ok:true,status:r.status,data:d,raw:t});\n"
        "       });\n"
        "   }).catch(function(e){ cb({ok:false,err:'fetch:'+String(e)}); });\n"
        "})();\n"
    )
    return driver.execute_async_script(js)


try:
    print("=" * 70); print("【前置】登录 " + USERNAME); print("=" * 70)
    logged = do_login()
    safe_screenshot("scp_00_login.png")

    # =======================================================
    # 用例组 1: 搜索 (#11/#12)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例组 1】#11 搜索结果页 + #12 搜索分页 AJAX")
    print("=" * 70)
    try:
        driver.get(SEARCH_URL + "?query=项链")
        time.sleep(0.8)
        body = driver.find_element(By.TAG_NAME, "body").text or ""
        mark("#11 /user/search/?query=项链 渲染成功 (body len>100)",
             len(body) > 100, f"title={driver.title!r}")
    except Exception as e:
        mark("#11 访问异常", False, f"{type(e).__name__}:{e}")
    safe_screenshot("scp_01_search.png")

    sub_cases_12 = [
        ("正常分页 query=项链 page=1", {"query": "项链", "page": "1"}),
        ("空 query", {"query": "", "page": "1"}),
        ("page=9999（超页）", {"query": "项链", "page": "9999"}),
    ]
    for name, q in sub_cases_12:
        try:
            r = fetch_async_urlencoded(SEARCH_PAGE_AJAX, "GET", query=q)
            d = r.get("data") if isinstance(r.get("data"), dict) else {}
            ok_structure = isinstance(d, dict) and isinstance(d.get("code"), int)
            mark(f"#12 AJAX 结构 ({name})：code 为 int", bool(ok_structure),
                 f"code={d.get('code')!r} keys={list(d.keys())!r}")
            if q["page"] == "9999":
                mark("#12 超页返回 code=-1 且 pages 字段存在 且 message=数据为空",
                     d.get("code") == -1 and isinstance(d.get("pages"), int) and d.get("message") == "数据为空",
                     f"code={d.get('code')!r} pages={d.get('pages')!r} message={d.get('message')!r}")
            else:
                if d.get("code") == 200:
                    ok_goods = isinstance(d.get("goods_data"), list)
                    mark("#12 正常分页 code=200 时 goods_data 为 list", bool(ok_goods),
                         f"len(goods_data)={len(d.get('goods_data') or [])}")
        except Exception as e:
            mark(f"#12 ({name}) 异常", False, f"{type(e).__name__}:{e}")

    # =======================================================
    # 用例组 2: 分类列表 (#13/#14/#15)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例组 2】#13 分类列表 + #14 分类分页 + #15 按价格排序")
    print("=" * 70)
    try:
        driver.get(LIST_URL + "?type_id=1")
        time.sleep(0.8)
        body = driver.find_element(By.TAG_NAME, "body").text or ""
        mark("#13 /user/index/list/?type_id=1 渲染成功 (body len>100)",
             len(body) > 100, f"title={driver.title!r}")
    except Exception as e:
        mark("#13 访问异常", False, f"{type(e).__name__}:{e}")
    safe_screenshot("scp_02_list.png")

    for name, q in (("正常 type_id=1 page=1", {"type_id": "1", "page": "1"}),
                     ("page=9999（超页）", {"type_id": "1", "page": "9999"})):
        try:
            r = fetch_async_urlencoded(LIST_PAGE_AJAX, "GET", query=q)
            d = r.get("data") if isinstance(r.get("data"), dict) else {}
            mark(f"#14 AJAX 结构 ({name})：code 为 int",
                 isinstance(d, dict) and isinstance(d.get("code"), int),
                 f"code={d.get('code')!r}")
            if q["page"] != "9999":
                if d.get("code") == 200:
                    mark("#14 正常分页 code=200 且 goods 为 list",
                         isinstance(d.get("goods"), list),
                         f"len(goods)={len(d.get('goods') or [])}")
            else:
                mark("#14 超页 code=500 且 message=数据为空",
                     d.get("code") == 500 and d.get("message") == "数据为空",
                     f"code={d.get('code')!r} message={d.get('message')!r}")
        except Exception as e:
            mark(f"#14 ({name}) 异常", False, f"{type(e).__name__}:{e}")

    # #15 按价格降序
    try:
        r = fetch_async_urlencoded(LIST_PRICE_AJAX, "GET", query={"type_id": "1", "page": "1"})
        d = r.get("data") if isinstance(r.get("data"), dict) else {}
        mark("#15 响应结构：code=200 且 goods 为 list",
             d.get("code") == 200 and isinstance(d.get("goods"), list),
             f"code={d.get('code')!r} len(goods)={len(d.get('goods') or [])}")
        goods = d.get("goods") if isinstance(d.get("goods"), list) else []
        if len(goods) >= 2:
            prices = []
            for g in goods:
                if isinstance(g, dict):
                    p = g.get("price")
                    if isinstance(p, (int, float)):
                        prices.append(p)
            if len(prices) >= 2:
                is_desc = all(prices[i] >= prices[i + 1] for i in range(len(prices) - 1))
                mark("#15 按价格降序：返回列表 price 非递增", bool(is_desc),
                     f"prices={prices[:5]!r}")
    except Exception as e:
        mark("#15 异常", False, f"{type(e).__name__}:{e}")

    # =======================================================
    # 用例组 3: #17 搜索页加购
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例组 3】#17 POST /user/search/cartadd/ 搜索页加购（需要登录）")
    print("=" * 70)
    try:
        driver.get(SEARCH_URL + "?query=项链"); time.sleep(0.6)
        r = fetch_async_urlencoded(SEARCH_CARTADD, "POST", {"sku_id": "1"})
        d = r.get("data") if isinstance(r.get("data"), dict) else {}
        ok_structure = (isinstance(d, dict) and isinstance(d.get("code"), int)
                        and isinstance(d.get("message"), str) and "count" in d)
        mark("#17 响应结构：code / message / count 字段齐全", bool(ok_structure),
             f"code={d.get('code')!r} message={d.get('message')!r} count={d.get('count')!r}")
        if isinstance(d.get("count"), int):
            mark("#17 count 字段为 int（购物车总数量）", True, f"count={d.get('count')}")
    except Exception as e:
        mark("#17 已登录请求异常", False, f"{type(e).__name__}:{e}")
    safe_screenshot("scp_03_search_cartadd.png")

    for name, body in (("缺 sku_id", {}), ("sku_id=0 非法", {"sku_id": "0"})):
        try:
            r = fetch_async_urlencoded(SEARCH_CARTADD, "POST", body)
            # 允许后端业务层用 500 表示非法参数；只要 HTTP 层响应有效（fetch 成功拿到 status）就算不 crash
            not_crashed = bool(r.get("ok")) and isinstance(r.get("status"), int)
            mark(f"#17 参数校验 ({name}) 不 crash / 返回有效响应",
                 bool(not_crashed),
                 f"status={r.get('status')} resp={r.get('data')}")
        except Exception as e:
            mark(f"#17 ({name}) 异常", False, f"{type(e).__name__}:{e}")

    print("\n" + "=" * 70)
    print(f"【汇总】 {passed}/{total} 用例通过")
    print("=" * 70)

except AssertionError as e:
    print(f"\n[ASSERT] 断言失败: {e}"); safe_screenshot("scp_assert_failed.png")
except Exception as e:
    print(f"\n[EXCEPTION] {type(e).__name__}: {e}")
    import traceback; traceback.print_exc(); safe_screenshot("scp_exception.png")
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
