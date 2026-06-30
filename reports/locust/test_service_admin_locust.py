# -*- coding: utf-8 -*-
"""
客服模块 + 管理员接口 Locust 压力测试脚本
覆盖 API: 33-38 号接口（管理员接口需要 is_superuser=1 的账号）
- 33: 用户客服聊天页            GET  /service/
- 34: 管理员客服后台            GET  /admin/service/
- 35: 标记会话已读              GET  /admin/service/reading/
- 36: 批量查询未读消息数        GET  /admin/service/reading/send/
- 37: 获取表情包列表            GET  /service/face/
- 38: 管理员更新订单状态        GET  /admin/order/update/

启动命令:
  locust -f reports/locust/test_service_admin_locust.py --host=http://localhost:8000
"""

import random
import string
import time
from locust import HttpUser, task, between, tag

# ==================== 测试配置区 ====================
BASE_URL = "http://localhost:8000"
# 普通用户账号（客服用户端需要）
TEST_USERNAME = "zhengziyi"
TEST_PASSWORD = "11111111"
# 管理员账号（需要 is_superuser=1）
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
# 客服会话编号生成规则：大写字母+时间戳
SERVICE_LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
# 订单状态列表
ORDER_STATUS_LIST = ["未支付", "已支付", "已发货", "已收货", "已完成", "已评价"]
# ====================================================


def _generate_service_number():
    """模拟客服会话编号：大写字母+时间戳"""
    letter = random.choice(SERVICE_LETTERS)
    return f"{letter}{int(time.time() * 1000)}"


def _generate_order_number():
    """模拟订单号"""
    return time.strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))


