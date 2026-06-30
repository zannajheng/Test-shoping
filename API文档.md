# 🛒 电商系统 API 文档

**Base URL:** `http://localhost:8000`  
**项目架构:** Django 5.0 + Channels (WebSocket)

---

## 一、用户认证模块

### 1. 验证码获取
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/verify/code/` |
| **请求参数** | 无 |
| **返回** | PNG 图片 (image/png)，验证码存入 session: `verifycode`，有效期 60 秒 |
| **备注** | 4位随机字符（字母+数字） |

---

### 2. 用户登录
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` / `POST` |
| **接口路径** | `/user/login/` |
| **GET** | 返回登录页面 |
| **POST 参数 (Form)** | |
| &nbsp;&nbsp;`user` | 用户名 (必填, 最多20字符) |
| &nbsp;&nbsp;`password` | 密码 (必填, 5-20字符) |
| &nbsp;&nbsp;`verifycode` | 验证码 (必填) |
| **成功返回** | 302 重定向到 `/user/index/`，设置 session `info` 有效期7天 |
| **失败返回** | 渲染登录页并显示错误消息 |

---

### 3. 登录用户名检查 (AJAX)
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/login/check/` |
| **参数** | `uname` (Query String): 用户名 |
| **返回 JSON** | |
| &nbsp;&nbsp;用户存在 | `{"code":200, "count":1}` |
| &nbsp;&nbsp;用户不存在 | `{"code":200, "count":0}` |

---

### 4. 注册页面
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/register/` |
| **返回** | 渲染注册页面 (RegisterForm) |

---

### 5. 注册提交
| 项 | 说明 |
|---|---|
| **请求方式** | `POST` |
| **接口路径** | `/user/register/sumbit/` |
| **CSRF 豁免** | ✅ 是 |
| **POST 参数 (Form)** | |
| &nbsp;&nbsp;`user` | 用户名 (必填, 最多25字符) |
| &nbsp;&nbsp;`password` | 密码 (必填, 5-20字符) |
| &nbsp;&nbsp;`password_confirmation` | 确认密码 (必填, 需与密码一致) |
| &nbsp;&nbsp;`email` | 邮箱 (可选) |
| **返回 JSON** | |
| &nbsp;&nbsp;成功 | `{"code":200, "message":"注册成功"}` |
| &nbsp;&nbsp;用户已存在 | `{"code":302, "message":"用户已存在"}` |
| &nbsp;&nbsp;密码不一致 | `{"code":302, "message":"两次密码不一致"}` |
| &nbsp;&nbsp;验证失败 | `{"code":302, "message":"验证失败"}` |

---

### 6. 注册用户名检查
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/register/check/` |
| **参数** | `uname` (Query String): 用户名 |
| **返回 JSON** | |
| &nbsp;&nbsp;可用 | `{"code":200, "count":0}` |
| &nbsp;&nbsp;已占用 | `{"code":200, "count":1}` |

---

### 7. 用户退出
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/logout/` |
| **返回** | 302 重定向到登录页，清除 session |

---

### 8. 找回密码/修改密码
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` / `POST` |
| **接口路径** | `/user/password/` |
| **GET** | 返回密码修改页面 |
| **POST 参数 (Form)** | |
| &nbsp;&nbsp;`user` | 用户名 |
| &nbsp;&nbsp;`password` | 新密码 (最少6字符) |
| &nbsp;&nbsp;`password_confirmation` | 确认密码 |
| **成功返回** | 302 重定向到登录页 |
| **失败返回** | 重定向回密码页，显示错误消息 |

---

## 二、商品浏览模块

### 9. 首页
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/index/` |
| **返回** | 渲染首页，按分类展示所有商品 |
| **根路径** | `/` 会 302 重定向到此 |

---

