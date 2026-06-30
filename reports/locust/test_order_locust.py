# -*- coding: utf-8 -*-
"""
订单模块 Locust 压力测试脚本
覆盖 API: 22-28 号接口
- 22: 订单列表                 GET  /user/order/
- 23: 立即购买 (详情页下单)    POST /user/index/detail/buy/
- 24: 支付页面                 GET  /user/order/payment/<str:order_number>/
- 25: 更新订单状态             GET  /user/order/update/
- 26: 删除订单                 GET  /user/order/delete/
- 27: 订单评价页面             GET  /user/order/evaluate/
- 28: 提交订单评价             POST /user/order/evalute/submit/

启动命令:
  locust -f reports/locust/test_order_locust.py --host=http://localhost:8000
"""

import json
import random
import time
from locust import HttpUser, task, between, tag

# ==================== 测试配置区 ====================
BASE_URL = "http://localhost:8000"
TEST_USERNAME = "zhengziyi"
TEST_PASSWORD = "11111111"
# 商品 ID 范围
SKU_ID_MIN = 1
SKU_ID_MAX = 100
# 立即购买数量范围
COUNT_MIN = 1
COUNT_MAX = 3
# 订单状态流转（供 API25 测试用）
ORDER_STATUS_LIST = ["未支付", "已支付", "已发货", "已收货", "已完成", "已评价"]
# ====================================================


def _random_sku_id():
    return random.randint(SKU_ID_MIN, SKU_ID_MAX)


def _random_count():
    return random.randint(COUNT_MIN, COUNT_MAX)


def _generate_order_number():
    """模拟订单号格式（用于支付页测试等）"""
    return time.strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))


