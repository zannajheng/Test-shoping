
CREATE DATABASE mydb DEFAULT CHARACTER SET utf8;
use mydb;



-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4  NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4  ROW_FORMAT = Dynamic;





-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4  NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (17, 'service', 'face');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (13, 'user', 'browse');
INSERT INTO `django_content_type` VALUES (7, 'user', 'cart');
INSERT INTO `django_content_type` VALUES (12, 'user', 'evaluate');
INSERT INTO `django_content_type` VALUES (11, 'user', 'feedback_image');
INSERT INTO `django_content_type` VALUES (8, 'user', 'feedback_user');
INSERT INTO `django_content_type` VALUES (9, 'user', 'goods');
INSERT INTO `django_content_type` VALUES (10, 'user', 'goodstype');
INSERT INTO `django_content_type` VALUES (16, 'user', 'message');
INSERT INTO `django_content_type` VALUES (14, 'user', 'order');
INSERT INTO `django_content_type` VALUES (15, 'user', 'service');

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4  NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4  NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 69 CHARACTER SET = utf8mb4  ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add 购物车信息', 7, 'add_cart');
INSERT INTO `auth_permission` VALUES (26, 'Can change 购物车信息', 7, 'change_cart');
INSERT INTO `auth_permission` VALUES (27, 'Can delete 购物车信息', 7, 'delete_cart');
INSERT INTO `auth_permission` VALUES (28, 'Can view 购物车信息', 7, 'view_cart');
INSERT INTO `auth_permission` VALUES (29, 'Can add 用户反馈', 8, 'add_feedback_user');
INSERT INTO `auth_permission` VALUES (30, 'Can change 用户反馈', 8, 'change_feedback_user');
INSERT INTO `auth_permission` VALUES (31, 'Can delete 用户反馈', 8, 'delete_feedback_user');
INSERT INTO `auth_permission` VALUES (32, 'Can view 用户反馈', 8, 'view_feedback_user');
INSERT INTO `auth_permission` VALUES (33, 'Can add 商品信息', 9, 'add_goods');
INSERT INTO `auth_permission` VALUES (34, 'Can change 商品信息', 9, 'change_goods');
INSERT INTO `auth_permission` VALUES (35, 'Can delete 商品信息', 9, 'delete_goods');
INSERT INTO `auth_permission` VALUES (36, 'Can view 商品信息', 9, 'view_goods');
INSERT INTO `auth_permission` VALUES (37, 'Can add 商品类型', 10, 'add_goodstype');
INSERT INTO `auth_permission` VALUES (38, 'Can change 商品类型', 10, 'change_goodstype');
INSERT INTO `auth_permission` VALUES (39, 'Can delete 商品类型', 10, 'delete_goodstype');
INSERT INTO `auth_permission` VALUES (40, 'Can view 商品类型', 10, 'view_goodstype');
INSERT INTO `auth_permission` VALUES (41, 'Can add feed back_ image', 11, 'add_feedback_image');
INSERT INTO `auth_permission` VALUES (42, 'Can change feed back_ image', 11, 'change_feedback_image');
INSERT INTO `auth_permission` VALUES (43, 'Can delete feed back_ image', 11, 'delete_feedback_image');
INSERT INTO `auth_permission` VALUES (44, 'Can view feed back_ image', 11, 'view_feedback_image');
INSERT INTO `auth_permission` VALUES (45, 'Can add 商品评论', 12, 'add_evaluate');
INSERT INTO `auth_permission` VALUES (46, 'Can change 商品评论', 12, 'change_evaluate');
INSERT INTO `auth_permission` VALUES (47, 'Can delete 商品评论', 12, 'delete_evaluate');
INSERT INTO `auth_permission` VALUES (48, 'Can view 商品评论', 12, 'view_evaluate');
INSERT INTO `auth_permission` VALUES (49, 'Can add browse', 13, 'add_browse');
INSERT INTO `auth_permission` VALUES (50, 'Can change browse', 13, 'change_browse');
INSERT INTO `auth_permission` VALUES (51, 'Can delete browse', 13, 'delete_browse');
INSERT INTO `auth_permission` VALUES (52, 'Can view browse', 13, 'view_browse');
INSERT INTO `auth_permission` VALUES (53, 'Can add order', 14, 'add_order');
INSERT INTO `auth_permission` VALUES (54, 'Can change order', 14, 'change_order');
INSERT INTO `auth_permission` VALUES (55, 'Can delete order', 14, 'delete_order');
INSERT INTO `auth_permission` VALUES (56, 'Can view order', 14, 'view_order');
INSERT INTO `auth_permission` VALUES (57, 'Can add service', 15, 'add_service');
INSERT INTO `auth_permission` VALUES (58, 'Can change service', 15, 'change_service');
INSERT INTO `auth_permission` VALUES (59, 'Can delete service', 15, 'delete_service');
INSERT INTO `auth_permission` VALUES (60, 'Can view service', 15, 'view_service');
INSERT INTO `auth_permission` VALUES (61, 'Can add message', 16, 'add_message');
INSERT INTO `auth_permission` VALUES (62, 'Can change message', 16, 'change_message');
INSERT INTO `auth_permission` VALUES (63, 'Can delete message', 16, 'delete_message');
INSERT INTO `auth_permission` VALUES (64, 'Can view message', 16, 'view_message');
INSERT INTO `auth_permission` VALUES (65, 'Can add 表情包', 17, 'add_face');
INSERT INTO `auth_permission` VALUES (66, 'Can change 表情包', 17, 'change_face');
INSERT INTO `auth_permission` VALUES (67, 'Can delete 表情包', 17, 'delete_face');
INSERT INTO `auth_permission` VALUES (68, 'Can view 表情包', 17, 'view_face');


-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4  NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4  NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4  NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4  NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4  NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `tel` varchar(255) CHARACTER SET utf8mb4  NULL DEFAULT NULL,
  `addr` varchar(255) CHARACTER SET utf8mb4  NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4  ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$720000$njJtbrDT6sdMmilGPGOv62$RauAC4nXRhtOW8Vw92J7/8LBk4REgF4+Q3kMNGPCjTU=', '2025-08-20 17:34:48.160851', 1, 'admin', '', '', '', 1, 1, '2025-08-19 18:03:25.365536', NULL, NULL);
INSERT INTO `auth_user` VALUES (2, 'pbkdf2_sha256$720000$oIBdG5RtBVFjznlIQKSoxe$2XGYkmgaBqrCoszGF0ysAm8qO9/CXKv/hHTW6PMXe+Y=', '2025-08-20 16:17:36.617460', 0, 'user1234', '', '', '', 0, 1, '2025-08-19 20:46:04.122951', NULL, NULL);

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id` ASC, `group_id` ASC) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4  ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4  ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for goods_type
-- ----------------------------
DROP TABLE IF EXISTS `goods_type`;
CREATE TABLE `goods_type`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `goods_type_name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `images` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `class_name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of goods_type
-- ----------------------------
INSERT INTO `goods_type` VALUES (1, '项链', 'images/1.jpg', '贵金属');
INSERT INTO `goods_type` VALUES (2, '手镯', 'images/2.jpg', '手腕手镯');
INSERT INTO `goods_type` VALUES (3, '发饰', 'images/3.jpg', '发饰');




-- ----------------------------
-- Table structure for goods
-- ----------------------------
DROP TABLE IF EXISTS `goods`;
CREATE TABLE `goods`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `goods_name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `intro` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `sell` int NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  `cation` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `images` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `type_id_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `goods_type_id_id_2ac78fcf_fk_goods_type_id`(`type_id_id` ASC) USING BTREE,
  CONSTRAINT `goods_type_id_id_2ac78fcf_fk_goods_type_id` FOREIGN KEY (`type_id_id`) REFERENCES `goods_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 254 CHARACTER SET = utf8mb4 ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of goods
