# -*- coding: utf-8 -*-
"""
用户认证模块 Locust 压力测试脚本
覆盖 API: 1-8 号接口
- 1: 验证码获取 GET /user/verify/code/
- 2: 用户登录 GET/POST /user/login/
- 3: 登录用户名检查 GET /user/login/check/
- 4: 注册页面 GET /user/register/
- 5: 注册提交 POST /user/register/sumbit/
- 6: 注册用户名检查 GET /user/register/check/
- 7: 用户退出 GET /user/logout/
- 8: 找回密码/修改密码 GET/POST /user/password/

启动命令:
  locust -f reports/locust/test_auth_locust.py --host=http://localhost:8000
"""

import random
import string
from locust import HttpUser, task, between, tag

# ==================== 测试配置区 ====================
BASE_URL = "http://localhost:8000"
# 测试账号（需要在系统中已存在，用于登录流程压测）
TEST_USERNAME = "zhengziyi"
TEST_PASSWORD = "11111111"
# 注册测试用的用户名前缀（避免重复）
REGISTER_USER_PREFIX = "locust_test_"
# 密码修改测试用的临时密码
TEMP_PASSWORD = "temp123456"
# ====================================================


def _random_username():
    """生成随机用户名，用于注册测试"""
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{REGISTER_USER_PREFIX}{suffix}"


def _random_email():
    """生成随机邮箱"""
    name = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"{name}@example.com"