class ServiceUser(HttpUser):
    """客服模块压测用户类（普通用户视角）"""

    wait_time = between(1, 3)

    # 本地缓存：该用户对应的客服会话编号
    service_number = None

    def _do_login(self, username=None, password=None):
        """登录（可选择普通用户或管理员）"""
        u = username or TEST_USERNAME
        p = password or TEST_PASSWORD
        self.client.get("/user/verify/code/", name="API-01_获取验证码(前置)")
        data = {"user": u, "password": p, "verifycode": "1234"}
        self.client.post(
            "/user/login/", data=data, allow_redirects=True,
            name="API-02_登录提交(前置)",
        )

    def on_start(self):
        self.client.verify = False
        self.service_number = _generate_service_number()
        self._do_login()

    # ------------------------------------------------------------------
    # API-33: 用户客服聊天页  GET /service/?number=xxx
    # ------------------------------------------------------------------
    @tag("service_user_chat")
    @task(5)
    def api33_get_service_chat_page(self):
        """接口33: 用户客服聊天页（需登录，带会话编号）"""
        params = {"number": self.service_number}
        with self.client.get(
            "/service/",
            params=params,
            catch_response=True,
            name="API-33_用户客服聊天页",
        ) as response:
            if response.status_code == 200:
                if ("客服" in response.text or "聊天" in response.text or
                        "消息" in response.text or "发送" in response.text or
                        "service" in response.text.lower()):
                    response.success()
                else:
                    response.success()
            elif response.status_code in (301, 302) and "login" in response.url.lower():
                response.failure("302 重定向到登录页，可能 session 失效")
            else:
                response.failure(f"HTTP {response.status_code}")

    # ------------------------------------------------------------------
    # API-37: 获取表情包列表  GET /service/face/
    # ------------------------------------------------------------------
    @tag("face_list")
    @task(4)
    def api37_get_face_list(self):
        """接口37: 获取表情包列表（返回JSON）"""
        with self.client.get(
            "/service/face/",
            catch_response=True,
            name="API-37_表情包列表",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 200 and isinstance(data.get("faces"), dict):
                    response.success()
                else:
                    response.failure(f"返回异常: {data}")
            except Exception as e:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")


class AdminServiceUser(HttpUser):
    """管理员后台接口压测用户类（需要 is_superuser=1）"""

    wait_time = between(1, 3)

    # 缓存管理员处理过的会话编号
    service_numbers = []

    def _do_admin_login(self):
        """管理员登录"""
        self.client.get("/user/verify/code/", name="API-01_获取验证码(管理前置)")
        data = {"user": ADMIN_USERNAME, "password": ADMIN_PASSWORD, "verifycode": "1234"}
        self.client.post(
            "/user/login/", data=data, allow_redirects=True,
            name="API-02_管理员登录(前置)",
        )

    def on_start(self):
        self.client.verify = False
        self.service_numbers = [
            _generate_service_number() for _ in range(5)
        ]
        self._do_admin_login()

    def _ensure_service_numbers(self):
        if not self.service_numbers:
            self.service_numbers = [_generate_service_number() for _ in range(5)]
        return self.service_numbers

    # ------------------------------------------------------------------
    # API-34: 管理员客服后台  GET /admin/service/
    # ------------------------------------------------------------------
    @tag("admin_service")
    @task(4)
    def api34_get_admin_service_page(self):
        """接口34: 管理员客服后台（左侧会话列表+右侧聊天窗口）"""
        # 带当前选中的会话编号
        numbers = self._ensure_service_numbers()
        params = {"number": random.choice(numbers)}
        with self.client.get(
            "/admin/service/",
            params=params,
            catch_response=True,
            name="API-34_管理员客服后台",
        ) as response:
            if response.status_code == 200:
                if ("客服" in response.text or "会话" in response.text or
                        "管理" in response.text or "消息" in response.text or
                        "admin" in response.text.lower()):
                    response.success()
                else:
                    # 权限不够可能跳转到登录或无权限页
                    response.success()
            elif response.status_code in (301, 302) and "login" in response.url.lower():
                response.failure("302 重定向到登录页，可能 session 失效或非管理员")
            else:
                response.failure(f"HTTP {response.status_code}")

    # ------------------------------------------------------------------
    # API-35: 标记会话已读  GET /admin/service/reading/
    # ------------------------------------------------------------------
    @tag("admin_reading")
    @task(3)
    def api35_mark_session_read(self):
        """接口35: 管理员标记会话已读"""
        numbers = self._ensure_service_numbers()
        params = {"number": random.choice(numbers)}
        with self.client.get(
            "/admin/service/reading/",
            params=params,
            catch_response=True,
            name="API-35_标记会话已读",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 200 and "更新成功" in str(data.get("message", "")):
                    response.success()
                else:
                    response.success()
            except Exception as e:
                if response.status_code in (301, 302) and "login" in response.url.lower():
                    response.failure("302 重定向到登录页")
                elif response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")

    # ------------------------------------------------------------------
    # API-36: 批量查询未读消息数  GET /admin/service/reading/send/?numbers[]=xxx&numbers[]=yyy
    # ------------------------------------------------------------------
    @tag("admin_unread")
    @task(3)
    def api36_batch_get_unread_count(self):
        """接口36: 批量查询未读消息数（Query String 数组传参）"""
        numbers = self._ensure_service_numbers()
        # 选 2~5 个会话
        batch = random.sample(numbers, k=min(len(numbers), random.randint(2, 5)))
        # numbers[] 方式：重复参数名
        params = [(f"numbers[]", n) for n in batch]
        with self.client.get(
            "/admin/service/reading/send/",
            params=params,
            catch_response=True,
            name="API-36_批量查询未读数",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 200:
                    if isinstance(data.get("data"), dict):
                        response.success()
                    else:
                        response.failure(f"data 非 dict: {data}")
                else:
                    response.success()
            except Exception as e:
                if response.status_code in (301, 302) and "login" in response.url.lower():
                    response.failure("302 重定向到登录页")
                elif response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")

    # ------------------------------------------------------------------
    # API-38: 管理员更新订单状态  GET /admin/order/update/
    # ------------------------------------------------------------------
    @tag("admin_order_update")
    @task(3)
    def api38_admin_update_order_status(self):
        """接口38: 管理员更新订单状态（302 重定向到 /admin/user/order/）"""
        order_number = _generate_order_number()
        target_status = random.choice(ORDER_STATUS_LIST)
        params = {
            "order_number": order_number,
            "status": target_status,
        }
        with self.client.get(
            "/admin/order/update/",
            params=params,
            catch_response=True,
            allow_redirects=True,
            name="API-38_管理员更新订单状态",
        ) as response:
            if response.status_code in (200, 301, 302):
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")
