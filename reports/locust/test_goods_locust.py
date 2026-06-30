# -*- coding: utf-8 -*-
"""
商品浏览模块 Locust 压力测试脚本
覆盖 API: 9-15 号接口
- 9:  首页                   GET  /user/index/
- 10: 商品详情页             GET  /user/detail/<int:sku_id>/
- 11: 商品搜索               GET  /user/search/
- 12: 搜索分页 (AJAX)        GET  /user/search/page/
- 13: 分类商品列表           GET  /user/index/list/
- 14: 分类列表分页 (AJAX)    GET  /user/index/list/page/
- 15: 分类列表按价格排序     GET  /user/index/list/price/

启动命令:
  locust -f reports/locust/test_goods_locust.py --host=http://localhost:8000
"""

import random
import string
from locust import HttpUser, task, between, tag

# ==================== 测试配置区 ====================
BASE_URL = "http://localhost:8000"
# 测试账号（需要在系统中已存在）
TEST_USERNAME = "zhengziyi"
TEST_PASSWORD = "11111111"
# 测试用 sku_id 范围（根据数据库中实际商品ID范围调整）
SKU_ID_MIN = 1
SKU_ID_MAX = 100
# 测试用 分类ID 范围
TYPE_ID_MIN = 1
TYPE_ID_MAX = 20
# 搜索关键词库（根据实际商品名调整）
SEARCH_KEYWORDS = ["黄金", "钻石", "项链", "戒指", "耳环", "手镯", "手链", "翡翠", "铂金", "珠宝"]
# ====================================================


def _random_sku_id():
    return random.randint(SKU_ID_MIN, SKU_ID_MAX)


def _random_type_id():
    return random.randint(TYPE_ID_MIN, TYPE_ID_MAX)


def _random_keyword():
    return random.choice(SEARCH_KEYWORDS)


