# 首饰购物商城 - Code Wiki 文档

## 目录
1. [项目概述](#项目概述)
2. [技术栈](#技术栈)
3. [项目架构](#项目架构)
4. [目录结构](#目录结构)
5. [核心模块详解](#核心模块详解)
6. [数据模型](#数据模型)
7. [API接口](#api接口)
8. [前端模板与静态资源](#前端模板与静态资源)
9. [依赖关系](#依赖关系)
10. [项目运行](#项目运行)
11. [配置说明](#配置说明)
12. [开发注意事项与已知问题](#开发注意事项与已知问题)

---

## 项目概述

本项目是一个基于 **Django 5.0** 开发的**首饰购物商城系统**，提供完整的电商功能，包括商品展示、购物车、订单管理、用户认证、商品评论、用户反馈以及在线客服等功能。系统采用传统的服务端渲染（SSR）模式，配合 Django Admin + SimpleUI 作为后台管理界面，使用 Django Channels 实现 WebSocket 实时聊天。

**主要功能特性：**
- 🛒 商品分类浏览与搜索
- 🛍️ 购物车管理（增删改查）
- 📦 订单管理与状态跟踪
- 💬 商品评论系统
- 📝 用户反馈与投诉（支持图片上传）
- 💬 在线客服（WebSocket 实时聊天，支持文字/表情/图片）
- 👤 用户注册/登录/密码找回
- 📊 用户浏览记录统计（最多10条）
- 🎨 后台管理系统（SimpleUI 定制）
- 🔐 图形验证码（已注释，可按需开启）
- 💰 支付宝支付接口封装

---

## 技术栈

### 后端框架
| 技术 | 版本 | 用途 |
|------|------|------|
| **Django** | 5.0.6 | 核心 Web 框架 |
| **Channels** | 3.0.5 | WebSocket 支持（在线客服） |
| **Django SimpleUI** | 2024.4.1 | 后台管理界面美化（Element UI 风格） |

### 数据库
| 技术 | 版本 | 用途 |
|------|------|------|
| **MySQL** | 8.0+ | 主数据库 |
| **mysqlclient** | 2.2.4 | MySQL 驱动 |

### 工具库
| 库 | 版本 | 用途 |
|----|------|------|
| **Pillow** | 10.3.0 | 图像处理（验证码生成、商品图片） |
| **pycryptodome** | 3.20.0 | 加密算法（支付宝 RSA2 签名） |
| **six** | 1.17.0 | Python 2/3 兼容库（BytesIO） |

### 前端
- 服务端渲染（Django Templates + Jinja2 语法）
- 原生 JavaScript + AJAX（jQuery 3.7.1）
- 静态资源：CSS、JS、图片、字体图标

---

## 项目架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                      客户端浏览器                        │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────▼─────────────┐
        │   HTTP / WebSocket       │
        └────────────┬─────────────┘
                     │
┌────────────────────▼─────────────────────────────────────┐
│                   ASGI Application                       │
│  ┌───────────────┐            ┌──────────────────┐      │
│  │  HTTP 协议    │            │  WebSocket 协议  │      │
│  └───────┬───────┘            └────────┬─────────┘      │
└──────────┼─────────────────────────────┼────────────────┘
           │                             │
┌──────────▼──────────┐      ┌──────────▼──────────┐
│   apps/user 应用    │      │  apps/service 应用  │
│  (商品/订单/用户)   │      │  (在线客服页面)     │
└──────────┬──────────┘      └──────────┬──────────┘
           │                             │
           └──────────────┬──────────────┘
                          │
               ┌──────────▼──────────┐
               │     MySQL 数据库    │
               └─────────────────────┘
```

### 架构说明

1. **ASGI 服务器**：项目使用 ASGI 协议替代传统的 WSGI，以支持 WebSocket 长连接
2. **双应用架构**：
   - `apps/user`：核心电商业务模块（商品、订单、购物车、用户、客服数据模型）
   - `apps/service`：在线客服模块（WebSocket 消费者、客服页面、表情包）
3. **数据库**：MySQL 作为主数据库，存储所有业务数据（共 11 张表）
4. **Channel Layer**：使用内存 Channel Layer（开发环境），用于 WebSocket 群组通信
5. **认证体系**：基于 Django Auth 系统 + Session，配合自定义中间件做登录校验

---

## 目录结构

```
Test-shoping/
├── apps/                          # Django 应用目录
│   ├── user/                      # 核心电商应用
│   │   ├── migrations/            # 数据库迁移文件
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── utils/                 # 工具模块
│   │   │   ├── keys/              # 支付宝密钥文件
│   │   │   │   ├── alipay_public_key.pem
│   │   │   │   └── app_private_key.pem
│   │   │   ├── auth_middle.py     # 登录认证中间件
│   │   │   ├── form.py            # 表单验证类
│   │   │   └── pay.py             # 支付宝支付封装
│   │   ├── __init__.py
│   │   ├── admin.py               # 后台管理配置
│   │   ├── apps.py                # 应用配置
│   │   ├── models.py              # 数据模型定义（10个模型）
│   │   ├── tests.py               # 测试文件
│   │   ├── urls.py                # URL 路由配置（32个路由）
│   │   └── views.py               # 视图函数（约30个）
│   └── service/                   # 客服/聊天应用
│       ├── migrations/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── consumers.py           # WebSocket 消费者（ChatConsumer）
│       ├── models.py              # 表情包模型（Face）
│       ├── tests.py
│       ├── urls.py                # 客服相关 URL
│       └── views.py               # 客服页面视图
├── media/                         # 用户上传的媒体文件
│   ├── images/                    # 商品分类/商品图片
│   ├── products/                  # 产品图片
│   └── uploads/                   # 用户反馈上传图片
├── shoping/                       # 项目配置目录
│   ├── __init__.py
│   ├── asgi.py                    # ASGI 入口配置
│   ├── routing.py                 # WebSocket 路由配置
│   ├── settings.py                # Django 全局配置
│   ├── urls.py                    # 主 URL 配置
│   └── wsgi.py                    # WSGI 配置（备用）
├── static/                        # 静态资源
│   ├── css/                       # 样式文件（7个CSS）
│   ├── js/                        # JavaScript 文件（16个JS）
│   ├── face/                      # 表情包图片（99个PNG）
│   ├── images/                    # 页面图片素材
│   ├── fonts/                     # 字体图标
│   └── simpleui/                  # SimpleUI 自定义样式
├── templates/                     # HTML 模板目录（20个模板）
│   ├── base_foot.html             # 底部公共模板
│   ├── bade.html                  # 基础模板
│   ├── user_base.html             # 用户中心基础模板
│   ├── index.html                 # 首页
│   ├── login.html                 # 登录页
│   ├── register.html              # 注册页
│   ├── password.html              # 找回密码页
│   ├── detail.html                # 商品详情页
│   ├── cart.html                  # 购物车页
│   ├── order.html                 # 订单列表页
│   ├── payment.html               # 支付页
│   ├── order_evaluate.html        # 订单评价页
│   ├── search.html                # 搜索结果页
│   ├── more_list.html             # 分类列表页
│   ├── usercenter.html            # 用户中心页
│   ├── address.html               # 收货地址页
│   ├── feedback.html              # 用户反馈页
│   ├── service.html               # 用户客服页
│   └── admin_service.html         # 管理员客服页
├── manage.py                      # Django 管理命令入口
├── requirements.txt               # 项目依赖列表
├── db.sql                         # 数据库初始化脚本
├── shopping.sql                   # 数据库备份
├── API文档.md                     # API 接口文档
├── 启动指南.md                    # 快速启动指南
├── README.md                      # 项目说明
└── CODE_WIKI.md                   # 本文档
```

---

## 核心模块详解

### 1. apps/user - 核心电商模块

#### 模块职责
负责商城的核心业务逻辑，包括：
- 商品展示与分类浏览
- 用户认证（注册/登录/找回密码）
- 购物车管理
- 订单管理（下单/支付/发货/收货/评价/删除）
- 商品评论
- 用户反馈/投诉（支持最多5张图片）
- 浏览历史记录
- 客服会话与消息数据模型

#### 核心文件说明

**[models.py](file:///d:/Desktop/Test-shoping/apps/user/models.py)**

定义了 10 个数据模型，详见 [数据模型](#数据模型) 章节。

**[views.py](file:///d:/Desktop/Test-shoping/apps/user/views.py)**

包含约 30 个视图函数，处理所有业务逻辑。关键函数：

| 函数名 | 功能说明 | 请求方式 | 权限 | 所在行 |
|--------|----------|----------|------|--------|
| `index()` | 首页，按分类展示商品 | GET | 公开 | L28-L39 |
| `detail(sku_id)` | 商品详情页，记录浏览历史 | GET | 公开 | L42-L61 |
| `user_login()` | 用户登录 | GET/POST | 公开 | L64-L95 |
| `register()` | 用户注册页面 | GET | 公开 | L114-L116 |
| `register_submit()` | 注册提交处理 | POST | 公开 | L119-L155 |
| `user_logout()` | 退出登录 | GET | 需登录 | L174-L177 |
| `password()` | 找回密码 | GET/POST | 公开 | L180-L202 |
| `cartadd()` | 添加商品到购物车 | POST | 需登录 | L205-L231 |
| `cart()` | 购物车列表/下单 | GET/POST | 需登录 | L252-L285 |
| `cart_add()` | 购物车数量+1 | POST | 需登录 | L288-L297 |
| `cart_decr()` | 购物车数量-1 | POST | 需登录 | L300-L309 |
| `cart_delete()` | 删除购物车商品 | POST | 需登录 | L312-L319 |
| `cart_count()` | 上下文处理器：购物车数量+客服编号 | - | 全局 | L234-L249 |
| `order()` | 我的订单列表（分页） | GET | 需登录 | L322-L342 |
| `payment(order_number)` | 订单支付页面 | GET | 需登录 | L415-L429 |
| `order_update_status()` | 更新订单状态 | GET | 需登录 | L505-L540 |
| `order_delete()` | 删除订单 | GET | 需登录 | L543-L578 |
| `order_evaluate()` | 订单评价页面 | GET | 需登录 | L581-L593 |
| `order_evaluate_sumbit()` | 提交订单评价 | POST | 需登录 | L596-L615 |
| `index_detail_buy()` | 商品详情页立即购买 | POST | 需登录 | L618-L630 |
| `search()` | 商品搜索 | GET | 公开 | L356-L362 |
| `search_page()` | 搜索分页（AJAX） | GET | 公开 | L384-L412 |
| `search_cartadd()` | 搜索页加购 | POST | 需登录 | L365-L381 |
| `more_list()` | 分类商品列表 | GET | 公开 | L432-L445 |
| `more_list_page()` | 分类列表分页（AJAX） | GET | 公开 | L473-L502 |
| `more_list_price()` | 分类按价格排序（AJAX） | GET | 公开 | L448-L470 |
| `user_center()` | 用户中心（浏览记录） | GET | 需登录 | L345-L349 |
| `address()` | 收货地址页 | GET | 需登录 | L352-L353 |
| `feedback()` | 用户反馈页面 | GET | 需登录 | L633-L634 |
| `feedback_upload()` | 提交反馈（含图片） | POST | 需登录 | L637-L657 |
| `verify_code()` | 生成图形验证码 | GET | 公开 | L660-L699 |
| `login_check()` | 登录用户名检查（AJAX） | GET | 公开 | L98-L111 |
| `register_check()` | 注册用户名检查（AJAX） | GET | 公开 | L158-L171 |

**[urls.py](file:///d:/Desktop/Test-shoping/apps/user/urls.py)**

定义了 32 个 URL 路由，统一前缀为 `/user/`。

**[admin.py](file:///d:/Desktop/Test-shoping/apps/user/admin.py)**

配置 Django Admin 后台管理界面，包括：
- **GoodsAdmin** - 商品管理（含图片预览）
- **CartAdmin** - 购物车管理（关联商品图片）
- **OrderAdmin** - 订单管理（含"确认发货"操作按钮）
- **GoodsTypeAdmin** - 商品类型管理（含图片预览）
- **BrowseAdmin** - 浏览记录管理
- **EvaluateAdmin** - 评论管理
- **Feedback_UserAdmin** - 用户反馈管理（含反馈图片预览）

**[utils/auth_middle.py](file:///d:/Desktop/Test-shoping/apps/user/utils/auth_middle.py)**

自定义登录认证中间件 `AuthLogin`，基于白名单机制：

- **免登录白名单路径**：
  - `/user/login/` - 登录页
  - `/user/register/` - 注册页
  - `/user/password/` - 找回密码页
  - `/user/index/` - 首页
  - `/user/detail/` - 商品详情
  - `/user/search/` - 搜索页
  - `/user/logout/` - 登出
  - `/user/verify/code/` - 验证码
  - `/admin/login/` - 管理员登录
  - `/media/` - 媒体文件
  - 所有 `/admin/` 开头的路径

- **特殊处理**：
  - AJAX 请求（`X-Requested-With: XMLHttpRequest`）直接放行，由视图函数自行判断
  - 未登录用户访问受保护页面：重定向到 `/user/login/?is_login=1` 并显示提示
  - 未登录访问 `/user/cartadd/`：返回 JSON `{"code": 302, "messsage": "用户未登录"}`

**[utils/form.py](file:///d:/Desktop/Test-shoping/apps/user/utils/form.py)**

表单验证类：

- **RegisterForm** - 注册表单验证
  - 字段：`user`（用户名，最多25字符）、`password`（密码）、`password_confirmation`（确认密码）、`email`（邮箱，可选）
  - 验证规则：密码长度 5-20 位、两次密码一致、用户名不存在
  - 所在行：L7-L33

- **Login** - 登录表单验证
  - 字段：`user`（用户名，最多20字符）、`password`（密码）、`verifycode`（验证码）
  - 验证规则：用户存在、密码长度 5-20 位
  - **注意**：验证码验证已被注释（L58-L59），当前验证码仅作展示不校验

**[utils/pay.py](file:///d:/Desktop/Test-shoping/apps/user/utils/pay.py)**

支付宝支付封装类 `AliPay`，支持：
- RSA2 签名算法（SHA256WithRSA）
- 电脑网站支付接口（`alipay.trade.page.pay`）
- 支付回调验签
- 沙箱/正式环境切换

主要方法：
| 方法 | 说明 |
|------|------|
| `direct_pay()` | 生成 PC 端支付链接（已签名） |
| `verify()` | 验证支付宝回调签名 |
| `sign_data()` | 对请求参数进行签名 |
| `ordered_data()` | 参数按 ASCII 排序 |

---

### 2. apps/service - 在线客服模块

#### 模块职责
提供基于 WebSocket 的实时在线客服功能，包括：
- 用户与管理员实时聊天
- 支持文字、表情、图片三种消息类型
- 消息已读/未读状态管理
- 管理员多用户会话管理
- 表情包管理

#### 核心文件说明

**[consumers.py](file:///d:/Desktop/Test-shoping/apps/service/consumers.py)**

`ChatConsumer` - WebSocket 消费者类，继承自 `WebsocketConsumer`：

| 方法 | 功能 | 所在行 |
|------|------|--------|
| `websocket_connect()` | 连接建立，加入群组 | L15-L19 |
| `websocket_receive()` | 接收消息，保存数据库，广播到群组 | L21-L43 |
| `group_send()` | 群组消息发送回调 | L45-L47 |
| `websocket_disconnect()` | 连接断开，离开群组 | L49-L52 |
| `save_image()` | 保存聊天图片（base64 解码） | L54-L74 |

**支持的消息类型：**
- `text` - 文本消息（`data['text']` 为内容）
- `face` - 表情消息（`data['id']` 为表情编号）
- `image` - 图片消息（`data['image_data']` 为 base64，`data['fileName']` 为文件名）

**消息状态说明：**
- `status=0` - 用户发送的消息
- `status=1` - 管理员发送的消息

**图片存储路径：** `media/service/` 目录下

**[views.py](file:///d:/Desktop/Test-shoping/apps/service/views.py)**

| 函数名 | 功能说明 | 权限 |
|--------|----------|------|
| `service()` | 用户端客服聊天页面，展示历史消息 | 需登录 |
| `admin_sercice()` | 管理员端客服管理页面（自动为普通用户创建客服编号） | 管理员 |
| `admin_reading()` | 标记会话消息为已读 | 管理员 |
| `admin_reading_send()` | 批量获取多个会话的未读消息数 | 管理员 |
| `admin_order_update_status()` | 管理员更新订单状态（发货等） | 管理员 |
| `face()` | 获取表情包列表（JSON） | 公开 |

**[models.py](file:///d:/Desktop/Test-shoping/apps/service/models.py)**

- **Face** - 表情包模型
  - 字段：`name`（表情名称）、`image`（图片文件名）
  - 表名：`face`

**客服编号生成规则：** `1位大写字母 + 13位毫秒时间戳`，例如 `A1692500000000`

---

### 3. shoping - 项目配置模块

**[settings.py](file:///d:/Desktop/Test-shoping/shoping/settings.py)**

核心配置文件，详见 [配置说明](#配置说明) 章节。

**[urls.py](file:///d:/Desktop/Test-shoping/shoping/urls.py)**

主 URL 路由：
- `/` → 302 重定向到 `/user/index/`
- `/user/` → `apps.user.urls`
- `/` → `apps.service.urls`（包含 `/service/`、`/admin/service/`、`/admin/order/update/` 等）
- `/admin/` → Django Admin 后台
- 静态文件和媒体文件服务（开发环境）

**[asgi.py](file:///d:/Desktop/Test-shoping/shoping/asgi.py)**

ASGI 应用入口，配置：
- HTTP 协议 → Django 常规处理
- WebSocket 协议 → `URLRouter(routing.websocket_urlpatterns)`

**[routing.py](file:///d:/Desktop/Test-shoping/shoping/routing.py)**

WebSocket 路由配置：
- `room/<group>/` → `ChatConsumer`（`group` 即客服会话编号）

---

## 数据模型

### 数据库表总览

| 表名 | 模型类 | 所在文件 | 说明 |
|------|--------|----------|------|
| `goods_type` | GoodsType | apps/user/models.py | 商品类型/分类 |
| `goods` | Goods | apps/user/models.py | 商品（首饰）信息 |
| `cart` | Cart | apps/user/models.py | 购物车 |
| `order` | Order | apps/user/models.py | 订单 |
| `browse` | Browse | apps/user/models.py | 用户浏览记录 |
| `evaluate` | Evaluate | apps/user/models.py | 商品评论 |
| `feedback_user` | FeedBack_user | apps/user/models.py | 用户反馈/投诉 |
| `feedback_image` | FeedBack_Image | apps/user/models.py | 反馈图片 |
| `service` | Service | apps/user/models.py | 客服会话 |
| `message` | Message | apps/user/models.py | 聊天消息 |
| `face` | Face | apps/service/models.py | 表情包 |

> **注意**：Service 和 Message 模型定义在 `apps/user/models.py` 中，Face 模型定义在 `apps/service/models.py` 中。

---

### 1. GoodsType（商品类型）

**表名：** `goods_type`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `goods_type_name` | CharField(255) | 类型名称 |
| `images` | ImageField(upload_to='images/') | 分类图片（jpg/jpeg/png） |
| `class_name` | CharField(255) | 标签/样式类名 |

**关联关系：**
- 被 `Goods.type_id` 外键引用（一对多）

---

### 2. Goods（商品）

**表名：** `goods`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `goods_name` | CharField(255) | 首饰名称 |
| `intro` | CharField(255) | 首饰说明/简介 |
| `sell` | IntegerField | 售出数量 |
| `price` | DecimalField(10,2) | 价格 |
| `cation` | CharField(255) | 单位（如：克、个、件） |
| `images` | ImageField(upload_to='images/') | 首饰图片 |
| `type_id` | ForeignKey → GoodsType | 所属商品分类（级联删除） |

**关联关系：**
- 外键 `type_id` → GoodsType（多对一）
- 被 Cart、Order、Browse、Evaluate 引用

---

### 3. Cart（购物车）

**表名：** `cart`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `user` | CharField(255) | 用户名（存 username 字符串） |
| `sku_id` | IntegerField | 商品ID（注意：不是外键） |
| `count` | IntegerField | 商品数量 |
| `updated_at` | DateTimeField(auto_now=True) | 更新时间 |
| `created_at` | DateTimeField(auto_now_add=True) | 创建时间 |

> **重要注意**：`sku_id` 字段是 IntegerField 而非 ForeignKey，代码中通过手动查询 Goods 表关联，这是一个设计缺陷。

---

### 4. Order（订单）

**表名：** `order`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `user` | CharField(255) | 用户名 |
| `order_number` | CharField(255) | 订单号 |
| `count` | IntegerField | 商品数量 |
| `status` | CharField(20) | 订单状态 |
| `sku_id` | ForeignKey → Goods | 商品（级联删除） |
| `evaluate` | IntegerField(choices) | 是否已评价（0=未评价，1=已评价） |
| `addr` | CharField(250) | 收货地址 |
| `tel` | CharField(20) | 联系电话 |
| `updated_at` | DateTimeField(auto_now=True) | 更新时间 |
| `created_at` | DateTimeField(auto_now_add=True) | 创建时间 |

**订单状态流转：**
```
未支付（立即购买）
    ↓
已下单（购物车下单） → 已发货 → 已收货 → 已评价
    ↓
  已取消（可删除，已发货的订单不可删除）
```

> **说明**：同一 `order_number` 对应多条订单记录（每个商品一条），通过订单号分组展示。
>
> **订单号生成规则**：`1位大写字母 + 13位毫秒时间戳`，例如 `A1692500000000`

---

### 5. Browse（浏览记录）

**表名：** `browse`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `user` | CharField(255) | 用户名（存 user 对象） |
| `sku_id` | ForeignKey → Goods | 浏览的商品 |
| `updated_at` | DateTimeField(auto_now=True) | 更新时间 |
| `created_at` | DateTimeField(auto_now_add=True) | 创建时间 |

**业务规则：**
- 每个用户最多保留 10 条浏览记录
- 超过 10 条时删除最早（updated_at 最小）的记录
- 重复浏览时更新 updated_at 时间戳

---

### 6. Evaluate（商品评论）

**表名：** `evaluate`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `user` | CharField(255) | 用户名 |
| `sku_id` | ForeignKey → Goods | 评论的商品 |
| `evaluate` | CharField(1000) | 评论内容 |
| `updated_at` | DateTimeField(auto_now=True) | 更新时间 |
| `created_at` | DateTimeField(auto_now_add=True) | 创建时间 |

---

### 7. FeedBack_user（用户反馈）

**表名：** `feedback_user`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `user` | CharField(255) | 用户名 |
| `textarea_name` | TextField | 反馈内容 |
| `input_name` | CharField(255) | 手机号码 |
| `feedback_number` | CharField(255, unique=True) | 反馈ID（唯一） |
| `created_at` | DateTimeField(auto_now_add=True) | 反馈时间 |

**反馈编号规则：** `2位大写字母-13位毫秒时间戳`，例如 `AB-1692500000000`

---

### 8. FeedBack_Image（反馈图片）

**表名：** `feedback_image`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `feedback_number` | ForeignKey → FeedBack_user | 关联反馈（通过 feedback_number 字段） |
| `file` | FileField(upload_to='uploads/') | 图片文件 |

> 每条反馈最多支持 5 张图片，上传字段名分别为 `file0` ~ `file4`。

---

### 9. Service（客服会话）

**表名：** `service`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `user` | ForeignKey → User | 关联 Django User（级联删除） |
| `number` | CharField(255) | 会话编号 |

**编号规则：** `1位大写字母 + 13位毫秒时间戳`，例如 `A1692500000000`

---

### 10. Message（聊天消息）

**表名：** `message`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `user` | ForeignKey → Service | 所属会话（级联删除） |
| `status` | IntegerField(choices) | 消息方向（0=用户发送，1=管理员发送） |
| `service` | CharField(255) | 消息内容（文本/表情编号/图片名） |
| `reading` | IntegerField(choices) | 已读状态（0=未读，1=已读，默认0） |
| `type` | CharField(255) | 消息类型（text/face/image，默认text） |
| `created_at` | DateTimeField(auto_now_add=True) | 创建时间 |

---

### 11. Face（表情包）

**表名：** `face`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `name` | CharField(255) | 表情名称 |
| `image` | CharField(255) | 图片文件名（如 001.png） |

> 表情图片存放在 `/static/face/` 目录下，共 99 个表情（001.png ~ 099.png）。

---

### ER 关系图

```
GoodsType (1) ───< (N) Goods
                      │
                      ├────────< Cart          （注意：Cart.sku_id 是 IntegerField，非外键）
                      ├────────< Order
                      ├────────< Browse
                      └────────< Evaluate

User (1) ───< (N) Service
                  │
                  └──< Message

FeedBack_user (1) ───< (N) FeedBack_Image

Face  ——  独立表，用于表情包管理
```

---

## API接口

### 用户认证接口

| 接口 | 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|------|
| 登录页面 | GET | `/user/login/` | 显示登录页 | 公开 |
| 登录提交 | POST | `/user/login/` | 用户登录 | 公开 |
| 登录检查 | GET | `/user/login/check/` | 检查用户名是否存在（AJAX） | 公开 |
| 注册页面 | GET | `/user/register/` | 显示注册页 | 公开 |
| 注册提交 | POST | `/user/register/sumbit/` | 提交注册（CSRF豁免） | 公开 |
| 注册检查 | GET | `/user/register/check/` | 检查用户名是否已注册（AJAX） | 公开 |
| 退出登录 | GET | `/user/logout/` | 退出登录 | 需登录 |
| 找回密码 | GET/POST | `/user/password/` | 密码重置 | 公开 |
| 验证码 | GET | `/user/verify/code/` | 获取图形验证码 | 公开 |

---

### 商品相关接口

| 接口 | 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|------|
| 首页 | GET | `/user/index/` | 商品分类展示 | 公开 |
| 商品详情 | GET | `/user/detail/<sku_id>/` | 商品详情页（记录浏览历史） | 公开 |
| 商品搜索 | GET | `/user/search/` | 搜索商品（模糊匹配） | 公开 |
| 搜索分页 | GET | `/user/search/page/` | 搜索结果分页（AJAX，JSON） | 公开 |
| 分类列表 | GET | `/user/index/list/` | 分类商品列表 | 公开 |
| 分类分页 | GET | `/user/index/list/page/` | 分类列表分页（AJAX，JSON） | 公开 |
| 价格排序 | GET | `/user/index/list/price/` | 按价格降序排序（AJAX，JSON） | 公开 |

---

### 购物车接口

| 接口 | 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|------|
| 购物车列表 | GET | `/user/cart/` | 查看购物车 | 需登录 |
| 添加购物车 | POST | `/user/cartadd/` | 详情页添加商品到购物车 | 需登录 |
| 增加数量 | POST | `/user/cart/add/` | 购物车商品+1 | 需登录 |
| 减少数量 | POST | `/user/cart/decr/` | 购物车商品-1 | 需登录 |
| 删除商品 | POST | `/user/cart/delete/` | 删除购物车商品 | 需登录 |
| 搜索页加购 | POST | `/user/search/cartadd/` | 搜索结果页加购 | 需登录 |
| 下单提交 | POST | `/user/cart/` | 购物车批量下单（JSON body） | 需登录 |

---

### 订单接口

| 接口 | 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|------|
| 订单列表 | GET | `/user/order/` | 我的订单（分页，每页5组） | 需登录 |
| 支付页面 | GET | `/user/order/payment/<order_number>/` | 订单支付页 | 需登录 |
| 更新订单状态 | GET | `/user/order/update/` | 修改订单状态 | 需登录 |
| 删除订单 | GET | `/user/order/delete/` | 删除订单（已发货不可删） | 需登录 |
| 订单评价 | GET | `/user/order/evaluate/` | 评价页面 | 需登录 |
| 评价提交 | POST | `/user/order/evalute/submit/` | 提交评价 | 需登录 |
| 立即购买 | POST | `/user/index/detail/buy/` | 商品详情页直接下单 | 需登录 |

---

### 用户中心接口

| 接口 | 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|------|
| 用户中心 | GET | `/user/center/` | 个人中心（浏览记录） | 需登录 |
| 地址管理 | GET | `/user/address/` | 收货地址页 | 需登录 |

---

### 反馈接口

| 接口 | 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|------|
| 反馈页面 | GET | `/user/feedback/` | 用户反馈页 | 需登录 |
| 反馈提交 | POST | `/user/feedback/upload/` | 提交反馈（含图片，CSRF豁免） | 需登录 |

---

### 客服聊天接口

| 接口 | 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|------|
| 用户客服页 | GET | `/service/` | 用户端聊天页 | 需登录 |
| 管理员客服页 | GET | `/admin/service/` | 管理员聊天管理 | 管理员 |
| 标记已读 | GET | `/admin/service/reading/` | 标记会话消息已读 | 管理员 |
| 未读数量 | GET | `/admin/service/reading/send/` | 批量获取未读数（AJAX） | 管理员 |
| 表情包列表 | GET | `/service/face/` | 获取表情包（JSON） | 公开 |
| 管理员更新订单 | GET | `/admin/order/update/` | 管理员更新订单状态 | 管理员 |
| WebSocket连接 | WS | `/room/<group>/` | 实时聊天连接 | Session |

---

### 通用响应状态码（JSON 接口）

| code | 含义 |
|------|------|
| 200 | 成功 |
| 302 | 业务失败（用户未登录/已存在/密码不一致等） |
| 500 | 服务器端错误 / 数据为空 |
| -1 | 分页数据为空 |

---

## 前端模板与静态资源

### 模板文件说明

项目使用 Django Template 引擎，模板位于 `templates/` 目录下。

| 模板文件 | 说明 | 对应视图 |
|----------|------|----------|
| `bade.html` | 基础布局模板（头部+主体） | 全局基础 |
| `base_foot.html` | 底部模板 | 全局底部 |
| `user_base.html` | 用户中心基础模板 | 用户中心页面 |
| `index.html` | 首页（分类商品展示） | `index()` |
| `login.html` | 登录页 | `user_login()` |
| `register.html` | 注册页 | `register()` |
| `password.html` | 找回密码页 | `password()` |
| `detail.html` | 商品详情页（评论+推荐） | `detail()` |
| `cart.html` | 购物车页 | `cart()` |
| `order.html` | 订单列表页 | `order()` |
| `payment.html` | 支付页 | `payment()` |
| `order_evaluate.html` | 订单评价页 | `order_evaluate()` |
| `search.html` | 搜索结果页 | `search()` |
| `more_list.html` | 分类商品列表页 | `more_list()` |
| `usercenter.html` | 用户中心（浏览历史） | `user_center()` |
| `address.html` | 收货地址页 | `address()` |
| `feedback.html` | 用户反馈页 | `feedback()` |
| `service.html` | 用户客服聊天页 | `service()` |
| `admin_service.html` | 管理员客服管理页 | `admin_sercice()` |

### 静态资源说明

**CSS 文件（static/css/）：**
- `main.css` - 主样式
- `reset.css` - 重置样式
- `edit.css` - 编辑页面样式
- `login.js` 对应的样式（在模板内联）
- `admin.css` - 后台自定义样式
- `admin_index.css` - 后台首页样式
- `service.css` - 客服页面样式

**JavaScript 文件（static/js/）：**
- `jquery-3.7.1.min.js` - jQuery 库
- `jquery-ui.min.js` - jQuery UI
- `index.js` - 首页逻辑
- `login.js` - 登录页逻辑
- `register.js` - 注册页逻辑
- `password.js` - 密码页逻辑
- `cart.js` - 购物车逻辑
- `detail.js` - 商品详情页逻辑
- `enlarge.js` - 图片放大效果
- `order_evaluate.js` - 订单评价逻辑
- `payment.js` - 支付页逻辑
- `search.js` - 搜索页逻辑（user_search_page.js）
- `more_list_page.js` - 分类列表页逻辑
- `page.js` - 分页逻辑
- `slide.js` - 轮播图/幻灯片
- `feedback.js` - 反馈页逻辑
- `service.js` - 用户客服页逻辑
- `admin_service.js` - 管理员客服页逻辑
- `admin_login.js` - 管理员登录逻辑

---

## 依赖关系

### 项目依赖（requirements.txt）

```
Django==5.0.6
pillow==10.3.0
mysqlclient==2.2.4
channels==3.0.5
django-simpleui==2024.4.1
pycryptodome==3.20.0
six==1.17.0
```

### 模块内部依赖关系图

```
shoping/settings.py
    ├── 注册 apps.user 到 INSTALLED_APPS
    ├── 注册 apps.service 到 INSTALLED_APPS
    ├── 注册 channels 到 INSTALLED_APPS
    ├── 注册 simpleui 到 INSTALLED_APPS（必须放第一个）
    ├── 引用 apps.user.utils.auth_middle.AuthLogin 到 MIDDLEWARE
    ├── 引用 apps.user.views.cart_count 到 TEMPLATES.context_processors
    ├── 配置 ASGI_APPLICATION = 'shoping.asgi.application'
    └── 配置 CHANNEL_LAYERS（内存模式）

apps/user/views.py
    ├── 依赖 .models（GoodsType, Goods, Cart, Order, Browse, Evaluate, FeedBack_user, FeedBack_Image, Service, Message）
    ├── 依赖 .utils.form（RegisterForm, Login）
    ├── 依赖 .utils.pay（AliPay）
    ├── 依赖 django.contrib.auth（authenticate, login, logout, User）
    ├── 依赖 django.contrib.messages（消息提示）
    └── 依赖 PIL.Image, ImageDraw, ImageFont（验证码生成）

apps/user/utils/auth_middle.py
    └── 被 settings.MIDDLEWARE 引用

apps/user/utils/form.py
    ├── 依赖 django.contrib.auth.models.User
    └── 被 apps.user.views 引用

apps/user/utils/pay.py
    ├── 依赖 Crypto.PublicKey.RSA 等（pycryptodome）
    └── 被 apps.user.views 引用

apps/service/consumers.py
    ├── 依赖 apps.user.models（Service, Message）
    ├── 依赖 channels.generic.websocket.WebsocketConsumer
    └── 被 shoping.routing 引用

apps/service/views.py
    ├── 依赖 apps.user.models（Service, Message, Order）
    ├── 依赖 apps.service.models（Face）
    └── 被 apps.service.urls 引用

shoping/asgi.py
    └── 依赖 shoping.routing（WebSocket 路由）

shoping/urls.py
    ├── include apps.user.urls
    └── include apps.service.urls
```

---

## 项目运行

### 环境要求

- **Python** 3.8+ （推荐 3.10+）
- **MySQL** 8.0+
- **虚拟环境**（推荐使用 venv）

### 安装步骤

1. **进入项目目录**
```powershell
cd d:\Desktop\Test-shoping
```

2. **创建并激活虚拟环境（Windows PowerShell）**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. **安装依赖**
```powershell
pip install -r requirements.txt
```

或逐个安装：
```powershell
pip install django-simpleui
pip install channels
pip install mysqlclient==2.2.4
pip install pycryptodome==3.20.0
pip install pillow
pip install six
```

4. **配置数据库**

确保 MySQL 服务已启动，创建数据库：
```sql
CREATE DATABASE mydb DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

或直接导入 `db.sql` 初始化脚本：
```powershell
mysql -u root -p mydb < db.sql
```

5. **修改数据库配置**

编辑 [settings.py](file:///d:/Desktop/Test-shoping/shoping/settings.py#L89-L98)：
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mydb",
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
```

6. **执行数据库迁移**
```powershell
python manage.py makemigrations
python manage.py migrate
```

7. **创建超级管理员**
```powershell
python manage.py createsuperuser
```

8. **启动开发服务器**
```powershell
python manage.py runserver
```

9. **访问项目**
- **前台首页**：http://127.0.0.1:8000/user/index/
- **后台管理**：http://127.0.0.1:8000/admin/
- **用户客服**：http://127.0.0.1:8000/service/?number=xxx
- **管理员客服**：http://127.0.0.1:8000/admin/service/

### 常用命令速查

```powershell
# 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 退出虚拟环境
deactivate

# 启动开发服务器
python manage.py runserver

# 指定端口启动
python manage.py runserver 0.0.0.0:8000

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 修改用户密码
python manage.py changepassword <username>

# 收集静态文件（生产环境）
python manage.py collectstatic

# 进入 Django shell
python manage.py shell

# 检查项目问题
python manage.py check
```

---

## 配置说明

### 核心配置（settings.py）

#### 基础配置
- `SECRET_KEY`：Django 密钥（生产环境需修改并从环境变量读取）
- `DEBUG = True`：调试模式（生产环境需设为 False）
- `ALLOWED_HOSTS = []`：允许的主机名（生产环境需配置）

#### 应用配置
```python
INSTALLED_APPS = [
    'simpleui',           # Admin UI 美化（必须放第一）
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.user',          # 核心电商应用
    'channels',           # WebSocket 支持
    'apps.service',       # 客服应用
]
```

#### 中间件配置
```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # 出现两次（冗余）
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'apps.user.utils.auth_middle.AuthLogin',  # 自定义登录认证中间件
]
```
> 注意：`AuthenticationMiddleware` 在列表中出现了两次（L55 和 L58），属于冗余配置，但不影响功能。

#### 数据库配置
| 配置项 | 值 |
|--------|-----|
| 引擎 | `django.db.backends.mysql` |
| 库名 | `mydb` |
| 用户 | `root` |
| 密码 | `123456` |
| 主机 | `localhost:3306` |

#### 国际化
- 语言：`zh-hans`（简体中文）
- 时区：`Asia/Shanghai`
- `USE_TZ = False`：不使用时区（使用本地时间）

#### 静态文件
- `STATIC_URL = 'static/'`
- `STATICFILES_DIRS = [BASE_DIR/static]`
- `STATIC_ROOT = BASE_DIR/staticfiles`

#### 媒体文件
- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = BASE_DIR/media`

#### 登录配置
- `LOGIN_URL = 'login'`：登录 URL 名称
- `LOGOUT_REDIRECT_URL = '/admin/login/'`：管理员登出后跳转

#### Session 配置
- 登录有效期：7 天（代码中设置：`60 * 60 * 24 * 7`）
- 验证码有效期：60 秒

#### SimpleUI 后台配置

| 配置项 | 值 | 说明 |
|--------|-----|------|
| `SIMPLEUI_LOGO` | `/static/images/logo.png` | 顶部导航栏 Logo |
| `SIMPLEUI_LOGIN_LOGO` | `/static/images/logo.png` | 登录页 Logo |
| `SIMPLEUI_HOME_PAGE` | `/static/images/zc.png` | 首页图片 |
| `SIMPLEUI_LOGIN_PARTICLES` | `False` | 关闭登录页粒子效果 |
| `SIMPLEUI_HOME_INFO` | `False` | 隐藏服务器信息 |
| `SIMPLEUI_STATIC_OFFLINE` | `True` | 离线模式（不加载 CDN） |
| `SIMPLEUI_CONFIG['show_theme_change']` | `False` | 隐藏主题切换按钮 |

**自定义菜单：**
1. 首饰管理 (`/admin/user/goods/`)
2. 订单管理 (`/admin/user/order/`)
3. 首饰类型 (`/admin/user/goodstype/`)
4. 用户浏览报表查看 (`/admin/user/browse/`)
5. 评论管理 (`/admin/user/evaluate/`)
6. 用户消息管理 (`/admin/service/`)
7. 投诉管理 (`/admin/user/feedback_user/`)
8. 用户管理 (`/admin/auth/user/`)

#### Channels 配置
```python
ASGI_APPLICATION = 'shoping.asgi.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
```
> 使用内存 Channel Layer（仅适用于开发环境，生产环境需配置 Redis Channel Layer）

#### 上下文处理器
- `apps.user.views.cart_count`：全局注入购物车数量（`cart_count`）和客服会话对象（`number`）
- `django.template.context_processors.media`：MEDIA_URL 模板变量

---

### 支付宝配置（utils/pay.py）

`AliPay` 类初始化参数：
| 参数 | 说明 |
|------|------|
| `appid` | 支付宝应用ID |
| `app_notify_url` | 异步回调地址 |
| `app_private_key_path` | 应用私钥路径（PEM格式） |
| `alipay_public_key_path` | 支付宝公钥路径（PEM格式） |
| `return_url` | 同步回调地址 |
| `debug` | 是否沙箱环境（True=沙箱，False=生产） |

**密钥文件位置：** `apps/user/utils/keys/`
- `app_private_key.pem` - 应用私钥
- `alipay_public_key.pem` - 支付宝公钥

> 注意：当前项目中的密钥文件为占位符，使用前需替换为真实的支付宝密钥。

---

## 开发注意事项与已知问题

### 已知问题与设计缺陷

1. **Cart 模型的 sku_id 是 IntegerField**
   - 不是 ForeignKey，无法使用 Django ORM 的关联查询
   - 代码中需要手动查询 Goods 表关联，影响性能
   - 建议：改为 `ForeignKey(Goods, on_delete=models.CASCADE)`

2. **AuthenticationMiddleware 重复配置**
   - `settings.py` 的 MIDDLEWARE 列表中 `AuthenticationMiddleware` 出现了两次
   - 不影响功能，但属于冗余配置，建议删除重复项

3. **验证码验证已被注释**
   - `form.py` 中验证码验证逻辑（L58-L59）被注释掉了
   - 当前验证码图片仅作展示，不做实际校验
   - 如需启用，取消注释即可

4. **购物车 user 字段类型不一致**
   - Cart.user 存的是字符串（username）
   - Browse.user 存的是 User 对象
   - 建议统一使用外键关联 User 模型

5. **WebSocket 使用内存 Channel Layer**
   - 仅适合开发/单服务器部署
   - 生产环境需改用 Redis Channel Layer
   - 多服务器部署时消息无法互通

6. **订单状态字符串硬编码**
   - 使用中文字符串（"未支付"、"已下单"、"已发货"等）
   - 建议使用 choices 常量定义，避免拼写错误

7. **CSRF 豁免接口**
   - `/user/register/sumbit/` 和 `/user/feedback/upload/` 使用了 `@csrf_exempt`
   - 有一定安全风险，建议前端正确携带 CSRF Token

8. **密码找回无安全验证**
   - 只需输入用户名即可重置密码
   - 缺少邮箱验证/手机验证码等安全机制

9. **浏览记录判断有潜在问题**
   - `detail()` 视图中先 `get_or_create` 再判断数量，可能存在并发问题
   - 用户未登录时访问详情页会报错（Browse.user 存的是 request.user 对象）

10. **管理员客服页无权限校验**
    - `admin_sercice()` 等视图未检查用户是否为管理员
    - 依赖中间件的 `/admin/` 路径白名单，但普通用户也可能访问

### 最佳实践建议

1. **生产环境部署前必须修改：**
   - `DEBUG = False`
   - 修改 `SECRET_KEY`
   - 配置 `ALLOWED_HOSTS`
   - 使用 Redis Channel Layer
   - 启用验证码验证

2. **数据库优化：**
   - 为常用查询字段添加索引（如 order_number, user 等）
   - Cart 模型改为外键关联 Goods
   - 考虑添加缓存层（Redis）

3. **安全加固：**
   - 移除不必要的 `@csrf_exempt`
   - 密码找回增加验证机制
   - 管理员接口增加权限校验
   - 敏感配置使用环境变量

4. **代码质量：**
   - 移除重复的中间件配置
   - 统一字段命名和类型
   - 增加单元测试
   - 补充错误处理和日志

---

*文档生成时间：2026-06-29*
*基于项目代码实际分析整理*