### 10. 商品详情页
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/detail/<int:sku_id>/` |
| **路径参数** | `sku_id`: 商品ID |
| **返回** | 渲染详情页，自动记录浏览历史（最多10条），含评论区 |

---

### 11. 商品搜索
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/search/` |
| **参数** | `query`: 搜索关键词；`page`: 页码(默认1，每页12条) |
| **返回** | 渲染搜索结果页，模糊匹配商品名 |

---

### 12. 搜索分页 (AJAX)
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/search/page/` |
| **参数** | `query`、`page` |
| **返回 JSON** | |
| &nbsp;&nbsp;成功 | `{"code":200, "goods_data":[{"id":xx, "goods_name":"xx", "price":xx, "images":"xx", "intro":"xx"}, ...]}` |
| &nbsp;&nbsp;空页 | `{"code":-1, "message":"数据为空", "pages":总页数}` |

---

### 13. 分类商品列表
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/index/list/` |
| **参数** | `type_id`: 分类ID；`page`: 页码(默认1，每页10条) |
| **返回** | 渲染商品列表页，含2个随机推荐商品 |

---

### 14. 分类列表分页 (AJAX)
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/index/list/page/` |
| **参数** | `type_id`、`page` |
| **返回 JSON** | |
| &nbsp;&nbsp;成功 | `{"code":200, "message":"操作成功", "goods":[{...}]}` |
| &nbsp;&nbsp;空页 | `{"code":500, "message":"数据为空", "pages":总页数}` |

---

### 15. 分类列表按价格排序 (AJAX)
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/index/list/price/` |
| **参数** | `type_id`、`page` |
| **返回 JSON** | `{"code":200, "goods":[{...}]}` 按价格降序 |

---

## 三、购物车模块

### 16. 加入购物车 (详情页)
| 项 | 说明 |
|---|---|
| **请求方式** | `POST` |
| **接口路径** | `/user/cartadd/` |
| **需要登录** | ✅ 是 |
| **POST 参数** | `sku_id`: 商品ID；`num_show`: 数量 |
| **返回 JSON** | |
| &nbsp;&nbsp;成功 | `{"code":200, "count":购物车总数, "message":"加入购物车成功"}` |
| &nbsp;&nbsp;未登录 | `{"code":302, "message":"用户未登录"}` |

---

### 17. 加入购物车 (搜索页)
| 项 | 说明 |
|---|---|
| **请求方式** | `POST` |
| **接口路径** | `/user/search/cartadd/` |
| **需要登录** | ✅ 是 |
| **POST 参数** | `sku_id` |
| **默认数量** | 1 |
| **返回 JSON** | `{"code":200, "message":"操作成功", "count":购物车总数}` |

---

### 18. 购物车页面
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` / `POST` |
| **接口路径** | `/user/cart/` |
| **GET** | 渲染购物车列表，展示商品、数量、总价 |
| **POST (下单)** | **需要登录** ✅ |
| &nbsp;&nbsp;请求体 (JSON) | `{"goods": [{"sku_id":xx, "count":xx, "addr":"地址", "tel":"电话"}]}` |
| &nbsp;&nbsp;返回 JSON | `{"code":200, "message":"订单生成"}`，自动删除对应购物车记录 |

---

### 19. 购物车数量 +1
| 项 | 说明 |
|---|---|
| **请求方式** | `POST` |
| **接口路径** | `/user/cart/add/` |
| **需要登录** | ✅ 是 |
| **POST 参数** | `sku_id` |
| **返回 JSON** | `{"code":200, "message":"添加成功"}` |

---

### 20. 购物车数量 -1
| 项 | 说明 |
|---|---|
| **请求方式** | `POST` |
| **接口路径** | `/user/cart/decr/` |
| **需要登录** | ✅ 是 |
| **POST 参数** | `sku_id` |
| **返回 JSON** | `{"code":200, "message":"操作成功"}` |

---

### 21. 删除购物车商品
| 项 | 说明 |
|---|---|
| **请求方式** | `POST` |
| **接口路径** | `/user/cart/delete/` |
| **需要登录** | ✅ 是 |
| **POST 参数** | `sku_id` |
| **返回 JSON** | `{"code":200, "message":"删除成功"}` |

---

## 四、订单模块

### 22. 订单列表
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/order/` |
| **需要登录** | ✅ 是 |
| **参数** | `page`: 页码(默认1，每页5个订单组) |
| **返回** | 渲染订单列表页，按订单号分组展示 |

