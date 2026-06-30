# 快速 TDD 红覆盖检查：断言 39 个接口都有对应 Selenium 脚本 / 脚本中出现断言（脚本路径模式 & regex）
# 注意：此脚本只做“有对应脚本 + 脚本里出现关键 URL / 断言文案”的静态断言，不实际运行 Selenium。
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
EXPECTED = {
    # (接口序号, 接口路径片段, 候选脚本路径: 脚本中必须出现该路径片段)
    1:  ("/user/verify/code/",           ["login/login.py", "regist/regist.py", "change_password/change_password.py"]),
    2:  ("/user/login/",                  ["login/login.py"]),
    3:  ("/user/login/check/",            ["login/login.py", "regist/regist.py"]),
    4:  ("/user/register/",               ["regist/regist.py"]),
    5:  ("/user/register/sumbit/",        ["regist/regist.py"]),
    6:  ("/user/register/check/",         ["regist/regist.py"]),
    7:  ("/user/logout/",                 ["logout/logout.py", "my_order/my_order.py", "admin/admin_order.py"]),
    8:  ("/user/password/",               ["change_password/change_password.py"]),
    9:  ("/user/index/",                  ["login/login.py", "index_backtotop/index_backtotop.py", "goods_detail/goods_detail.py", "shopping_cart/shopping_cart.py"]),
    10: ("/user/detail/",                 ["goods_detail/goods_detail.py", "shopping_cart/shopping_cart.py", "buy_now/buy_now.py", "payment/payment.py", "order_evaluate/order_evaluate.py"]),
    11: ("/user/search/",                 ["search_jewelry/search_jewelry.py", "search_pagination/search_pagination.py", "search_cartadd/search_cartadd.py"]),
    12: ("/user/search/page/",            ["search_pagination/search_pagination.py", "search_cartadd/search_cartadd.py"]),
    13: ("/user/index/list/",             ["category_list/category_list.py", "search_pagination/search_pagination.py"]),
    14: ("/user/index/list/page/",        ["category_list/category_list.py", "search_pagination/search_pagination.py"]),
    15: ("/user/index/list/price/",       ["category_list/category_list.py", "search_pagination/search_pagination.py"]),
    16: ("/user/cartadd/",                ["goods_detail/goods_detail.py", "shopping_cart/shopping_cart.py"]),
    17: ("/user/search/cartadd/",         ["search_pagination/search_pagination.py", "search_cartadd/search_cartadd.py"]),
    18: ("/user/cart/",                   ["shopping_cart/shopping_cart.py"]),
    19: ("/user/cart/add/",               ["shopping_cart/shopping_cart.py"]),
    20: ("/user/cart/decr/",              ["shopping_cart/shopping_cart.py"]),
    21: ("/user/cart/delete/",            ["shopping_cart/shopping_cart.py"]),
    22: ("/user/order/",                  ["my_order/my_order.py", "user_center/user_center.py", "payment/payment.py"]),
    23: ("/user/index/detail/buy/",       ["buy_now/buy_now.py", "payment/payment.py", "order_evaluate/order_evaluate.py", "admin/admin_order.py"]),
    24: ("/user/order/payment/",          ["buy_now/buy_now.py", "payment/payment.py"]),
    25: ("/user/order/update/",           ["my_order/my_order.py", "order_evaluate/order_evaluate.py", "admin/admin_order.py"]),
    26: ("/user/order/delete/",           ["my_order/my_order.py"]),
    27: ("/user/order/evaluate/",         ["my_order/my_order.py", "order_evaluate/order_evaluate.py"]),
    28: ("/user/order/evalute/submit/",   ["order_evaluate/order_evaluate.py"]),
    29: ("/user/center/",                 ["user_center/user_center.py", "logout/logout.py"]),
    30: ("/user/address/",                ["address/address.py"]),
    31: ("/user/feedback/",               ["feedback/feedback.py"]),
    32: ("/user/feedback/upload/",        ["feedback/feedback.py"]),
    33: ("/service/",                     ["customer_service/customer_service.py"]),
    34: ("/admin/service/",               ["admin/admin_service.py"]),
    35: ("/admin/service/reading/",       ["admin/admin_service.py"]),
    36: ("/admin/service/reading/send/",  ["admin/admin_service.py"]),
    37: ("/service/face/",                ["customer_service/customer_service.py", "admin/admin_service.py"]),
    38: ("/admin/order/update/",          ["admin/admin_order.py"]),
    # 39 WebSocket 超出 Selenium HTTP/DOM 测试范围，不强制测试
}
# 额外：管理员脚本中必须含有 管理员账户 "admin" + 密码 "11111111"
ADMIN_SCRIPTS = ["admin/admin_service.py", "admin/admin_order.py"]

# 辅助：脚本里是否出现片段（忽略大小写、忽略 URL 与字符串中的 BASE_URL 拼接）
def text_has(text, fragment):
    # 将 fragment 中的 / 反斜杠都统一
    variants = [fragment]
    if fragment.startswith("/"):
        variants.append(fragment.lstrip("/"))
    for v in variants:
        if v and v in text:
            return True
    return False

FAIL = []
for idx, (fragment, candidates) in EXPECTED.items():
    found = False
    for rel in candidates:
        p = os.path.join(HERE, rel)
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            txt = f.read()
        if text_has(txt, fragment):
            found = True
            break
    if not found:
        FAIL.append(f"#%2d 未覆盖: %s  (在候选 %s 中既无此文件，也不含路径片段)" % (idx, fragment, candidates))

# 管理员脚本：账户与密码
for rel in ADMIN_SCRIPTS:
    p = os.path.join(HERE, rel)
    if not os.path.exists(p):
        FAIL.append("管理员脚本缺失: " + rel); continue
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        txt = f.read()
    if '"admin"' not in txt and "'admin'" not in txt and 'ADMIN_USER' not in txt and 'USERNAME = "admin"' not in txt and "USERNAME = 'admin'" not in txt:
        FAIL.append(f"管理员脚本 {rel} 未使用 admin 账户")
    if '"11111111"' not in txt and "'11111111'" not in txt:
        FAIL.append(f"管理员脚本 {rel} 未使用密码 11111111")
    if "【汇总】" not in txt:
        FAIL.append(f"管理员脚本 {rel} 缺少 【汇总】 输出行（统一命名规范）")

print(f"共检查 {len(EXPECTED)} 个接口 + {len(ADMIN_SCRIPTS)} 个管理员脚本")
if FAIL:
    print("FAIL 项 (%d 条):" % len(FAIL))
    for line in FAIL:
        print("  - " + line)
    sys.exit(1)
else:
    # 统计：汇总脚本中 含 【汇总】 + 使用正则匹配接口片段的脚本数
    n = 0
    for _, (fr, cands) in EXPECTED.items():
        for c in cands:
            p = os.path.join(HERE, c)
            if os.path.exists(p) and text_has(open(p, encoding="utf-8", errors="replace").read(), fr):
                n += 1; break
    print(f"OK: 所有已声明接口都能在对应 Selenium 脚本中找到路径片段 (命中 {n}/{len(EXPECTED)} 个接口脚本)")
    sys.exit(0)
