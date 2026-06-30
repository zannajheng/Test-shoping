import requests
import unittest

class Test(unittest.TestCase):#创建测试类，使用TestCase作为基类
    # 一、用户认证模块
    # 1. 验证码获取 — 真实路径 /user/verify/code/ （来自 apps/user/urls.py:36）


    # 2. 用户登录
    def test_login(self):
        url = "http://localhost:8000/user/login/"
        data = {"user": "zhengziyi", "password": "11111111", "verifycode": "1"}
        header = {"User-Agent":
                      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"}
        # 1. 创建会话，保存cookie  ---先 GET 页面，服务器才会下发 csrftoken Cookie
        session = requests.Session()
        session.get(url, headers=header)  # 先去访问一下
        # 2.取出 csrf token
        csrf_token = session.cookies.get("csrftoken")
        # 3. 构造POST请求头，
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            "X-CSRFToken": csrf_token}
        # print(header)
        response = session.post(url=url, data=data, headers=header)
        # print(response.url)
        # expect_code = 200
        # self.assertEqual(expect_code,response["code"], msg="错误了")

#如果去完成性能测试，需要解决的问题是 如何使用  self.client去获得session。
if __name__ == "__main__":
    unittest.main()