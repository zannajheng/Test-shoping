# 首饰购物商城 - Code Wiki 文档

## 目录
1. [项目概述](#项目概述)
2. [技术栈](#技术栈)
3. [项目架构](#项目架构)
4. [目录结构](#目录结构)
5. [核心模块详解](#核心模块详解)
6. [数据模型](#数据模型)
7. [API接口](#api接口)
8. [依赖关系](#依赖关系)
9. [项目运行](#项目运行)
10. [配置说明](#配置说明)

---

## 项目概述

本项目是一个基于 Django 5.0 开发的**首饰购物商城系统**，提供完整的电商功能，包括商品展示、购物车、订单管理、用户认证、商品评论、用户反馈以及在线客服等功能。系统采用传统的服务端渲染（SSR）模式，配合 Django Admin + SimpleUI 作为后台管理界面。

**主要功能特性：**
- 🛒 商品分类浏览与搜索
- 🛍️ 购物车管理
- 📦 订单管理与状态跟踪
- 💬 商品评论系统
- 📝 用户反馈与投诉
- 💬 在线客服（WebSocket实时聊天）
- 👤 用户注册/登录/密码找回
- 📊 用户浏览记录统计
- 🎨 后台管理系统（SimpleUI）

---

## 技术栈

### 后端框架
- **Django 5.0.6** - Web 框架
- **Channels 3.0.5** - WebSocket 支持
- **Django SimpleUI 2024.4.1** - 后台管理界面

### 数据库
- **MySQL 8.0+** - 主数据库
- **mysqlclient 2.2.4** - MySQL 驱动

### 工具库
- **Pillow 10.3.0** - 图像处理（验证码、商品图片）
- **pycryptodome 3.20.0** - 加密算法（支付宝签名）
- **six 1.17.0** - Python 2/3 兼容库

### 前端
- 服务端渲染（Django Templates）
- 原生 JavaScript + AJAX
- 静态资源：CSS、图片

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
│  (商品/订单/用户)   │      │  (在线客服/聊天)    │
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
   - `apps/user`：核心电商业务模块
   - `apps/service`：在线客服模块（基于 WebSocket）
3. **数据库**：MySQL 作为主数据库，存储所有业务数据
4. **Channel Layer**：使用内存 Channel Layer（开发环境），用于 WebSocket 群组通信

---

## 目录结构

```
shoping/
├── apps/                          # 应用目录
│   ├── user/                      # 用户/商品/订单核心应用
│   │   ├── migrations/            # 数据库迁移文件
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
│   │   ├── models.py              # 数据模型定义
│   │   ├── tests.py               # 测试文件
│   │   ├── urls.py                # URL路由配置
│   │   └── views.py               # 视图函数
│   └── service/                   # 客服/聊天应用
│       ├── migrations/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── consumers.py           # WebSocket 消费者
│       ├── models.py              # 表情包模型
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── media/                         # 用户上传的媒体文件
│   ├── images/                    # 商品图片
│   ├── products/                  # 产品图片
│   └── uploads/                   # 用户上传文件
├── shoping/                       # 项目配置目录
│   ├── __init__.py
│   ├── asgi.py                    # ASGI 入口配置
│   ├── routing.py                 # WebSocket 路由配置
│   ├── settings.py                # Django 配置文件
│   ├── urls.py                    # 主 URL 配置
│   └── wsgi.py                    # WSGI 配置
├── static/                        # 静态资源
│   ├── css/                       # 样式文件
│   └── face/                      # 表情包图片
├── templates/                     # 模板目录（需创建）
├── .venv/                         # Python 虚拟环境
├── manage.py                      # Django 管理命令入口
├── requirements.txt               # 项目依赖列表
├── db.sql                         # 数据库初始化脚本
├── shopping.sql                   # 数据库备份
└── README.md                      # 项目说明
```

---

## 核心模块详解

### 1. apps/user - 核心电商模块

#### 模块职责
负责商城的核心业务逻辑，包括：
- 商品展示与分类
- 用户认证（注册/登录/找回密码）
- 购物车管理
- 订单管理
- 商品评论
- 用户反馈/投诉
- 浏览记录

#### 核心文件说明

**[models.py](file:///d:/Desktop/test-project/shoping/apps/user/models.py)**
定义了 10 个数据模型，详见 [数据模型](#数据模型) 章节。

**[views.py](file:///d:/Desktop/test-project/shoping/apps/user/views.py)**
包含 30+ 个视图函数，处理所有业务逻辑。关键函数：

| 函数名 | 功能说明 | 请求方式 | 权限 |
|--------|----------|----------|------|
| `index()` | 首页，按分类展示商品 | GET | 公开 |
| `detail(sku_id)` | 商品详情页，记录浏览历史 | GET | 公开 |
| `user_login()` | 用户登录 | GET/POST | 公开 |
| `register()` | 用户注册页面 | GET | 公开 |
| `register_submit()` | 注册提交处理 | POST | 公开 |
| `cart()` | 购物车列表/下单 | GET/POST | 需登录 |
| `cartadd()` | 添加商品到购物车 | POST | 需登录 |
| `order()` | 我的订单列表 | GET | 需登录 |
| `payment(order_number)` | 订单支付页面 | GET | 需登录 |
| `order_update_status()` | 更新订单状态 | GET | 需登录 |
| `order_evaluate()` | 订单评价 | GET/POST | 需登录 |
| `search()` | 商品搜索 | GET | 公开 |
| `feedback()` | 用户反馈页面 | GET | 需登录 |
| `feedback_upload()` | 提交反馈（含图片） | POST | 需登录 |
| `verify_code()` | 生成图形验证码 | GET | 公开 |
| `cart_count()` | 上下文处理器：购物车数量 | - | 全局 |

**[urls.py](file:///d:/Desktop/test-project/shoping/apps/user/urls.py)**
定义了 36 个 URL 路由，前缀为 `/user/`。

**[admin.py](file:///d:/Desktop/test-project/shoping/apps/user/admin.py)**
配置 Django Admin 后台管理界面，包括：
- 商品管理（GoodsAdmin）
- 购物车管理（CartAdmin）
- 订单管理（OrderAdmin）- 含发货操作按钮
- 商品类型管理（GoodsTypeAdmin）
- 浏览记录管理（BrowseAdmin）
- 评论管理（EvaluateAdmin）
- 用户反馈管理（Feedback_UserAdmin）

**utils/auth_middle.py**
自定义登录认证中间件 `AuthLogin`，白名单机制：
- 免登录路径：`/user/login/`, `/user/register/`, `/user/index/`, `/user/detail/` 等
- AJAX 请求返回 JSON 状态码
- 未登录用户重定向到登录页

**utils/form.py**
表单验证类：
- `RegisterForm` - 注册表单验证（用户名、密码、确认密码、邮箱）
- `Login` - 登录表单验证（用户名、密码、验证码）

**utils/pay.py**
支付宝支付封装类 `AliPay`，支持：
- RSA2 签名验证
- 电脑网站支付接口
- 支付回调验签

---

### 2. apps/service - 在线客服模块

#### 模块职责
提供基于 WebSocket 的实时在线客服功能，包括：
- 用户与管理员实时聊天
- 支持文字、表情、图片消息
- 消息已读状态管理
- 管理员多用户会话管理

#### 核心文件说明

**[consumers.py](file:///d:/Desktop/test-project/shoping/apps/service/consumers.py)**
`ChatConsumer` - WebSocket 消费者类，处理：

| 方法 | 功能 |
|------|------|
| `websocket_connect()` | 连接建立，加入群组 |
| `websocket_receive()` | 接收消息，保存数据库，广播到群组 |
| `group_send()` | 群组消息发送 |
| `websocket_disconnect()` | 连接断开，离开群组 |
| `save_image()` | 保存聊天图片（base64 解码） |

**支持的消息类型：**
- `text` - 文本消息
- `face` - 表情消息
- `image` - 图片消息（base64 编码）

**[views.py](file:///d:/Desktop/test-project/shoping/apps/service/views.py)**

| 函数名 | 功能说明 |
|--------|----------|
| `service()` | 用户端客服聊天页面 |
| `admin_sercice()` | 管理员端客服管理页面 |
| `admin_reading()` | 标记消息已读 |
| `admin_reading_send()` | 批量获取未读消息数 |
| `admin_order_update_status()` | 管理员更新订单状态 |
| `face()` | 获取表情包列表 |

**[models.py](file:///d:/Desktop/test-project/shoping/apps/service/models.py)**
- `Face` - 表情包模型

---

### 3. shoping - 项目配置模块

**[settings.py](file:///d:/Desktop/test-project/shoping/shoping/settings.py)**
核心配置文件，详见 [配置说明](#配置说明) 章节。

**[urls.py](file:///d:/Desktop/test-project/shoping/shoping/urls.py)**
主 URL 路由：
- `/user/` → apps.user.urls
- `/` → apps.service.urls
- `/admin/` → Django Admin
- 静态文件和媒体文件服务

**[asgi.py](file:///d:/Desktop/test-project/shoping/shoping/asgi.py)**
ASGI 应用入口，配置：
- HTTP 协议 → Django 常规处理
- WebSocket 协议 → URLRouter(routing.websocket_urlpatterns)

**[routing.py](file:///d:/Desktop/test-project/shoping/shoping/routing.py)**
WebSocket 路由配置：
- `room/<group>/` → ChatConsumer

---

## 数据模型

### 数据库表总览

| 表名 | 模型类 | 说明 |
|------|--------|------|
| `goods_type` | GoodsType | 商品类型/分类 |
| `goods` | Goods | 商品（首饰）信息 |
| `cart` | Cart | 购物车 |
| `order` | Order | 订单 |
| `browse` | Browse | 用户浏览记录 |
| `evaluate` | Evaluate | 商品评论 |
| `feedback_user` | FeedBack_user | 用户反馈/投诉 |
| `feedback_image` | FeedBack_Image | 反馈图片 |
| `service` | Service | 客服会话 |
| `message` | Message | 聊天消息 |
| `face` | Face | 表情包 |

---

### 1. GoodsType（商品类型）

**表名：** `goods_type`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `goods_type_name` | CharField(255) | 类型名称 |
| `images` | ImageField | 分类图片 |
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
| `images` | ImageField | 首饰图片 |
| `type_id` | ForeignKey → GoodsType | 所属商品分类 |

**关联关系：**
- 外键 `type_id` → GoodsType（多对一）
- 被 Cart、Order、Browse、Evaluate 引用

---

### 3. Cart（购物车）

**表名：** `cart`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `user` | CharField(255) | 用户名 |
| `sku_id` | IntegerField | 商品ID（注意：不是外键） |
| `count` | IntegerField | 商品数量 |
| `updated_at` | DateTimeField | 更新时间 |
| `created_at` | DateTimeField | 创建时间 |

> **注意：** `sku_id` 字段是 IntegerField 而非 ForeignKey，代码中通过手动查询 Goods 表关联。

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
| `sku_id` | ForeignKey → Goods | 商品 |
| `evaluate` | IntegerField | 是否已评价（0=未评价，1=已评价） |
| `addr` | CharField(250) | 收货地址 |
| `tel` | CharField(20) | 联系电话 |
| `updated_at` | DateTimeField | 更新时间 |
| `created_at` | DateTimeField | 创建时间 |

**订单状态流转：**
```
未支付 → 已下单 → 已发货 → 已收货 → 已评价
          ↓
        已取消（可删除）
```

> **说明：** 同一 `order_number` 对应多条订单记录（每个商品一条）。

---

### 5. Browse（浏览记录）

**表名：** `browse`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `user` | CharField(255) | 用户名 |
| `sku_id` | ForeignKey → Goods | 浏览的商品 |
| `updated_at` | DateTimeField | 更新时间 |
| `created_at` | DateTimeField | 创建时间 |

**业务规则：**
- 每个用户最多保留 10 条浏览记录
- 超过 10 条时删除最早的记录
- 重复浏览时更新时间戳

---

### 6. Evaluate（商品评论）

**表名：** `evaluate`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `user` | CharField(255) | 用户名 |
| `sku_id` | ForeignKey → Goods | 评论的商品 |
| `evaluate` | CharField(1000) | 评论内容 |
| `updated_at` | DateTimeField | 更新时间 |
| `created_at` | DateTimeField | 创建时间 |

---

### 7. FeedBack_user（用户反馈）

**表名：** `feedback_user`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `user` | CharField(255) | 用户名 |
| `textarea_name` | TextField | 反馈内容 |
| `input_name` | CharField(255) | 手机号码 |
| `feedback_number` | CharField(255) | 反馈ID（唯一） |
| `created_at` | DateTimeField | 反馈时间 |

**编号规则：** `两位大写字母-时间戳`，如 `AB-1692500000000`

---

### 8. FeedBack_Image（反馈图片）

**表名：** `feedback_image`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `feedback_number` | ForeignKey → FeedBack_user | 关联反馈（通过 feedback_number 字段） |
| `file` | FileField | 图片文件 |

> 每条反馈最多支持 5 张图片。

---

### 9. Service（客服会话）

**表名：** `service`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `user` | ForeignKey → User | 关联用户 |
| `number` | CharField(255) | 会话编号 |

**编号规则：** `1位大写字母+时间戳`，如 `A1692500000000`

---

### 10. Message（聊天消息）

**表名：** `message`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `user` | ForeignKey → Service | 所属会话 |
| `status` | IntegerField | 消息方向（0=用户发送，1=接收/管理员发送） |
| `service` | CharField(255) | 消息内容 |
| `reading` | IntegerField | 已读状态（0=未读，1=已读） |
| `type` | CharField(255) | 消息类型（text/face/image） |
| `created_at` | DateTimeField | 创建时间 |

---

### 11. Face（表情包）

**表名：** `face`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BigAutoField | 主键 |
| `name` | CharField(255) | 表情名称 |
| `image` | CharField(255) | 图片文件名 |

---

### ER 关系图

```
GoodsType (1) ───< (N) Goods
                      │
                      ├────────< Cart
                      ├────────< Order
                      ├────────< Browse
                      └────────< Evaluate

User (1) ───< (N) Service
                  │
                  └──< Message

FeedBack_user (1) ───< (N) FeedBack_Image
```

---

## API接口

### 用户认证接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 登录页面 | GET | `/user/login/` | 显示登录页 |
| 登录提交 | POST | `/user/login/` | 用户登录 |
| 登录检查 | GET | `/user/login/check/` | 检查用户名是否存在 |
| 注册页面 | GET | `/user/register/` | 显示注册页 |
| 注册提交 | POST | `/user/register/sumbit/` | 提交注册 |
| 注册检查 | GET | `/user/register/check/` | 检查用户名是否已注册 |
| 退出登录 | GET | `/user/logout/` | 退出登录 |
| 找回密码 | GET/POST | `/user/password/` | 密码重置 |
| 验证码 | GET | `/user/verify/code/` | 获取图形验证码 |

---

### 商品相关接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 首页 | GET | `/user/index/` | 商品分类展示 |
| 商品详情 | GET | `/user/detail/<sku_id>/` | 商品详情页 |
| 商品搜索 | GET | `/user/search/` | 搜索商品 |
| 搜索分页 | GET | `/user/search/page/` | 搜索结果分页（AJAX） |
| 分类列表 | GET | `/user/index/list/` | 分类商品列表 |
| 分类分页 | GET | `/user/index/list/page/` | 分类列表分页（AJAX） |
| 价格排序 | GET | `/user/index/list/price/` | 按价格降序排序 |

---

### 购物车接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 购物车列表 | GET | `/user/cart/` | 查看购物车 |
| 添加购物车 | POST | `/user/cartadd/` | 添加商品到购物车 |
| 增加数量 | POST | `/user/cart/add/` | 购物车商品+1 |
| 减少数量 | POST | `/user/cart/decr/` | 购物车商品-1 |
| 删除商品 | POST | `/user/cart/delete/` | 删除购物车商品 |
| 搜索页加购 | POST | `/user/search/cartadd/` | 搜索结果页加购 |
| 下单提交 | POST | `/user/cart/` | 购物车批量下单 |

---

### 订单接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 订单列表 | GET | `/user/order/` | 我的订单 |
| 支付页面 | GET | `/user/order/payment/<order_number>/` | 订单支付页 |
| 更新订单状态 | GET | `/user/order/update/` | 修改订单状态 |
| 删除订单 | GET | `/user/order/delete/` | 删除订单 |
| 订单评价 | GET | `/user/order/evaluate/` | 评价页面 |
| 评价提交 | POST | `/user/order/evalute/submit/` | 提交评价 |
| 立即购买 | POST | `/user/index/detail/buy/` | 商品详情页直接下单 |

---

### 用户中心接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 用户中心 | GET | `/user/center/` | 个人中心（浏览记录） |
| 地址管理 | GET | `/user/address/` | 收货地址页 |

---

### 反馈接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 反馈页面 | GET | `/user/feedback/` | 用户反馈页 |
| 反馈提交 | POST | `/user/feedback/upload/` | 提交反馈（含图片） |

---

### 客服聊天接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 用户客服页 | GET | `/service/` | 用户端聊天页 |
| 管理员客服页 | GET | `/admin/service/` | 管理员聊天管理 |
| 标记已读 | GET | `/admin/service/reading/` | 标记消息已读 |
| 未读数量 | GET | `/admin/service/reading/send/` | 批量获取未读数 |
| 表情包列表 | GET | `/service/face/` | 获取表情包 |
| WebSocket连接 | WS | `/room/<group>/` | 实时聊天连接 |

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

### 模块内部依赖

```
shoping/settings.py
    ├── 依赖 apps.user (INSTALLED_APPS)
    ├── 依赖 apps.service (INSTALLED_APPS)
    ├── 依赖 channels (WebSocket)
    └── 依赖 simpleui (Admin后台)

apps/user/views.py
    ├── 依赖 .models (所有数据模型)
    ├── 依赖 .utils.form (表单验证)
    ├── 依赖 .utils.pay (支付宝支付)
    └── 依赖 django.contrib.auth (用户认证)

apps/user/utils/auth_middle.py
    └── 被 settings.MIDDLEWARE 引用

apps/service/consumers.py
    ├── 依赖 apps.user.models (Service, Message)
    └── 依赖 channels (WebSocket框架)

apps/service/views.py
    ├── 依赖 apps.user.models (Service, Message, Order)
    └── 依赖 apps.service.models (Face)

shoping/asgi.py
    └── 依赖 shoping.routing (WebSocket路由)
```

---

## 项目运行

### 环境要求

- Python 3.8+
- MySQL 8.0+
- 虚拟环境（推荐）

### 安装步骤

1. **克隆/进入项目目录**
```bash
cd d:\Desktop\test-project\shoping
```

2. **激活虚拟环境（Windows PowerShell）**
```bash
.\.venv\Scripts\Activate.ps1
```

3. **安装依赖**（如虚拟环境已配置可跳过）
```bash
pip install django-simpleui
pip install channels
pip install mysqlclient==2.2.4
pip install pycryptodome==3.20.0
```

或直接安装 requirements.txt：
```bash
pip install -r requirements.txt
```

4. **配置数据库**

确保 MySQL 服务已启动，创建数据库：
```sql
CREATE DATABASE mydb DEFAULT CHARACTER SET utf8;
```

或直接导入 `db.sql` 初始化脚本：
```bash
mysql -u root -p < db.sql
```

5. **修改数据库配置**

编辑 [settings.py](file:///d:/Desktop/test-project/shoping/shoping/settings.py#L89-L98)：
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
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **创建超级管理员**
```bash
python manage.py createsuperuser
```

8. **启动开发服务器**
```bash
python manage.py runserver
```

9. **访问项目**
- 前台首页：http://127.0.0.1:8000/user/index/
- 后台管理：http://127.0.0.1:8000/admin/

### 常用命令

```bash
# 进入虚拟环境
.\.venv\Scripts\Activate.ps1

# 退出虚拟环境
deactivate

# 启动服务器
python manage.py runserver

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 收集静态文件
python manage.py collectstatic
```

---

## 配置说明

### 核心配置（settings.py）

#### 基础配置
- `SECRET_KEY`：Django 密钥（生产环境需修改）
- `DEBUG = True`：调试模式（生产环境需设为 False）
- `ALLOWED_HOSTS = []`：允许的主机名

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
    # Django 内置中间件
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 自定义登录认证中间件
    'apps.user.utils.auth_middle.AuthLogin',
]
```

#### 数据库配置
- 引擎：`django.db.backends.mysql`
- 库名：`mydb`
- 用户：`root`
- 密码：`123456`
- 主机：`localhost:3306`

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
- `LOGOUT_REDIRECT_URL = '/admin/login/'`：登出后跳转

#### SimpleUI 后台配置
- 自定义菜单：首饰管理、订单管理、首饰类型、浏览报表、评论管理、消息管理、投诉管理、用户管理
- 隐藏主题切换按钮
- 关闭登录页粒子效果
- 自定义 Logo 和首页

#### Channels 配置
```python
ASGI_APPLICATION = 'shoping.asgi.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
```
> 使用内存 Channel Layer（仅适用于开发环境，生产环境需配置 Redis）

#### 上下文处理器
- `apps.user.views.cart_count`：全局注入购物车数量和客服会话编号

---

### 支付宝配置（utils/pay.py）

`AliPay` 类初始化参数：
- `appid`：支付宝应用ID
- `app_notify_url`：异步回调地址
- `app_private_key_path`：应用私钥路径
- `alipay_public_key_path`：支付宝公钥路径
- `return_url`：同步回调地址
- `debug`：是否沙箱环境（True=沙箱，False=生产）

密钥文件位置：`apps/user/utils/keys/`

---

## 开发注意事项

1. **Cart 模型的 sku_id 是 IntegerField**，不是外键，关联查询需手动进行
2. **同一订单号对应多条 Order 记录**，每个商品一条，通过 `order_number` 分组
3. **浏览记录上限 10 条**，超过自动删除最早的
4. **WebSocket 使用内存 Channel Layer**，仅适合开发/单服务器部署
5. **验证码功能已注释**，登录表单中验证码验证被禁用
6. **订单状态字符串**：未支付、已下单、已发货 等，注意中英文一致性
7. **反馈最多5张图片**，通过 `file0`-`file4` 字段名上传

---

## 默认账号

根据 `db.sql` 中的数据：

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | （需重置） | 超级管理员 |
| user1234 | （需重置） | 普通用户 |

> 建议使用 `python manage.py createsuperuser` 创建新的管理员账号。

---

*文档生成时间：2026-06-29*