---

### 23. 立即购买 (详情页直接下单)
| 项 | 说明 |
|---|---|
| **请求方式** | `POST` |
| **接口路径** | `/user/index/detail/buy/` |
| **需要登录** | ✅ 是 |
| **POST 参数** | `sku_id`: 商品ID；`count`: 数量 |
| **返回 JSON** | `{"code":200, "message":"操作成功", "order_number":"订单号"}` |
| **状态** | 初始状态为 `未支付` |

---

### 24. 支付页面
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/order/payment/<str:order_number>/` |
| **路径参数** | `order_number`: 订单号 |
| **返回** | 渲染支付页，展示商品列表和总金额 |

---

### 25. 更新订单状态
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/order/update/` |
| **参数** | `order_number`: 订单号；`status`: 目标状态 (如：`已发货`、`已收货`) |
| **返回** | 302 重定向回订单列表，Django messages 提示 |
| **备注** | 同订单号下所有商品状态一并更新 |

---

### 26. 删除订单
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/order/delete/` |
| **参数** | `order_number`: 订单号 |
| **限制** | 已发货的订单不可删除 |
| **返回** | 302 重定向回订单列表 |

---

### 27. 订单评价页面
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/order/evaluate/` |
| **需要登录** | ✅ 是 |
| **参数** | `order_number` |
| **返回** | 渲染评价页，展示待评价商品 |

---

### 28. 提交订单评价
| 项 | 说明 |
|---|---|
| **请求方式** | `POST` |
| **接口路径** | `/user/order/evalute/submit/` |
| **POST 参数** | |
| &nbsp;&nbsp;`order_number` | 订单号 |
| &nbsp;&nbsp;`reviews` | JSON 字符串: `[{"sku_id":xx, "evaluate":"评论文本"}, ...]` |
| **返回 JSON** | `{"code":200, "page":"添加N条评论！"}` |

---

## 五、个人中心

### 29. 用户中心
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/center/` |
| **需要登录** | ✅ 是 |
| **返回** | 渲染用户中心，展示浏览历史商品 |

---

### 30. 收货地址页
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/address/` |
| **返回** | 渲染地址填写页面 |

---

## 六、反馈模块

### 31. 反馈页面
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/user/feedback/` |
| **返回** | 渲染反馈提交页面 |

---

### 32. 提交反馈
| 项 | 说明 |
|---|---|
| **请求方式** | `POST` |
| **接口路径** | `/user/feedback/upload/` |
| **需要登录** | ✅ 是 |
| **CSRF 豁免** | ✅ 是 |
| **POST 参数 (multipart/form-data)** | |
| &nbsp;&nbsp;`textarea_name` | 反馈内容 |
| &nbsp;&nbsp;`input_name` | 反馈标题/分类 |
| &nbsp;&nbsp;`file0` ~ `file4` | 最多5张图片 (可选) |
| **返回 JSON** | `{"code":200, "message":"反馈成功"}` |
| **自动生成** | `feedback_number` (2大写字母-时间戳格式) |

---

## 七、客服模块 (Service)

### 33. 用户客服聊天页
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/service/` |
| **需要登录** | ✅ 是 |
| **参数** | `number`: 客服会话编号 |
| **返回** | 渲染聊天页面，展示历史消息 |

---

### 34. 管理员客服后台
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/admin/service/` |
| **需要管理员** | ✅ 是 (is_superuser=1) |
| **参数** | `number` (可选): 当前选中的会话编号 |
| **返回** | 渲染客服管理页，左侧会话列表+右侧聊天窗口 |
| **自动创建** | 为每个普通用户生成唯一客服编号 (格式：大写字母+时间戳) |

---

### 35. 标记会话已读
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/admin/service/reading/` |
| **参数** | `number`: 会话编号 |
| **返回 JSON** | `{"code":200, "message":"更新成功"}` |

