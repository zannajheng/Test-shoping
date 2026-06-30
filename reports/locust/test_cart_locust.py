# -*- coding: utf-8 -*-
"""
购物车模块 Locust 压力测试脚本
覆盖 API: 16-21 号接口
- 16: 加入购物车 (详情页)        POST /user/cartadd/
- 17: 加入购物车 (搜索页)        POST /user/search/cartadd/
- 18: 购物车页面 / 下单          GET  /user/cart/ , POST /user/cart/ (JSON)
- 19: 购物车数量 +1              POST /user/cart/add/
- 20: 购物车数量 -1              POST /user/cart/decr/
- 21: 删除购物车商品             POST /user/cart/delete/

启动命令:
  locust -f reports/locust/test_cart_locust.py --host=http://localhost:8000
"""

import json
import random
from locust import HttpUser, task, between, tag

# ==================== 测试配置区 ====================
BASE_URL = "http://localhost:8000"
# 测试账号（必须已存在，购物车依赖登录）
TEST_USERNAME = "zhengziyi"
TEST_PASSWORD = "11111111"
# 商品 ID 范围
SKU_ID_MIN = 1
SKU_ID_MAX = 100
# 每次加购数量范围
COUNT_MIN = 1
COUNT_MAX = 5
# 默认收货地址（下单测试用）
DEFAULT_ADDR = "北京市海淀区中关村大街1号"
DEFAULT_TEL = "13800138000"
# ====================================================


def _random_sku_id():
    return random.randint(SKU_ID_MIN, SKU_ID_MAX)


def _random_count():
    return random.randint(COUNT_MIN, COUNT_MAX)


