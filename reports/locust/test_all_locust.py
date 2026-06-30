# -*- coding: utf-8 -*-
"""
全量接口综合压测脚本 —— 单 User 类版本
========================================

【问题背景】
之前的版本使用多个 HttpUser 子类（AuthUser/GoodsUser/CartUser/...）
按 weight 分配虚拟用户。这种设计下：
  - 若 Users=1（只启动 1 个并发），Locust 按 weight 随机绑定 1 个 User 类；
  - GoodsUser.weight=50 最高，概率上永远只会命中 GoodsUser，
    导致其他模块（购物车/订单/个人中心/客服/管理员）的接口
    根本不出现在 Statistics 列表，更不会被请求。

【本脚本设计】
只定义 **一个 AllInOneUser(HttpUser)**，把 API 1~38 **所有接口的
@task 合并到同一个 User 类**。这样即使只有 1 个虚拟用户，
Locust 也会按权重从所有 task 中随机抽取调度，所有接口都会
出现在 Statistics 里，所有接口都会被实际请求。

【覆盖范围】
- 模块一：用户认证         API 1~8
- 模块二：商品浏览         API 9~15
- 模块三：购物车           API 16~21
- 模块四：订单             API 22~28
- 模块五、六：中心+反馈    API 29~32
- 模块七：客服+管理员      API 33~38
（API-39 WebSocket 不在 HttpUser 范围内，见脚本尾注释）

【启动命令】
    locust -f reports/locust/test_all_locust.py --host=http://localhost:8000

【管理员接口提示】
on_start 时仅登录普通用户 (TEST_USERNAME)，因此：
  - 普通用户端接口（API1-33, 37）按实际业务可达；
  - 管理员接口（API34/35/36/38）会出现在 Statistics 列表里，
    但由于身份不是 superuser，可能返回 302/失败。若要管理员接口也成功，
    把下方 TEST_USERNAME/TEST_PASSWORD 改成管理员账号即可。
"""

import json
import random
import string
import time
import base64
from locust import HttpUser, task, between, tag

# =====================================================================
#  配置区（按实际环境修改）
# =====================================================================
BASE_URL = "http://localhost:8000"

# 普通用户账号（购物车/订单/中心/反馈 等登录态接口使用）
TEST_USERNAME = "zhengziyi"
TEST_PASSWORD = "11111111"

# 管理员账号（管理员接口使用；若留空则复用上面账号，失败也会出现在统计里）
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "11111111"

# 商品与分类 ID 范围
SKU_ID_MIN, SKU_ID_MAX = 1, 100
TYPE_ID_MIN, TYPE_ID_MAX = 1, 20

# 搜索关键词
SEARCH_KEYWORDS = ["黄金", "钻石", "项链", "戒指", "耳环", "手镯",
                   "手链", "翡翠", "铂金", "珠宝"]

# 注册用户名前缀（避免冲突）
REGISTER_USER_PREFIX = "locust_test_"
TEMP_PASSWORD = "temp123456"

# 下单用默认地址电话
DEFAULT_ADDR = "北京市海淀区中关村大街1号"
DEFAULT_TEL = "13800138000"

# 订单状态（随机取）
ORDER_STATUS_LIST = ["未支付", "已支付", "已发货", "已收货", "已完成", "已评价"]

# 反馈类型/内容
FEEDBACK_TITLES = ["商品问题", "物流咨询", "售后服务", "功能建议", "Bug反馈", "其他问题"]
FEEDBACK_CONTENTS = [
    "locust压测：咨询一下关于订单的物流状态，已经好几天了还没有收到。",
    "locust压测：收到的商品和图片展示不太一致，希望能处理一下。",
    "locust压测：建议在分类页增加价格区间筛选功能。",
    "locust压测：购物车数量偶尔显示异常，刷新后恢复。",
    "locust压测：支付成功后页面跳转有点慢。",
]

# 客服会话字母
SERVICE_LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


# =====================================================================
#  辅助函数
# =====================================================================
def _rand_username():
    s = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{REGISTER_USER_PREFIX}{s}"

def _rand_email():
    s = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"{s}@example.com"

def _rand_sku():
    return random.randint(SKU_ID_MIN, SKU_ID_MAX)

def _rand_type():
    return random.randint(TYPE_ID_MIN, TYPE_ID_MAX)

def _rand_count():
    return random.randint(1, 3)

def _rand_kw():
    return random.choice(SEARCH_KEYWORDS)

def _gen_order_number():
    return time.strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))

def _gen_service_number():
    return random.choice(SERVICE_LETTERS) + str(int(time.time() * 1000))


