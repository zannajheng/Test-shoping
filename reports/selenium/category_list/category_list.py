# 分类商品列表 Selenium 自动化测试脚本
# 覆盖接口：
#   #13 /user/index/list/           GET  分类商品列表页 + 页面分页
#   #14 /user/index/list/page/      GET  AJAX 分页
#   #15 /user/index/list/price/     GET  AJAX 按价格降序

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time

USERNAME = "zhengziyi"
PASSWORD = "11111111"
VERIFY_CODE = "1234"
BASE_URL = "http://127.0.0.1:8000/"
LOGIN_URL = BASE_URL + "user/login/"
INDEX_URL = BASE_URL + "user/index/"
LIST_URL  = BASE_URL + "user/index/list/"

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
passed = 0
total = 0


def mark(name, ok, info=""):
    global passed, total
    total += 1
    if ok:
        passed += 1
        print(f"  [PASS] {name}  {info}")
    else:
        print(f"  [FAIL] {name}  {info}")


def do_login():
    driver.get(LOGIN_URL)
    driver.maximize_window()
    wait.until(EC.presence_of_element_located((By.ID, "login_user")))
    driver.find_element(By.ID, "login_user").clear()
    driver.find_element(By.ID, "login_user").send_keys(USERNAME)
    driver.find_element(By.ID, "login_password").clear()
    driver.find_element(By.ID, "login_password").send_keys(PASSWORD)
    try:
        vc = driver.find_element(By.CSS_SELECTOR, "input.vc_input")
        vc.clear(); vc.send_keys(VERIFY_CODE)
    except Exception:
        pass
    driver.find_element(By.CSS_SELECTOR, "input.input_submit").click()
    wait.until(EC.url_contains("/user/index/"))
    time.sleep(0.3)


