/*
 Navicat Premium Data Transfer

 Source Server         : django_database_mysql
 Source Server Type    : MySQL
 Source Server Version : 80021
 Source Host           : localhost:3306
 Source Schema         : django_database

 Target Server Type    : MySQL
 Target Server Version : 80021
 File Encoding         : 65001

 Date: 27/01/2022 16:26:13
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for app1_app1permission
-- ----------------------------
DROP TABLE IF EXISTS `app1_app1permission`;
CREATE TABLE `app1_app1permission`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `user_group` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `views_func` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 51 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_app1permission
-- ----------------------------
INSERT INTO `app1_app1permission` VALUES (7, 'others', '/logout/', '用户登出');
INSERT INTO `app1_app1permission` VALUES (8, 'others', '/home/', '用户主页');
INSERT INTO `app1_app1permission` VALUES (9, 'others', '/home/page', '用户主页翻页');
INSERT INTO `app1_app1permission` VALUES (10, 'others', '/home/search/page', '用户书本查询');
INSERT INTO `app1_app1permission` VALUES (11, 'others', '/home/search/type', '用户查询书本分类');
INSERT INTO `app1_app1permission` VALUES (12, 'others', '/book/download', '用户下载书本');
INSERT INTO `app1_app1permission` VALUES (15, 'admin', '/logout/', '用户登出');
INSERT INTO `app1_app1permission` VALUES (16, 'admin', '/home/', '用户主页');
INSERT INTO `app1_app1permission` VALUES (17, 'admin', '/home/page', '用户主页翻页');
INSERT INTO `app1_app1permission` VALUES (18, 'admin', '/home/search/page', '用户书本查询');
INSERT INTO `app1_app1permission` VALUES (19, 'admin', '/home/search/type', '用户查询书本分类');
INSERT INTO `app1_app1permission` VALUES (20, 'admin', '/book/download', '用户下载书本');
INSERT INTO `app1_app1permission` VALUES (21, 'admin', '/admin/', 'Django_ADMIN');
INSERT INTO `app1_app1permission` VALUES (22, 'admin', '/management/user/', '后台管理页面用户管理');
INSERT INTO `app1_app1permission` VALUES (23, 'admin', '/management/user/page', '后台管理页面用户管理翻页');
INSERT INTO `app1_app1permission` VALUES (24, 'admin', '/management/user/changegroup', '后台管理页面用户管理更改用户组');
INSERT INTO `app1_app1permission` VALUES (25, 'admin', '/management/user/delete', '后台管理页面用户管理删除用户');
INSERT INTO `app1_app1permission` VALUES (26, 'admin', '/management/user/addusers/', '后台管理页面用户管理添加用户(批量导入)');
INSERT INTO `app1_app1permission` VALUES (27, 'admin', '/management/user/addusers/download/', '后台管理页面用户管理下载批量导入用户模板');
INSERT INTO `app1_app1permission` VALUES (28, 'admin', '/management/refresh/', '后台管理页面用户管理刷新页面');
INSERT INTO `app1_app1permission` VALUES (29, 'admin', '/management/book/', '后台管理页面书本管理');
INSERT INTO `app1_app1permission` VALUES (30, 'admin', '/management/book/page', '后台管理页面书本管理翻页');
INSERT INTO `app1_app1permission` VALUES (31, 'admin', '/management/book/update/', '后台管理页面书本管理修改书本信息');
INSERT INTO `app1_app1permission` VALUES (32, 'admin', '/management/book/delete', '后台管理页面书本管理删除书本');
INSERT INTO `app1_app1permission` VALUES (33, 'admin', '/management/book/addbook/', '后台管理页面书本管理添加书本');
INSERT INTO `app1_app1permission` VALUES (34, 'admin', '/management/system/', '后台管理页面系统管理');
INSERT INTO `app1_app1permission` VALUES (35, 'admin', '/management/system/page', '后台管理页面系统管理翻页');
INSERT INTO `app1_app1permission` VALUES (36, 'admin', '/management/system/permission/add/', '后台管理页面系统管理添加权限');
INSERT INTO `app1_app1permission` VALUES (37, 'admin', '/management/system/permission/update/', '后台管理页面系统管理修改权限');
INSERT INTO `app1_app1permission` VALUES (38, 'admin', '/management/system/permission/delete', '后台管理页面系统管理删除权限');
INSERT INTO `app1_app1permission` VALUES (39, 'admin', '/management/system/permission/upload/', '后台管理页面系统管理导入权限');
INSERT INTO `app1_app1permission` VALUES (40, 'admin', '/management/system/permission/upload/download', '后台管理页面系统管理下载批量导入权限模板');

-- ----------------------------
-- Table structure for app1_books
-- ----------------------------
DROP TABLE IF EXISTS `app1_books`;
CREATE TABLE `app1_books`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `book_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `book_type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `book_introduction` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `issue_year` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `book_file_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `add_book_time` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `number_of_downloads` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of app1_books
-- ----------------------------
INSERT INTO `app1_books` VALUES (1, 'flask web 开发', 'Python', '本书不仅适合初级Web开发人员学习阅读，更是Python程序员用来学习高级Web开发技术的优秀参考书。', '2014-12-01', '1641794484.4267302.zip', '2022-01-10 14:01:24', 4);
INSERT INTO `app1_books` VALUES (2, 'Python Cookbook', 'Python', '本书适合具有一定Python基础的读者阅读参考。', '2010-05-01', '1641796086.68088.zip', '2022-01-10 14:28:06', 0);
INSERT INTO `app1_books` VALUES (3, '流畅的Python', 'None', '“对于想要扩充知识的中级和高级Python程序员来说，这本书是充满了实用编程技巧的宝藏。”——Daniel Greenfeld和Audrey Roy Greenfeld，Two Scoops of Django作者', '2017-05-15', '1641796203.0678923.zip', '2022-01-10 14:30:04', 1);
INSERT INTO `app1_books` VALUES (4, 'Explore Flask', 'Javascript', 'Explore Flask is a book about best practices and patterns for developing web applications with Flask. The book was funded by 426 backers on Kickstarter in July 2013.', '2017-02-26', '1641796331.585363.zip', '2022-01-10 14:32:11', 0);
INSERT INTO `app1_books` VALUES (5, 'Python高级编程', 'None', '《Python高级编程》通过大量的实例，介绍了Python语言的最佳实践和敏捷开发方法，并涉及整个软件生命周期的高级主题，诸如持续集成、版本控制系统、包的发行和分发、开发模式、文档编写等。《Python高级编程》首先介绍如何设置最优的开发环境，然后以Python敏捷开发方法为线索，阐述如何将已被验证的面向对象原则应用到设计中。这些内容为开发人员和项目管理人员提供了整个软件工程中的许多高级概念以及专家级的建议，其中有些内容的意义甚至超出了Python语言本身。\r\n《Python高级编程》针对具备一定Python基础并希望通过在项目中应用最佳实践和新的开发技术来提升自己的Python开发人员。', '2010-01-01', '1641796432.7635562.zip', '2022-01-10 14:33:56', 0);
INSERT INTO `app1_books` VALUES (6, 'Python灰帽子', 'Python', '      《Python灰帽子》是由知名安全机构Immunity Inc的资深黑帽Justin Seitz主笔撰写的一本关于编程语言Python如何被广泛应用于黑客与逆向工程领域的书籍。老牌黑客，同时也是Immunity Inc的创始人兼首席技术执行官（CTO）Dave Aitel为这本书担任了技术编辑一职。书中绝大部分篇幅着眼于黑客技术领域中的两大经久不衰的话题：逆向工程与漏洞挖掘，并向读者呈现了几乎每个逆向工程师或安全研究人员在日常工作中所面临的各种场景，其中包括：如何设计与构建自己的调试工具，如何自动化实现烦琐的逆向分析任务，如何设计与构建自己的fuzzing工具，如何利用fuzzing 测试来找出存在于软件产品中的安全漏洞，一些小技巧诸如钩子与注入技术的应用，以及对一些主流Python安全工具如PyDbg、 Immunity Debugger、Sulley、IDAPython、PyEmu等的深入介绍。作者借助于如今黑客社区中备受青睐的编程语言 Python引领读者构建出精悍的脚本程序来一一应对上述这些问题。出现在书中的相当一部分Python代码实例借鉴或直接来源于一些优秀的开源安全项目，诸如Pedram Amini的Paimei，由此读者可以领略到安全研究者们是如何将黑客艺术与工程技术优雅融合来解决那些棘手问题的。', '2011-03-01', '1641796544.0368505.zip', '2022-01-10 14:35:45', 0);
INSERT INTO `app1_books` VALUES (7, 'The Flask Mega-Tutorial ', 'Python', '本系列是作者平时使用 Flask 微框架编写应用的经验之谈，这里是这一系列中所有已经发布的文章的索引。', '2018-05-01', '1641796643.0475228.zip', '2022-01-10 14:37:23', 0);
INSERT INTO `app1_books` VALUES (8, 'JavaScript权威指南', 'Javascript', '    《JavaScript权威指南(第5版)》全面介绍了JavaScript语言的核心，以及Web浏览器中实现的遗留和标准的DOM。它运用了一些复杂的例子，说明如何处理验证表单数据、使用cookie、创建可移植的DHTML动画等常见任务。《JavaScript权威指南(第5版)》还包括详细的参考手册，涵盖了JavaScript的核心API、遗留的客户端API和W3C标准DOM API，记述了这些API中的每一个JavaScript对象、方法、性质、构造函数、常量和事件处理程序', '2007-08-01', '1641866448.8781621.zip', '2022-01-11 10:00:49', 2);
INSERT INTO `app1_books` VALUES (9, 'React Native开发指南', 'Javascript', '      React Native开发指南通过丰富的示例和详细的讲解，介绍了React Native这款JavaScript框架。在React Native中利用现有的JavaScript和React知识，就可以开发和部署功能完备的、真正原生的移动应用，并同时支持iOS与Android平台。除了框架本身的概念讲解之外，本书还讨论了如何使用第三方库，以及如何编写自己的Java或Objective-C的React Native扩展。', '2017-01-01', '1641866543.5904787.zip', '2022-01-11 10:02:24', 0);
INSERT INTO `app1_books` VALUES (10, '关云长', 'None', '1122', '2022-01-12', '1641966162.068082.zip', '2022-01-12 13:42:42', 0);
INSERT INTO `app1_books` VALUES (11, '风吹麦浪', 'Linux', '撒打算', '2022-01-22', '1641997996.8420873.zip', '2022-01-12 22:33:16', 0);
INSERT INTO `app1_books` VALUES (12, 'GO 语言入门', 'Go', 'GO语言入门的必备书籍', '2022-01-12', '1641998859.577477.zip', '2022-01-12 22:47:39', 0);

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `group_id` int(0) NOT NULL,
  `permission_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(0) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 33 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

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
INSERT INTO `auth_permission` VALUES (25, 'Can add books', 7, 'add_books');
INSERT INTO `auth_permission` VALUES (26, 'Can change books', 7, 'change_books');
INSERT INTO `auth_permission` VALUES (27, 'Can delete books', 7, 'delete_books');
INSERT INTO `auth_permission` VALUES (28, 'Can view books', 7, 'view_books');
INSERT INTO `auth_permission` VALUES (29, 'Can add permission', 8, 'add_permission');
INSERT INTO `auth_permission` VALUES (30, 'Can change permission', 8, 'change_permission');
INSERT INTO `auth_permission` VALUES (31, 'Can delete permission', 8, 'delete_permission');
INSERT INTO `auth_permission` VALUES (32, 'Can view permission', 8, 'view_permission');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$260000$i9n5dMKbtfHH5AZv8bTqqP$1hRaaKh/mL6qIzKmaJ8NtBsZgEUlaHx//AObgPDPj2c=', '2022-01-25 11:39:14.799838', 1, 'heyi01', '何', '壹', '1300202481@qq.com', 1, 1, '2022-01-24 16:49:27.713911');
INSERT INTO `auth_user` VALUES (2, 'pbkdf2_sha256$260000$mQbpQd39AFIvJcxQfDyhjP$E8OXSJK+KRHo7kR5TC1MdKLQjJjStKB8ANxnmy7iO2s=', '2022-01-25 11:19:51.509047', 0, 'zhangfei01', '', '', '', 0, 1, '2022-01-24 17:26:07.855309');
INSERT INTO `auth_user` VALUES (3, 'pbkdf2_sha256$260000$sCnGIcdSkZhEkmfsPW7UPC$GqyUZcJHorZRw1qPh6T22Dh3IUzAAfCfAieyvyKvZ9o=', NULL, 0, 'zhangfei02', '', '', '', 0, 1, '2022-01-24 17:26:08.131571');
INSERT INTO `auth_user` VALUES (4, 'pbkdf2_sha256$260000$ZpuyCmFfVkIV1EG4qvbNUM$1UptDl9SWHoPx2fHYp8WhgLjemi9dzI1kt4DgwcJeBI=', NULL, 0, 'zhangfei03', '', '', '', 0, 1, '2022-01-24 17:26:08.386889');
INSERT INTO `auth_user` VALUES (5, 'pbkdf2_sha256$260000$Ko89hd0bhBrjg9gtX1QVhM$rlefJGqLaoFxUg0TbpJlTB67CLHD24eCOb6VRgJ4jho=', NULL, 0, 'zhangfei04', '', '', '', 0, 1, '2022-01-24 17:26:08.645237');
INSERT INTO `auth_user` VALUES (6, 'pbkdf2_sha256$260000$VhQtdjzztUd3m9jGXQeAnN$b5ncSsG+CS/6Gr1yA0YBx+aKwZxY9mPQJMAPIhC3i5E=', NULL, 0, 'zhangfei05', '', '', '', 0, 1, '2022-01-24 17:26:08.893572');
INSERT INTO `auth_user` VALUES (7, 'pbkdf2_sha256$260000$jhxHmvSm96W0rkIWtVGVYP$tkRvyXqbD+aMI7Xb8+pvqkvwy8T9NH6CC/o5omNx39c=', NULL, 0, 'zhangfei06', '', '', '', 0, 1, '2022-01-24 17:26:09.148853');
INSERT INTO `auth_user` VALUES (8, 'pbkdf2_sha256$260000$4GAufpL253ZRpPOJA5EqVu$BxK6zVLErT+8l1oEqu/hr0KRVhRfXGfMsB/GtwUR7Qk=', NULL, 0, 'zhangfei07', '', '', '', 0, 1, '2022-01-24 17:26:09.401178');
INSERT INTO `auth_user` VALUES (9, 'pbkdf2_sha256$260000$dDgfjMqFATvJ30gTyJBFNV$yUirDiEZPHaVVoC97BhXkYCh4KYfjZAkNmXOxAj6u9A=', NULL, 0, 'zhangfei08', '', '', '', 0, 1, '2022-01-24 17:26:09.652539');
INSERT INTO `auth_user` VALUES (10, 'pbkdf2_sha256$260000$I3fueBRKf3rNpJAfRMV2qY$a4eTrM1gWFhs2x364p6XFwwUCsxnRPV8JqrCJhoFFu4=', NULL, 0, 'zhangfei09', '', '', '', 0, 1, '2022-01-24 17:26:09.908821');
INSERT INTO `auth_user` VALUES (11, 'pbkdf2_sha256$260000$BlJLvZ2ybonuMKkl3PyEwW$nT12oh5UbPpYxbwXJimsdRFfepAHMVqJa5fDAJ1aSXE=', NULL, 0, 'zhangfei010', '', '', '', 0, 1, '2022-01-24 17:26:10.160149');
INSERT INTO `auth_user` VALUES (12, 'pbkdf2_sha256$260000$SawJAOwVsCRn9j6mKsQ8T1$arrvAE+p3OcwTfyabaVH0Efh/IiIFyWoTYPfoNE+kRU=', NULL, 0, 'zhangfei011', '', '', '', 0, 1, '2022-01-24 17:29:27.025493');
INSERT INTO `auth_user` VALUES (13, 'pbkdf2_sha256$260000$hlN1ODKXin6PZw1kR61Tyo$wndbC+59EBY56QhAlSzBvq3+tl3xquxwCVZfToVOr14=', NULL, 0, 'zhangfei021', '', '', '', 0, 1, '2022-01-24 17:29:27.616911');
INSERT INTO `auth_user` VALUES (14, 'pbkdf2_sha256$260000$CsW2qEFBWcVxlTgQs408OE$1FF+ytBqaBFsESjaYHU5w+14nPt5Zf5de0lxTRY1x4c=', NULL, 0, 'zhangfei031', '', '', '', 0, 1, '2022-01-24 17:29:27.897126');
INSERT INTO `auth_user` VALUES (15, 'pbkdf2_sha256$260000$1RDpXBRvKAeqhAZf0rlVnr$DlgZ7FdyBDC5SLfyiFg59g9SwP//cTQHbQzGIg4NGpI=', NULL, 0, 'zhangfei041', '', '', '', 0, 1, '2022-01-24 17:29:28.148489');
INSERT INTO `auth_user` VALUES (16, 'pbkdf2_sha256$260000$VlmtXyTY0icbgR31EQUWeZ$uo+Xz8xsFpOVuBdeqHvVg4dM9YRh5cCAQS126peBl50=', NULL, 0, 'zhangfei051', '', '', '', 0, 1, '2022-01-24 17:29:28.400814');
INSERT INTO `auth_user` VALUES (17, 'pbkdf2_sha256$260000$gZKz8V6POmItvjC2TepGB9$QJZfdoVXkrdUqhm+OReN8X2oQxjvBkAAE3v+uuN4CKw=', NULL, 0, 'zhangfei061', '', '', '', 0, 1, '2022-01-24 17:29:28.663105');
INSERT INTO `auth_user` VALUES (18, 'pbkdf2_sha256$260000$PJztDOipVF1iG9TrpUhFcG$6h7FhQNdm5kTZ2TfYi0reoGVWFh1Pff9vO6PNbbbBeU=', NULL, 0, 'zhangfei071', '', '', '', 0, 1, '2022-01-24 17:29:28.926375');
INSERT INTO `auth_user` VALUES (19, 'pbkdf2_sha256$260000$GatueW4zntO0rbdnA1M55X$wkDHORqfLrcU5e+uev9IWdN1xqG0dXsk/W8D2r6BzXY=', NULL, 0, 'zhangfei081', '', '', '', 0, 1, '2022-01-24 17:29:29.175708');
INSERT INTO `auth_user` VALUES (20, 'pbkdf2_sha256$260000$jIK9CPk40lhtqJHqddJrkK$VkqupeN3yUWf5p0F8OuwTYAeD4fehN/+9OZENjJp2n0=', NULL, 0, 'zhangfei091', '', '', '', 0, 1, '2022-01-24 17:29:29.430028');
INSERT INTO `auth_user` VALUES (21, 'pbkdf2_sha256$260000$hzqwYmG5pvuY4TXBIpAUf3$sFfQmANAplew7DSf2FkyKuVqzelLIY0yv9nOIkg3uF4=', NULL, 0, 'zhangfei0101', '', '', '', 0, 1, '2022-01-24 17:29:29.698311');
INSERT INTO `auth_user` VALUES (22, 'pbkdf2_sha256$260000$WTHp4sZCJxpdXSgGnUFiFU$BgvY/37S8J02bsVKALqC8j3C53uxcw9K8L2sXPRVuKI=', NULL, 0, 'admin01', '', '', '', 0, 1, '2022-01-25 23:06:38.942295');
INSERT INTO `auth_user` VALUES (23, 'pbkdf2_sha256$260000$BSBzJo087TmXDFqJcXwVmi$Jf5JctshPHB+cXpQvMaKBf8V1Vhj2FrzuFnWcfDYo4Q=', NULL, 0, 'admin02', '', '', '', 0, 1, '2022-01-25 23:06:39.245439');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `user_id` int(0) NOT NULL,
  `group_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `user_id` int(0) NOT NULL,
  `permission_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NULL,
  `object_id` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(0) NULL DEFAULT NULL,
  `user_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (7, 'app1', 'books');
INSERT INTO `django_content_type` VALUES (8, 'app1', 'permission');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `applied` datetime(6) NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2022-01-24 16:45:52.054098');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2022-01-24 16:45:53.220453');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2022-01-24 16:45:53.415929');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2022-01-24 16:45:53.431886');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2022-01-24 16:45:53.449839');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2022-01-24 16:45:53.598402');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2022-01-24 16:45:53.751115');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2022-01-24 16:45:53.932203');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2022-01-24 16:45:53.973044');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2022-01-24 16:45:54.120649');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2022-01-24 16:45:54.130661');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2022-01-24 16:45:54.170517');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2022-01-24 16:45:54.347094');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2022-01-24 16:45:54.501631');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2022-01-24 16:45:54.645282');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2022-01-24 16:45:54.690125');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2022-01-24 16:45:54.845266');
INSERT INTO `django_migrations` VALUES (18, 'sessions', '0001_initial', '2022-01-24 16:45:54.944003');
INSERT INTO `django_migrations` VALUES (19, 'app1', '0001_initial', '2022-01-24 16:48:00.231790');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `expire_date` datetime(6) NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('0wk926taowmh5e3208ghhwfd05ukd46f', '.eJxVjDsOwyAQBe9CHSFw-Cwu0-cMiIXFJrFAMnYV5e6JJTdu38y8DyvdL20qlY3butON-bBvs987rb4kNjLJLhuG-KZ6gPQKdWo8trqtBfmh8JN2_myJlsfpXg7m0Od_TZCVtWhc1CBdEBEwDSqSVmAiWcr3aEA7dMHqLKU2Ak0adHIigwBC9v0B8s89tg:1nCCfq:hJDrfZDKjOi9uJEWfdhPcs2cPPAbsK32MoFENo4Q-Ks', '2022-02-08 11:39:14.804824');

SET FOREIGN_KEY_CHECKS = 1;
