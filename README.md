## 📋 项目介绍：首饰购物电商网站 (Shoping)

这是一个基于 Django 5.0.6 开发的**首饰购物电商平台**，包含前台用户购物系统和后台管理系统，以及实时在线客服功能。

---

### 🏗️ 技术栈

| 技术/依赖 | 版本 | 用途 |
|-----------|------|------|
| Django | 5.0.6 | 核心 Web 框架 |
| django-simpleui | 2024.4.1 | 后台管理界面美化（Element UI 风格） |
| channels | 3.0.5 | WebSocket 实时通讯（在线客服） |
| mysqlclient | 2.2.4 | MySQL 数据库驱动 |
| pycryptodome | 3.20.0 | 加密库（支付宝支付签名） |
| Pillow | 10.3.0 | 图像处理（验证码生成） |

- 配置文件：`settings.py`
- 数据库配置：MySQL `mydb`，用户 `root/123456`（settings.py#L89-L98）

---

### 📁 项目结构

```
shoping/
├── apps/
│   ├── user/          # 核心业务模块（商品、订单、购物车、用户等）
│   └── service/       # 在线客服模块（WebSocket聊天）
├── shoping/           # Django 项目配置目录
├── media/             # 用户上传文件（商品图片、反馈图片、客服图片）
├── static/            # 静态资源（CSS、头像表情包）
├── templates/         # HTML 模板
├── db.sql / shopping.sql  # 数据库SQL文件
├── manage.py
└── requirements.txt
```

---

### 🛒 核心功能模块

#### 一、前台用户端（apps/user）

| 功能 | 说明 | 主要文件 |
|------|------|----------|
| 首页展示 | 按分类展示首饰商品 | views.py#L28-L39 |
| 商品详情 | 商品信息、评论、浏览记录、推荐商品 | views.py#L42-L61 |
| 用户注册/登录 | Django auth 系统 + 图形验证码 | views.py#L64-L177 |
| 密码找回 | 通过用户名重置密码 | views.py#L180-L202 |
| 图形验证码 | PIL 动态生成，存入 Session | views.py#L661-L700 |
| 购物车 | 添加/增减/删除商品，批量下单 | views.py#L205-L319 |
| 订单管理 | 下单、支付、状态更新、删除、评价 | views.py#L322-L579 |
| 商品搜索 | 模糊搜索 + 分页 + 价格排序 | views.py#L356-L503 |
| 商品评价 | 订单完成后批量评价商品 | views.py#L582-L616 |
| 用户中心 | 浏览历史记录 | views.py#L345-L349 |
| 用户反馈/投诉 | 支持上传最多5张图片 | views.py#L634-L658 |
| 支付宝支付 | 集成 Alipay SDK（待配置密钥） | utils/pay.py |

---

#### 二、后台管理端（SimpleUI 定制）

后台菜单已自定义配置（settings.py#L148-L165）：

- **首饰管理** — 商品 CRUD
- **订单管理** — 订单状态更新/发货
- **首饰类型** — 商品分类管理
- **用户浏览报表** — 用户浏览记录统计
- **评论管理** — 商品评论审核
- **用户消息管理** — 在线客服会话
- **投诉管理** — 用户反馈处理
- **用户管理** — Django 用户系统

---

#### 三、实时在线客服（apps/service）

基于 Django Channels + WebSocket 实现：

- 用户端和管理员端实时聊天
- 支持**文字、表情包、图片**三种消息类型
- 消息已读/未读状态管理
- 管理员可切换不同用户的会话

核心文件：

- WebSocket 消费者：`consumers.py`
- 客服视图：`views.py`
- 路由配置：`routing.py`

---

### 🗄️ 数据库模型（11张表）

定义在 `apps/user/models.py`：

| 模型 | 表名 | 说明 |
|------|------|------|
| GoodsType | goods_type | 首饰类型/分类 |
| Goods | goods | 首饰商品（名称、价格、销量、图片） |
| Cart | cart | 购物车 |
| Order | order | 订单（含收货地址、电话、评价状态） |
| Browse | browse | 用户浏览记录（最多保留10条） |
| Evaluate | evaluate | 商品评论 |
| FeedBack_user | feedback_user | 用户投诉/反馈 |
| FeedBack_Image | feedback_image | 反馈图片（1对多） |
| Service | service | 客服会话编号 |
| Message | message | 聊天消息（发送/接收，已读/未读） |
| Face | face | 表情包素材 |

---

### 🔐 认证与中间件

- 自定义登录验证中间件：`auth_middle.py`
- 注册/登录表单验证：`form.py`
- 登录 URL：`/user/login/`，Session 有效期 7 天

---

### 🚀 启动方式

```powershell
# 1. 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 2. 安装依赖（如未安装）
pip install -r requirements.txt

# 3. 启动服务
python manage.py runserver
```

访问地址：

- **前台首页**：http://127.0.0.1:8000/user/index/
- **后台管理**：http://127.0.0.1:8000/admin/
- **在线客服**：http://127.0.0.1:8000/service/

---

### 💡 项目亮点

1. **完整电商闭环** — 浏览 → 搜索 → 购物车 → 下单 → 支付 → 评价 → 售后
2. **实时通讯** — WebSocket 客服系统支持文字、表情、图片
3. **后台美化** — SimpleUI 定制化菜单，管理体验好
4. **图形验证码** — 防机器人注册登录
5. **浏览历史** — 自动记录并限制最多10条
6. **订单状态流转** — 已下单 → 已发货 → 已完成，支持删除和评价