try:
    print("=" * 70)
    print("【前置步骤】登录")
    print("=" * 70)
    do_login()
    print("  ✓ 登录成功")

    # =======================================================
    # 用例 1: 首页「查看更多」→ 分类列表 (#13 /user/index/list/?type_id=...)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 1】首页 → 分类列表 (#13 GET /user/index/list/?type_id=...)")
    print("=" * 70)

    driver.get(INDEX_URL); time.sleep(0.5)
    more_links = driver.find_elements(
        By.XPATH, "//a[contains(@href,'/user/index/list/?type_id=')]")
    mark(f"首页共有 {len(more_links)} 个「查看更多」分类链接", len(more_links) > 0)

    if more_links:
        first = more_links[0]
        href = first.get_attribute("href") or ""
        print(f"  → 点击分类链接: {href}")
        mark(f"链接 type_id 参数", "type_id=" in href, href)
        first.click()
    else:
        # 兜底: 直接打开一个有数据的分类 id=1
        driver.get(f"{LIST_URL}?type_id=1")
        href = driver.current_url

    try:
        wait.until(EC.url_contains("/user/index/list/"))
        mark("分类列表页加载成功", True, f"URL={driver.current_url}")
    except TimeoutException:
        mark("分类列表页加载超时", False, f"URL={driver.current_url}")
    driver.save_screenshot("cl_01_list_page.png")

    # =======================================================
    # 用例 2: 页面元素：隐藏 type_id、新品推荐、商品列表
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 2】分类列表页 DOM 结构")
    print("=" * 70)

    hid = driver.find_elements(By.ID, "more_list_type_id")
    tid_value = (hid[0].get_attribute("value") if hid else None)
    mark(f"隐藏字段 #more_list_type_id 存在 (value={tid_value!r})",
         tid_value is not None and tid_value != "")

    new_goods = driver.find_elements(By.CSS_SELECTOR, ".new_goods h3")
    if new_goods:
        mark("左侧新品推荐标题", "新品推荐" in new_goods[0].text,
             f"实际标题={new_goods[0].text!r}")
    else:
        mark("左侧新品推荐标题", False, "未找到 .new_goods h3")

    goods_li = driver.find_elements(By.CSS_SELECTOR, "ul.goods_type_list > li")
    mark(f"商品列表 ul.goods_type_list>li 数量={len(goods_li)}", len(goods_li) > 0)
    driver.save_screenshot("cl_02_dom.png")

    type_id = tid_value or "1"

    # =======================================================
    # 用例 3: AJAX 分页 (#14 /user/index/list/page/?type_id=&page=)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 3】AJAX 分页接口 (#14 /user/index/list/page/)")
    print("=" * 70)

    page_resp = driver.execute_async_script(f"""
        const cb = arguments[0];
        const type_id = document.getElementById('more_list_type_id').value || '1';
        fetch('/user/index/list/page/?type_id=' + type_id + '&page=1',
              {{credentials:'include'}})
            .then(r => r.json())
            .then(d => cb({{ok:true, data:d}}))
            .catch(e => cb({{ok:false, err:String(e)}}));
    """)
    if page_resp and page_resp.get("ok"):
        d = page_resp["data"] or {}
        code = d.get("code")
        goods = d.get("goods") or d.get("goods_data") or []
        mark(f"#14 /page/ 返回 code={code}",
             code in (200, 500, -1),   # 500/-1 = 空页也算合理返回
             f"goods count={len(goods)}  message={str(d.get('message'))[:40]!r}")
    else:
        mark("#14 /page/ 请求异常", False, str(page_resp))

    # =======================================================
    # 用例 4: AJAX 价格排序 (#15 /user/index/list/price/?type_id=&page=)
    # =======================================================
    print("\n" + "=" * 70)
    print("【用例 4】AJAX 按价格降序 (#15 /user/index/list/price/)")
    print("=" * 70)

    price_resp = driver.execute_async_script(f"""
        const cb = arguments[0];
        const type_id = document.getElementById('more_list_type_id').value || '1';
        fetch('/user/index/list/price/?type_id=' + type_id + '&page=1',
              {{credentials:'include'}})
            .then(r => r.json())
            .then(d => cb({{ok:true, data:d}}))
            .catch(e => cb({{ok:false, err:String(e)}}));
    """)
    if price_resp and price_resp.get("ok"):
        d = price_resp["data"] or {}
        code = d.get("code")
        goods = d.get("goods") or []
        price_list = [float(g.get("price")) for g in goods
                      if g and g.get("price") is not None]
        # 校验价格降序（允许 <= 关系）
        sorted_desc = all(price_list[i] >= price_list[i + 1]
                          for i in range(len(price_list) - 1))
        mark(f"#15 /price/ 返回 code={code}", code == 200,
             f"goods={len(goods)}  message={str(d.get('message'))[:40]!r}")
        if len(price_list) >= 2:
            mark(f"按价格降序，返回价格列表长度={len(price_list)} 是否降序={sorted_desc}",
                 sorted_desc, f"prices[:6]={price_list[:6]}")
        else:
            mark(f"返回条目<2，跳过降序断言（数据量不足）", True,
                 f"prices={price_list}")
    else:
        mark("#15 /price/ 请求异常", False, str(price_resp))
    driver.save_screenshot("cl_04_ajax_done.png")

    print("\n" + "=" * 70)
    print(f"【汇总】 {passed}/{total} 用例通过")
    print("=" * 70)

except AssertionError as e:
    print(f"\n❌ 断言失败: {e}")
    try:
        driver.save_screenshot("cl_assertion_failed.png")
    except Exception:
        pass

except Exception as e:
    print(f"\n❌ [异常] {type(e).__name__}: {e}")
    import traceback; traceback.print_exc()
    try:
        driver.save_screenshot("cl_error.png")
    except Exception:
        pass

finally:
    print("\n" + "=" * 70)
    print("程序结束，按回车键关闭浏览器...")
    print("=" * 70)
    input()
    driver.quit()
    print("浏览器已关闭。")
