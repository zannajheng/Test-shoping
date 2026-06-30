# 注册界面 Selenium 自动化测试脚本
# 覆盖接口：
#   #1 GET  /user/verify/code/       验证码图片
#   #4 GET  /user/register/          注册页面
#   #5 POST /user/register/sumbit/   注册提交 (CSRF exempt)
#   #6 GET  /user/register/check/    注册用户名检查 (AJAX)

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

# ========== 测试配置 ==========
# 每次运行都换一个全新用户名（加时间戳），避免"用户已存在"导致第 5 步提交中断
_ts = int(time.time())
USERNAME = "zanna_test_%d" % _ts
PASSWORD = "11111111"
PASSWORD_CONFIRM = "11111111"
BASE_URL = "http://127.0.0.1:8000/"
REGISTER_URL = BASE_URL + "user/register/"
REGISTER_CHECK_URL = BASE_URL + "user/register/check/"
REGISTER_SUBMIT_URL = BASE_URL + "user/register/sumbit/"
VERIFY_URL = BASE_URL + "user/verify/code/"
LOGIN_URL_AFTER_REG = BASE_URL + "user/login/"

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


# ========== 初始化驱动 ==========
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


try:
    # ========== 1. #4 GET 注册页 ==========
    print("=" * 70)
    print("[1/7] #4 GET /user/register/ 打开注册页面")
    print("=" * 70)
    driver.get(REGISTER_URL)
    try:
        driver.maximize_window()
    except Exception:
        try:
            driver.set_window_size(1600, 1200)
        except Exception:
            pass

    wait.until(EC.presence_of_element_located((By.ID, "user_name")))
    mark("#4 注册页渲染成功（#user_name 输入框已出现）", True,
         f"url={driver.current_url}")
    safe_screenshot("register_page_before.png")

    # ========== 2. #1 GET 验证码图片接口 ==========
    print("\n" + "=" * 70)
    print("[2/7] #1 GET /user/verify/code/ 验证码图片请求")
    print("=" * 70)
    try:
        vc_img = None
        for sel in ((By.CSS_SELECTOR, "img[src*='verify']"),
                    (By.CSS_SELECTOR, "img[src*='code']"),
                    (By.XPATH, "//*[contains(@id,'verify') or contains(@class,'verify')]/img")):
            xs = driver.find_elements(*sel)
            if xs:
                vc_img = xs[0]
                break
        if vc_img is None:
            check_js = (
                "var cb = arguments[arguments.length - 1];"
                "fetch(" + repr(VERIFY_URL) + ",{credentials:'include'})"
                ".then(function(r){"
                " return r.blob().then(function(b){ cb({ok:true,status:r.status,type:b.type,size:b.size}); });"
                "}).catch(function(e){ cb({ok:false,err:'fetch:'+String(e)}); });"
            )
            r = driver.execute_async_script(check_js)
            ok = (r.get("ok") and isinstance(r.get("status"), int) and 200 <= int(r["status"]) < 400)
            is_img = isinstance(r.get("type"), str) and "image" in r["type"]
            mark("#1 验证码接口 2xx 且返回 image/*", bool(ok and is_img),
                 f"status={r.get('status')} type={r.get('type')!r} size={r.get('size')}")
        else:
            src = vc_img.get_attribute("src") or ""
            mark("#1 注册页含验证码图片，src 含 verify/code 片段",
                 "verify" in src or "code" in src, f"src={src!r}")
    except Exception as e:
        mark("#1 验证码访问异常", False, f"{type(e).__name__}:{e}")

    # ========== 3. #6 GET 注册用户名检查 AJAX ==========
    print("\n" + "=" * 70)
    print("[3/7] #6 GET /user/register/check/ 注册用户名检查 AJAX")
    print("=" * 70)
    try:
        check_js = (
            "var cb = arguments[arguments.length - 1];"
            "var U1 = " + repr(REGISTER_CHECK_URL + "?uname=" + USERNAME) + ";"
            "var U2 = " + repr(REGISTER_CHECK_URL + "?uname=admin") + ";"
            "Promise.all([fetch(U1,{credentials:'include'}),fetch(U2,{credentials:'include'})])"
            ".then(function(rs){ return Promise.all(rs.map(function(r){return r.json()})); })"
            ".then(function(arr){ cb({ok:true,new_user:arr[0],exist_user:arr[1]}); })"
            ".catch(function(e){ cb({ok:false,err:'fetch:'+String(e)}); });"
        )
        r = driver.execute_async_script(check_js)
        if r.get("ok"):
            new_ok = (isinstance(r.get("new_user"), dict) and r["new_user"].get("code") == 200 and r["new_user"].get("count") == 0)
            ex_ok = (isinstance(r.get("exist_user"), dict) and r["exist_user"].get("code") == 200 and r["exist_user"].get("count") == 1)
            mark(f"#6 新用户 {USERNAME}: code=200 / count=0 (可用)", bool(new_ok), f"resp={r.get('new_user')!r}")
            mark("#6 已存在用户 admin: code=200 / count=1 (被占用)", bool(ex_ok), f"resp={r.get('exist_user')!r}")
        else:
            mark("#6 /user/register/check/ AJAX 失败", False, f"resp={r}")
    except Exception as e:
        mark("#6 注册用户名检查异常", False, f"{type(e).__name__}:{e}")

    # ========== 4. 表单填写 ==========
    print("\n" + "=" * 70)
    print(f"[4/7] 填写注册表单 user={USERNAME}")
    print("=" * 70)
    user_input = wait.until(EC.element_to_be_clickable((By.ID, "user_name")))
    user_input.clear(); user_input.send_keys(USERNAME)
    try:
        driver.execute_script("$(arguments[0]).blur();", user_input)
    except Exception:
        user_input.send_keys("\t")
    time.sleep(0.6)

    pwd_input = wait.until(EC.element_to_be_clickable((By.ID, "pwd")))
    pwd_input.clear(); pwd_input.send_keys(PASSWORD)

    cpwd_input = wait.until(EC.element_to_be_clickable((By.ID, "cpwd")))
    cpwd_input.clear(); cpwd_input.send_keys(PASSWORD_CONFIRM)

    # 有些模板里有邮箱字段，有些没有，不影响注册成功
    try:
        email_input = driver.find_element(By.ID, "email")
        if email_input.is_displayed():
            email_input.clear()
    except Exception:
        pass
    mark("用户名/密码/确认密码 填写成功", True)
    safe_screenshot("register_page_filled.png")

    # ========== 5. #5 POST 注册提交 (button.click -> AJAX POST -> login 页) ==========
    print("\n" + "=" * 70)
    print("[5/7] #5 POST /user/register/sumbit/ 点击注册按钮提交")
    print("=" * 70)
    submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "button")))
    submit_btn.click()
    mark("#5 注册提交按钮点击成功（无异常）", True)

    # ========== 6. 验证 #5 POST 结果 302 -> /user/login/ ==========
    print("\n" + "=" * 70)
    print("[6/7] 验证 #5 POST 结果 302 -> /user/login/")
    print("=" * 70)
    try:
        wait.until(EC.url_contains("/user/login/"))
        mark("#5 注册成功后跳转到登录页", True, f"url={driver.current_url}")
        time.sleep(0.8)
        safe_screenshot("register_success_to_login.png")
    except TimeoutException:
        cur = driver.current_url
        emsgs = []
        for sel in ("#user_name + .error_tip", "#pwd + .error_tip", "#cpwd + .error_tip",
                    ".error_tip", ".error", "#message"):
            try:
                e = driver.find_element(By.CSS_SELECTOR, sel)
                if e.is_displayed() and e.text.strip():
                    emsgs.append(f"{sel}:{e.text.strip()}")
            except Exception:
                continue
        info = f"url={cur} ; errors={emsgs}"
        mark("#5 注册后未跳转登录页（检查密码/用户已存在/模板差异）", False, info)
        safe_screenshot("register_failed.png")

    # ========== 7. 汇总 ==========
    print("\n" + "=" * 70)
    print(f"【汇总】 {passed}/{total} 用例通过")
    print("=" * 70)

except Exception as e:
    print(f"\n[异常] 脚本执行出错: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    safe_screenshot("register_error.png")

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