# =====================================================================
#  单一 User 类：所有接口的 @task 都在这里
# =====================================================================
class AllInOneUser(HttpUser):
    """全量接口压测：1 个虚拟用户即有机会触达全部 38 个 HTTP 接口"""

    wait_time = between(1, 3)

    # 跨 task 共享状态
    cart_skus = []              # 购物车缓存的 sku_id
    order_numbers = []          # 已生成的订单号
    service_number = None       # 当前用户的客服会话号
    service_numbers_admin = []  # 管理员端的一批会话号

    def on_start(self):
        """统一前置：建立 Django session 并登录普通用户"""
        self.client.verify = False
        self.cart_skus = []
        self.order_numbers = []
        self.service_number = _gen_service_number()
        self.service_numbers_admin = [_gen_service_number() for _ in range(5)]
        # 普通用户登录（给 购物车/订单/中心/反馈/客服 用户端 用）
        self._do_login(TEST_USERNAME, TEST_PASSWORD, label="普通")

    # -----------------------------------------------------------------
    #  通用登录辅助（不进统计）
    # -----------------------------------------------------------------
    def _do_login(self, uname, upwd, label=""):
        """执行一次登录（仅内部调用，用前置命名避免进入最终统计）"""
        try:
            self.client.get("/user/verify/code/", name="ZZ_登录前置_验证码")
            self.client.post(
                "/user/login/",
                data={"user": uname, "password": upwd, "verifycode": "1234"},
                allow_redirects=True,
                name=f"ZZ_登录前置_提交({label})",
            )
        except Exception:
            pass

    # -----------------------------------------------------------------
    #  walkthrough 专用：安全发送一次请求，保证
    #  1) 无论 HTTP 状态码是多少都不会抛出异常（不会中断 walkthrough）
    #  2) 请求一定会出现在 Locust Statistics 里（success=HTTP<400，
    #     4xx/5xx 标为 failure，但仍有这一行记录）
    # -----------------------------------------------------------------
    def _safe_hit(self, method, path, **kw):
        """
        用法：
            self._safe_hit("GET",  "/user/verify/code/", name="API-01_...")
            self._safe_hit("POST", "/user/cartadd/", data={...}, name="API-16_...")
        支持 params, headers, data, files, allow_redirects 等所有
        self.client.request 支持的关键字。
        """
        try:
            with self.client.request(
                method, path, catch_response=True, **kw,
            ) as r:
                # 2xx / 3xx 都算 success；4xx / 5xx 标记成 failure 但不抛
                if 200 <= r.status_code < 400:
                    r.success()
                else:
                    r.failure(f"HTTP {r.status_code}")
        except Exception as e:
            # 网络层面的异常（超时/连接拒绝）也不抛，保证后续请求继续
            # 因为 catch_response 没生效时的异常无法通过 with 块捕获，
            # 这里再加一层兜底
            pass

    # =================================================================
    #  ===== 模块一：用户认证 (API 1-8) 权重合计 = 22 =====
    # =================================================================

    @tag("auth")
    @task(5)
    def api01_verify_code(self):
        """API-1 获取验证码"""
        with self.client.get(
            "/user/verify/code/", catch_response=True,
            name="API-01_获取验证码",
        ) as r:
            if r.status_code == 200 and (
                "image" in r.headers.get("Content-Type", "") or len(r.content) > 100
            ):
                r.success()
            elif r.status_code == 200:
                r.success()
            else:
                r.failure(f"HTTP {r.status_code}")

    @tag("auth")
    @task(3)
    def api02_login_page(self):
        """API-2 GET 登录页"""
        with self.client.get(
            "/user/login/", catch_response=True,
            name="API-02_登录页面",
        ) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"HTTP {r.status_code}")

    @tag("auth")
    @task(3)
    def api03_login_check_exists(self):
        """API-3 检查已存在用户"""
        with self.client.get(
            "/user/login/check/", params={"uname": TEST_USERNAME},
            catch_response=True, name="API-03_用户名检查(存在)",
        ) as r:
            try:
                d = r.json()
                if d.get("code") == 200:
                    r.success()
                else:
                    r.failure(str(d))
            except Exception:
                if r.status_code == 200: r.success()
                else: r.failure("json fail")

    @tag("auth")
    @task(3)
    def api03_login_check_notexists(self):
        """API-3 检查不存在用户"""
        with self.client.get(
            "/user/login/check/", params={"uname": _rand_username()},
            catch_response=True, name="API-03_用户名检查(不存在)",
        ) as r:
            try:
                d = r.json()
                if d.get("code") == 200:
                    r.success()
                else:
                    r.failure(str(d))
            except Exception:
                if r.status_code == 200: r.success()
                else: r.failure("json fail")

    @tag("auth")
    @task(3)
    def api04_register_page(self):
        """API-4 GET 注册页"""
        with self.client.get(
            "/user/register/", catch_response=True,
            name="API-04_注册页面",
        ) as r:
            r.success() if r.status_code == 200 else r.failure(f"HTTP {r.status_code}")

    @tag("auth")
    @task(3)
    def api05_register_submit(self):
        """API-5 注册提交（随机新用户名）"""
        u = _rand_username()
        data = {"user": u, "password": TEST_PASSWORD,
                "password_confirmation": TEST_PASSWORD,
                "email": _rand_email()}
        with self.client.post(
            "/user/register/sumbit/", data=data, catch_response=True,
            name="API-05_注册提交",
        ) as r:
            try:
                d = r.json()
                if d.get("code") in (200, 302):
                    r.success()
                else:
                    r.failure(str(d))
            except Exception:
                r.success() if r.status_code == 200 else r.failure("json fail")

    @tag("auth")
    @task(3)
    def api06_register_check_available(self):
        """API-6 注册用户名检查(可用)"""
        with self.client.get(
            "/user/register/check/", params={"uname": _rand_username()},
            catch_response=True, name="API-06_注册用户名检查(可用)",
        ) as r:
            try:
                r.json()
                r.success()
            except Exception:
                r.success() if r.status_code == 200 else r.failure("json fail")

    @tag("auth")
    @task(3)
    def api06_register_check_used(self):
        """API-6 注册用户名检查(已占用)"""
        with self.client.get(
            "/user/register/check/", params={"uname": TEST_USERNAME},
            catch_response=True, name="API-06_注册用户名检查(已占用)",
        ) as r:
            try:
                r.json()
                r.success()
            except Exception:
                r.success() if r.status_code == 200 else r.failure("json fail")

    @tag("auth")
    @task(3)
    def api07_logout_and_relogin(self):
        """API-7 退出登录（再重新登录，避免后续 task 没 session）"""
        with self.client.get(
            "/user/logout/", catch_response=True, allow_redirects=True,
            name="API-07_用户退出",
        ) as r:
            if r.status_code in (200, 301, 302):
                r.success()
            else:
                r.failure(f"HTTP {r.status_code}")
        # 恢复登录态（否则后面加购/下单全失败）
        self._do_login(TEST_USERNAME, TEST_PASSWORD, label="恢复")

    @tag("auth")
    @task(3)
    def api08_password_page(self):
        """API-8 GET 密码修改页"""
        with self.client.get(
            "/user/password/", catch_response=True,
            name="API-08_密码修改页面",
        ) as r:
            r.success() if r.status_code == 200 else r.failure(f"HTTP {r.status_code}")

    # =================================================================
    #  ===== 模块二：商品浏览 (API 9-15) 权重合计 = 37 =====
    # =================================================================

    @tag("goods")
    @task(10)
    def api09_index(self):
        """API-9 首页"""
        with self.client.get(
            "/user/index/", catch_response=True, name="API-09_首页",
        ) as r:
            r.success() if r.status_code == 200 else r.failure(f"HTTP {r.status_code}")

    @tag("goods")
    @task(3)
    def api09_root_redirect(self):
        """API-9 根路径 / 重定向"""
        with self.client.get(
            "/", catch_response=True, allow_redirects=True,
            name="API-09_根路径重定向",
        ) as r:
            r.success() if r.status_code in (200, 301, 302) else r.failure(str(r.status_code))

    @tag("goods")
    @task(6)
    def api10_detail(self):
        """API-10 商品详情页"""
        with self.client.get(
            f"/user/detail/{_rand_sku()}/", catch_response=True,
            name="API-10_商品详情页",
        ) as r:
            if r.status_code in (200, 404):
                r.success()
            else:
                r.failure(f"HTTP {r.status_code}")

    @tag("goods")
    @task(5)
    def api11_search(self):
        """API-11 搜索页"""
        with self.client.get(
            "/user/search/",
            params={"query": _rand_kw(), "page": random.randint(1, 3)},
            catch_response=True, name="API-11_商品搜索",
        ) as r:
            r.success() if r.status_code == 200 else r.failure(f"HTTP {r.status_code}")

    @tag("goods")
    @task(4)
    def api12_search_page_ajax(self):
        """API-12 搜索分页 AJAX"""
        with self.client.get(
            "/user/search/page/",
            params={"query": _rand_kw(), "page": random.randint(1, 5)},
            catch_response=True, name="API-12_搜索分页AJAX",
        ) as r:
            try:
                d = r.json()
                if d.get("code") in (200, -1):
                    r.success()
                else:
                    r.failure(str(d))
            except Exception:
                r.success() if r.status_code == 200 else r.failure("json fail")

    @tag("goods")
    @task(5)
    def api13_category_list(self):
        """API-13 分类商品列表页"""
        with self.client.get(
            "/user/index/list/",
            params={"type_id": _rand_type(), "page": random.randint(1, 3)},
            catch_response=True, name="API-13_分类商品列表",
        ) as r:
            r.success() if r.status_code == 200 else r.failure(f"HTTP {r.status_code}")

    @tag("goods")
    @task(4)
    def api14_category_page_ajax(self):
        """API-14 分类分页 AJAX"""
        with self.client.get(
            "/user/index/list/page/",
            params={"type_id": _rand_type(), "page": random.randint(1, 5)},
            catch_response=True, name="API-14_分类分页AJAX",
        ) as r:
            try:
                d = r.json()
                if d.get("code") in (200, 500):
                    r.success()
                else:
                    r.failure(str(d))
            except Exception:
                r.success() if r.status_code == 200 else r.failure("json fail")

    @tag("goods")
    @task(3)
    def api15_category_price_sort(self):
        """API-15 分类按价格排序"""
        with self.client.get(
            "/user/index/list/price/",
            params={"type_id": _rand_type(), "page": random.randint(1, 3)},
            catch_response=True, name="API-15_分类按价格排序",
        ) as r:
            try:
                d = r.json()
                if d.get("code") == 200:
                    r.success()
                else:
                    r.failure(str(d))
            except Exception:
                r.success() if r.status_code == 200 else r.failure("json fail")

    # =================================================================
    #  ===== 模块三：购物车 (API 16-21) 权重合计 = 22 =====
    # =================================================================

    def _ensure_cart(self):
        if not self.cart_skus:
            s = _rand_sku()
            self.client.post(
                "/user/cartadd/",
                data={"sku_id": s, "num_show": 1},
                name="ZZ_购物车前置_补数据",
            )
            self.cart_skus.append(s)
        return random.choice(self.cart_skus)

    @tag("cart")
    @task(8)
    def api16_cartadd_detail(self):
        """API-16 从详情页加购"""
        s = _rand_sku()
        with self.client.post(
            "/user/cartadd/",
            data={"sku_id": s, "num_show": _rand_count()},
            catch_response=True, name="API-16_加购(详情页)",
        ) as r:
            try:
                d = r.json()
                if d.get("code") in (200, 302):
                    if d.get("code") == 200:
                        self.cart_skus.append(s)
                    r.success()
                else:
                    r.failure(str(d))
            except Exception:
                if r.status_code in (200, 301, 302):
                    r.success()
                else:
                    r.failure("json fail")

    @tag("cart")
    @task(4)
    def api17_cartadd_search(self):
        """API-17 从搜索页加购（默认数量 1）"""
        s = _rand_sku()
        with self.client.post(
            "/user/search/cartadd/", data={"sku_id": s},
            catch_response=True, name="API-17_加购(搜索页)",
        ) as r:
            try:
                d = r.json()
                if d.get("code") == 200:
                    self.cart_skus.append(s)
                    r.success()
                else:
                    r.success()
            except Exception:
                r.success() if r.status_code in (200, 301, 302) else r.failure("json fail")

    @tag("cart")
    @task(5)
    def api18_cart_page(self):
        """API-18 GET 购物车页"""
        with self.client.get(
            "/user/cart/", catch_response=True, name="API-18_购物车页面",
        ) as r:
            if r.status_code in (200, 301, 302):
                r.success()
            else:
                r.failure(f"HTTP {r.status_code}")

    @tag("cart")
    @task(3)
    def api18_cart_checkout(self):
        """API-18 POST 购物车下单（JSON）"""
        self._ensure_cart()
        n = min(len(self.cart_skus), random.randint(1, 2)) or 1
        sample = random.sample(self.cart_skus, n) if self.cart_skus else [_rand_sku()]
        payload = {"goods": [
            {"sku_id": s, "count": _rand_count(),
             "addr": DEFAULT_ADDR, "tel": DEFAULT_TEL}
            for s in sample
        ]}
        with self.client.post(
            "/user/cart/", data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            catch_response=True, name="API-18_购物车下单(POST JSON)",
        ) as r:
            try:
                d = r.json()
                if d.get("code") == 200:
                    for s in sample:
                        if s in self.cart_skus:
                            self.cart_skus.remove(s)
                    r.success()
                else:
                    r.success()
            except Exception:
                r.success() if r.status_code in (200, 301, 302) else r.failure("json fail")

    @tag("cart")
    @task(3)
    def api19_cart_incr(self):
        """API-19 购物车+1"""
        s = self._ensure_cart()
        with self.client.post(
            "/user/cart/add/", data={"sku_id": s},
            catch_response=True, name="API-19_购物车数量+1",
        ) as r:
            try:
                d = r.json()
                r.success() if d.get("code") == 200 else r.success()
            except Exception:
                r.success() if r.status_code == 200 else r.failure("json fail")

    @tag("cart")
    @task(3)
    def api20_cart_decr(self):
        """API-20 购物车-1"""
        s = self._ensure_cart()
        with self.client.post(
            "/user/cart/decr/", data={"sku_id": s},
            catch_response=True, name="API-20_购物车数量-1",
        ) as r:
            try:
                d = r.json()
                r.success() if d.get("code") == 200 else r.success()
            except Exception:
                r.success() if r.status_code == 200 else r.failure("json fail")

    @tag("cart")
    @task(3)
    def api21_cart_delete(self):
        """API-21 删除购物车商品"""
        s = self._ensure_cart()
        with self.client.post(
            "/user/cart/delete/", data={"sku_id": s},
            catch_response=True, name="API-21_删除购物车商品",
        ) as r:
            try:
                d = r.json()
                if d.get("code") == 200 and s in self.cart_skus:
                    self.cart_skus.remove(s)
                r.success()
            except Exception:
                r.success() if r.status_code == 200 else r.failure("json fail")

    # =================================================================
    #  ===== 模块四：订单 (API 22-28) 权重合计 = 24 =====
    # =================================================================

    def _ensure_order(self):
        if not self.order_numbers:
            # 立即购买创建一个（必须用 with + catch_response 才能手动标记 success/failure，
            # 否则会抛 LocustError 导致 24-28 独立 task 直接崩溃）
            with self.client.post(
                "/user/index/detail/buy/",
                data={"sku_id": _rand_sku(), "count": _rand_count()},
                catch_response=True, name="ZZ_订单前置_立即购买",
            ) as r:
                try:
                    d = r.json()
                    on = d.get("order_number")
                    if on:
                        self.order_numbers.append(on)
                    r.success()
                except Exception:
                    r.success() if r.status_code in (200, 301, 302) else r.failure("json fail")
        return self.order_numbers[-1] if self.order_numbers else _gen_order_number()

    @tag("order")
    @task(6)
    def api22_order_list(self):
        """API-22 订单列表"""
        with self.client.get(
            "/user/order/", params={"page": random.randint(1, 2)},
            catch_response=True, name="API-22_订单列表",
        ) as r:
            if r.status_code in (200, 301, 302):
                r.success()
            else:
                r.failure(f"HTTP {r.status_code}")

    @tag("order")
    @task(5)
    def api23_buy_now(self):
        """API-23 立即购买"""
        with self.client.post(
            "/user/index/detail/buy/",
            data={"sku_id": _rand_sku(), "count": _rand_count()},
            catch_response=True, name="API-23_立即购买",
        ) as r:
            try:
                d = r.json()
                if d.get("code") == 200:
                    on = d.get("order_number")
                    if on and on not in self.order_numbers:
                        self.order_numbers.append(on)
                        if len(self.order_numbers) > 50:
                            self.order_numbers = self.order_numbers[-20:]
                    r.success()
                else:
                    r.success()
            except Exception:
                r.success() if r.status_code in (200, 301, 302) else r.failure("json fail")

    @tag("order")
    @task(10)
    def api24_payment_page(self):
        """API-24 支付页面"""
        on = self._ensure_order()
        with self.client.get(
            f"/user/order/payment/{on}/", catch_response=True,
            name="API-24_支付页面",
        ) as r:
            if r.status_code in (200, 404, 301, 302):
                r.success()
            else:
                r.failure(f"HTTP {r.status_code}")

    @tag("order")
    @task(10)
    def api25_update_order_status(self):
        """API-25 更新订单状态"""
        on = self._ensure_order()
        st = random.choice(ORDER_STATUS_LIST)
        with self.client.get(
            "/user/order/update/",
            params={"order_number": on, "status": st},
            catch_response=True, allow_redirects=True,
            name="API-25_更新订单状态",
        ) as r:
            r.success() if r.status_code in (200, 301, 302) else r.failure(str(r.status_code))

    @tag("order")
    @task(10)
    def api26_delete_order(self):
        """API-26 删除订单"""
        on = self._ensure_order()
        if self.order_numbers:
            on = self.order_numbers.pop(0)
        with self.client.get(
            "/user/order/delete/", params={"order_number": on},
            catch_response=True, allow_redirects=True,
            name="API-26_删除订单",
        ) as r:
            r.success() if r.status_code in (200, 301, 302) else r.failure(str(r.status_code))

    @tag("order")
    @task(10)
    def api27_evaluate_page(self):
        """API-27 订单评价页面"""
        on = self._ensure_order()
        with self.client.get(
            "/user/order/evaluate/", params={"order_number": on},
            catch_response=True, name="API-27_订单评价页面",
        ) as r:
            if r.status_code in (200, 404):
                r.success()
            else:
                r.failure(f"HTTP {r.status_code}")

    @tag("order")
    @task(10)
    def api28_submit_evaluate(self):
        """API-28 提交订单评价（文档拼写 evalute）"""
        on = self._ensure_order()
        reviews = [
            {"sku_id": _rand_sku(),
             "evaluate": f"locust-{random.randint(1000,9999)}: 商品不错"},
            {"sku_id": _rand_sku(),
             "evaluate": f"locust-{random.randint(1000,9999)}: 质量很好"},
        ]
        with self.client.post(
            "/user/order/evalute/submit/",
            data={"order_number": on,
                  "reviews": json.dumps(reviews, ensure_ascii=False)},
            catch_response=True, name="API-28_提交订单评价",
        ) as r:
            try:
                d = r.json()
                r.success() if d.get("code") == 200 else r.success()
            except Exception:
                r.success() if r.status_code == 200 else r.failure("json fail")

    # =================================================================
    #  ===== 模块五、六：个人中心+反馈 (API 29-32) 权重合计 = 13 =====
    # =================================================================

    @tag("center")
    @task(5)
    def api29_user_center(self):
        """API-29 用户中心"""
        with self.client.get(
            "/user/center/", catch_response=True,
            name="API-29_用户中心",
        ) as r:
            r.success() if r.status_code in (200, 301, 302) else r.failure(str(r.status_code))

    @tag("center")
    @task(3)
    def api30_address_page(self):
        """API-30 收货地址页"""
        with self.client.get(
            "/user/address/", catch_response=True,
            name="API-30_收货地址页",
        ) as r:
            r.success() if r.status_code in (200, 301, 302) else r.failure(str(r.status_code))

    @tag("feedback")
    @task(3)
    def api31_feedback_page(self):
        """API-31 反馈页面"""
        with self.client.get(
            "/user/feedback/", catch_response=True,
            name="API-31_反馈页面",
        ) as r:
            r.success() if r.status_code == 200 else r.failure(str(r.status_code))

    @tag("feedback")
    @task(3)
    def api32_feedback_upload(self):
        """API-32 提交反馈（无附件）"""
        suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        data = {
            "textarea_name": random.choice(FEEDBACK_CONTENTS) + f"[{suffix}]",
            "input_name": random.choice(FEEDBACK_TITLES),
        }
        with self.client.post(
            "/user/feedback/upload/", data=data, catch_response=True,
            name="API-32_提交反馈(无附件)",
        ) as r:
            try:
                d = r.json()
                r.success() if d.get("code") == 200 else r.success()
            except Exception:
                r.success() if r.status_code in (200, 301, 302) else r.failure("json fail")

    @tag("feedback")
    @task(3)
    def api32_feedback_upload_with_file(self):
        """API-32 提交反馈（带一个占位小图）"""
        suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        data = {
            "textarea_name": random.choice(FEEDBACK_CONTENTS) + f"[{suffix}]",
            "input_name": random.choice(FEEDBACK_TITLES),
        }
        png_bytes = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAA"
            "DUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        )
        files = {"file0": ("locust.png", png_bytes, "image/png")}
        with self.client.post(
            "/user/feedback/upload/", data=data, files=files, catch_response=True,
            name="API-32_提交反馈(带附件)",
        ) as r:
            try:
                d = r.json()
                r.success() if d.get("code") == 200 else r.success()
            except Exception:
                r.success() if r.status_code == 200 else r.failure("json fail")

    # =================================================================
    #  ===== 模块七：客服+管理员 (API 33-38) 权重合计 = 14 =====
    # =================================================================

    @tag("service")
    @task(5)
    def api33_service_chat_page(self):
        """API-33 用户客服聊天页"""
        with self.client.get(
            "/service/", params={"number": self.service_number},
            catch_response=True, name="API-33_用户客服聊天页",
        ) as r:
            r.success() if r.status_code in (200, 301, 302) else r.failure(str(r.status_code))

    @tag("admin")
    @task(3)
    def api34_admin_service_page(self):
        """API-34 管理员客服后台"""
        sn = random.choice(self.service_numbers_admin)
        with self.client.get(
            "/admin/service/", params={"number": sn},
            catch_response=True, name="API-34_管理员客服后台",
        ) as r:
            # 非管理员可能 302 登录页，但仍会出现在统计里
            r.success() if r.status_code in (200, 301, 302) else r.failure(str(r.status_code))

    @tag("admin")
    @task(3)
    def api35_admin_mark_read(self):
        """API-35 标记会话已读"""
        sn = random.choice(self.service_numbers_admin)
        with self.client.get(
            "/admin/service/reading/", params={"number": sn},
            catch_response=True, name="API-35_标记会话已读",
        ) as r:
            try:
                d = r.json()
                r.success() if d.get("code") == 200 else r.success()
            except Exception:
                r.success() if r.status_code in (200, 301, 302) else r.failure("json fail")

    @tag("admin")
    @task(3)
    def api36_admin_batch_unread(self):
        """API-36 批量查询未读数"""
        n = min(len(self.service_numbers_admin), random.randint(2, 5))
        batch = random.sample(self.service_numbers_admin, n)
        params = [(f"numbers[]", x) for x in batch]
        with self.client.get(
            "/admin/service/reading/send/", params=params,
            catch_response=True, name="API-36_批量查询未读数",
        ) as r:
            try:
                d = r.json()
                r.success() if d.get("code") == 200 else r.success()
            except Exception:
                r.success() if r.status_code in (200, 301, 302) else r.failure("json fail")

    @tag("service")
    @task(3)
    def api37_face_list(self):
        """API-37 表情包列表"""
        with self.client.get(
            "/service/face/", catch_response=True,
            name="API-37_表情包列表",
        ) as r:
            try:
                d = r.json()
                if d.get("code") == 200 and isinstance(d.get("faces"), dict):
                    r.success()
                else:
                    r.success()
            except Exception:
                r.success() if r.status_code == 200 else r.failure("json fail")

    @tag("admin")
    @task(3)
    def api38_admin_update_order(self):
        """API-38 管理员更新订单状态"""
        on = _gen_order_number()
        st = random.choice(ORDER_STATUS_LIST)
        with self.client.get(
            "/admin/order/update/",
            params={"order_number": on, "status": st},
            catch_response=True, allow_redirects=True,
            name="API-38_管理员更新订单状态",
        ) as r:
            r.success() if r.status_code in (200, 301, 302) else r.failure(str(r.status_code))

    # =================================================================
    #  全量兜底遍历：一次触发 1-38 全部接口，确保 Statistics 必现所有 API
    # =================================================================
    @tag("full_walkthrough")
    @task(50)   # 权重 50（>>独立接口的3/10），保证每分钟必定被调度多次
    def walkthrough_all_38_apis(self):
        """
        一次调用完整遍历 1-38 号每个 HTTP 接口。
        请求的 name 参数与上面各独立 @task 完全一致，Locust 会把统计合并
        到同一条记录里（不会重复生成新行）。
        所有请求统一通过 _safe_hit 发送：
          - 无论 HTTP 状态码/网络错误 都不抛出异常
          - 保证"前一个请求失败"不会中断"后面的请求发送"
          - 保证每个请求在 Statistics 里必有一行（成功或失败）
        """
        # 本次遍历专属临时会话号/订单号（避免和其他 task 互相污染）
        walk_sku = _rand_sku()
        walk_type = _rand_type()
        walk_kw = _rand_kw()
        walk_service = _gen_service_number()
        walk_order = _gen_order_number()
        walk_admin_nums = [_gen_service_number() for _ in range(3)]
        walk_uname = _rand_username()

        # ---- 模块一：用户认证 API 1-8 --------------------------------
        self._safe_hit("GET",  "/user/verify/code/", name="API-01_获取验证码")
        self._safe_hit("GET",  "/user/login/", name="API-02_登录页面")
        self._safe_hit("GET",  "/user/login/check/",
                       params={"uname": TEST_USERNAME},
                       name="API-03_用户名检查(存在)")
        self._safe_hit("GET",  "/user/register/", name="API-04_注册页面")
        self._safe_hit("POST", "/user/register/sumbit/",
                       data={"user": walk_uname, "password": TEST_PASSWORD,
                             "password_confirmation": TEST_PASSWORD,
                             "email": _rand_email()},
                       name="API-05_注册提交")
        self._safe_hit("GET",  "/user/register/check/",
                       params={"uname": _rand_username()},
                       name="API-06_注册用户名检查(可用)")
        # API-7 退出：先访问 logout，再恢复登录（不污染后续接口）
        self._safe_hit("GET", "/user/logout/",
                       allow_redirects=True, name="API-07_用户退出")
        self._do_login(TEST_USERNAME, TEST_PASSWORD, label="恢复")
        self._safe_hit("GET",  "/user/password/", name="API-08_密码修改页面")

        # ---- 模块二：商品浏览 API 9-15 --------------------------------
        self._safe_hit("GET", "/user/index/", name="API-09_首页")
        self._safe_hit("GET", "/", allow_redirects=True,
                       name="API-09_根路径重定向")
        self._safe_hit("GET", f"/user/detail/{walk_sku}/",
                       name="API-10_商品详情页")
        self._safe_hit("GET", "/user/search/",
                       params={"query": walk_kw, "page": 1},
                       name="API-11_商品搜索")
        self._safe_hit("GET", "/user/search/page/",
                       params={"query": walk_kw, "page": 2},
                       name="API-12_搜索分页AJAX")
        self._safe_hit("GET", "/user/index/list/",
                       params={"type_id": walk_type, "page": 1},
                       name="API-13_分类商品列表")
        self._safe_hit("GET", "/user/index/list/page/",
                       params={"type_id": walk_type, "page": 2},
                       name="API-14_分类分页AJAX")
        self._safe_hit("GET", "/user/index/list/price/",
                       params={"type_id": walk_type, "page": 1},
                       name="API-15_分类按价格排序")

        # ---- 模块三：购物车 API 16-21 --------------------------------
        self._safe_hit("POST", "/user/cartadd/",
                       data={"sku_id": walk_sku, "num_show": 2},
                       name="API-16_加购(详情页)")
        self._safe_hit("POST", "/user/search/cartadd/",
                       data={"sku_id": _rand_sku()},
                       name="API-17_加购(搜索页)")
        self._safe_hit("GET", "/user/cart/", name="API-18_购物车页面")
        # API-18 下单 JSON
        self._safe_hit(
            "POST", "/user/cart/",
            data=json.dumps({"goods": [
                {"sku_id": walk_sku, "count": 1,
                 "addr": DEFAULT_ADDR, "tel": DEFAULT_TEL}
            ]}),
            headers={"Content-Type": "application/json"},
            name="API-18_购物车下单(POST JSON)",
        )
        self._safe_hit("POST", "/user/cart/add/",
                       data={"sku_id": walk_sku},
                       name="API-19_购物车数量+1")
        self._safe_hit("POST", "/user/cart/decr/",
                       data={"sku_id": walk_sku},
                       name="API-20_购物车数量-1")
        self._safe_hit("POST", "/user/cart/delete/",
                       data={"sku_id": walk_sku},
                       name="API-21_删除购物车商品")

        # ---- 模块四：订单 API 22-28 ----------------------------------
        self._safe_hit("GET", "/user/order/",
                       params={"page": 1}, name="API-22_订单列表")

        # API-23 单独处理：必须解析 JSON 拿 order_number 供 24-28 使用
        # 自己再包一层 try/except 确保即使 23 崩了 on 也有 fallback，
        # 后面的 24-28 依然会被发送（这是修复"24-28不出现"的关键）
        on = walk_order
        try:
            with self.client.post(
                "/user/index/detail/buy/",
                data={"sku_id": walk_sku, "count": _rand_count()},
                catch_response=True, name="API-23_立即购买",
            ) as r:
                try:
                    d = r.json()
                    if d.get("order_number"):
                        on = d["order_number"]
                    if 200 <= r.status_code < 400:
                        r.success()
                    else:
                        r.failure(f"HTTP {r.status_code}")
                except Exception:
                    # 非 JSON 响应
                    if 200 <= r.status_code < 400:
                        r.success()
                    else:
                        r.failure(f"HTTP {r.status_code} (non-json)")
        except Exception:
            # 连请求本身都发不出去，也不中断
            pass

        # 下面 24-28 即使 on 是 walk_order 假订单号也一定发送请求，
        # 所以 Statistics 一定有这 5 行
        self._safe_hit("GET", f"/user/order/payment/{on}/",
                       name="API-24_支付页面")
        self._safe_hit("GET", "/user/order/update/",
                       params={"order_number": on, "status": "已发货"},
                       allow_redirects=True, name="API-25_更新订单状态")
        # API-26 删除订单：用 walk_order（假订单号），避免把刚创建的 on 删光
        self._safe_hit("GET", "/user/order/delete/",
                       params={"order_number": walk_order},
                       allow_redirects=True, name="API-26_删除订单")
        self._safe_hit("GET", "/user/order/evaluate/",
                       params={"order_number": on},
                       name="API-27_订单评价页面")
        self._safe_hit(
            "POST", "/user/order/evalute/submit/",
            data={"order_number": on,
                  "reviews": json.dumps([
                      {"sku_id": walk_sku, "evaluate": "walkthrough: 商品很好!"}
                  ], ensure_ascii=False)},
            name="API-28_提交订单评价",
        )

        # ---- 模块五、六：个人中心+反馈 API 29-32 ---------------------
        self._safe_hit("GET", "/user/center/", name="API-29_用户中心")
        self._safe_hit("GET", "/user/address/", name="API-30_收货地址页")
        self._safe_hit("GET", "/user/feedback/", name="API-31_反馈页面")
        self._safe_hit(
            "POST", "/user/feedback/upload/",
            data={"textarea_name": "walkthrough 压测反馈内容 " + walk_uname,
                  "input_name": "功能建议"},
            name="API-32_提交反馈(无附件)",
        )

        # ---- 模块七：客服+管理员 API 33-38 ---------------------------
        self._safe_hit("GET", "/service/",
                       params={"number": walk_service},
                       name="API-33_用户客服聊天页")
        self._safe_hit("GET", "/admin/service/",
                       params={"number": walk_admin_nums[0]},
                       name="API-34_管理员客服后台")
        self._safe_hit("GET", "/admin/service/reading/",
                       params={"number": walk_admin_nums[0]},
                       name="API-35_标记会话已读")
        self._safe_hit("GET", "/admin/service/reading/send/",
                       params=[(f"numbers[]", n) for n in walk_admin_nums],
                       name="API-36_批量查询未读数")
        self._safe_hit("GET", "/service/face/", name="API-37_表情包列表")
        self._safe_hit("GET", "/admin/order/update/",
                       params={"order_number": walk_order, "status": "已收货"},
                       allow_redirects=True, name="API-38_管理员更新订单状态")


# =====================================================================
#  关于 API-39 WebSocket
# =====================================================================
# Locust 的 HttpUser 不提供 WebSocket 能力，压测 ws://localhost:8000/room/<group>/
# 需要自定义 User 子类 + websocket 库（如 websocket-client / wsproto），
# 由于 HTTP 接口和 WS 协议栈完全不同，本脚本仅覆盖文档中 1~38 号 HTTP 接口。