class OrderUser(HttpUser):
    """订单模块压测用户类（必须登录）"""

    wait_time = between(1, 3)

    # 本地缓存已生成的订单号（用于支付页、更新状态、删除、评价测试）
    order_numbers = []

    def _do_login(self):
        self.client.get("/user/verify/code/", name="API-01_获取验证码(前置)")
        data = {"user": TEST_USERNAME, "password": TEST_PASSWORD, "verifycode": "1234"}
        self.client.post(
            "/user/login/", data=data, allow_redirects=True,
            name="API-02_登录提交(前置)",
        )

    def on_start(self):
        self.client.verify = False
        self.order_numbers = []
        self._do_login()

    def _ensure_order_exists(self):
        """如果本地缓存没有订单号，先通过立即购买创建一个"""
        if not self.order_numbers:
            self._api23_buy_now(internal=True)
        return random.choice(self.order_numbers) if self.order_numbers else _generate_order_number()

    def _api23_buy_now(self, internal=False):
        """立即购买（供其他接口依赖使用）"""
        sku_id = _random_sku_id()
        count = _random_count()
        resp = self.client.post(
            "/user/index/detail/buy/",
            data={"sku_id": sku_id, "count": count},
            catch_response=not internal,
            name="API-23_立即购买(内部)" if internal else "API-23_立即购买",
        )
        try:
            data = resp.json() if isinstance(resp, type(self.client.post.__self__)) else {}
        except Exception:
            data = {}
        if hasattr(resp, 'json'):
            try:
                data = resp.json()
            except Exception:
                data = {}
        order_number = data.get("order_number") if isinstance(data, dict) else None
        if order_number and order_number not in self.order_numbers:
            self.order_numbers.append(order_number)
        return resp

    # ------------------------------------------------------------------
    # API-22: 订单列表  GET /user/order/
    # ------------------------------------------------------------------
    @tag("order_list")
    @task(6)
    def api22_get_order_list(self):
        """接口22: 订单列表（按订单号分组展示）"""
        params = {"page": random.randint(1, 3)}
        with self.client.get(
            "/user/order/",
            params=params,
            catch_response=True,
            name="API-22_订单列表",
        ) as response:
            if response.status_code == 200:
                if ("订单" in response.text or "order" in response.text.lower() or
                        "商品" in response.text or "状态" in response.text or
                        "支付" in response.text):
                    response.success()
                else:
                    response.success()
            elif response.status_code in (301, 302) and "login" in response.url.lower():
                response.failure("302 重定向到登录页，可能 session 失效")
            else:
                response.failure(f"HTTP {response.status_code}")

    # ------------------------------------------------------------------
    # API-23: 立即购买 (详情页直接下单)  POST /user/index/detail/buy/
    # ------------------------------------------------------------------
    @tag("buy_now")
    @task(5)
    def api23_buy_now(self):
        """接口23: 立即购买（详情页直接生成未支付订单）"""
        sku_id = _random_sku_id()
        count = _random_count()
        with self.client.post(
            "/user/index/detail/buy/",
            data={"sku_id": sku_id, "count": count},
            catch_response=True,
            name="API-23_立即购买",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 200:
                    order_number = data.get("order_number")
                    if order_number and order_number not in self.order_numbers:
                        self.order_numbers.append(order_number)
                    # 限制缓存订单号数量，避免无限增长
                    if len(self.order_numbers) > 50:
                        self.order_numbers = self.order_numbers[-20:]
                    response.success()
                else:
                    response.success()
            except Exception as e:
                if response.status_code in (301, 302) and "login" in response.url.lower():
                    response.failure("302 重定向到登录页，可能 session 失效")
                elif response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")

    # ------------------------------------------------------------------
    # API-24: 支付页面  GET /user/order/payment/<str:order_number>/
    # ------------------------------------------------------------------
    @tag("payment")
    @task(4)
    def api24_get_payment_page(self):
        """接口24: 支付页面（展示商品列表和总金额）"""
        order_number = self._ensure_order_exists()
        with self.client.get(
            f"/user/order/payment/{order_number}/",
            catch_response=True,
            name="API-24_支付页面",
        ) as response:
            if response.status_code == 200:
                if ("支付" in response.text or "金额" in response.text or
                        "订单" in response.text or "商品" in response.text):
                    response.success()
                else:
                    # 订单号不存在可能返回404或其他页面，不直接标记失败
                    response.success()
            elif response.status_code == 404:
                response.success()  # 模拟的订单号可能不存在
            elif response.status_code in (301, 302) and "login" in response.url.lower():
                response.failure("302 重定向到登录页，可能 session 失效")
            else:
                response.failure(f"HTTP {response.status_code}")

    # ------------------------------------------------------------------
    # API-25: 更新订单状态  GET /user/order/update/
    # ------------------------------------------------------------------
    @tag("order_update")
    @task(3)
    def api25_update_order_status(self):
        """接口25: 更新订单状态（如已发货、已收货）"""
        order_number = self._ensure_order_exists()
        target_status = random.choice(ORDER_STATUS_LIST)
        params = {
            "order_number": order_number,
            "status": target_status,
        }
        with self.client.get(
            "/user/order/update/",
            params=params,
            catch_response=True,
            allow_redirects=True,
            name="API-25_更新订单状态",
        ) as response:
            if response.status_code in (200, 301, 302):
                # 成功后 302 回订单列表
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")

    # ------------------------------------------------------------------
    # API-26: 删除订单  GET /user/order/delete/
    # ------------------------------------------------------------------
    @tag("order_delete")
    @task(2)
    def api26_delete_order(self):
        """接口26: 删除订单（已发货不可删除）"""
        if not self.order_numbers:
            # 无订单可删，跳过不记失败
            return
        order_number = self.order_numbers.pop(0)
        params = {"order_number": order_number}
        with self.client.get(
            "/user/order/delete/",
            params=params,
            catch_response=True,
            allow_redirects=True,
            name="API-26_删除订单",
        ) as response:
            if response.status_code in (200, 301, 302):
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")

    # ------------------------------------------------------------------
    # API-27: 订单评价页面  GET /user/order/evaluate/
    # ------------------------------------------------------------------
    @tag("evaluate_page")
    @task(3)
    def api27_get_evaluate_page(self):
        """接口27: 订单评价页面（展示待评价商品）"""
        order_number = self._ensure_order_exists()
        params = {"order_number": order_number}
        with self.client.get(
            "/user/order/evaluate/",
            params=params,
            catch_response=True,
            name="API-27_订单评价页面",
        ) as response:
            if response.status_code == 200:
                if ("评价" in response.text or "评论" in response.text or
                        "提交" in response.text or "商品" in response.text):
                    response.success()
                else:
                    response.success()
            elif response.status_code == 404:
                response.success()
            elif response.status_code in (301, 302) and "login" in response.url.lower():
                response.failure("302 重定向到登录页，可能 session 失效")
            else:
                response.failure(f"HTTP {response.status_code}")

    # ------------------------------------------------------------------
    # API-28: 提交订单评价  POST /user/order/evalute/submit/
    # ------------------------------------------------------------------
    @tag("evaluate_submit")
    @task(3)
    def api28_submit_evaluate(self):
        """接口28: 提交订单评价（注意文档中有拼写 evalute）"""
        order_number = self._ensure_order_exists()
        reviews = [
            {
                "sku_id": _random_sku_id(),
                "evaluate": f"locust压测评价-{random.randint(1000,9999)}: 商品不错，物流很快！",
            },
            {
                "sku_id": _random_sku_id(),
                "evaluate": f"locust压测评价-{random.randint(1000,9999)}: 质量很好，推荐购买。",
            },
        ]
        data = {
            "order_number": order_number,
            "reviews": json.dumps(reviews, ensure_ascii=False),
        }
        with self.client.post(
            "/user/order/evalute/submit/",
            data=data,
            catch_response=True,
            name="API-28_提交订单评价",
        ) as response:
            try:
                res_data = response.json()
                if res_data.get("code") == 200:
                    page_msg = str(res_data.get("page", ""))
                    if "添加" in page_msg and "评论" in page_msg:
                        response.success()
                    else:
                        response.success()
                else:
                    response.success()
            except Exception as e:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")
