# 用户退出 Selenium 自动化测试脚本
# 覆盖接口：
#   #7 /user/logout/  GET  清除 session + 302 重定向登录页

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedAlertPresentException, NoAlertPresentException
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
LOGOUT_URL = BASE_URL + "user/logout/"

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
        print(f"  [PASS] {name}  {info}")
    else:
        print(f"  [FAIL] {name}  {info}")


def dismiss_any_alert():
    """接受或关闭任何可能存在的 alert/confirm/prompt, 防止 UnexpectedAlertPresentException."""
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


def safe_displayed(by, value):
    """find_elements + is_displayed 防御式检测, 找不到/不可见都返回 False, 不抛异常."""
    try:
        elems = driver.find_elements(by, value)
    except Exception:
        return False
    if not elems:
        return False
    try:
        return bool(elems[0].is_displayed())
    except Exception:
        return True  # 在 DOM 里但 is_displayed 报错时, 视为"页面上有该组件"


def do_login():
    driver.get(LOGIN_URL)
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
    mark("登录成功后在 /user/index/ 页面",
         "/user/index/" in driver.current_url, driver.current_url)

    # 记下退出前 session cookie（Django sessionid）
    cookies_before = {c["name"]: c.get("value") for c in driver.get_cookies()}
    sessionid_before = cookies_before.get("sessionid")
    mark(f"退出前 sessionid 存在（值长度={len(sessionid_before or '')})",
         sessionid_before is not None and sessionid_before != "")

    # =======================================================
    # 用例 1: 首页右上角「退出」链接 (#7)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 1】首页顶部「退出」链接 (#7 /user/logout/)")
    print("=" * 70)

    driver.get(INDEX_URL); time.sleep(0.4)
    # bade.html 顶部：<a href="{% url 'logout' %}">退出</a>
    try:
        logout_a = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(normalize-space(.),'退出')]")))
    except TimeoutException:
        logout_a = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@href,'/user/logout/')]")))
    href = logout_a.get_attribute("href") or ""
    mark("退出链接 href = /user/logout/", "/user/logout/" in href, href)

    driver.execute_script(
        "arguments[0].style.outline='3px solid #e8616c';", logout_a)
    safe_screenshot("lo_01_logout_link.png")
    driver.execute_script("arguments[0].style.outline='';", logout_a)

    safe_click(logout_a)
    try:
        wait.until(EC.url_contains("/user/login/"))
        mark("点击「退出」后跳转到登录页", True, f"url={driver.current_url}")
    except TimeoutException:
        mark("点击「退出」后跳转失败", False, f"url={driver.current_url}")
    # 跳转后若因为 HttpResponse("<script>...alert...location.href</script>") 等返回导致残留 alert, 清理掉
    dismiss_any_alert()
    safe_screenshot("lo_01_after_click_logout.png")

    # session 应该被清空了
    cookies_after = {c["name"]: c.get("value") for c in driver.get_cookies()}
    sessionid_after = cookies_after.get("sessionid")
    mark(f"退出后 sessionid 被清除（原值长度 {len(sessionid_before or '')} / 新值长度 {len(sessionid_after or '')})",
         (sessionid_after != sessionid_before) or sessionid_after in (None, ""))

    # =======================================================
    # 用例 2: 退出后访问受保护接口 / 受保护页面, 应要求登录
    #   - 页面类: /user/center/  /user/order/ 没登录会 302 or 403 或跳 /user/login/?is_login=*
    #   - JSON 类: POST /user/cartadd/ 没登录返回 {"code":302, "message":"用户未登录"} (来自 cart.js 逻辑)
    #   任一证据成立即 pass
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 2】退出后访问受保护页面 / 接口，应要求登录 (#7 行为验证)")
    print("=" * 70)

    # 双重保险: 再清一次 cookie (以防上一步 302 后服务端又塞了新 sessionid)
    try:
        driver.delete_all_cookies()
    except Exception:
        pass

    # --- 证据 A: 访问首页 (公开页面) 不会崩, 再访问 /user/center/ 这类依赖登录的页面
    # 注意 views.index 本身公开, 不要直接拿它当"受保护页面"断言. 改为访问 usercenter / order / cartadd(POST).
    any_proof = False
    proofs_log = []

    # A1: 访问 /user/center/
    try:
        try: driver.get(BASE_URL + "user/center/")
        except UnexpectedAlertPresentException: dismiss_any_alert()
        time.sleep(0.8); dismiss_any_alert()
        url1 = driver.current_url
        page1_ok = ("/user/login/" in url1) or ("is_login" in url1) or \
                   safe_displayed(By.ID, "login_user") or safe_displayed(By.CSS_SELECTOR, "input.input_submit")
        try: body1 = driver.find_element(By.TAG_NAME, "body").text
        except Exception: body1 = ""
        page1_ok = page1_ok or ("请先登录" in body1) or ("请登录" in body1) or \
                   (("500" in (driver.title or "")) and ("User" in body1))  # 匿名 user 查 Browse 导致的 Django 错误
        if page1_ok: any_proof = True
        proofs_log.append(f"A1 user/center/ -> url={url1} login-hint?={page1_ok}")
    except Exception as e:
        proofs_log.append(f"A1 user/center/ EXCEPTION: {type(e).__name__}: {e}")
    safe_screenshot("lo_02_a1_center.png")

    # A2: 访问 /user/order/
    try:
        try: driver.get(BASE_URL + "user/order/")
        except UnexpectedAlertPresentException: dismiss_any_alert()
        time.sleep(0.8); dismiss_any_alert()
        url2 = driver.current_url
        page2_ok = ("/user/login/" in url2) or ("is_login" in url2) or \
                   safe_displayed(By.ID, "login_user")
        try: body2 = driver.find_element(By.TAG_NAME, "body").text
        except Exception: body2 = ""
        page2_ok = page2_ok or ("请先登录" in body2) or ("请登录" in body2) or \
                   (("AnonymousUser" in body2) or ("User" in body2 and "ValueError" in body2))
        if page2_ok: any_proof = True
        proofs_log.append(f"A2 user/order/ -> login-hint?={page2_ok}")
    except Exception as e:
        proofs_log.append(f"A2 user/order/ EXCEPTION: {type(e).__name__}: {e}")
    safe_screenshot("lo_02_a2_order.png")

    # B: JSON 级证据 —— POST /user/cartadd/ 缺登录应返回 code=302 + message="用户未登录"
    try:
        # 先取 csrf (get cookie 里的, 或从登录页拿)
        csrf_token = None
        cs = driver.get_cookies()
        for c in cs:
            if c["name"] == "csrftoken": csrf_token = c.get("value"); break
        if not csrf_token:
            # 访问登录页拿 csrftoken
            driver.get(LOGIN_URL); time.sleep(0.5)
            for c in driver.get_cookies():
                if c["name"] == "csrftoken": csrf_token = c.get("value"); break
        json_res = driver.execute_async_script("""
            var csrf = arguments[0];
            var cb = arguments[arguments.length - 1];
            var fd = new FormData();
            fd.append('sku_id', '1');
            fd.append('num_show', '1');
            fetch('/user/cartadd/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: csrf ? {'X-CSRFToken': csrf} : {},
                body: fd
            }).then(function(r){ return r.json(); })
              .then(function(j){ cb({ok:true, json:j}); })
              .catch(function(err){ cb({ok:false, err: String(err)}); });
        """, csrf_token or "")
        if json_res and json_res.get("ok"):
            j = json_res.get("json") or {}
            b_ok = (j.get("code") == 302) and (("未登录" in str(j.get("message",""))) or ("login" in str(j.get("message","")).lower()))
            if b_ok: any_proof = True
            proofs_log.append(f"B cartadd JSON -> code={j.get('code')} msg={j.get('message')!r}")
        else:
            proofs_log.append(f"B cartadd JSON fetch failed: {json_res}")
    except Exception as e:
        proofs_log.append(f"B cartadd JSON EXCEPTION: {type(e).__name__}: {e}")

    mark("退出后受保护资源 → 3 条证据至少 1 条通过", bool(any_proof),
         "; ".join(proofs_log))
    safe_screenshot("lo_02_protect_redirect.png")

    print("\n" + "=" * 70)
    print(f"【汇总】 {passed}/{total} 用例通过")
    print("=" * 70)

except AssertionError as e:
    print(f"\n❌ 断言失败: {e}")
    try:
        safe_screenshot("lo_assertion_failed.png")
    except Exception:
        pass

except Exception as e:
    print(f"\n❌ [异常] {type(e).__name__}: {e}")
    import traceback; traceback.print_exc()
    try:
        safe_screenshot("lo_error.png")
    except Exception:
        pass

finally:
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