-- ----------------------------
INSERT INTO `goods` VALUES (1, '黄金项链20克', '品牌 定制 是否支持加工定制 是 是否支持加印LOGO 是 包装规格 OPP袋独立包装 处理工艺 镶钻 风格 定制 适用送礼场合 其他 颜色 定制 样式 男女通用 造型 定制 产品特性 金属 贵金属质量 9g 纯度 18K 产地 广东 包装 独立包装 加工定制 是 销售序列号 JR-N11227 生产编号 JR-N105 可售卖地 全国 材质 黄金', 0, 99999.00, '条', 'images/xl1.jpg', 1);
INSERT INTO `goods` VALUES (2, '18K金上帝之眼项链项坠定制创意个性吊坠挂件镶钻金属饰品', '价格：商品在爱采购的展示标价，具体的成交价格可能因商品参加活动等情况发生变化，也可能随着购买数量不同或所选规格不同而发生变化，如用户与商家线下达成协议，以线下协议的结算价格为准，如用户在爱采购上完成线上购买，则最终以订单结算页价格为准。  抢购价：商品参与营销活动的活动价格，也可能随着购买数量不同或所选规格不同而发生变化，最终以订单结算页价格为准。', 4, 12456.00, '25g', 'images/xl2.jpg', 1);
INSERT INTO `goods` VALUES (3, '和田玉手饰手串圆珠挂牌手镯白玉石观音菩萨女首饰珍品直播专拍1', '型号 见描述 加工定制 见描述 品牌 颍上卓越 规格 【非对应产品】,KJ09089-鸭蛋', 4, 32.00, '30g', 'images/sz1.jpg', 2);
INSERT INTO `goods` VALUES (4, '欧美跨境不锈钢C型手镯 6MM男女通用款', '联系人 张经理  电子邮箱 594262132@qq.com  联系电话 13911942347', 4, 888.00, '20g', 'images/sz2.jpg', 2);
INSERT INTO `goods` VALUES (5, '圈马尾皮筋发箍发饰', '品牌 巨丰 是否支持加工定制 否 是否支持加印LOGO 否 包装规格 盒装 处理工艺 高级 风格 回收全品类库存 适用送礼场合 皆可', 3, 29.90, '个', 'images/fs1.jpg', 3);

-- ----------------------------
-- Table structure for browse
-- ----------------------------
DROP TABLE IF EXISTS `browse`;
CREATE TABLE `browse`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user` varchar(255) CHARACTER SET utf8mb4  NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `sku_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `browse_sku_id_5d19b52d_fk_goods_id`(`sku_id` ASC) USING BTREE,
  CONSTRAINT `browse_sku_id_5d19b52d_fk_goods_id` FOREIGN KEY (`sku_id`) REFERENCES `goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4  ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of browse
-- ----------------------------
INSERT INTO `browse` VALUES (1, 'user1234', '2025-08-20 16:11:17.735859', '2025-08-19 20:46:16.010102', 1);
INSERT INTO `browse` VALUES (2, 'user1234', '2025-08-20 23:24:17.624052', '2025-08-20 00:17:42.498232', 2);
INSERT INTO `browse` VALUES (3, 'user1234', '2025-08-20 16:42:07.951088', '2025-08-20 16:41:45.068442', 3);

-- ----------------------------
-- Table structure for cart
-- ----------------------------
DROP TABLE IF EXISTS `cart`;
CREATE TABLE `cart`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user` varchar(255) CHARACTER SET utf8mb4  NOT NULL,
  `sku_id` int NOT NULL,
  `count` int NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4  ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cart