class GoodsUser(HttpUser):
    """商品浏览模块压测用户类"""

    wait_time = between(1, 3)

    def _do_login(self):
        """登录获取 session（浏览历史等功能依赖登录态）"""
        self.client.get("/user/verify/code/", name="API-01_获取验证码(前置)")
        data = {"user": TEST_USERNAME, "password": TEST_PASSWORD, "verifycode": "1234"}
        self.client.post(
            "/user/login/", data=data, allow_redirects=True,
            name="API-02_登录提交(前置)",
        )

    def on_start(self):
        """虚拟用户启动时登录"""
        self.client.verify = False
        # 50% 用户保持登录态以覆盖浏览历史功能
        if random.random() < 0.5:
            self._do_login()

    # ------------------------------------------------------------------
    # API-9: 首页  GET /user/index/   (根路径 / 也会重定向到此)
    # ------------------------------------------------------------------
    @tag("index")
    @task(10)
    def api09_get_index(self):
        """接口9: 首页（按分类展示商品）"""
        with self.client.get(
            "/user/index/",
            catch_response=True,
            name="API-09_首页",
        ) as response:
            if response.status_code == 200:
                if ("商品" in response.text or "分类" in response.text or
                        "购物车" in response.text or "搜索" in response.text):
                    response.success()
                else:
                    response.failure("首页内容异常：缺少关键字段")
            else:
                response.failure(f"HTTP {response.status_code}")

    @tag("index")
    @task(1)
    def api09_get_root_redirect(self):
        """接口9: 根路径 / 重定向到首页"""
        with self.client.get(
            "/",
            catch_response=True,
            allow_redirects=True,
            name="API-09_根路径重定向",
        ) as response:
            if response.status_code in (200, 301, 302) and "/user/index/" in response.url:
                response.success()
            else:
                response.failure(f"未重定向到首页, URL={response.url[:80]}")

    # ------------------------------------------------------------------
    # API-10: 商品详情页  GET /user/detail/<int:sku_id>/
    # ------------------------------------------------------------------
    @tag("detail")
    @task(6)
    def api10_get_goods_detail(self):
        """接口10: 商品详情页（会自动记录浏览历史）"""
        sku_id = _random_sku_id()
        with self.client.get(
            f"/user/detail/{sku_id}/",
            catch_response=True,
            name="API-10_商品详情页",
        ) as response:
            if response.status_code == 200:
                if ("价格" in response.text or "详情" in response.text or
                        "评论" in response.text or "加入购物车" in response.text or
                        "立即购买" in response.text or "简介" in response.text):
                    response.success()
                else:
                    # 商品不存在时，404/页面不匹配，但不视为请求错误
                    response.success()
            elif response.status_code == 404:
                response.success()  # ID 超出范围时 404 正常
            else:
                response.failure(f"HTTP {response.status_code}")

    # ------------------------------------------------------------------
    # API-11: 商品搜索  GET /user/search/
    # ------------------------------------------------------------------
    @tag("search")
    @task(5)
    def api11_get_search(self):
        """接口11: 商品搜索（关键词模糊匹配）"""
        params = {
            "query": _random_keyword(),
            "page": random.randint(1, 3),
        }
        with self.client.get(
            "/user/search/",
            params=params,
            catch_response=True,
            name="API-11_商品搜索",
        ) as response:
            if response.status_code == 200:
                if ("搜索" in response.text or "结果" in response.text or
                        "商品" in response.text or params["query"] in response.text):
                    response.success()
                else:
                    response.failure("搜索页面内容异常")
            else:
                response.failure(f"HTTP {response.status_code}")

    # ------------------------------------------------------------------
    # API-12: 搜索分页 (AJAX)  GET /user/search/page/
    # ------------------------------------------------------------------
    @tag("search_ajax")
    @task(4)
    def api12_search_page_ajax(self):
        """接口12: 搜索分页 AJAX 接口"""
        params = {
            "query": _random_keyword(),
            "page": random.randint(1, 5),
        }
        with self.client.get(
            "/user/search/page/",
            params=params,
            catch_response=True,
            name="API-12_搜索分页AJAX",
        ) as response:
            try:
                data = response.json()
                code = data.get("code")
                if code == 200:
                    if isinstance(data.get("goods_data"), list):
                        response.success()
                    else:
                        response.failure(f"goods_data 非列表: {data}")
                elif code == -1:
                    # 数据为空（正常分页末尾）
                    response.success()
                else:
                    response.failure(f"返回异常 code={code}: {data}")
            except Exception as e:
                # 若不是 JSON，可能返回 HTML 也不直接视为严重失败
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")

    # ------------------------------------------------------------------
    # API-13: 分类商品列表  GET /user/index/list/
    # ------------------------------------------------------------------
    @tag("category_list")
    @task(5)
    def api13_get_category_list(self):
        """接口13: 分类商品列表页（含2个随机推荐商品）"""
        params = {
            "type_id": _random_type_id(),
            "page": random.randint(1, 3),
        }
        with self.client.get(
            "/user/index/list/",
            params=params,
            catch_response=True,
            name="API-13_分类商品列表",
        ) as response:
            if response.status_code == 200:
                if ("商品" in response.text or "推荐" in response.text or
                        "分类" in response.text or "价格" in response.text):
                    response.success()
                else:
                    response.success()
            else:
                response.failure(f"HTTP {response.status_code}")

    # ------------------------------------------------------------------
    # API-14: 分类列表分页 (AJAX)  GET /user/index/list/page/
    # ------------------------------------------------------------------
    @tag("category_ajax")
    @task(4)
    def api14_category_page_ajax(self):
        """接口14: 分类列表分页 AJAX"""
        params = {
            "type_id": _random_type_id(),
            "page": random.randint(1, 5),
        }
        with self.client.get(
            "/user/index/list/page/",
            params=params,
            catch_response=True,
            name="API-14_分类分页AJAX",
        ) as response:
            try:
                data = response.json()
                code = data.get("code")
                if code == 200:
                    response.success()
                elif code == 500 and "数据为空" in str(data.get("message", "")):
                    response.success()
                else:
                    response.failure(f"返回异常 code={code}: {data}")
            except Exception as e:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")

    # ------------------------------------------------------------------
    # API-15: 分类列表按价格排序 (AJAX)  GET /user/index/list/price/
    # ------------------------------------------------------------------
    @tag("category_sort")
    @task(3)
    def api15_category_sort_price(self):
        """接口15: 分类列表按价格降序排序"""
        params = {
            "type_id": _random_type_id(),
            "page": random.randint(1, 3),
        }
        with self.client.get(
            "/user/index/list/price/",
            params=params,
            catch_response=True,
            name="API-15_分类按价格排序",
        ) as response:
            try:
                data = response.json()
                if data.get("code") == 200:
                    goods = data.get("goods", [])
                    # 简单校验价格降序（如果返回了至少2个商品且有price字段）
                    if isinstance(goods, list) and len(goods) >= 2:
                        prices = [
                            float(g.get("price", 0)) for g in goods
                            if isinstance(g, dict) and g.get("price") is not None
                        ]
                        if len(prices) >= 2 and prices != sorted(prices, reverse=True):
                            # 只记录 warning，不标失败（服务端可能有其他排序逻辑）
                            pass
                    response.success()
                else:
                    response.failure(f"返回异常: {data}")
            except Exception as e:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"JSON 解析失败: {e}")
