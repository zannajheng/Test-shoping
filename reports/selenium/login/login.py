# 登录界面 Selenium 自动化测试脚本
# 覆盖接口：
#   #1 GET  /user/verify/code/       验证码图片
#   #2 GET/POST /user/login/         登录页 + 登录提交
#   #3 GET  /user/login/check/       登录用户名检查 (AJAX)

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
USERNAME = "zhengziyi"       # 登录用户名
PASSWORD = "11111111"       # 登录密码
VERIFY_CODE = "1234"        # 验证码（后端校验已注释，随便填即可）
BASE_URL = "http://127.0.0.1:8000/"
LOGIN_URL = BASE_URL + "user/login/"
INDEX_URL = BASE_URL + "user/index/"
VERIFY_URL = BASE_URL + "user/verify/code/"   # #1 验证码
LOGIN_CHECK_URL = BASE_URL + "user/login/check/"  # #3 用户名检查 AJAX

passed = 0
total = 0
HERE = os.path.dirname(os.path.abspath(__file__))


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
# 优先使用本地 chromedriver（显式指定路径，跳过联网下载）
driver_path = r"D:\chrome-win64\chromedriver-win64\chromedriver.exe"

if os.path.exists(driver_path):
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
else:
    # 缓存路径兜底
    fallback_path = r"C:\Users\Zanna\.cache\selenium\chromedriver\win64\149.0.7827.155\chromedriver.exe"
    if os.path.exists(fallback_path):
        service = Service(executable_path=fallback_path)
        driver = webdriver.Chrome(service=service)
    else:
        # 最后退回 Selenium Manager 自动管理（需要能联网）
        driver = webdriver.Chrome()

# 显式等待工具（最多等待 10 秒，每 0.5 秒检查一次）
wait = WebDriverWait(driver, 10, 0.5)

try:
    # ========== 1. #2 GET 打开登录页面 ==========
    print("=" * 70)
    print("[1/7] #2 GET /user/login/ 打开登录页面")
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
    mark("#2 登录页渲染成功（用户名输入框已出现）", True, f"url={driver.current_url}")
    safe_screenshot("login_page_before.png")

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
            mark("#1 登录页含验证码图片，其 src 包含 verify/code 片段",
                 "verify" in src or "code" in src, f"src={src!r}")
    except Exception as e:
        mark("#1 验证码访问异常", False, f"{type(e).__name__}:{e}")

    # ========== 3. #3 GET 登录用户名检查 (AJAX) ==========
    print("\n" + "=" * 70)
    print("[3/7] #3 GET /user/login/check/ 登录用户名检查 AJAX")
    print("=" * 70)
    try:
        check_js = (
            "var cb = arguments[arguments.length - 1];"
            "var U1 = " + repr(LOGIN_CHECK_URL + "?uname=" + USERNAME) + ";"
            "var U2 = " + repr(LOGIN_CHECK_URL + "?uname=__user_not_exist_xyz_999__") + ";"
            "Promise.all([fetch(U1,{credentials:'include'}),fetch(U2,{credentials:'include'})])"
            ".then(function(rs){ return Promise.all(rs.map(function(r){return r.json()})); })"
            ".then(function(arr){ cb({ok:true,exist:arr[0],not_exist:arr[1]}); })"
            ".catch(function(e){ cb({ok:false,err:'fetch:'+String(e)}); });"
        )
        r = driver.execute_async_script(check_js)
        if r.get("ok"):
            e1 = isinstance(r.get("exist"), dict) and r["exist"].get("code") == 200 and r["exist"].get("count") == 1
            e2 = isinstance(r.get("not_exist"), dict) and r["not_exist"].get("code") == 200 and r["not_exist"].get("count") == 0
            mark(f"#3 已存在用户 {USERNAME}: code=200 / count=1", bool(e1), f"resp={r.get('exist')!r}")
            mark("#3 不存在用户: code=200 / count=0", bool(e2), f"resp={r.get('not_exist')!r}")
        else:
            mark("#3 /user/login/check/ AJAX 调用失败", False, f"resp={r}")
    except Exception as e:
        mark("#3 用户名检查异常", False, f"{type(e).__name__}:{e}")

    # ========== 4. 表单填写 ==========
    print("\n" + "=" * 70)
    print("[4/7] 填写用户名/密码/验证码")
    print("=" * 70)
    user_input = wait.until(EC.element_to_be_clickable((By.ID, "login_user")))
    user_input.clear(); user_input.send_keys(USERNAME)
    pwd_input = wait.until(EC.element_to_be_clickable((By.ID, "login_password")))
    pwd_input.clear(); pwd_input.send_keys(PASSWORD)
    vc_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.vc_input")))
    vc_input.clear(); vc_input.send_keys(VERIFY_CODE)
    mark("用户名/密码/验证码已填写", True)
    safe_screenshot("login_page_filled.png")

    # ========== 5. #2 POST 点击登录按钮 ==========
    print("\n" + "=" * 70)
    print("[5/7] #2 POST /user/login/ 点击登录按钮提交")
    print("=" * 70)
    submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input_submit")))
    submit_btn.click()
    mark("#2 POST 提交成功（无异常）", True)

    # ========== 6. 验证 #2 POST 结果 302 -> /user/index/ ==========
    print("\n" + "=" * 70)
    print("[6/7] 验证登录后 302 重定向至 /user/index/")
    print("=" * 70)
    try:
        wait.until(EC.url_contains("/user/index/"))
        current_url = driver.current_url
        mark("#2 POST 成功后 302 重定向到 /user/index/", True, f"url={current_url}")
        time.sleep(1)
        safe_screenshot("login_success.png")
    except TimeoutException:
        current_url = driver.current_url
        mark("#2 POST 后未跳转到首页", False, f"url={current_url}")
        try:
            msg_elem = driver.find_element(By.CSS_SELECTOR, ".login_message, .error_tip")
            print(f"  错误消息: {msg_elem.text}")
        except Exception:
            pass
        safe_screenshot("login_failed.png")

    # ========== 7. 汇总 ==========
    print("\n" + "=" * 70)
    print(f"【汇总】 {passed}/{total} 用例通过")
    print("=" * 70)

except Exception as e:
    print(f"\n[异常] 脚本执行出错: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    safe_screenshot("login_error.png")

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