-- ----------------------------
INSERT INTO `cart` VALUES (14, 'user1234', 2, 1, '2025-08-20 23:24:19.508951', '2025-08-20 23:24:19.508951');

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4  NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4  NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4  NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 258 CHARACTER SET = utf8mb4  ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
INSERT INTO `django_admin_log` VALUES (1, '2025-08-19 20:44:32.636409', '220', 'HAEWI国行【2024款15代英特尔酷睿i7】大屏笔记本', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (2, '2025-08-19 20:44:32.638261', '221', '戴睿（dere）政府补贴英特尔轻薄本14英寸便携笔记本', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (3, '2025-08-19 20:44:32.639267', '224', '荣耀畅玩20A', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (4, '2025-08-19 20:44:32.640267', '225', 'LEBEST', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (5, '2025-08-19 20:44:32.640267', '226', '小米Redmi', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (6, '2025-08-19 20:44:32.641266', '227', 'OPPO', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (7, '2025-08-19 20:44:32.642266', '228', 'vivo', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (8, '2025-08-19 20:44:32.643733', '229', '小米（MI）Redmi', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (9, '2025-08-19 20:44:32.644738', '230', '小米Redmi', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (10, '2025-08-19 20:44:32.644738', '231', '一加', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (11, '2025-08-19 20:44:32.645738', '232', 'OPPO', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (12, '2025-08-19 20:44:32.646738', '233', '荣耀Play9C', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (13, '2025-08-19 20:44:32.647740', '234', '一加', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (14, '2025-08-19 20:44:32.648738', '235', '酷派COOL50Lite全新超薄智能八核256G便宜大屏学生百元机长续航老人老年国产备用机游戏电竞', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (15, '2025-08-19 20:44:32.649903', '236', '荣耀X60', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (16, '2025-08-19 20:44:32.650903', '237', '荣耀X50', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (17, '2025-08-19 20:44:32.650903', '238', '魅紫新款15promax灵动岛大屏智能256g可用5G卡4g全网通电竞游戏长续航全新学生老人超薄便宜16pro', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (18, '2025-08-19 20:44:32.651904', '239', '荣耀X60', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (19, '2025-08-19 20:44:32.652903', '240', 'OPPO', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (20, '2025-08-19 20:44:32.653903', '241', 'vivo', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (21, '2025-08-19 20:44:32.654903', '242', 'OPPOPROM60Pro五星抗摔9800mAh快充大电池16+1TB大内存双卡5G全网通电竞游戏骁龙888高清大屏美颜拍照', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (22, '2025-08-19 20:44:32.655904', '243', 'vivo', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (23, '2025-08-19 20:44:32.656903', '244', '小米（MI）Redmi', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (24, '2025-08-19 20:44:32.657903', '245', '华为5G智选Hi', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (25, '2025-08-19 20:44:32.657903', '246', '荣耀显通M60PRO2024新上市骁龙888', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (26, '2025-08-19 20:44:32.658903', '247', '华为智选70', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (27, '2025-08-19 20:44:32.659903', '248', '华为（HUAWEI）华为畅享9', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (28, '2025-08-19 20:44:32.660903', '249', 'vivo', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (29, '2025-08-19 20:44:32.661903', '250', '荣耀90', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (30, '2025-08-19 20:44:32.662903', '251', '小米', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (31, '2025-08-19 20:44:32.663904', '252', 'vivo', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (32, '2025-08-19 20:44:32.664904', '253', '小米（MI）Redmi', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (33, '2025-08-19 20:44:45.149634', '120', '甘肃天水大樱桃新鲜车厘子', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (34, '2025-08-19 20:44:45.151258', '121', '甘肃秦安红富士苹果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (35, '2025-08-19 20:44:45.152261', '122', '山东烟台红富士苹果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (36, '2025-08-19 20:44:45.153270', '123', '进口香蕉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (37, '2025-08-19 20:44:45.154269', '124', '山东烟台栖霞红富士苹果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (38, '2025-08-19 20:44:45.155270', '125', '泰国进口金枕头榴莲', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (39, '2025-08-19 20:44:45.156261', '126', '海南贵妃芒小芒果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (40, '2025-08-19 20:44:45.157261', '127', '山东栖霞红富士苹果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (41, '2025-08-19 20:44:45.158261', '128', '红富士苹果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (42, '2025-08-19 20:44:45.158261', '129', '四川不知火丑橘', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (43, '2025-08-19 20:44:45.159763', '130', '大凉山草莓礼盒', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (44, '2025-08-19 20:44:45.160765', '131', '米易枇杷', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (45, '2025-08-19 20:44:45.161774', '132', '（Midea）破壁机国家补贴', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (46, '2025-08-19 20:44:45.162765', '133', '（Midea）【国家补贴】快捷微波炉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (47, '2025-08-19 20:44:45.163772', '134', '（Midea）M60系列421法式四门白色多门60cm超薄无缝嵌入底部散热9分钟急速净味一级能效电冰箱换新补贴20%', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (48, '2025-08-19 20:44:45.164775', '135', '（Midea）不粘锅炒锅', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (49, '2025-08-19 20:44:45.165775', '136', '空调', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (50, '2025-08-19 20:44:45.166788', '137', '空调', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (51, '2025-08-19 20:44:45.167775', '138', '补贴省20%！', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (52, '2025-08-19 20:44:45.168775', '139', '（Midea）电磁炉电陶炉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (53, '2025-08-19 20:44:45.169890', '140', '（Midea）空气炸锅', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (54, '2025-08-19 20:44:45.170490', '141', '（Midea）波轮洗衣机全自动家用', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (55, '2025-08-19 20:44:45.171496', '142', '（Midea）【国家补贴】电热水壶煮水壶家用烧水壶', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (56, '2025-08-19 20:44:45.172496', '143', '（Midea）【国家补贴】微波炉烤箱一体机', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (57, '2025-08-19 20:44:45.173495', '144', '冰洗套装223小型三门三温家用冰箱', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (58, '2025-08-19 20:44:45.173495', '145', '（Midea）电煮锅', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (59, '2025-08-19 20:44:45.174495', '146', '（Midea）破壁机国家补贴', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (60, '2025-08-19 20:44:45.175495', '147', '（Midea）电压力锅5升【深汤双胆】E523电饭煲', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (61, '2025-08-19 20:44:45.176495', '148', '（Midea）【超级单品】暖风机/小太阳取暖器/全屋升温/电暖器', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (62, '2025-08-19 20:44:45.177495', '149', '（Midea）电压力锅5升双胆家用高压锅全自动智能预约煲汤煮饭煮粥锅', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (63, '2025-08-19 20:44:45.178495', '150', '（Midea）M60双系统系列525零嵌纯平全嵌十字四开门底部散热一级能效家用无霜换新补贴冰箱', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (64, '2025-08-19 20:44:45.179495', '151', '（Midea）电煮锅', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (65, '2025-08-19 20:44:45.179495', '152', '（Midea）不粘锅', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (66, '2025-08-19 20:44:45.180495', '153', '（Midea）家用电磁炉电陶炉电池炉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (67, '2025-08-19 20:44:45.182496', '154', '（Midea）【国家补贴】变频微波炉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (68, '2025-08-19 20:44:45.183496', '155', '（Midea）', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (69, '2025-08-19 20:44:45.184496', '156', '（Midea）458M60系列十字对开四门60cm纯平全嵌9分钟急速净味一级变频风冷无霜智能电冰箱以旧换新', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (70, '2025-08-19 20:44:45.185496', '157', '（Midea）【国家补贴】电水壶烧水壶电热水壶1.7升大容量暖水壶', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (71, '2025-08-19 20:44:45.186496', '158', '（Midea）八千万负离子电吹风', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (72, '2025-08-19 20:44:45.186496', '159', '（Midea）五千万负离子电吹风', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (73, '2025-08-19 20:44:45.187830', '160', '（Midea）电火锅电煮锅分体式可拆洗家用多功能锅4.5L大容量火锅专用锅不粘锅MC-HGE3026', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (74, '2025-08-19 20:44:45.188835', '161', '（Midea）炒锅', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (75, '2025-08-19 20:44:45.189835', '162', '兰蔻全新菁纯「逆龄」面霜轻盈版60ml', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (76, '2025-08-19 20:44:45.190835', '163', '李佳琪推荐13支化妆套刷软毛眼影刷散粉刷鼻影粉底刷初学者套装刷', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (77, '2025-08-19 20:44:45.191842', '164', '韩露熙绿茶冰肌高岭土泥膜植物精华深层清洁保湿控油去黑头洁面120g一瓶', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (78, '2025-08-19 20:44:45.192835', '165', '欧莱雅（L\'OREAL）', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (79, '2025-08-19 20:44:45.193631', '166', '【一盘搞定】SWEET', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (80, '2025-08-19 20:44:45.194638', '167', 'AKF定妆散粉持久防水防汗不脱妆控油隐形毛孔轻透控油散粉10g', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (81, '2025-08-19 20:44:45.194638', '168', '雅诗兰黛小棕瓶精华露30ml礼盒护肤品套装化妆品新年礼物送女友送老婆', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (82, '2025-08-19 20:44:45.196638', '169', '【网红爆款】100分超软棉花糖粉扑粉底液专用气垫干湿两用不卡粉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (83, '2025-08-19 20:44:45.197639', '170', '卡姿兰（Carslan）彩妆套装化妆品全套礼盒进阶全妆爆款产品21件套', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (84, '2025-08-19 20:44:45.198638', '171', '卡姿兰（Carslan）彩妆套装礼盒化妆品套装全套新手初学者520七夕情人节礼物送女友', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (85, '2025-08-19 20:44:45.199543', '172', '大宝', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (86, '2025-08-19 20:44:45.200548', '173', '京迭化妆镜子台式桌面梳妆镜折叠便携男士高清', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (87, '2025-08-19 20:44:45.200548', '174', '雅诗兰黛绒雾哑光唇膏333#干枫叶色口红礼盒化妆品新年礼物送女友送老婆', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (88, '2025-08-19 20:44:45.201549', '175', '尤莉尤拉跨年礼物彩妆礼盒10件套化妆品全套口红女生生日送女友老婆', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (89, '2025-08-19 20:44:45.202549', '176', 'YARAYCIN维生素e护肤甘油脸部嫩肤滋润补水保湿锁水精华化妆前打底不卡粉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (90, '2025-08-19 20:44:45.202549', '177', 'NAXR小方瓶遮瑕粉底液养肤持久奶油肌防汗防水保湿不脱妆平价10ml瓶装', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (91, '2025-08-19 20:44:45.203549', '178', '忆香缘绿茶氨基酸洁面乳去角质洗面奶深层清洁补水保湿控油', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (92, '2025-08-19 20:44:45.203549', '179', '拉美拉（lameila）持妆遮瑕粉底液女持久不闷痘不脱妆保湿控油裸妆轻薄学生新手定妆', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (93, '2025-08-19 20:44:45.204549', '180', '兰蔻196口红哑光雾面唇膏经典朱砂橘', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (94, '2025-08-19 20:44:45.204549', '181', '吟美黄芪霜面霜抗皱嫩肤翻盖滋润肌肤修护紧致补水防冻裂秋冬新升级70', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (95, '2025-08-19 20:44:45.205806', '182', 'MAFFICK四色修容盘高光修容一体盘便携式哑光提亮闪粉防', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (96, '2025-08-19 20:44:45.205806', '183', '拉美拉【东方彩妆】彩妆套装化妆品一整套学生全套不卡粉初学者入门便宜', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (97, '2025-08-19 20:44:45.206810', '184', 'VSEA秋冬香水香氛护手霜伴手礼防干裂补水保湿嫩白呵护男女四季礼盒装', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (98, '2025-08-19 20:44:45.206810', '185', '蓝桥10化妆刷套装初学者散粉腮红遮瑕粉底眼影刷子全套工具超软毛', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (99, '2025-08-19 20:44:45.207810', '186', '谷雨第三代光感水150ml', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (100, '2025-08-19 20:44:45.208810', '187', '懒人双尖麦穗升级款假睫毛细梗塔尖新手大容量睫毛书分段浓密', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (101, '2025-08-19 20:44:45.208810', '188', 'ILISYA【情人节礼物24件】化妆品全套彩妆套装初学者口红眉笔送女友礼物', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (102, '2025-08-19 20:44:45.209810', '189', 'GUOXIAONIU郭小妞巧克力饼干气垫粉扑粉底液专用不易吃粉上妆海绵定妆散粉扑', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (103, '2025-08-19 20:44:45.210809', '190', 'BEKAY法国兰黛小黑瓶护肤品套装礼盒补水保湿全套化妆品情人节礼物', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (104, '2025-08-19 20:44:45.210809', '191', 'HLOFF跨年礼物一鹿有你彩妆礼盒化妆品全套口红女生生日送女朋友老婆', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (105, '2025-08-19 20:44:45.212809', '192', 'i5', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (106, '2025-08-19 20:44:45.212809', '193', '吉优比2024新款16+1TB平板', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (107, '2025-08-19 20:44:45.213810', '194', 'LENO国行【2024', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (108, '2025-08-19 20:44:45.214812', '195', '华硕全家桶12600kf+4060Ti主机/4060', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (109, '2025-08-19 20:44:45.215810', '196', '金刚侠酷睿i5i7升i9级18核64G内存2T硬盘4060电竞独显吃鸡台式机', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (110, '2025-08-19 20:44:45.216810', '197', '联想', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (111, '2025-08-19 20:44:45.217810', '198', '飞利浦（PHILIPS）S9', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (112, '2025-08-19 20:44:45.218810', '199', '牛头英特尔i5酷睿i7升i9级十八核/RTX4060独显迷你台式机', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (113, '2025-08-19 20:44:45.219810', '200', '方正笔记本', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (114, '2025-08-19 20:44:45.220810', '201', '方正2024新款笔记本', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (115, '2025-08-19 20:44:45.221810', '202', '第三星种2024新款超薄十核安卓超高清4K全面屏5G全网通娱乐办公多功能二合一游戏网课学习平板', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (116, '2025-08-19 20:44:45.222810', '203', '技械骑士128g内存酷睿i7升24核台式机', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (117, '2025-08-19 20:44:45.223810', '204', '江慕大额补贴20%台式', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (118, '2025-08-19 20:44:45.223810', '205', '华硕', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (119, '2025-08-19 20:44:45.224810', '206', '觅狐128g内存酷睿i7升24核畅玩黑神话电竞台式', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (120, '2025-08-19 20:44:45.226810', '207', '七彩虹', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (121, '2025-08-19 20:44:45.227810', '208', '英邦达英特尔酷睿i7升十八核4060独显64G内存组装台式机', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (122, '2025-08-19 20:44:45.228810', '209', '联想小新16/14/15', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (123, '2025-08-19 20:44:45.229810', '210', 'LAVRIKOW2024拯救系列', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (124, '2025-08-19 20:44:45.230810', '211', '和谐号（HEXIEHAO）L19', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (125, '2025-08-19 20:44:45.231810', '212', 'HAEWI国行【2024款15代英特尔酷睿i7】大屏笔记本', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (126, '2025-08-19 20:44:45.231810', '213', '技械骑士128g内存酷睿i7升24核台式机', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (127, '2025-08-19 20:44:45.232809', '214', '圣技仕', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (128, '2025-08-19 20:44:45.233810', '215', 'HUATWAI国行【2024新款英特尔酷睿i7】笔记本', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (129, '2025-08-19 20:44:45.234811', '216', '机械革命蛟龙16Pro游戏本', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (130, '2025-08-19 20:44:45.235810', '217', '华硕无畏14', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (131, '2025-08-19 20:44:45.236810', '218', '领睿英特尔酷睿i7升24核RTX4060独显64G内存台式', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (132, '2025-08-19 20:44:45.237810', '219', '卫战神【英特尔14代酷睿i9】4060独显diy台式机', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (133, '2025-08-19 20:45:02.102465', '11', '羊肉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (134, '2025-08-19 20:45:02.103472', '12', '牛排', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (135, '2025-08-19 20:45:02.105115', '14', '猕猴桃', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (136, '2025-08-19 20:45:02.106121', '29', '黄杏', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (137, '2025-08-19 20:45:02.107120', '30', '油桃', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (138, '2025-08-19 20:45:02.107120', '31', '李子', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (139, '2025-08-19 20:45:02.108120', '32', '梨', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (140, '2025-08-19 20:45:02.109120', '33', '坚果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (141, '2025-08-19 20:45:02.110359', '34', '香蕉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (142, '2025-08-19 20:45:02.110992', '35', '青苹果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (143, '2025-08-19 20:45:02.111997', '36', '树莓', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (144, '2025-08-19 20:45:02.112997', '38', '橙子', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (145, '2025-08-19 20:45:02.112997', '39', '柑橘', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (146, '2025-08-19 20:45:02.113998', '40', '水蜜桃', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (147, '2025-08-19 20:45:02.114998', '41', '樱桃', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (148, '2025-08-19 20:45:02.116998', '42', '红颜草莓', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (149, '2025-08-19 20:45:02.117998', '43', '广西苹果蕉新鲜香蕉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (150, '2025-08-19 20:45:02.118998', '44', '山东黄蜜樱桃', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (151, '2025-08-19 20:45:02.120007', '45', '新疆无籽克伦生红提脆甜葡萄马奶', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (152, '2025-08-19 20:45:02.121007', '46', '京鲜生 国产蓝莓', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (153, '2025-08-19 20:45:02.121998', '47', '陕西红富士苹果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (154, '2025-08-19 20:45:02.122998', '48', '京鲜到海南妃子笑荔枝', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (155, '2025-08-19 20:45:02.123998', '49', '杨梅鲜果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (156, '2025-08-19 20:45:02.125006', '50', '鑫果伴攀枝花米易枇杷', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (157, '2025-08-19 20:45:02.125006', '51', '赛鲜者泰国金枕榴莲', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (158, '2025-08-19 20:45:02.125997', '52', '泰国金枕头榴莲', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (159, '2025-08-19 20:45:02.126998', '53', '金枕头榴莲鲜果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (160, '2025-08-19 20:45:02.127997', '54', '绿宝甜瓜', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (161, '2025-08-19 20:45:02.128998', '55', '特星鲜蓝莓', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (162, '2025-08-19 20:45:02.129998', '56', '赛鲜者泰国金枕榴莲', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (163, '2025-08-19 20:45:02.130998', '57', '十里馋海南妃子笑荔枝', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (164, '2025-08-19 20:45:02.131998', '58', '颜曼箐樱桃车厘子', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (165, '2025-08-19 20:45:02.131998', '59', '海南妃子笑荔枝', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (166, '2025-08-19 20:45:02.132997', '60', '美国晚熟脐橙', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (167, '2025-08-19 20:45:02.133997', '61', '果迎鲜红心火龙果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (168, '2025-08-19 20:45:02.134997', '62', '沙窝曙光泰国山竹', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (169, '2025-08-19 20:45:02.135997', '63', '山东烟台红富士苹果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (170, '2025-08-19 20:45:02.136997', '64', '赛鲜者泰国金枕榴莲', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (171, '2025-08-19 20:45:02.137997', '65', '新鲜时令水果整箱', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (172, '2025-08-19 20:45:02.137997', '66', '广西百香果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (173, '2025-08-19 20:45:02.139694', '67', '泰国金枕头榴莲', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (174, '2025-08-19 20:45:02.140519', '68', '头茬羊角蜜甜瓜', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (175, '2025-08-19 20:45:02.141327', '69', '山东玉菇甜瓜冰激凌香瓜甜瓜', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (176, '2025-08-19 20:45:02.142333', '70', '迎畔车厘子樱桃', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (177, '2025-08-19 20:45:02.142333', '71', '山东小蜜蜂甜瓜', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (178, '2025-08-19 20:45:02.143333', '72', '红心三华李', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (179, '2025-08-19 20:45:02.144334', '73', '东北新鲜梅花鹿肉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (180, '2025-08-19 20:45:02.145732', '74', '新鲜兔肉整只', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (181, '2025-08-19 20:45:02.146878', '75', '厨哈哈料理包预制菜外卖快餐速食', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (182, '2025-08-19 20:45:02.148000', '76', '发晓食品原香猪肚丝', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (183, '2025-08-19 20:45:02.149007', '77', '温氏 供港鲜熟盐焗鸡', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (184, '2025-08-19 20:45:02.150286', '78', '发晓食品五香酱牛肉卤牛肉即食熟牛肉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (185, '2025-08-19 20:45:02.150286', '79', '原装进口西班牙火腿伊比利亚火腿', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (186, '2025-08-19 20:45:02.151299', '80', '聪灵铺子山东五香驴肉牛肉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (187, '2025-08-19 20:45:02.152299', '81', '好拾味熟食酱牛肉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (188, '2025-08-19 20:45:02.152299', '82', '清真腊味咸卤味', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (189, '2025-08-19 20:45:02.153299', '83', '猪腿肉猪前后腿', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (190, '2025-08-19 20:45:02.154299', '84', '新鲜猪黄喉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (191, '2025-08-19 20:45:02.155302', '85', '茶牛原切牛排', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (192, '2025-08-19 20:45:02.156300', '86', '内蒙古酱牛肉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (193, '2025-08-19 20:45:02.157299', '87', '太湖海【现切淡水鱼片】', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (194, '2025-08-19 20:45:02.159005', '88', '原切新鲜梅花鹿肉生鲜', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (195, '2025-08-19 20:45:02.160402', '89', '火锅丸子', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (196, '2025-08-19 20:45:02.161405', '90', '整只梅花鹿腿', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (197, '2025-08-19 20:45:02.161405', '91', '鹿腱子肉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (198, '2025-08-19 20:45:02.162405', '92', '内蒙古酱牛肉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (199, '2025-08-19 20:45:02.163407', '93', '生鲜羊肉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (200, '2025-08-19 20:45:02.164414', '94', '羊杂新鲜', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (201, '2025-08-19 20:45:02.165416', '95', '骆驼肉内蒙古骆驼腿肉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (202, '2025-08-19 20:45:02.165416', '96', '澳洲谷饲原切肥牛卷', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (203, '2025-08-19 20:45:02.166813', '97', '新西兰进口新鲜腩肉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (204, '2025-08-19 20:45:02.167820', '98', '胡椒猪肚鸡', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (205, '2025-08-19 20:45:02.169549', '99', '兔腿', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (206, '2025-08-19 20:45:02.170420', '100', '猪头肉', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (207, '2025-08-19 20:45:02.171427', '101', '人工养殖鳄鱼', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (208, '2025-08-19 20:45:02.171427', '102', '美鲜旺', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (209, '2025-08-19 20:45:02.172471', '103', '福建下河杨桃', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (210, '2025-08-19 20:45:02.174506', '104', '进口5A级山竹', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (211, '2025-08-19 20:45:02.175506', '105', '烟台脆甜苹果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (212, '2025-08-19 20:45:02.176847', '106', '飘香果度山西国产大樱桃车厘子', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (213, '2025-08-19 20:45:02.178351', '107', '山竹泰国进口山竹', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (214, '2025-08-19 20:45:02.178351', '108', '礼品', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (215, '2025-08-19 20:45:02.179355', '109', '泰国进口5A级山竹', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (216, '2025-08-19 20:45:02.179355', '110', '京鲜到泰国山竹', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (217, '2025-08-19 20:45:02.181356', '111', '新西兰宝石红奇异', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (218, '2025-08-19 20:45:02.181356', '112', '四川米易甜枇杷高山枇杷', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (219, '2025-08-19 20:45:02.182356', '113', '麒麟大西瓜', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (220, '2025-08-19 20:45:02.183355', '114', '桂七大芒果', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (221, '2025-08-19 20:45:02.185355', '115', '泰国进口山竹', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (222, '2025-08-19 20:45:02.186763', '116', '枇杷', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (223, '2025-08-19 20:45:02.187539', '117', '红心三华李', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (224, '2025-08-19 20:45:02.187539', '118', '小凤西瓜', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (225, '2025-08-19 20:45:02.188604', '119', '山东羊角蜜甜瓜', 3, '', 9, 1);
INSERT INTO `django_admin_log` VALUES (226, '2025-08-19 21:17:27.660700', '5', 'rtytyrtytry', 2, '[{\"changed\": {\"fields\": [\"\\u5546\\u54c1\\u540d\\u79f0\"]}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (227, '2025-08-19 21:17:35.471901', '2', '5555', 2, '[{\"changed\": {\"fields\": [\"\\u5546\\u54c1\\u540d\\u79f0\"]}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (228, '2025-08-19 21:20:06.408718', '1', 'Order object (1)', 2, '[{\"changed\": {\"fields\": [\"\\u8ba2\\u5355\\u72b6\\u6001\"]}}]', 14, 1);
INSERT INTO `django_admin_log` VALUES (229, '2025-08-19 22:29:08.759614', '7', '测试', 1, '[{\"added\": {}}]', 10, 1);
INSERT INTO `django_admin_log` VALUES (230, '2025-08-19 22:30:10.814686', '4', '旗舰电脑', 3, '', 10, 1);
INSERT INTO `django_admin_log` VALUES (231, '2025-08-19 22:30:10.815724', '5', '3C数码', 3, '', 10, 1);
INSERT INTO `django_admin_log` VALUES (232, '2025-08-19 22:30:10.815724', '6', '风味肉类', 3, '', 10, 1);
INSERT INTO `django_admin_log` VALUES (233, '2025-08-19 22:30:10.816723', '7', '测试', 3, '', 10, 1);
INSERT INTO `django_admin_log` VALUES (234, '2025-08-19 22:30:34.227451', '1', '新鲜水果', 2, '[{\"changed\": {\"fields\": [\"\\u5206\\u7c7b\\u56fe\\u7247\"]}}]', 10, 1);
INSERT INTO `django_admin_log` VALUES (235, '2025-08-19 22:37:40.590856', '1', '新鲜水果', 2, '[{\"changed\": {\"fields\": [\"\\u5206\\u7c7b\\u56fe\\u7247\"]}}]', 10, 1);
INSERT INTO `django_admin_log` VALUES (236, '2025-08-19 22:38:04.842782', '1', '新鲜水果', 2, '[{\"changed\": {\"fields\": [\"\\u5206\\u7c7b\\u56fe\\u7247\"]}}]', 10, 1);
INSERT INTO `django_admin_log` VALUES (237, '2025-08-19 22:39:28.974549', '1', '新鲜水果', 2, '[{\"changed\": {\"fields\": [\"\\u5206\\u7c7b\\u56fe\\u7247\"]}}]', 10, 1);
INSERT INTO `django_admin_log` VALUES (238, '2025-08-19 22:39:35.894350', '1', '新鲜水果', 2, '[{\"changed\": {\"fields\": [\"\\u5206\\u7c7b\\u56fe\\u7247\"]}}]', 10, 1);
INSERT INTO `django_admin_log` VALUES (239, '2025-08-19 23:10:20.995420', '1', '项链', 2, '[{\"changed\": {\"fields\": [\"\\u5546\\u54c1\\u7c7b\\u578b\\u540d\\u79f0\", \"\\u6807\\u7b7e\"]}}]', 10, 1);
INSERT INTO `django_admin_log` VALUES (240, '2025-08-19 23:13:01.297008', '1', '项链', 2, '[{\"changed\": {\"fields\": [\"\\u5206\\u7c7b\\u56fe\\u7247\"]}}]', 10, 1);
INSERT INTO `django_admin_log` VALUES (241, '2025-08-19 23:13:13.983232', '2', '手镯', 2, '[{\"changed\": {\"fields\": [\"\\u5546\\u54c1\\u7c7b\\u578b\\u540d\\u79f0\", \"\\u5206\\u7c7b\\u56fe\\u7247\"]}}]', 10, 1);
INSERT INTO `django_admin_log` VALUES (242, '2025-08-19 23:13:25.632313', '2', '手镯', 2, '[{\"changed\": {\"fields\": [\"\\u6807\\u7b7e\"]}}]', 10, 1);
INSERT INTO `django_admin_log` VALUES (243, '2025-08-19 23:13:39.219131', '3', '发饰', 2, '[{\"changed\": {\"fields\": [\"\\u5546\\u54c1\\u7c7b\\u578b\\u540d\\u79f0\", \"\\u5206\\u7c7b\\u56fe\\u7247\", \"\\u6807\\u7b7e\"]}}]', 10, 1);
INSERT INTO `django_admin_log` VALUES (244, '2025-08-19 23:21:30.613288', '1', '黄金项链20克', 2, '[{\"changed\": {\"fields\": [\"\\u9996\\u9970\\u540d\\u79f0\", \"\\u7b80\\u4ecb\", \"\\u9996\\u9970\\u56fe\\u7247\"]}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (245, '2025-08-19 23:21:44.002910', '1', '黄金项链20克', 2, '[{\"changed\": {\"fields\": [\"\\u5355\\u4f4d\"]}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (246, '2025-08-19 23:23:15.520527', '2', '18K金上帝之眼项链项坠定制创意个性吊坠挂件镶钻金属饰品', 2, '[{\"changed\": {\"fields\": [\"\\u9996\\u9970\\u540d\\u79f0\", \"\\u7b80\\u4ecb\", \"\\u5355\\u4f4d\", \"\\u9996\\u9970\\u56fe\\u7247\"]}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (247, '2025-08-19 23:25:35.019201', '3', '和田玉手饰手串圆珠挂牌手镯白玉石观音菩萨女首饰珍品直播专拍1', 2, '[{\"changed\": {\"fields\": [\"\\u9996\\u9970\\u540d\\u79f0\", \"\\u7b80\\u4ecb\", \"\\u5355\\u4f4d\", \"\\u9996\\u9970\\u56fe\\u7247\", \"\\u9996\\u9970\\u6240\\u5c5e\\u7c7b\\u578b\"]}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (248, '2025-08-19 23:27:54.896306', '4', '欧美跨境不锈钢C型手镯 6MM男女通用款', 2, '[{\"changed\": {\"fields\": [\"\\u9996\\u9970\\u540d\\u79f0\", \"\\u7b80\\u4ecb\", \"\\u4ef7\\u683c\", \"\\u5355\\u4f4d\", \"\\u9996\\u9970\\u56fe\\u7247\", \"\\u9996\\u9970\\u6240\\u5c5e\\u7c7b\\u578b\"]}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (249, '2025-08-19 23:28:07.385211', '1', '黄金项链20克', 2, '[{\"changed\": {\"fields\": [\"\\u4ef7\\u683c\"]}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (250, '2025-08-19 23:28:15.554160', '2', '18K金上帝之眼项链项坠定制创意个性吊坠挂件镶钻金属饰品', 2, '[{\"changed\": {\"fields\": [\"\\u4ef7\\u683c\"]}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (251, '2025-08-19 23:29:41.593913', '5', '圈马尾皮筋发箍发饰', 2, '[{\"changed\": {\"fields\": [\"\\u9996\\u9970\\u540d\\u79f0\", \"\\u7b80\\u4ecb\", \"\\u9996\\u9970\\u56fe\\u7247\", \"\\u9996\\u9970\\u6240\\u5c5e\\u7c7b\\u578b\"]}}]', 9, 1);
INSERT INTO `django_admin_log` VALUES (252, '2025-08-20 17:27:15.645795', '18', 'Order object (18)', 2, '[{\"changed\": {\"fields\": [\"\\u8ba2\\u5355\\u72b6\\u6001\"]}}]', 14, 1);
INSERT INTO `django_admin_log` VALUES (253, '2025-08-20 17:27:24.531002', '18', 'Order object (18)', 2, '[{\"changed\": {\"fields\": [\"\\u8ba2\\u5355\\u72b6\\u6001\"]}}]', 14, 1);
INSERT INTO `django_admin_log` VALUES (254, '2025-08-20 17:38:05.442619', '18', 'Order object (18)', 2, '[{\"changed\": {\"fields\": [\"\\u8ba2\\u5355\\u72b6\\u6001\"]}}]', 14, 1);
INSERT INTO `django_admin_log` VALUES (255, '2025-08-20 17:39:15.784505', '18', 'Order object (18)', 2, '[{\"changed\": {\"fields\": [\"\\u8ba2\\u5355\\u72b6\\u6001\"]}}]', 14, 1);
INSERT INTO `django_admin_log` VALUES (256, '2025-08-20 17:41:06.174045', '18', 'Order object (18)', 2, '[{\"changed\": {\"fields\": [\"\\u8ba2\\u5355\\u72b6\\u6001\"]}}]', 14, 1);
INSERT INTO `django_admin_log` VALUES (257, '2025-08-20 17:42:18.381954', '18', 'Order object (18)', 2, '[{\"changed\": {\"fields\": [\"\\u8ba2\\u5355\\u72b6\\u6001\"]}}]', 14, 1);



-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2025-08-19 18:02:27.653439');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2025-08-19 18:02:27.852443');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2025-08-19 18:02:27.901223');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2025-08-19 18:02:27.906230');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2025-08-19 18:02:27.911221');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2025-08-19 18:02:27.937579');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2025-08-19 18:02:27.957572');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2025-08-19 18:02:27.969619');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2025-08-19 18:02:27.973633');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2025-08-19 18:02:27.991626');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2025-08-19 18:02:27.993636');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2025-08-19 18:02:27.998626');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2025-08-19 18:02:28.018626');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2025-08-19 18:02:28.065703');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2025-08-19 18:02:28.077703');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2025-08-19 18:02:28.082713');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2025-08-19 18:02:28.127559');
INSERT INTO `django_migrations` VALUES (18, 'service', '0001_initial', '2025-08-19 18:02:28.147222');
INSERT INTO `django_migrations` VALUES (19, 'sessions', '0001_initial', '2025-08-19 18:02:28.183745');
INSERT INTO `django_migrations` VALUES (20, 'user', '0001_initial', '2025-08-19 18:02:28.374741');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('0a6yy0zjbfnh6fensfvjdzt0mepn3o7l', 'eyJ2ZXJpZnljb2RlIjoiYWFkNiIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uoXt1:5ZNSirg-ZikFhfEEO8gy4k8lbjiIXsE7xZpBMPk4lDo', '2025-08-20 09:46:11.521291');
INSERT INTO `django_session` VALUES ('4aw15ne8cch3am6gxk397ab72iiv4s9w', 'eyJ2ZXJpZnljb2RlIjoiVjN1bCIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uoOKi:VnMs8-xCgA-vIiUjmJ5_3oedAvP0secp5BHVwaKUwXk', '2025-08-19 23:34:08.289237');
INSERT INTO `django_session` VALUES ('4nw5t6wpbp8voq2jbpa0d51h4htxr2mu', 'eyJ2ZXJpZnljb2RlIjoiSUVDUyIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uoP6i:z1U_ofGcI0YZk_KKpi3jkm_BEnel0GulihwYK2g_LQ4', '2025-08-20 00:23:44.962603');
INSERT INTO `django_session` VALUES ('8ysmpwf5800xko4gu409ajbs35g13j91', 'eyJ2ZXJpZnljb2RlIjoiZjllWCIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uoXae:1_YVk7zh9gRvRjkxJqaBr0-VNlwHEJ0uW-KV572VQBo', '2025-08-20 09:27:12.882702');
INSERT INTO `django_session` VALUES ('ab6h8w9ao2rn44vcz3j15q36gxo4bwqr', 'eyJ2ZXJpZnljb2RlIjoib1lIUSIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uoJCO:-tz1jk49gWFEieDvqxH8SWwScN6ZIbf_TqSoM4F9TUM', '2025-08-19 18:05:12.695280');
INSERT INTO `django_session` VALUES ('bnqihwzsne0zeb0s0zrm0sjx0ueqag9d', 'e30:1uoYEc:afO7muBtaYPBymweyI4GlF8SaSSEljwwuRnML4OJJKw', '2025-09-03 10:07:30.773428');
INSERT INTO `django_session` VALUES ('ccj2vurpr1mwqz57yi63nptv296x54sa', 'eyJ2ZXJpZnljb2RlIjoiRlBXcCIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uod3z:x-HxPOXYV6xEZqgJxF4VwzRhuGJ79pAyvkNqVtkGUcQ', '2025-08-20 15:17:51.313824');
INSERT INTO `django_session` VALUES ('d8mzcgm7uwtewolvtehp7l4tgwfozjn5', 'e30:1uoY5D:nAzIpL5-ZjHeqTQlpjlsYisb9gel1cBzNgacLAe2b1s', '2025-09-03 09:57:47.252372');
INSERT INTO `django_session` VALUES ('e0ajiw07ohksx60jqhmvdma9667glat5', 'eyJ2ZXJpZnljb2RlIjoiMDdzVyIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uoY2m:kC1D4VKtjDmOiiKogsZs2UPZ66x5PR_cGwzTxQtP-Pw', '2025-08-20 09:56:16.211899');
INSERT INTO `django_session` VALUES ('fb38gq3zvmjrfzgun9tqslqmmnfaspw3', '.eJxVj7sOwjAMRf_FM6pSN02abrAzdq7cxKXhkaAGEAjx7yQSC5vle3xsv-HBq59fNjqGHtR2GGADY-KUfAwjP69-fUGvhOyEyAHdb8t4T7yO3mUe4a83kT1xKIE7UjjEysZwW_1UFaT6pana52Xn3Y_9EyyUljJtmJsW1dS1s1bEjFJaQ450o7tJaNGw61ytSCEpstiatjaImdPG1iyz1Ic5Qv-GciZuoNgDXcqPpayxkfD5fAFPpFH_:1uoYQB:VtVa2UjzPoXOSkIqKmbSWNxASfBUGucJXsIf_r4vZYo', '2025-08-27 10:19:27.851548');
INSERT INTO `django_session` VALUES ('fds1uyek06ft4l8i9kdvdcf62j2bh0ms', 'eyJ2ZXJpZnljb2RlIjoiQUdkayIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uomWY:A9Y7D-X4KayQ2hLZF7b2FmctT__oMl7Pi5Yz15nqItg', '2025-08-21 01:23:58.623678');
INSERT INTO `django_session` VALUES ('gktyacune0bb37v17n1iafx2ss5nsewl', 'eyJ2ZXJpZnljb2RlIjoiSkQ1QiIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uoY0c:64XkKevK-YhDbRRWXUj9gTNUmh-r919kmj8wUJX5cuM', '2025-08-20 09:54:02.278741');
INSERT INTO `django_session` VALUES ('hzkyz9f5fzi2rwvg5e72fqfv9ol8qhje', 'eyJ2ZXJpZnljb2RlIjoidHZGYyIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uoY1f:aEtvxv0yQUdzeH99YG0m4KXc0MVm1J4doJVLee-Ztcg', '2025-08-20 09:55:07.884370');
INSERT INTO `django_session` VALUES ('jvkcgk0vthcrhbnqx2qvucqb8yzj1xyj', 'eyJ2ZXJpZnljb2RlIjoiUTVSbyIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uoYDY:we26RKBNbEeftvg4t9_PeMbKV4DkKWfulUfXZiFjW2Y', '2025-08-20 10:07:24.909865');
INSERT INTO `django_session` VALUES ('kedyaepiklorvri32b3qkeimtyoltdwp', 'eyJ2ZXJpZnljb2RlIjoiUlB0YSIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uoXxZ:DTJz9YNplK_LP4eJBiE6K6VrZGiIJny1y9A4pDf58HY', '2025-08-20 09:50:53.799921');
INSERT INTO `django_session` VALUES ('lajk18ac273g3lrw4p2s96kmf9c482e7', '.eJytlEuP2yAUhf9K5HUeGJtXlt132VVdWTwuCa1jImNnGo3y3wv2LOqJJxOp3fhy4QCfDtZ5zWo59Md6CNDVzmT7LM_Wf88pqX9BmxbMT9ke_Fb7tu-c2ibJ9m01bL96A82XN-3sgKMMx7gbJJECcVA813lJDeXamkJo4ByBFYwSizEpACvCmSijwuqCUl1g4LIsWDr0BO0Q4lnfX6uslSeosv2qyqpqEELQsTAUC1MyT6VEtMrWUeEi86SFZpOaTdicO3_yvUsLSTJ0zaTYSXNy7S6h7w7em7CbBPULuMOxTyKUenAmjXOE8tt69R6IK4ljIQUhzwGNVz1A8Z2J3zuUfI6CF1DeeaOZSmCMq49QGi-Naw-f-dJfz3APhOdAxQIQI5jHQnHBUjGlTYYJPU3KZBjndOwYjPYx9CGs9tEZ18oeHvCqzr-EBdhiDlsuPqQux6Lk44e0chN848wqDqC9QOPPj5DgIpshUt9DlXMo8oSDfOwQtf_8r0W0i9MLVGRORReoKBZkckz8V6ssgEk5M8bJPRmdk7FP_XrCoXTTxLjMldJtt4zD5jj89iMm1wU6Z686ZmRML_stNCnNAoQQ86eG32fXXbM9Rbc_GZG36g:1uof6Q:WNwA7lvSflf_IgoyjsG50IWXtCyFVFP-moYs2I3cSjA', '2025-08-20 17:28:30.775787');
INSERT INTO `django_session` VALUES ('no2mq10zizlx5dppziyl5cfyjmz8iabg', 'eyJ2ZXJpZnljb2RlIjoiWWNTSCIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uokga:6TsA2og1bFQjHlR-hiK4ItZQTlDLeotnC-ayaG5Yen4', '2025-08-20 23:26:12.530327');
INSERT INTO `django_session` VALUES ('rp1yislaix64nwohmaund6jgh7lod8h0', '.eJyt1MtuozAUBuBXibxOgrHxrcvZzxOUKvLlkLglOOKSqqry7mNDF0ND00jthoPxwf70g_yOdnroD7uhg3bnHXpAOVr__8xo-wJNmnDPutmHrQ1N33qzTS3bj9lu-zc4qP989M4WOOjuEN8GzbTCEozMbV5wx6WtHFUWpMRQKcFZRQijQAyTQhWxo7KUc0sJSF1QkRY9QjN0ca3H9xI1-ggleliVqCwHpRQfi8CxCKPzVArMS7SOHT6ap16oN2mw6TanNhxD79NEahnaeurItDv6Jkv0bB-C67KpYfcKfn_oUxNOY_Au3ecY55f16jNIGk1iYZSx-0DjVjcooXXxekXJ5xSyQPmUjRUmwYQ0X1HqoJ1v9t_l0r-d4BpE5iC6ABKMyFg4oSIVV1QpMGWnhzoFJiUfRwLG-AT-EmtDTMY3uocbXtOG124BS-fYYvFD2mIsRt_-kJXedKH2bhVvoDlDHU63SHDW9RDV16hijmJ3JCjHEebVj_-1SDt7u6BicxVfUHGi2JSY-tWoKgCXzpnxOLmW8blMfJvXHQmlnSbjsiudbtkyR8w58vKELv8AxRKpvw:1uolbT:qxCQDP57QZqFhluxJs3wvO94QC9a7_2ZU7GzPXzUgdY', '2025-09-04 00:23:59.098732');
INSERT INTO `django_session` VALUES ('sp069dum727rkvhui0t8donu6b59twbc', 'eyJ2ZXJpZnljb2RlIjoiMHpXUSIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uokii:z_XDx5G3Jk_JEB9vS7746jy0EGFZA-W9hwFxD5-gnqw', '2025-08-20 23:28:24.738381');
INSERT INTO `django_session` VALUES ('w3bmmxgntz1vxuhuxr57ovaivetvtm7k', 'eyJ2ZXJpZnljb2RlIjoielNaRiIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uoXfq:OKEVEHmU3OOs__4HLpv5KDkpjwpR8T8_Dqj3hv1uN84', '2025-08-20 09:32:34.162844');
INSERT INTO `django_session` VALUES ('wuofp3cpph18l3zpb4l7cxdmbrrryhqu', 'eyJ2ZXJpZnljb2RlIjoiT3c0diIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uoYEh:Ax-lsU2U_HGdEuuv1XOUwhHHPInvzshWS49JuY7WThA', '2025-08-20 10:08:35.031513');
INSERT INTO `django_session` VALUES ('x5afgvfbqb265d4dnq0wr6y6h949eipk', 'eyJ2ZXJpZnljb2RlIjoiUmhNcSIsIl9zZXNzaW9uX2V4cGlyeSI6NjB9:1uomIF:mntE4FozUUkevNA78sKZ7qGqN6B3wFdnssEc1iQlhT4', '2025-08-21 01:09:11.073102');
INSERT INTO `django_session` VALUES ('zb51p1srg0uzwy9nhiohb2o2dsjbigkh', '.eJytlM1uozAUhV8lYp0EY_BflrOaTZ-gjCL_XBJPCY4w0ImqvPvY0MXQ0DRSZ8P1tY_tT8fovCV72XfHfe-h3VuT7JIsWf87p6R-gSYumN-yObitdk3XWrWNku37qt8-OQP1j3ft7ICj9MewGySRAnFQPNNZQQ3lujK50MA5gkowSiqMSQ5YEc5EERSVzinVOQYui5zFQ0_Q9D6c9fxWJo08QZnsVmVSlr0Qgo6FoVCYklksBaJlsg4KG5gnLdSb2Gz85ty6k-tsXIiSvq0nRSrNyTZpRE8PzhmfToL9K9jDsYsiFHuwJo4zhLLrevURiCuJQyE5IY8BjVfdQXGtCd8blGyOghdQPnijmYpgjKvPUGonjW0OX_nSXc5wC4TnQPkCECOYh0JxzmIxRRUNE3qalNEwzunYMRjtY-hTWO2CM7aRHdzhVa179Quw-Ry2WHxIXYxFyfsPWcmNd7U1qzCAZoDane8hwSDrPlDfQhVzKPKAg3zsEK2-_a8FtMHqBSoyp6ILVBQLMjkm_qtVFYCJOTPGyS0ZnZOxL_16wKF408S4zBXTLV3GYXMcfv0VkmuA1lYXHTIypBf5-TLENPPgfcifPfw52_aS7Ci6_gUTPLeu:1uoYli:88PpKShQkpLGH4pnj7TrwkoAX_6_NtLOrIl7As_IUes', '2025-08-20 10:42:42.969182');

-- ----------------------------
-- Table structure for evaluate
-- ----------------------------
DROP TABLE IF EXISTS `evaluate`;
CREATE TABLE `evaluate`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `evaluate` varchar(1000) CHARACTER SET utf8mb4 NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `sku_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `evaluate_sku_id_a2ea6bce_fk_goods_id`(`sku_id` ASC) USING BTREE,
  CONSTRAINT `evaluate_sku_id_a2ea6bce_fk_goods_id` FOREIGN KEY (`sku_id`) REFERENCES `goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of evaluate
-- ----------------------------
INSERT INTO `evaluate` VALUES (1, 'user1234', 'okok', '2025-08-19 21:20:20.157511', '2025-08-19 21:20:20.157511', 1);

-- ----------------------------
-- Table structure for face
-- ----------------------------
DROP TABLE IF EXISTS `face`;
CREATE TABLE `face`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 99 CHARACTER SET = utf8mb4 ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of face
-- ----------------------------
INSERT INTO `face` VALUES (1, '微笑', '001.png');
INSERT INTO `face` VALUES (2, '害羞', '002.png');
INSERT INTO `face` VALUES (3, '吐舌头', '003.png');
INSERT INTO `face` VALUES (4, '忧伤', '047.png');
INSERT INTO `face` VALUES (5, '再见', '024.png');
INSERT INTO `face` VALUES (6, '迷惑', '030.png');
INSERT INTO `face` VALUES (7, '安慰', '009.png');
INSERT INTO `face` VALUES (8, '飞吻', '008.png');
INSERT INTO `face` VALUES (9, '天使', '023.png');
INSERT INTO `face` VALUES (10, '挥泪告别', '054.png');
INSERT INTO `face` VALUES (11, '爱慕', '005.png');
INSERT INTO `face` VALUES (12, '加油', '011.png');
INSERT INTO `face` VALUES (13, '傻笑', '040.png');
INSERT INTO `face` VALUES (14, '小样', '036.png');
INSERT INTO `face` VALUES (15, '委屈', '048.png');
INSERT INTO `face` VALUES (16, '悲泣', '049.png');
INSERT INTO `face` VALUES (17, '大哭', '050.png');
INSERT INTO `face` VALUES (18, '痛哭', '051.png');
INSERT INTO `face` VALUES (19, '对不起', '053.png');
INSERT INTO `face` VALUES (20, '小二', '070.png');
INSERT INTO `face` VALUES (21, '恭喜发财', '069.png');
INSERT INTO `face` VALUES (22, '财神', '067.png');
INSERT INTO `face` VALUES (23, '抱抱', '010.png');
INSERT INTO `face` VALUES (24, '玫瑰', '085.png');
INSERT INTO `face` VALUES (25, '爱心', '087.png');
INSERT INTO `face` VALUES (26, '漂亮MM', '078.png');
INSERT INTO `face` VALUES (27, '帅哥', '079.png');
INSERT INTO `face` VALUES (28, '胜利', '012.png');
INSERT INTO `face` VALUES (29, '成交', '081.png');
INSERT INTO `face` VALUES (30, '鼓掌', '082.png');
INSERT INTO `face` VALUES (31, '握手', '083.png');
INSERT INTO `face` VALUES (32, '疑问', '031.png');
INSERT INTO `face` VALUES (33, '无奈', '042.png');
INSERT INTO `face` VALUES (34, '强', '013.png');
INSERT INTO `face` VALUES (35, '跳舞', '007.png');
INSERT INTO `face` VALUES (36, '查找', '017.png');
INSERT INTO `face` VALUES (37, '享受', '026.png');
INSERT INTO `face` VALUES (38, '偷笑', '004.png');
INSERT INTO `face` VALUES (39, '好主意', '021.png');
INSERT INTO `face` VALUES (40, '流口水', '025.png');
INSERT INTO `face` VALUES (41, '露齿笑', '016.png');
INSERT INTO `face` VALUES (42, '流汗', '043.png');
INSERT INTO `face` VALUES (43, '呆若木鸡', '028.png');
INSERT INTO `face` VALUES (44, '皱眉', '055.png');
INSERT INTO `face` VALUES (45, '摇头', '037.png');
INSERT INTO `face` VALUES (46, '算账', '019.png');
INSERT INTO `face` VALUES (47, '亲亲', '014.png');
INSERT INTO `face` VALUES (48, '花痴', '015.png');
INSERT INTO `face` VALUES (49, '呼叫', '018.png');
INSERT INTO `face` VALUES (50, '思考', '029.png');
INSERT INTO `face` VALUES (51, '大笑', '006.png');
INSERT INTO `face` VALUES (52, '嘘', '035.png');
INSERT INTO `face` VALUES (53, '惊讶', '060.png');
INSERT INTO `face` VALUES (54, '惊愕', '061.png');
INSERT INTO `face` VALUES (55, '生气', '066.png');
INSERT INTO `face` VALUES (56, '老大', '071.png');
INSERT INTO `face` VALUES (57, '学习雷锋', '068.png');
INSERT INTO `face` VALUES (58, '心碎', '088.png');
INSERT INTO `face` VALUES (59, '招财猫', '080.png');
INSERT INTO `face` VALUES (60, '红唇', '084.png');
INSERT INTO `face` VALUES (61, '举杯庆祝', '094.png');
INSERT INTO `face` VALUES (62, '钱', '089.png');
INSERT INTO `face` VALUES (63, '很晚了', '097.png');
INSERT INTO `face` VALUES (64, '礼物', '091.png');
INSERT INTO `face` VALUES (65, '购物', '090.png');
INSERT INTO `face` VALUES (66, '等待', '096.png');
INSERT INTO `face` VALUES (67, '时钟', '095.png');
INSERT INTO `face` VALUES (68, '财迷', '020.png');
INSERT INTO `face` VALUES (69, '鬼脸', '022.png');
INSERT INTO `face` VALUES (70, '色情狂', '027.png');
INSERT INTO `face` VALUES (71, '没钱了', '032.png');
INSERT INTO `face` VALUES (72, '无聊', '033.png');
INSERT INTO `face` VALUES (73, '怀疑', '034.png');
INSERT INTO `face` VALUES (74, '感冒', '038.png');
INSERT INTO `face` VALUES (75, '尴尬', '039.png');
INSERT INTO `face` VALUES (76, '不会吧', '041.png');
INSERT INTO `face` VALUES (77, '凄凉', '044.png');
INSERT INTO `face` VALUES (78, '困了', '045.png');
INSERT INTO `face` VALUES (79, '晕', '046.png');
INSERT INTO `face` VALUES (80, 'I服了U', '052.png');
INSERT INTO `face` VALUES (81, '好累', '056.png');
INSERT INTO `face` VALUES (82, '吐', '058.png');
INSERT INTO `face` VALUES (83, '背', '059.png');
INSERT INTO `face` VALUES (84, '闭嘴', '062.png');
INSERT INTO `face` VALUES (85, '欠扁', '063.png');
INSERT INTO `face` VALUES (86, '鄙视你', '064.png');
INSERT INTO `face` VALUES (87, '大怒', '065.png');
INSERT INTO `face` VALUES (88, '邪恶', '072.png');
INSERT INTO `face` VALUES (89, '单挑', '073.png');
INSERT INTO `face` VALUES (90, 'CS', '074.png');
INSERT INTO `face` VALUES (91, '隐形人', '075.png');
INSERT INTO `face` VALUES (92, '炸弹', '076.png');
INSERT INTO `face` VALUES (93, '惊声尖叫', '077.png');
INSERT INTO `face` VALUES (94, '残花', '086.png');
INSERT INTO `face` VALUES (95, '收邮件', '092.png');
INSERT INTO `face` VALUES (96, '电话', '093.png');
INSERT INTO `face` VALUES (97, '飞机', '098.png');
INSERT INTO `face` VALUES (98, '支付宝', '099.png');


-- ----------------------------
-- Table structure for feedback_user
-- ----------------------------
DROP TABLE IF EXISTS `feedback_user`;
CREATE TABLE `feedback_user`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `textarea_name` longtext CHARACTER SET utf8mb4 NOT NULL,
  `input_name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `feedback_number` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `feedback_number`(`feedback_number` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of feedback_user
-- ----------------------------
INSERT INTO `feedback_user` VALUES (1, 'user1234', '我问问23232323', '18711927383', 'GC-1755614416914', '2025-08-19 22:40:16.914089');

-- ----------------------------
-- Table structure for feedback_image
-- ----------------------------
DROP TABLE IF EXISTS `feedback_image`;
CREATE TABLE `feedback_image`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(100) CHARACTER SET utf8mb4 NOT NULL,
  `feedback_number_id` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `feedback_image_feedback_number_id_5a2777dd_fk_feedback_`(`feedback_number_id` ASC) USING BTREE,
  CONSTRAINT `feedback_image_feedback_number_id_5a2777dd_fk_feedback_` FOREIGN KEY (`feedback_number_id`) REFERENCES `feedback_user` (`feedback_number`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of feedback_image
-- ----------------------------
INSERT INTO `feedback_image` VALUES (1, 'uploads/syboo2.jpg', 'GC-1755614416914');

-- ----------------------------
-- Table structure for service
-- ----------------------------
DROP TABLE IF EXISTS `service`;
CREATE TABLE `service`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `number` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `service_user_id_bc66613e_fk_auth_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `service_user_id_bc66613e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of service
-- ----------------------------
INSERT INTO `service` VALUES (1, 'T1755597826684', 1);
INSERT INTO `service` VALUES (2, 'B1755607573148', 2);

SET FOREIGN_KEY_CHECKS = 1;


-- ----------------------------
-- Table structure for message
-- ----------------------------
DROP TABLE IF EXISTS `message`;
CREATE TABLE `message`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` int NOT NULL,
  `service` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `reading` int NOT NULL,
  `type` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `message_user_id_60e6a50a_fk_service_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `message_user_id_60e6a50a_fk_service_id` FOREIGN KEY (`user_id`) REFERENCES `service` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of message
-- ----------------------------
INSERT INTO `message` VALUES (1, 1, '时代大厦', '2025-08-19 23:31:17.849497', 1, 'text', 2);

-- ----------------------------
-- Table structure for order
-- ----------------------------
DROP TABLE IF EXISTS `order`;
CREATE TABLE `order`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `order_number` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `count` int NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `evaluate` int NOT NULL,
  `sku_id_id` bigint NOT NULL,
  `addr` varchar(255) CHARACTER SET utf8mb4 NULL DEFAULT NULL,
  `tel` varchar(255) CHARACTER SET utf8mb4 NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `order_sku_id_id_87894515_fk_goods_id`(`sku_id_id` ASC) USING BTREE,
  CONSTRAINT `order_sku_id_id_87894515_fk_goods_id` FOREIGN KEY (`sku_id_id`) REFERENCES `goods` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of order
-- ----------------------------
INSERT INTO `order` VALUES (18, 'user1234', 'L1755680038422', 1, '已发货', '2025-08-20 17:42:18.379954', '2025-08-20 16:53:58.427832', 0, 2, '张家界学院门卫', '18711945623');


