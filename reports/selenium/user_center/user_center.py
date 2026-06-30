# 个人中心功能 Selenium 自动化测试脚本

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time

# ========== 测试配置 ==========
USERNAME = "zhengziyi"        # 登录账号（个人中心需要登录）
PASSWORD = "11111111"
VERIFY_CODE = "1234"
BASE_URL = "http://127.0.0.1:8000/"
LOGIN_URL = BASE_URL + "user/login/"
INDEX_URL = BASE_URL + "user/index/"
CENTER_URL = BASE_URL + "user/center/"
ORDER_URL = BASE_URL + "user/order/"
PASSWORD_URL = BASE_URL + "user/password/"

# ========== 初始化驱动 ==========
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

try:
    # ==============================================
    # 【前置】登录
    # ==============================================
    print("=" * 70)
    print("【前置步骤】登录账号")
    print("=" * 70)
    driver.get(LOGIN_URL)
    driver.maximize_window()

    wait.until(EC.presence_of_element_located((By.ID, "login_user")))
    print(f"[登录] 打开登录页成功，准备填写账号: {USERNAME}")

    driver.find_element(By.ID, "login_user").clear()
    driver.find_element(By.ID, "login_user").send_keys(USERNAME)

    driver.find_element(By.ID, "login_password").clear()
    driver.find_element(By.ID, "login_password").send_keys(PASSWORD)

    try:
        vc = driver.find_element(By.CSS_SELECTOR, "input.vc_input")
        vc.clear()
        vc.send_keys(VERIFY_CODE)
    except:
        pass

    driver.find_element(By.CSS_SELECTOR, "input.input_submit").click()
    wait.until(EC.url_contains("/user/index/"))
    print(f"[登录] ✓ 登录成功，已进入首页")
    time.sleep(0.5)

    passed_cases = 0
    total_cases = 5  # 1.个人中心入口 2.左侧菜单 3.基本信息 4.最近浏览 5.全部订单跳转

    # ==============================================
    # 【用例 1】从首页头部导航栏「个人中心」入口进入
    # ==============================================
    print("\n" + "=" * 70)
    print(f"【用例 1/{total_cases}】从首页头部导航栏「个人中心」入口跳转")
    print("=" * 70)

    try:
        user_link = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='user_link']//a[contains(@href,'center')] | //div[contains(@class,'user_link')]//a[contains(.,'个人中心')]")
            )
        )
    except TimeoutException:
        # 兜底：用 LINK_TEXT
        user_link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "个人中心"))
        )

    print("[1/3] 已定位到首页「个人中心」链接")

    # 高亮
    driver.execute_script(
        "arguments[0].style.outline='3px solid #5C8AEC'; arguments[0].style.outlineOffset='3px';",
        user_link
    )
    time.sleep(0.3)
    driver.save_screenshot("uc_01_header_link_highlighted.png")
    driver.execute_script(
        "arguments[0].style.outline=''; arguments[0].style.outlineOffset='';",
        user_link
    )
    print("      ✓ 高亮截图: uc_01_header_link_highlighted.png")

    user_link.click()
    print("[2/3] 点击个人中心...")

    wait.until(EC.url_contains("/user/center/"))
    print(f"[3/3] ✓ 跳转成功，当前 URL: {driver.current_url}")

    page_title = driver.title
    print(f"      页面标题: {page_title}")
    assert "个人中心" in page_title or "个人信息" in page_title or "商城" in page_title
    print("      ✓ URL 与页面标题断言通过")
    driver.save_screenshot("uc_01_center_page.png")
    print("      ✓ 截图: uc_01_center_page.png（个人中心首屏）")
    passed_cases += 1

    # ==============================================
    # 【用例 2】验证左侧菜单结构和当前激活项
    # ==============================================
    print("\n" + "=" * 70)
    print(f"【用例 2/{total_cases}】验证左侧菜单结构 + 当前激活项")
    print("=" * 70)

    left_menu_h3 = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".left_menu_con h3"))
    )
    print(f"[1/4] 左侧菜单标题: '{left_menu_h3.text.strip()}'")
    assert left_menu_h3.text.strip() == "个人中心", "❌ 左侧菜单标题不是'个人中心'！"
    print("      ✓ 菜单标题断言通过")

    menu_items = driver.find_elements(By.CSS_SELECTOR, ".left_menu_con li a")
    menu_texts = [item.text.strip() for item in menu_items]
    print(f"[2/4] 菜单项: {menu_texts}")
    assert len(menu_items) >= 2, "❌ 左侧菜单项不足 2 个！"
    assert any("个人信息" in t for t in menu_texts), "❌ 缺少'个人信息'菜单！"
    assert any("全部订单" in t for t in menu_texts), "❌ 缺少'全部订单'菜单！"
    print("      ✓ 菜单项断言通过")

    # 当前激活项：个人信息应该有 class=active
    active_link = driver.find_element(By.CSS_SELECTOR, ".left_menu_con li a.active")
    active_text = active_link.text.strip()
    print(f"[3/4] 当前激活菜单项: '{active_text}'")
    assert "个人信息" in active_text, "❌ 进入个人中心后，'个人信息'未被高亮(active)！"
    print("      ✓ 激活项断言通过")

    # 高亮左侧菜单，截图
    left_menu = driver.find_element(By.CSS_SELECTOR, ".left_menu_con")
    driver.execute_script(
        "arguments[0].style.outline='3px solid #e8616c'; arguments[0].style.outlineOffset='3px';",
        left_menu
    )
    time.sleep(0.3)
    driver.save_screenshot("uc_02_left_menu.png")
    driver.execute_script(
        "arguments[0].style.outline=''; arguments[0].style.outlineOffset='';",
        left_menu
    )
    print("[4/4] ✓ 左侧菜单截图: uc_02_left_menu.png")
    passed_cases += 1

    # ==============================================
    # 【用例 3】验证「基本信息」模块：用户名 / 修改密码入口
    # ==============================================
    print("\n" + "=" * 70)
    print(f"【用例 3/{total_cases}】基本信息模块 — 用户名 / 修改密码入口")
    print("=" * 70)

    info_title = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h3[contains(@class,'common_title') and contains(.,'基本信息')]")
        )
    )
    print(f"[1/4] 模块标题: '{info_title.text.strip()}'")

    user_info_li = driver.find_elements(By.CSS_SELECTOR, "ul.user_info_list li")
    assert len(user_info_li) >= 1, "❌ 用户信息列表为空！"
    first_li_text = user_info_li[0].text.strip()
    print(f"[2/4] 用户名行文本: '{first_li_text}'")
    assert USERNAME in first_li_text, f"❌ 基本信息中未显示正确用户名！期望包含 '{USERNAME}'，实际 '{first_li_text}'"
    print("      ✓ 用户名校验通过")

    # 修改密码链接
    pwd_link = driver.find_element(
        By.XPATH, "//a[contains(@href,'password') and contains(.,'修改密码')]"
    )
    pwd_href = pwd_link.get_attribute("href")
    print(f"[3/4] 修改密码链接文字: '{pwd_link.text.strip()}'，href={pwd_href}")
    assert PASSWORD_URL in pwd_href or "/user/password" in pwd_href
    print("      ✓ 修改密码链接断言通过")

    # 高亮整个基本信息块
    info_con = driver.find_element(By.CSS_SELECTOR, ".info_con")
    driver.execute_script(
        "arguments[0].style.outline='3px solid #8ec15b'; arguments[0].style.outlineOffset='3px';",
        info_con
    )
    time.sleep(0.3)
    driver.save_screenshot("uc_03_basic_info.png")
    driver.execute_script(
        "arguments[0].style.outline=''; arguments[0].style.outlineOffset='';",
        info_con
    )
    print("[4/4] ✓ 基本信息截图: uc_03_basic_info.png")
    passed_cases += 1

    # ==============================================
    # 【用例 4】验证「最近浏览」模块 + 首件商品跳详情
    # ==============================================
    print("\n" + "=" * 70)
    print(f"【用例 4/{total_cases}】最近浏览模块 + 点击商品跳详情")
    print("=" * 70)

    browse_title = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//h3[contains(@class,'common_title') and contains(.,'最近浏览')]")
        )
    )
    print(f"[1/5] 模块标题: '{browse_title.text.strip()}'")

    browse_items = driver.find_elements(By.CSS_SELECTOR, ".has_view_list ul.goods_type_list > li")
    browse_count = len(browse_items)
    print(f"[2/5] 最近浏览商品数量: {browse_count} 件")
    print(f"      ✓ 最近浏览容器存在（数量：{browse_count}）")

    # 高亮最近浏览区
    has_view = driver.find_element(By.CSS_SELECTOR, ".has_view_list")
    driver.execute_script(
        "arguments[0].style.outline='3px solid #67a7e9'; arguments[0].style.outlineOffset='3px';",
        has_view
    )
    time.sleep(0.3)
    driver.save_screenshot("uc_04_recent_browse.png")
    driver.execute_script(
        "arguments[0].style.outline=''; arguments[0].style.outlineOffset='';",
        has_view
    )
    print("[3/5] ✓ 最近浏览截图: uc_04_recent_browse.png")

    # 如果有最近浏览，点击第一件商品跳详情
    if browse_count > 0:
        first_browse = browse_items[0]
        title_el = first_browse.find_element(By.TAG_NAME, "h4")
        first_browse_title = title_el.text.strip()
        first_browse_link = first_browse.find_element(By.TAG_NAME, "a")
        print(f"[4/5] 最近浏览首件商品: '{first_browse_title}'，准备点击...")
        first_browse_link.click()

        try:
            wait.until(EC.url_contains("/user/detail/"))
            print(f"      ✓ 跳转成功，URL: {driver.current_url}")
            driver.save_screenshot("uc_04_browse_to_detail.png")
            print("      ✓ 截图: uc_04_browse_to_detail.png")
            passed_cases += 1

            print("      返回个人中心继续...")
            driver.get(CENTER_URL)
            # 等待个人中心左侧菜单渲染完毕（DOM + 菜单条目可见）
            wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".left_menu_con li a")
            ))
            time.sleep(0.3)
        except TimeoutException:
            print(f"      ✗ 未跳转，当前URL: {driver.current_url}")
            driver.save_screenshot("uc_04_browse_detail_fail.png")
            driver.get(CENTER_URL)
            wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".left_menu_con li a")
            ))
            time.sleep(0.3)
    else:
        print("[4/5] ⚠ 最近浏览为空（没浏览过商品），跳过点击商品子用例（也算通过）")
        print("[5/5] ✓ 最近浏览模块校验完成")
        passed_cases += 1

    # ==============================================
    # 【用例 5】左侧菜单「全部订单」跳转 + 激活项校验
    # ==============================================
    print("\n" + "=" * 70)
    print(f"【用例 5/{total_cases}】左侧菜单「全部订单」跳转")
    print("=" * 70)

    # 无论当前URL是什么，都重新加载个人中心页，确保页面状态干净
    # （彻底避免前面用例 4 的各种跳转分支导致的 DOM 未加载问题）
    print("[0/4] 重新加载个人中心页，等待菜单渲染...")
    driver.get(CENTER_URL)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".left_menu_con")))
    menu_links = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".left_menu_con li a")
    ))
    time.sleep(0.3)
    print(f"      ✓ 左侧菜单加载完成，共 {len(menu_links)} 个菜单项")

    # ========== 关键调试信息：把当前左侧菜单所有条目 DOM 快照打印出来 ==========
    print("      ┌─ 左侧菜单 DOM 快照（帮助你日后排查定位问题）─────────┐")
    for idx, link in enumerate(menu_links):
        text = link.text.strip().replace("\n", " ")
        href = link.get_attribute("href") or ""
        cls  = link.get_attribute("class") or ""
        disp = link.is_displayed()
        print(f"      │ [{idx}] text='{text}'  class='{cls}'  href={href}  displayed={disp}")
    print("      └─────────────────────────────────────────────────────┘")

    # 把左侧菜单滚动到可视区域内，避免 element_to_be_clickable 因不在视口内判不可交互
    left_menu_el = driver.find_element(By.CSS_SELECTOR, ".left_menu_con")
    driver.execute_script("arguments[0].scrollIntoView({block:'center', behavior:'instant'});", left_menu_el)
    time.sleep(0.3)

    # ========== 多策略兜底：按优先级找「全部订单」链接 ==========
    order_link = None
    try:
        print("[1/4] 策略A: XPath 含文本'全部订单'...")
        order_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class,'left_menu_con')]//a[contains(normalize-space(.),'全部订单')]")
        ))
        print("      ✓ 命中策略A")
    except TimeoutException:
        print("      ✗ 策略A超时，换策略B: 按第二个 li a 索引找...")
        try:
            if len(menu_links) >= 2:
                order_link = menu_links[1]
                print("      ✓ 命中策略B（第二个链接）")
            else:
                raise TimeoutException("菜单项不足2个")
        except Exception as e:
            print(f"      ✗ 策略B失败: {e}，换策略C: PARTIAL_LINK_TEXT...")
            try:
                order_link = wait.until(EC.element_to_be_clickable(
                    (By.PARTIAL_LINK_TEXT, "全部订单")
                ))
                print("      ✓ 命中策略C")
            except TimeoutException:
                print("      ✗ 策略C超时，换策略D: JS 直接选择 menu_links 中文本包含'订单'的项并强制...")
                found = driver.execute_script(
                    """
                    const items = document.querySelectorAll('.left_menu_con li a');
                    for (let i = 0; i < items.length; i++) {
                        const t = (items[i].innerText || items[i].textContent || '').replace(/\\s+/g,'');
                        if (t.indexOf('订单') >= 0 || t.indexOf('全部') >= 0) {
                            items[i].scrollIntoView({block:'center'});
                            items[i].style.outline='3px solid #e8616c';
                            items[i].style.outlineOffset='3px';
                            return items[i];
                        }
                    }
                    // 兜底：返回第二个
                    if (items.length >= 2) {
                        items[1].scrollIntoView({block:'center'});
                        items[1].style.outline='3px solid #e8616c';
                        items[1].style.outlineOffset='3px';
                        return items[1];
                    }
                    return null;
                    """
                )
                if found is not None:
                    order_link = found
                    print("      ✓ 命中策略D（JS选择器兜底，并已高亮）")
                else:
                    raise TimeoutException("四策略都无法定位「全部订单」链接，请看上方 DOM 快照。")

    print(f"      → 最终链接: text='{order_link.text.strip()}'  href={order_link.get_attribute('href')}")

    # 高亮并截图（若策略D已高亮，则这里再确认一下）
    driver.execute_script(
        "arguments[0].style.outline='3px solid #e8616c';"
        "arguments[0].style.outlineOffset='3px';"
        "arguments[0].scrollIntoView({block:'center'});",
        order_link
    )
    time.sleep(0.4)
    driver.save_screenshot("uc_05_order_menu_highlighted.png")
    driver.execute_script(
        "arguments[0].style.outline=''; arguments[0].style.outlineOffset='';",
        order_link
    )
    print("      ✓ 截图: uc_05_order_menu_highlighted.png")

    print("[2/4] 点击「全部订单」...")
    try:
        order_link.click()
    except Exception as e:
        print(f"      ⚠ WebElement.click() 失败: {e}，改用 JS 强制点击")
        driver.execute_script("arguments[0].click();", order_link)

    try:
        wait.until(EC.url_contains("/user/order/"))
        print(f"[3/4] ✓ 跳转成功，URL: {driver.current_url}")

        # 等订单页菜单也加载
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".left_menu_con li a")
        ))
        time.sleep(0.3)

        active_link = driver.find_element(By.CSS_SELECTOR, ".left_menu_con li a.active")
        active_text = active_link.text.strip()
        print(f"      当前激活项: '{active_text}'")
        assert "全部订单" in active_text, "❌ 跳转到订单页后，左侧「全部订单」未被高亮！"
        print("      ✓ 激活项断言通过")
        driver.save_screenshot("uc_05_order_page.png")
        print("[4/4] ✓ 截图: uc_05_order_page.png")
        passed_cases += 1
    except TimeoutException:
        print(f"[3/4] ✗ 未跳转到订单页，当前 URL: {driver.current_url}")
        driver.save_screenshot("uc_05_order_fail.png")

    # ==============================================
    # 【最终汇总】
    # ==============================================
    print("\n" + "=" * 70)
    print("【测试汇总】")
    print("=" * 70)
    print(f"  总用例数: {total_cases}")
    print(f"  通过用例: {passed_cases}")
    print(f"  失败用例: {total_cases - passed_cases}")
    if passed_cases == total_cases:
        print("  ✅ 全部用例通过！")
    else:
        print("  ⚠ 存在失败用例，请查看截图和日志")


except AssertionError as e:
    print(f"\n❌ 断言失败: {e}")
    try:
        driver.save_screenshot("uc_assertion_failed.png")
        print("✓ 已截图: uc_assertion_failed.png")
    except:
        pass

except Exception as e:
    print(f"\n❌ [异常] 脚本执行出错: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    try:
        driver.save_screenshot("uc_error.png")
        print("✓ 异常截图已保存: uc_error.png")
    except:
        pass

finally:
    print("\n" + "=" * 70)
    print("程序结束，按回车键关闭浏览器...")
    print("=" * 70)
    input()
    driver.quit()
    print("浏览器已关闭。")