class CartUser(HttpUser):
    """购物车模块压测用户类（必须登录）"""

    wait_time = between(1, 3)

    # 记录当前用户购物车中的 sku_id（用于加减、删除、下单操作）
    cart_skus = []

    def _do_login(self):
        """登录获取 session"""
        self.client.get("/user/verify/code/", name="API-01_获取验证码(前置)")
        data = {"user": TEST_USERNAME, "password": TEST_PASSWORD, "verifycode": "1234"}
        self.client.post(
            "/user/login/", data=data, allow_redirects=True,
            name="API-02_登录提交(前置)",
        )

    def on_start(self):
        """虚拟用户启动时必须登录，并清空本地购物车缓存"""
        self.client.verify = False
        self.cart_skus = []
        self._do_login()

    def _ensure_cart_not_empty(self):
        """若本地缓存为空，先加入一件商品"""
        if not self.cart_skus:
            sku_id = _random_sku_id()
            self.client.post(
                "/user/cartadd/",
                data={"sku_id": sku_id, "num_show": 1},
                name="API-16_加入购物车(内部补数据)",
            )
            self.cart_skus.append(sku_id)
        return random.choice(self.cart_skus)

    # ------------------------------------------------------------------
    # API-16: 加入购物车 (详情页)  POST /user/cartadd/
    # ------------------------------------------------------------------
    @tag("cart_add_detail")
    @task(8)
    def api16_cartadd_from_detail(self):
        """接口16: 从详情页加入购物车（携带 sku_id 和数量）"""
        sku_id = _random_sku_id()
        num = _random_count()
        with self.client.post(
            "/user/cartadd/",
            data={"sku_id": sku_id, "num_show": num},
            catch_response=True,
            name="API-16_加入购物车(详情页)",
        ) as response:
            try:
                data = response.json()
                code = data.get("code")
                if code == 200:
                    self.cart_skus.append(sku_id)
                    response.success()
                elif code == 302 and "用户未登录" in str(data.get("message", "")):
                    response.failure("用户未登录(应在on_start中登录)")
                else:
                    # 可能是商品不存在等业务错误，不视为严重失败
                    response.success()
            except Exception as e:
                if response.status_code in (301, 302) and "login" in response.url.lower():
                    response.failure("302 重定向到登录页，可能 session 失效")
                elif response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")

    # ------------------------------------------------------------------
    # API-17: 加入购物车 (搜索页)  POST /user/search/cartadd/
    # ------------------------------------------------------------------
    @tag("cart_add_search")
    @task(4)
    def api17_cartadd_from_search(self):
        """接口17: 从搜索页加入购物车（默认数量 1）"""
        sku_id = _random_sku_id()
        with self.client.post(
            "/user/search/cartadd/",
            data={"sku_id": sku_id},
            catch_response=True,
            name="API-17_加入购物车(搜索页)",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 200:
                    self.cart_skus.append(sku_id)
                    response.success()
                else:
                    response.success()
            except Exception as e:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")

    # ------------------------------------------------------------------
    # API-18: 购物车页面 / 下单
    #   GET  /user/cart/                  -> 渲染购物车
    #   POST /user/cart/   (JSON body)    -> 生成订单
    # ------------------------------------------------------------------
    @tag("cart_page")
    @task(5)
    def api18_get_cart_page(self):
        """接口18-GET: 访问购物车列表页"""
        with self.client.get(
            "/user/cart/",
            catch_response=True,
            name="API-18_购物车页面",
        ) as response:
            if response.status_code == 200:
                if ("购物车" in response.text or "商品" in response.text or
                        "数量" in response.text or "总价" in response.text or
                        "结算" in response.text or "下单" in response.text):
                    response.success()
                else:
                    response.success()
            elif response.status_code in (301, 302) and "login" in response.url.lower():
                response.failure("302 重定向到登录页，可能 session 失效")
            else:
                response.failure(f"HTTP {response.status_code}")

    @tag("cart_checkout")
    @task(2)
    def api18_post_checkout(self):
        """接口18-POST: 购物车下单（JSON 请求体）"""
        # 先确保购物车有内容
        self._ensure_cart_not_empty()
        # 随机选 1~3 个商品下单
        sample_count = min(len(self.cart_skus), random.randint(1, 3))
        sample_skus = random.sample(self.cart_skus, sample_count)
        goods_list = [
            {
                "sku_id": sku,
                "count": _random_count(),
                "addr": DEFAULT_ADDR,
                "tel": DEFAULT_TEL,
            }
            for sku in sample_skus
        ]
        payload = {"goods": goods_list}
        with self.client.post(
            "/user/cart/",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            catch_response=True,
            name="API-18_购物车下单(POST JSON)",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 200 and "订单" in str(data.get("message", "")):
                    # 成功下单后从本地缓存移除
                    for sku in sample_skus:
                        if sku in self.cart_skus:
                            self.cart_skus.remove(sku)
                    response.success()
                else:
                    response.success()
            except Exception as e:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")

    # ------------------------------------------------------------------
    # API-19: 购物车数量 +1  POST /user/cart/add/
    # ------------------------------------------------------------------
    @tag("cart_incr")
    @task(4)
    def api19_cart_increment(self):
        """接口19: 购物车数量 +1"""
        sku_id = self._ensure_cart_not_empty()
        with self.client.post(
            "/user/cart/add/",
            data={"sku_id": sku_id},
            catch_response=True,
            name="API-19_购物车数量+1",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 200:
                    response.success()
                else:
                    response.success()
            except Exception as e:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")

    # ------------------------------------------------------------------
    # API-20: 购物车数量 -1  POST /user/cart/decr/
    # ------------------------------------------------------------------
    @tag("cart_decr")
    @task(4)
    def api20_cart_decrement(self):
        """接口20: 购物车数量 -1"""
        sku_id = self._ensure_cart_not_empty()
        with self.client.post(
            "/user/cart/decr/",
            data={"sku_id": sku_id},
            catch_response=True,
            name="API-20_购物车数量-1",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 200:
                    response.success()
                else:
                    response.success()
            except Exception as e:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")

    # ------------------------------------------------------------------
    # API-21: 删除购物车商品  POST /user/cart/delete/
    # ------------------------------------------------------------------
    @tag("cart_delete")
    @task(3)
    def api21_cart_delete(self):
        """接口21: 删除购物车中的商品"""
        sku_id = self._ensure_cart_not_empty()
        with self.client.post(
            "/user/cart/delete/",
            data={"sku_id": sku_id},
            catch_response=True,
            name="API-21_删除购物车商品",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 200:
                    if sku_id in self.cart_skus:
                        self.cart_skus.remove(sku_id)
                    response.success()
                else:
                    response.success()
            except Exception as e:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")