---

### 36. 批量查询未读消息数
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/admin/service/reading/send/` |
| **参数** | `numbers[]`: 会话编号数组 (Query String 重复传参) |
| **返回 JSON** | `{"code":200, "data":{"编号1":未读数, "编号2":未读数...}, "message":"更新成功"}` |

---

### 37. 获取表情包列表
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/service/face/` |
| **返回 JSON** | `{"code":200, "faces":{"001":"笑脸", "002":"哭脸"...}, "message":"操作成功"}` |
| **图片资源** | 存放于 `/static/face/xxx.png` |

---

### 38. 管理员更新订单状态
| 项 | 说明 |
|---|---|
| **请求方式** | `GET` |
| **接口路径** | `/admin/order/update/` |
| **需要管理员** | ✅ 是 |
| **参数** | `order_number`: 订单号；`status`: 目标状态 |
| **返回** | 302 重定向到 `/admin/user/order/` |

---

## 八、WebSocket 实时聊天

### 39. WebSocket 连接
| 项 | 说明 |
|---|---|
| **协议** | `ws://` |
| **连接地址** | `ws://localhost:8000/room/<group>/` |
| **路径参数** | `group`: 客服会话编号 (即 `number`) |
| **认证** | 依赖 Django session |

---

### 发送消息格式 (客户端 → 服务器)

**① 文本消息**
```json
{
  "type": "text",
  "username": "admin 或 普通用户名",
  "text": "消息内容"
}
```

**② 表情消息**
```json
{
  "type": "face",
  "username": "admin 或 普通用户名",
  "id": "001"
}
```

**③ 图片消息**
```json
{
  "type": "image",
  "username": "admin 或 普通用户名",
  "fileName": "图片名",
  "image_data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ..."
}
```

**消息存储说明:**
- `status=0`: 用户发送
- `status=1`: 管理员发送
- `type` 字段默认为 `text`，图片和表情分别为 `image` / `face`

---

## 九、支付宝支付 (AliPay SDK 封装)

### 初始化参数
| 参数 | 说明 |
|---|---|
| `appid` | 支付宝应用 ID |
| `app_notify_url` | 异步回调地址 |
| `app_private_key_path` | 应用私钥路径 (PEM) |
| `alipay_public_key_path` | 支付宝公钥路径 (PEM) |
| `return_url` | 同步回调地址 |
| `debug` | `True`=沙箱环境，`False`=正式环境 |

### 主要方法
| 方法 | 说明 |
|---|---|
| `direct_pay(subject, out_trade_no, total_amount, ...)` | 生成 PC 端支付链接字符串 (已签名) |
| `verify(data, signature)` | 验证支付宝回调签名 |

---

## 十、通用约定

### 🔐 认证方式
- **Session/Cookie 认证**：登录后 Django 自动管理
- 受保护接口返回未登录时：JSON 返回 `{"code":302, "message":"用户未登录"}` 或页面 302 跳转到 `/user/login/?is_login=1`

### 📦 响应状态码 (JSON 接口)
| code | 含义 |
|---|---|
| 200 | 成功 |
| 302 | 业务失败 (用户未登录/已存在/密码不一致等) |
| 500 | 服务器端错误 / 数据为空 |
| -1 | 分页数据为空 |

### 🔑 CSRF Token
- 大部分接口需要 CSRF Token
- 已豁免接口 (标注 `@csrf_exempt`)：`/user/register/sumbit/`、`/user/feedback/upload/`

---

> 💡 **测试建议**: 使用 Postman / Apifox 导入以上接口进行测试。页面渲染类接口建议直接用浏览器访问，JSON 接口可用 Postman 测试请求参数和返回格式。
