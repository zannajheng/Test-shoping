# -*- coding: utf-8 -*-
"""
报告输出: reports/unittest/Shoping珠宝首饰商城系统测试报告.html
"""

import os
import sys
import unittest

#引入测试用例
from test_shopping_interface import TestShoppingInterface

# 实例化测试套件
suite = unittest.TestSuite()

# 添加测试用例的方法
suite.addTest(TestShoppingInterface("test_01_verify_code"))
suite.addTest(TestShoppingInterface("test_02_login_get"))
suite.addTest(TestShoppingInterface("test_02_login_post_failed"))
suite.addTest(TestShoppingInterface("test_03_login_check_exist"))
suite.addTest(TestShoppingInterface("test_03_login_check_not_exist"))
suite.addTest(TestShoppingInterface("test_04_register_page"))
suite.addTest(TestShoppingInterface("test_05_register_submit_success"))
suite.addTest(TestShoppingInterface("test_05_register_submit_dup_user"))
suite.addTest(TestShoppingInterface("test_05_register_submit_pwd_mismatch"))
suite.addTest(TestShoppingInterface("test_05_register_submit_form_invalid"))
suite.addTest(TestShoppingInterface("test_06_register_check_available"))
suite.addTest(TestShoppingInterface("test_06_register_check_taken"))
suite.addTest(TestShoppingInterface("test_07_logout"))
suite.addTest(TestShoppingInterface("test_08_password_get"))
suite.addTest(TestShoppingInterface("test_08_password_post_success"))
suite.addTest(TestShoppingInterface("test_08_password_post_short"))
suite.addTest(TestShoppingInterface("test_08_password_post_user_not_exist"))
suite.addTest(TestShoppingInterface("test_09_index"))
suite.addTest(TestShoppingInterface("test_09_root_redirect"))
suite.addTest(TestShoppingInterface("test_10_detail"))
suite.addTest(TestShoppingInterface("test_11_search"))
suite.addTest(TestShoppingInterface("test_11_search_empty_query"))
suite.addTest(TestShoppingInterface("test_12_search_page_data"))
suite.addTest(TestShoppingInterface("test_12_search_page_empty"))
suite.addTest(TestShoppingInterface("test_13_more_list"))
suite.addTest(TestShoppingInterface("test_14_more_list_page"))
suite.addTest(TestShoppingInterface("test_15_more_list_price"))
suite.addTest(TestShoppingInterface("test_16_cartadd_not_login"))
suite.addTest(TestShoppingInterface("test_16_cartadd_logged_in"))
suite.addTest(TestShoppingInterface("test_17_search_cartadd_not_login"))
suite.addTest(TestShoppingInterface("test_17_search_cartadd_logged_in"))
suite.addTest(TestShoppingInterface("test_18_cart_get"))
suite.addTest(TestShoppingInterface("test_18_cart_post_place_order"))
suite.addTest(TestShoppingInterface("test_19_cart_add_plus"))
suite.addTest(TestShoppingInterface("test_20_cart_decr"))
suite.addTest(TestShoppingInterface("test_21_cart_delete"))
suite.addTest(TestShoppingInterface("test_22_order_list"))
suite.addTest(TestShoppingInterface("test_23_index_detail_buy"))
suite.addTest(TestShoppingInterface("test_24_payment_page"))
suite.addTest(TestShoppingInterface("test_25_order_update_status"))
suite.addTest(TestShoppingInterface("test_25_order_update_missing_param"))
suite.addTest(TestShoppingInterface("test_26_order_delete_shipped_forbidden"))
suite.addTest(TestShoppingInterface("test_26_order_delete_ok"))
suite.addTest(TestShoppingInterface("test_27_order_evaluate_page"))
suite.addTest(TestShoppingInterface("test_28_order_evaluate_submit"))
suite.addTest(TestShoppingInterface("test_29_user_center"))
suite.addTest(TestShoppingInterface("test_30_address_page"))
suite.addTest(TestShoppingInterface("test_31_feedback_page"))
suite.addTest(TestShoppingInterface("test_32_feedback_upload_not_login"))
suite.addTest(TestShoppingInterface("test_32_feedback_upload_logged_in"))
suite.addTest(TestShoppingInterface("test_33_service_page_need_login"))
suite.addTest(TestShoppingInterface("test_34_admin_service_page"))
suite.addTest(TestShoppingInterface("test_35_admin_reading"))
suite.addTest(TestShoppingInterface("test_36_admin_reading_send"))
suite.addTest(TestShoppingInterface("test_37_service_face"))
suite.addTest(TestShoppingInterface("test_38_admin_order_update"))
suite.addTest(TestShoppingInterface("test_38_admin_order_update_missing_param"))
suite.addTest(TestShoppingInterface("test_99_websocket_and_alipay_out_of_scope"))


from HTMLTestRunner import HTMLTestRunner

#参数1 stream 文件流，要生成的报告要写/出到哪一个文件夹中去
#参数2 title 可选参数，报告标题
#参数3 description 可选参数，描述信息

# 引入 HTMLTestRunner
runner = HTMLTestRunner(
    stream=open("./Shoping珠宝首饰商城系统测试报告.html", "wb"),
    title="Shoping珠宝首饰商城系统测试报告",
    description="这是一个基于Django的珠宝首饰商城系统的测试报告"
)

runner.run(suite)