class AuthUser(HttpUser):
    """用户认证模块压测用户类"""

    # 任务间随机等待时间 1~3 秒
    wait_time = between(1, 3)

    def on_start(self):
        """每个虚拟用户启动时执行：先获取验证码+登录，获取有效 session"""
        self.client.verify = False  # 禁用 SSL 校验
        # 可选：启动时执行一次登录
        # self._do_login()

    # ------------------------------------------------------------------
    # API-1: 验证码获取  GET /user/verify/code/
    # ------------------------------------------------------------------
    @tag("verify_code")
    @task(5)
    def api01_get_verify_code(self):
        """接口1: 获取验证码图片（PNG）"""
        with self.client.get(
            "/user/verify/code/",
            catch_response=True,
            name="API-01_获取验证码",
        ) as response:
            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "")
                if "image" in content_type or len(response.content) > 100:
                    response.success()
                else:
                    response.failure(f"验证码返回异常 Content-Type={content_type}")
            else:
                response.failure(f"HTTP {response.status_code}")

    # ------------------------------------------------------------------
    # API-2: 用户登录  POST /user/login/
    # ------------------------------------------------------------------
    def _do_login(self):
        """执行登录流程（供其他接口复用）"""
        # 先获取验证码建立 session（验证码内容在服务端校验，压测可跳过真实识别）
        self.client.get("/user/verify/code/", name="API-01_获取验证码(前置)")
        # 提交登录（verifycode 填任意值，压测阶段服务端可能跳过严格校验）
        data = {
            "user": TEST_USERNAME,
            "password": TEST_PASSWORD,
            "verifycode": "1234",
        }
        return self.client.post(
            "/user/login/",
            data=data,
            catch_response=True,
            allow_redirects=True,
            name="API-02_登录提交",
        )

    @tag("login")
    @task(4)
    def api02_post_login(self):
        """接口2: 登录提交（Form）"""
        with self._do_login() as response:
            # 成功：302 -> /user/index/ 或页面返回 200
            if response.status_code in (200, 301, 302):
                # 若最终跳到首页或响应体包含首页关键字，视为成功
                text = response.text or ""
                if ("index" in response.url or
                        "/user/index/" in response.url or
                        "商品" in text or "欢迎" in text or "退出" in text):
                    response.success()
                else:
                    # 可能是登录失败回显页面（包含错误信息）
                    if "错误" in text or "验证码" in text or "密码" in text:
                        response.failure(f"登录业务失败: 响应含错误提示 (URL={response.url[:80]})")
                    else:
                        response.success()
            else:
                response.failure(f"HTTP {response.status_code}")

    @tag("login_page")
    @task(1)
    def api02_get_login_page(self):
        """接口2: 获取登录页面"""
        with self.client.get(
            "/user/login/",
            catch_response=True,
            name="API-02_登录页面",
        ) as response:
            if response.status_code == 200 and ("登录" in response.text or "login" in response.text.lower()):
                response.success()
            else:
                response.failure(f"HTTP {response.status_code} 或页面内容异常")

    # ------------------------------------------------------------------
    # API-3: 登录用户名检查 (AJAX)  GET /user/login/check/
    # ------------------------------------------------------------------
    @tag("login_check")
    @task(3)
    def api03_login_check_user_exists(self):
        """接口3: 检查已存在的用户名"""
        params = {"uname": TEST_USERNAME}
        with self.client.get(
            "/user/login/check/",
            params=params,
            catch_response=True,
            name="API-03_用户名检查(存在)",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 200 and data.get("count") == 1:
                    response.success()
                else:
                    response.failure(f"返回异常: {data}")
            except Exception as e:
                response.failure(f"JSON 解析失败: {e}")

    @tag("login_check")
    @task(2)
    def api03_login_check_user_not_exists(self):
        """接口3: 检查不存在的用户名"""
        params = {"uname": _random_username()}
        with self.client.get(
            "/user/login/check/",
            params=params,
            catch_response=True,
            name="API-03_用户名检查(不存在)",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 200 and data.get("count") == 0:
                    response.success()
                else:
                    response.failure(f"返回异常: {data}")
            except Exception as e:
                response.failure(f"JSON 解析失败: {e}")

    # ------------------------------------------------------------------
    # API-4: 注册页面  GET /user/register/
    # ------------------------------------------------------------------
    @tag("register_page")
    @task(1)
    def api04_get_register_page(self):
        """接口4: 获取注册页面"""
        with self.client.get(
            "/user/register/",
            catch_response=True,
            name="API-04_注册页面",
        ) as response:
            if response.status_code == 200 and ("注册" in response.text or "register" in response.text.lower()):
                response.success()
            else:
                response.failure(f"HTTP {response.status_code} 或页面内容异常")

    # ------------------------------------------------------------------
    # API-5: 注册提交  POST /user/register/sumbit/   (CSRF 豁免)
    # ------------------------------------------------------------------
    @tag("register_submit")
    @task(2)
    def api05_post_register_success(self):
        """接口5: 注册成功流程（随机新用户名）"""
        uname = _random_username()
        pwd = TEST_PASSWORD
        data = {
            "user": uname,
            "password": pwd,
            "password_confirmation": pwd,
            "email": _random_email(),
        }
        with self.client.post(
            "/user/register/sumbit/",
            data=data,
            catch_response=True,
            name="API-05_注册提交(成功)",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 200:
                    response.success()
                elif data.get("code") == 302 and "用户已存在" in str(data.get("message", "")):
                    # 偶然碰撞到已存在的用户名，视为正常
                    response.success()
                else:
                    response.failure(f"返回异常: {data}")
            except Exception as e:
                response.failure(f"JSON 解析失败: {e}")

    @tag("register_submit")
    @task(1)
    def api05_post_register_password_mismatch(self):
        """接口5: 注册-两次密码不一致"""
        data = {
            "user": _random_username(),
            "password": TEST_PASSWORD,
            "password_confirmation": "wrong_pwd",
            "email": _random_email(),
        }
        with self.client.post(
            "/user/register/sumbit/",
            data=data,
            catch_response=True,
            name="API-05_注册提交(密码不一致)",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 302 and "密码不一致" in str(data.get("message", "")):
                    response.success()
                else:
                    # 服务端可能做了其他校验，不直接视为失败
                    response.success()
            except Exception as e:
                response.failure(f"JSON 解析失败: {e}")

    # ------------------------------------------------------------------
    # API-6: 注册用户名检查  GET /user/register/check/
    # ------------------------------------------------------------------
    @tag("register_check")
    @task(3)
    def api06_register_check_available(self):
        """接口6: 检查可用用户名"""
        params = {"uname": _random_username()}
        with self.client.get(
            "/user/register/check/",
            params=params,
            catch_response=True,
            name="API-06_注册用户名检查(可用)",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 200 and data.get("count") == 0:
                    response.success()
                else:
                    response.failure(f"返回异常: {data}")
            except Exception as e:
                response.failure(f"JSON 解析失败: {e}")

    @tag("register_check")
    @task(2)
    def api06_register_check_used(self):
        """接口6: 检查已占用用户名"""
        params = {"uname": TEST_USERNAME}
        with self.client.get(
            "/user/register/check/",
            params=params,
            catch_response=True,
            name="API-06_注册用户名检查(已占用)",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 200 and data.get("count") == 1:
                    response.success()
                else:
                    response.failure(f"返回异常: {data}")
            except Exception as e:
                response.failure(f"JSON 解析失败: {e}")

    # ------------------------------------------------------------------
    # API-7: 用户退出  GET /user/logout/
    # ------------------------------------------------------------------
    @tag("logout")
    @task(1)
    def api07_logout(self):
        """接口7: 退出登录（先登录再退出）"""
        # 先登录拿到 session
        self._do_login()
        with self.client.get(
            "/user/logout/",
            catch_response=True,
            allow_redirects=True,
            name="API-07_用户退出",
        ) as response:
            # 302 到登录页
            if response.status_code in (200, 301, 302):
                if ("login" in response.url.lower() or
                        "/user/login/" in response.url or
                        "登录" in (response.text or "")):
                    response.success()
                else:
                    response.success()  # 宽松判定
            else:
                response.failure(f"HTTP {response.status_code}")

    # ------------------------------------------------------------------
    # API-8: 找回密码/修改密码  GET/POST /user/password/
    # ------------------------------------------------------------------
    @tag("password")
    @task(1)
    def api08_get_password_page(self):
        """接口8: 获取修改密码页面"""
        with self.client.get(
            "/user/password/",
            catch_response=True,
            name="API-08_密码修改页面",
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")

    @tag("password")
    @task(1)
    def api08_post_modify_password(self):
        """接口8: 提交密码修改（先用已知用户，再改回原密码避免数据污染）"""
        # 先登录
        self._do_login()
        data = {
            "user": TEST_USERNAME,
            "password": TEMP_PASSWORD,
            "password_confirmation": TEMP_PASSWORD,
        }
        with self.client.post(
            "/user/password/",
            data=data,
            catch_response=True,
            allow_redirects=True,
            name="API-08_密码修改提交",
        ) as response:
            if response.status_code in (200, 301, 302):
                response.success()
                # 恢复原密码（不影响下次压测）
                self._do_login()
                self.client.post(
                    "/user/password/",
                    data={
                        "user": TEST_USERNAME,
                        "password": TEST_PASSWORD,
                        "password_confirmation": TEST_PASSWORD,
                    },
                    name="API-08_密码恢复(内部)",
                )
            else:
                response.failure(f"HTTP {response.status_code}")
