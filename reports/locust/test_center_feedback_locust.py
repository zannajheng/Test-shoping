# -*- coding: utf-8 -*-
"""
个人中心 + 反馈模块 Locust 压力测试脚本
覆盖 API: 29-32 号接口
- 29: 用户中心                GET  /user/center/
- 30: 收货地址页              GET  /user/address/
- 31: 反馈页面                GET  /user/feedback/
- 32: 提交反馈                POST /user/feedback/upload/  (CSRF 豁免)

启动命令:
  locust -f reports/locust/test_center_feedback_locust.py --host=http://localhost:8000
"""

import random
import string
import time
from locust import HttpUser, task, between, tag

# ==================== 测试配置区 ====================
BASE_URL = "http://localhost:8000"
TEST_USERNAME = "zhengziyi"
TEST_PASSWORD = "11111111"
# 反馈类型/标题选项
FEEDBACK_TITLES = [
    "商品问题",
    "物流咨询",
    "售后服务",
    "功能建议",
    "Bug反馈",
    "其他问题",
]
FEEDBACK_CONTENTS = [
    "locust压测：咨询一下关于订单的物流状态，已经好几天了还没有收到。",
    "locust压测：收到的商品和图片展示不太一致，希望能处理一下。",
    "locust压测：建议在分类页增加价格区间筛选功能，方便用户查找。",
    "locust压测：购物车数量偶尔显示异常，刷新后恢复，麻烦查一下。",
    "locust压测：支付成功后页面跳转有点慢，体验有待优化。",
]
# ====================================================


def _random_feedback_title():
    return random.choice(FEEDBACK_TITLES)


def _random_feedback_content():
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return random.choice(FEEDBACK_CONTENTS) + f" [{suffix}]"


class CenterFeedbackUser(HttpUser):
    """个人中心+反馈模块压测用户类"""

    wait_time = between(1, 3)

    def _do_login(self):
        self.client.get("/user/verify/code/", name="API-01_获取验证码(前置)")
        data = {"user": TEST_USERNAME, "password": TEST_PASSWORD, "verifycode": "1234"}
        self.client.post(
            "/user/login/", data=data, allow_redirects=True,
            name="API-02_登录提交(前置)",
        )

    def on_start(self):
        self.client.verify = False
        self._do_login()

    # ------------------------------------------------------------------
    # API-29: 用户中心  GET /user/center/
    # ------------------------------------------------------------------
    @tag("user_center")
    @task(5)
    def api29_get_user_center(self):
        """接口29: 用户中心（展示浏览历史商品）"""
        with self.client.get(
            "/user/center/",
            catch_response=True,
            name="API-29_用户中心",
        ) as response:
            if response.status_code == 200:
                if ("中心" in response.text or "浏览" in response.text or
                        "历史" in response.text or "个人" in response.text or
                        "我的" in response.text):
                    response.success()
                else:
                    response.success()
            elif response.status_code in (301, 302) and "login" in response.url.lower():
                response.failure("302 重定向到登录页，可能 session 失效")
            else:
                response.failure(f"HTTP {response.status_code}")

    # ------------------------------------------------------------------
    # API-30: 收货地址页  GET /user/address/
    # ------------------------------------------------------------------
    @tag("address")
    @task(3)
    def api30_get_address_page(self):
        """接口30: 收货地址填写页面"""
        with self.client.get(
            "/user/address/",
            catch_response=True,
            name="API-30_收货地址页",
        ) as response:
            if response.status_code == 200:
                if ("地址" in response.text or "收货" in response.text or
                        "电话" in response.text or "邮编" in response.text or
                        "详细" in response.text):
                    response.success()
                else:
                    response.success()
            elif response.status_code in (301, 302) and "login" in response.url.lower():
                response.failure("302 重定向到登录页，可能 session 失效")
            else:
                response.failure(f"HTTP {response.status_code}")

    # ------------------------------------------------------------------
    # API-31: 反馈页面  GET /user/feedback/
    # ------------------------------------------------------------------
    @tag("feedback_page")
    @task(3)
    def api31_get_feedback_page(self):
        """接口31: 反馈提交页面"""
        with self.client.get(
            "/user/feedback/",
            catch_response=True,
            name="API-31_反馈页面",
        ) as response:
            if response.status_code == 200:
                if ("反馈" in response.text or "提交" in response.text or
                        "建议" in response.text or "意见" in response.text or
                        "上传" in response.text):
                    response.success()
                else:
                    response.success()
            else:
                response.failure(f"HTTP {response.status_code}")

    # ------------------------------------------------------------------
    # API-32: 提交反馈  POST /user/feedback/upload/  (CSRF 豁免, multipart/form-data)
    #   参数: textarea_name (反馈内容), input_name (反馈标题/分类), file0~file4 (可选图片)
    #   返回: {"code":200, "message":"反馈成功"}
    #   自动生成 feedback_number: 2大写字母-时间戳
    # ------------------------------------------------------------------
    @tag("feedback_submit")
    @task(4)
    def api32_submit_feedback_no_files(self):
        """接口32: 提交反馈（不带文件）"""
        data = {
            "textarea_name": _random_feedback_content(),
            "input_name": _random_feedback_title(),
        }
        with self.client.post(
            "/user/feedback/upload/",
            data=data,
            catch_response=True,
            name="API-32_提交反馈(无附件)",
        ) as response:
            try:
                res_data = response.json()
                if res_data.get("code") == 200 and "反馈" in str(res_data.get("message", "")):
                    response.success()
                elif res_data.get("code") == 302 and "用户未登录" in str(res_data.get("message", "")):
                    response.failure("用户未登录")
                else:
                    response.success()
            except Exception as e:
                if response.status_code in (301, 302) and "login" in response.url.lower():
                    response.failure("302 重定向到登录页，可能 session 失效")
                elif response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")

    @tag("feedback_submit")
    @task(1)
    def api32_submit_feedback_with_small_file(self):
        """接口32: 提交反馈（带一个 1x1 占位图，模拟 multipart 文件上传）"""
        # 构造一个最小的 PNG (1x1 透明像素)
        import base64
        png_bytes = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        )
        files = {
            "file0": ("locust_test.png", png_bytes, "image/png"),
        }
        data = {
            "textarea_name": _random_feedback_content(),
            "input_name": _random_feedback_title(),
        }
        with self.client.post(
            "/user/feedback/upload/",
            data=data,
            files=files,
            catch_response=True,
            name="API-32_提交反馈(带附件)",
        ) as response:
            try:
                res_data = response.json()
                if res_data.get("code") == 200:
                    response.success()
                else:
                    response.success()
            except Exception as e:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")
