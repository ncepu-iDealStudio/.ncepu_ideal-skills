/*
 Navicat Premium Dump SQL

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80404 (8.4.4)
 Source Host           : localhost:3306
 Source Schema         : api_security_demo

 Target Server Type    : MySQL
 Target Server Version : 80404 (8.4.4)
 File Encoding         : 65001

 Date: 17/07/2026 13:28:11
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin`  (
  `auto_id` int NOT NULL AUTO_INCREMENT,
  `admin_id` bigint NULL DEFAULT NULL COMMENT '管理员用户ID',
  `user_id` varchar(22) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '对应的用户表ID',
  `department_id` bigint NULL DEFAULT NULL COMMENT '所属的部门)ID',
  `name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '姓名',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '电话',
  `office_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '办公地址',
  `is_delete` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  `add_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`auto_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES (1, 2022071815113247, NULL, NULL, '李四', NULL, 'H+nVS/65gACOy8AK8OqXLATPBOWQQ/S670ga2UXw1V/dkpslD4ILoeyxRFh833rF/BpfNFM5we2jW9yVYJdfTw==', NULL, 0, '2022-07-18 15:11:22');
INSERT INTO `admin` VALUES (2, 2022071815207869, NULL, NULL, '张伟', NULL, NULL, NULL, 0, '2022-07-18 15:20:04');
INSERT INTO `admin` VALUES (6, 2022091421286985, NULL, NULL, '张三', 'zhangsan@126.com', 'wNxPC7sPUCNL7+Cg/sGFJg==', NULL, 1, '2022-09-14 21:28:12');
INSERT INTO `admin` VALUES (7, 666, '2023052318326027', NULL, '管理员', 'admin@126.com', NULL, '北京昌平', 0, '2023-05-23 18:33:27');
INSERT INTO `admin` VALUES (8, 9155745665227132, NULL, NULL, 'Skill更', 'skill_admin@example.com', '13912345678', '行政楼B202', 1, '2026-07-16 17:41:04');
INSERT INTO `admin` VALUES (9, 9502225893265217, NULL, NULL, 'Skill更', 'skill_admin@example.com', '13912345678', '行政楼B202', 1, '2026-07-16 18:02:36');
INSERT INTO `admin` VALUES (10, 9653436978215620, NULL, NULL, 'Skill更', 'skill_admin@example.com', '13912345678', '行政楼B202', 1, '2026-07-16 18:22:13');
INSERT INTO `admin` VALUES (11, 9722289456419147, NULL, NULL, 'Skill更', 'skill_admin@example.com', '13912345678', '行政楼B202', 1, '2026-07-16 18:29:13');
INSERT INTO `admin` VALUES (12, 9726129710862053, NULL, NULL, 'Skill更', 'skill_admin@example.com', '13912345678', '行政楼B202', 1, '2026-07-16 18:30:00');
INSERT INTO `admin` VALUES (13, 9520917330735826, NULL, NULL, 'Skill更', 'skill_admin@example.com', '13912345678', '行政楼B202', 1, '2026-07-16 19:11:56');
INSERT INTO `admin` VALUES (14, 9624063959665171, NULL, NULL, 'Skill更', 'skill_admin@example.com', '13912345678', '行政楼B202', 1, '2026-07-16 19:15:45');
INSERT INTO `admin` VALUES (15, 9900923569448731, NULL, NULL, 'Skill更', 'skill_admin@example.com', '13912345678', '行政楼B202', 1, '2026-07-16 19:24:11');
INSERT INTO `admin` VALUES (16, 9757529023854457, NULL, NULL, 'Skill更', 'skill_admin@example.com', '13912345678', '行政楼B202', 1, '2026-07-17 10:51:06');
INSERT INTO `admin` VALUES (17, 9670145652688805, NULL, NULL, 'Skill更', 'skill_admin@example.com', '13912345678', '行政楼B202', 1, '2026-07-17 11:33:46');
INSERT INTO `admin` VALUES (18, 9503778709470420, NULL, NULL, 'Skill更', 'skill_admin@example.com', '13912345678', '行政楼B202', 1, '2026-07-17 11:44:03');

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course`  (
  `autoID` int NOT NULL AUTO_INCREMENT,
  `courseID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '课程编号',
  `courseName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '课程名称',
  `teacherID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '任课教师编号',
  `credit` float NULL DEFAULT NULL COMMENT '学分',
  `isDelete` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE,
  UNIQUE INDEX `uk_course_courseID`(`courseID` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 82 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '课程基本信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course
-- ----------------------------
INSERT INTO `course` VALUES (1, '1', 'python程序设计', '50501253', 3, 0, '2022-02-15 16:21:13');
INSERT INTO `course` VALUES (2, '00690270', 'C语言程序设计', '50500954', 3, 0, '2022-02-17 12:46:04');
INSERT INTO `course` VALUES (3, '00690160', '软件工程', '50501234', 3.5, 0, '2022-02-17 12:51:21');
INSERT INTO `course` VALUES (4, '12156541', '数据库原理', '50501239', 3, 0, '2022-04-06 11:19:09');
INSERT INTO `course` VALUES (22, '561464649', '测试课程修改接口', '50501239', 2.5, 0, '2022-04-07 15:09:45');
INSERT INTO `course` VALUES (26, '2023041314184106', '测试课程修改接口', '50501239', 2.5, 1, '2023-04-13 14:18:32');
INSERT INTO `course` VALUES (27, '2023041314377246', '测试课程添加接口', '50501239', 2, 0, '2023-04-13 14:37:53');
INSERT INTO `course` VALUES (28, '2023041315145278', '测试课程添加接口', '50501239', 2, 0, '2023-04-13 15:14:40');
INSERT INTO `course` VALUES (29, '2023041410342941', '测试课程添加接口', '50501239', 2, 0, '2023-04-14 10:34:32');
INSERT INTO `course` VALUES (30, '2023041410382380', '测试课程添加接口', '50501239', 2, 0, '2023-04-14 10:38:06');
INSERT INTO `course` VALUES (31, '2023041411012381', '测试课程添加接口', '50501239', 2, 0, '2023-04-14 11:01:58');
INSERT INTO `course` VALUES (32, '2023041411128025', '测试课程添加接口', '50501239', 2, 0, '2023-04-14 11:12:36');
INSERT INTO `course` VALUES (33, '2023041411178253', '测试课程添加接口', '50501239', 2, 0, '2023-04-14 11:17:20');
INSERT INTO `course` VALUES (34, '2023041411192689', '测试课程添加接口', '50501239', 2, 0, '2023-04-14 11:19:46');
INSERT INTO `course` VALUES (35, '2023041411203871', '测试课程添加接口', '50501239', 2, 0, '2023-04-14 11:20:30');
INSERT INTO `course` VALUES (36, '2023041411214916', '测试课程添加接口', '50501239', 2, 0, '2023-04-14 11:21:57');
INSERT INTO `course` VALUES (37, '2023041411229654', '测试课程添加接口', '50501239', 2, 0, '2023-04-14 11:22:46');
INSERT INTO `course` VALUES (38, '2023041411259275', '测试课程添加接口', '50501239', 2, 0, '2023-04-14 11:25:35');
INSERT INTO `course` VALUES (39, '2023041411294207', '测试课程添加接口', '50501239', 2, 0, '2023-04-14 11:29:29');
INSERT INTO `course` VALUES (40, '2023041411302186', '测试课程添加接口', '50501239', 2, 0, '2023-04-14 11:30:54');
INSERT INTO `course` VALUES (41, '2023041411528245', '测试课程添加接口', '50501239', 2, 0, '2023-04-14 11:52:37');
INSERT INTO `course` VALUES (42, '2023041417113427', '测试课程添加接口', '50501239', 2, 0, '2023-04-14 17:11:38');
INSERT INTO `course` VALUES (43, '2023041417139703', '测试课程添加接口', '50501239', 2, 0, '2023-04-14 17:13:53');
INSERT INTO `course` VALUES (44, '2023041519326382', '测试课程添加接口', '50501239', 2, 0, '2023-04-15 19:32:41');
INSERT INTO `course` VALUES (45, '2023041520245036', '测试课程添加接口', '50501239', 2, 0, '2023-04-15 20:24:47');
INSERT INTO `course` VALUES (46, '2023041520272138', '测试课程添加接口', '50501239', 2, 0, '2023-04-15 20:27:52');
INSERT INTO `course` VALUES (47, '2023041520325072', '测试课程添加接口', '50501239', 2, 0, '2023-04-15 20:32:19');
INSERT INTO `course` VALUES (48, '2023041520375893', '测试课程添加接口', '50501239', 2, 0, '2023-04-15 20:37:08');
INSERT INTO `course` VALUES (49, '2023041520384697', '测试课程添加接口', '50501239', 2, 0, '2023-04-15 20:38:10');
INSERT INTO `course` VALUES (50, '2023042619018371', '测试课程添加接口', '50501239', 2, 0, '2023-04-26 19:01:51');
INSERT INTO `course` VALUES (51, '2023050320428209', '测试课程添加接口', '50501239', 2, 0, '2023-05-03 20:42:26');
INSERT INTO `course` VALUES (52, '2023050320487081', '测试课程添加接口', '50501239', 2, 0, '2023-05-03 20:48:50');
INSERT INTO `course` VALUES (53, '2023050320498167', '测试课程添加接口', '50501239', 2, 0, '2023-05-03 20:49:17');
INSERT INTO `course` VALUES (54, '2023060515554068', NULL, NULL, NULL, 0, '2023-06-05 15:55:55');
INSERT INTO `course` VALUES (55, '2023060515571845', 'python程序设计', NULL, NULL, 0, '2023-06-05 15:57:04');
INSERT INTO `course` VALUES (56, '2023060515580583', 'python程序设计11', '123456', NULL, 0, '2023-06-05 15:58:25');
INSERT INTO `course` VALUES (57, '2023060515598954', 'python程序设计', NULL, NULL, 0, '2023-06-05 15:59:55');
INSERT INTO `course` VALUES (58, '2023060516320187', '1111', '111111', 11, 0, '2023-06-05 16:32:41');
INSERT INTO `course` VALUES (59, '2023060516324015', 'C语言程序设计002', '50500954', 3, 0, '2023-06-05 16:32:41');
INSERT INTO `course` VALUES (60, '2023060516325492', 'C语言程序设计003', '50500954', 3, 0, '2023-06-05 16:32:41');
INSERT INTO `course` VALUES (61, '2023060516598674', NULL, NULL, NULL, 0, '2023-06-05 16:59:06');
INSERT INTO `course` VALUES (63, '2023060614556321', '软件测试', '501416186', 2.5, 0, '2023-06-06 14:55:42');
INSERT INTO `course` VALUES (64, 'TEST4E34E4C93A', '集成测试课程', '501416186', 3, 0, '2026-07-15 21:23:48');
INSERT INTO `course` VALUES (65, 'TEST73C746FA9E', '重名课程', NULL, NULL, 0, '2026-07-15 21:23:48');
INSERT INTO `course` VALUES (66, 'TEST6E904E49FB', '集成更新课程', '501416186', 4, 1, '2026-07-15 21:24:11');
INSERT INTO `course` VALUES (67, 'TESTFF880C18A1', '重名课程', NULL, NULL, 0, '2026-07-15 21:24:11');
INSERT INTO `course` VALUES (68, 'TEST491452069E', '集成更新课程', '501416186', 4, 1, '2026-07-15 21:24:23');
INSERT INTO `course` VALUES (69, 'TEST650EDACA79', '重名课程', NULL, NULL, 0, '2026-07-15 21:24:23');
INSERT INTO `course` VALUES (70, 'TEST2FD6463AE7', '集成更新课程', '501416186', 4, 1, '2026-07-16 18:22:13');
INSERT INTO `course` VALUES (71, 'TEST66E133695C', '重名课程', NULL, NULL, 0, '2026-07-16 18:22:13');
INSERT INTO `course` VALUES (72, 'TEST6186FFECE7', '集成更新课程', '501416186', 4, 1, '2026-07-16 18:29:13');
INSERT INTO `course` VALUES (73, 'TESTA1356E72C7', '重名课程', NULL, NULL, 0, '2026-07-16 18:29:13');
INSERT INTO `course` VALUES (74, 'TEST15814ABF26', '集成更新课程', '501416186', 4, 1, '2026-07-16 18:30:02');
INSERT INTO `course` VALUES (75, 'TESTBC822CE071', '重名课程', NULL, NULL, 0, '2026-07-16 18:30:02');
INSERT INTO `course` VALUES (76, 'TEST4E08D48462', '集成更新课程', '501416186', 4, 1, '2026-07-16 19:11:58');
INSERT INTO `course` VALUES (77, 'TEST8882801E0A', '重名课程', NULL, NULL, 0, '2026-07-16 19:11:58');
INSERT INTO `course` VALUES (78, 'TESTEE5703BA85', '集成更新课程', '501416186', 4, 1, '2026-07-16 19:15:48');
INSERT INTO `course` VALUES (79, 'TEST808D9C93B5', '重名课程', NULL, NULL, 0, '2026-07-16 19:15:48');
INSERT INTO `course` VALUES (80, 'TEST93E8834584', '集成更新课程', '501416186', 4, 1, '2026-07-16 19:24:11');
INSERT INTO `course` VALUES (81, 'TESTC3F4063C93', '重名课程', NULL, NULL, 0, '2026-07-16 19:24:11');

-- ----------------------------
-- Table structure for course_arrangement
-- ----------------------------
DROP TABLE IF EXISTS `course_arrangement`;
CREATE TABLE `course_arrangement`  (
  `autoID` int NOT NULL AUTO_INCREMENT COMMENT '自增序号',
  `courseID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '课程编号',
  `termID` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '学期ID',
  `classTime` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '上课时间：1-2；3-4；5-6；7-8；',
  `count` int NULL DEFAULT NULL COMMENT '课程容量-可选人数',
  `isDelete` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '课程安排表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course_arrangement
-- ----------------------------

-- ----------------------------
-- Table structure for sso_user
-- ----------------------------
DROP TABLE IF EXISTS `sso_user`;
CREATE TABLE `sso_user`  (
  `autoID` bigint NOT NULL AUTO_INCREMENT COMMENT '物理主键，自增',
  `userID` varchar(22) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户业务ID，被业务表 userID 引用',
  `account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '登录账号（手机号/邮箱/用户名）',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码哈希（新数据请用 bcrypt）',
  `userType` tinyint(1) NULL DEFAULT NULL COMMENT '账号类型：1学生 2教师 3管理员',
  `status` tinyint(1) NOT NULL DEFAULT 1 COMMENT '账号状态：1-可用; 0--锁定',
  `addTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`autoID`) USING BTREE,
  UNIQUE INDEX `uk_sso_user_userID`(`userID` ASC) USING BTREE,
  UNIQUE INDEX `uk_sso_user_account`(`account` ASC) USING BTREE,
  INDEX `idx_sso_user_userType`(`userType` ASC) USING BTREE,
  INDEX `idx_sso_user_status`(`status` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户账号信息表（登录中心）' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sso_user
-- ----------------------------
INSERT INTO `sso_user` VALUES (1, '202607151958175405', '13522673569', '$2b$12$2k62odO9j/7AA8sMFdH9fuDQNnq.N8jr6gylAD0Lr00o7nZiUhnlq', 1, 1, '2026-07-15 19:58:17');
INSERT INTO `sso_user` VALUES (2, '202607152046489526', 'auth_d7c8c6cb', '$2b$12$X4pvWJc8rJObpwjnmFapPOBrBcyFuF0Xkq/wZtbciBnS.OgqgkMRa', 1, 1, '2026-07-15 20:46:49');
INSERT INTO `sso_user` VALUES (3, '202607152046491757', 'chgpwd_2a0e6c10', '$2b$12$GKd/zcJfUR8Lp0jqcIsCBu.3zooXnw/jlb1m84Ov9ZhRNNFRylmzm', 1, 1, '2026-07-15 20:46:49');
INSERT INTO `sso_user` VALUES (4, '202607152046503104', 'badpwd_ae6608a0', '$2b$12$v719NwhLkjTb.g7J4cpB4.k2IJloEJT0k4awFtWnirtIX8O/Z4YCO', 1, 1, '2026-07-15 20:46:50');
INSERT INTO `sso_user` VALUES (6, '202607161729531960', 'auth_99e20415', '$2b$12$jD/72d7Cwum2osuN2PPG2OelomY0Q4q.F.GscgPGdqXuWnTQA8dHS', 1, 1, '2026-07-16 17:29:54');
INSERT INTO `sso_user` VALUES (7, '202607161729540519', 'chgpwd_5f507e67', '$2b$12$Jw5oBzwI4GYQfFFXe3LTvOA/wmz26YZjJgX9K0Un6pCcSf0XNcR3S', 1, 1, '2026-07-16 17:29:54');
INSERT INTO `sso_user` VALUES (8, '202607161729552190', 'badpwd_6be45f68', '$2b$12$pHToMe6OdoabYXwEjM.At.OGGquylYgJ.E2EvK9h02i7kcxre.KQK', 1, 1, '2026-07-16 17:29:55');
INSERT INTO `sso_user` VALUES (9, '202607161830004858', 'auth_3398124c', '$2b$12$NDqXTxNXPH7BAQOnIGw72.fXjZNx8WlwcHHYoLesWNL2c5UNKDxUe', 1, 1, '2026-07-16 18:30:00');
INSERT INTO `sso_user` VALUES (10, '202607161830002025', 'chgpwd_4b14cfb0', '$2b$12$zSqDJQvHcDoxEUZMJGFK7uaYjMWy/M642SA7YB0uXT96tj5w9Rkhm', 1, 1, '2026-07-16 18:30:01');
INSERT INTO `sso_user` VALUES (11, '202607161830024826', 'badpwd_aa9bca2d', '$2b$12$yZ.b171vrJwBehHHmhGl5eOnVnTHuQJQZakUiPr/no/aFbJ0ppth.', 1, 1, '2026-07-16 18:30:02');
INSERT INTO `sso_user` VALUES (13, '202607161911564770', 'auth_446495c5', '$2b$12$3KQtcyUY16.CxTf3iAdWW.4JAbqbxYtefnAB7BEmeQsh4bK2MFNie', 1, 1, '2026-07-16 19:11:56');
INSERT INTO `sso_user` VALUES (14, '202607161911565811', 'chgpwd_498f734e', '$2b$12$SLAHQyeCjtyS2TWffI7y9OGr2HOtSYiUCsFDE5BecoeJE4mz148mi', 1, 1, '2026-07-16 19:11:56');
INSERT INTO `sso_user` VALUES (15, '202607161911573863', 'badpwd_8b6d9727', '$2b$12$lpqxgGPPCCBCMAp1k.2RCenl2oGB4BhX0X4IslHdQJEhg/QALrgly', 1, 1, '2026-07-16 19:11:58');
INSERT INTO `sso_user` VALUES (17, '202607161915463214', 'auth_9b34cf5c', '$2b$12$lUSMS/WICkmvEdgFxb0qduucX8q9vP9lBMdLgFOGLnuWQRm5KrL/q', 1, 1, '2026-07-16 19:15:46');
INSERT INTO `sso_user` VALUES (18, '202607161915461507', 'chgpwd_7a24a4ef', '$2b$12$e3hdobTUC8USWJP444IL2ur3hHZnpuTX003OCWJxuF6LApGC/bPZW', 1, 1, '2026-07-16 19:15:46');
INSERT INTO `sso_user` VALUES (19, '202607161915474307', 'badpwd_e9558164', '$2b$12$IM6wFMyVZgi3A4bRjsxzIu0nuYVnARdGHdb7xSKQzYwlZYyhSMYZG', 1, 1, '2026-07-16 19:15:48');

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `autoID` int NOT NULL AUTO_INCREMENT COMMENT '自增字段',
  `studentID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '学号，业务主键',
  `userID` varchar(22) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '关联 sso_user.userID（逻辑外键）',
  `classID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '所属班级ID',
  `collegeID` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '所属学院',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '学生姓名',
  `phoneNumber` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '手机号码',
  `age` int NULL DEFAULT NULL COMMENT '年龄',
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '性别：男/女/其他',
  `isDelete` tinyint(1) NOT NULL DEFAULT 0 COMMENT '软删除：0未删 1已删',
  `addTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`autoID`) USING BTREE,
  UNIQUE INDEX `uk_student_studentID`(`studentID` ASC) USING BTREE,
  INDEX `idx_student_userID`(`userID` ASC) USING BTREE,
  INDEX `idx_student_classID`(`classID` ASC) USING BTREE,
  INDEX `idx_student_collegeID`(`collegeID` ASC) USING BTREE,
  INDEX `idx_student_isDelete_name`(`isDelete` ASC, `name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 148 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '学生基本信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES (3, '23462327', '2022022813551869', '200002', '527', '翠花', NULL, 20, '女', 0, '2023-04-14 10:27:16');
INSERT INTO `student` VALUES (62, '2022041314492801', '666', '1', '1', '麦当', NULL, 18, '男', 0, '2023-04-14 10:27:16');
INSERT INTO `student` VALUES (64, '2022041314551943', '7777', NULL, NULL, '笛亚', NULL, NULL, '女', 0, '2023-04-14 10:27:17');
INSERT INTO `student` VALUES (65, '2022041314557284', '8888', NULL, NULL, '咕咚', NULL, NULL, '男', 0, '2023-04-14 10:27:18');
INSERT INTO `student` VALUES (95, '1', '123', '1', '1', '王五', '7A78C25C4AE963FEB06C3E07BDB8E7FE', 18, '男', 0, '2023-04-14 10:27:19');
INSERT INTO `student` VALUES (97, '2022071914401893', '2022040714482918', '2000401', '527', '王老五', '3VjpCuDvsUv8h+prm6hsiA==', 21, NULL, 0, '2023-04-14 10:27:20');
INSERT INTO `student` VALUES (98, '2022071914431785', '202204071448291', '2000400', '527', '白晶晶', 'w0RbCMnQxDmy66G4dJy/UA==', 21, '女', 0, '2023-04-14 10:27:21');
INSERT INTO `student` VALUES (99, '2424', '27724', '72', '742', '张', '1235413215313', 50, '男', 0, '2023-05-23 18:05:21');
INSERT INTO `student` VALUES (100, '123456', '20230523', '1', '527', '张三', '10085', 20, '男', 0, '2023-05-23 19:45:02');
INSERT INTO `student` VALUES (101, '654321', '20230524', '1', '527', '李四', '188', 19, '男', 0, '2023-05-23 18:06:25');
INSERT INTO `student` VALUES (127, '2025888', NULL, '1', '527', '测试学生1', NULL, 19, '男', 0, '2025-11-19 13:31:21');
INSERT INTO `student` VALUES (128, 'TESTD15E41216A', NULL, NULL, NULL, '集成更新', NULL, 20, '男', 1, '2026-07-15 16:34:13');
INSERT INTO `student` VALUES (129, 'TESTE06B15FBAF', NULL, NULL, NULL, '重名', NULL, NULL, NULL, 0, '2026-07-15 16:34:13');
INSERT INTO `student` VALUES (130, 'TEST399C35954D', NULL, NULL, NULL, '集成更新', NULL, 20, '男', 1, '2026-07-15 16:42:19');
INSERT INTO `student` VALUES (131, 'TESTA9DFCD9D54', NULL, NULL, NULL, '重名', NULL, NULL, NULL, 0, '2026-07-15 16:42:19');
INSERT INTO `student` VALUES (132, 'TEST9D11774D36', NULL, NULL, NULL, '集成更新', NULL, 20, '男', 1, '2026-07-15 16:55:10');
INSERT INTO `student` VALUES (133, 'TEST3A83F5C9C5', NULL, NULL, NULL, '重名', NULL, NULL, NULL, 0, '2026-07-15 16:55:10');
INSERT INTO `student` VALUES (134, 'TEST3EC25E404D', NULL, NULL, NULL, '集成更新', NULL, 20, '男', 1, '2026-07-15 20:46:51');
INSERT INTO `student` VALUES (135, 'TEST504724BA1C', NULL, NULL, NULL, '重名', NULL, NULL, NULL, 0, '2026-07-15 20:46:51');
INSERT INTO `student` VALUES (136, 'TEST19434B88E3', NULL, NULL, NULL, '集成更新', NULL, 20, '男', 1, '2026-07-16 18:22:13');
INSERT INTO `student` VALUES (137, 'TEST51641D73B6', NULL, NULL, NULL, '重名', NULL, NULL, NULL, 0, '2026-07-16 18:22:13');
INSERT INTO `student` VALUES (138, 'TEST265B60EAD6', NULL, NULL, NULL, '集成更新', NULL, 20, '男', 1, '2026-07-16 18:29:13');
INSERT INTO `student` VALUES (139, 'TEST2C4D2E10B3', NULL, NULL, NULL, '重名', NULL, NULL, NULL, 0, '2026-07-16 18:29:13');
INSERT INTO `student` VALUES (140, 'TESTE2EB576FDA', NULL, NULL, NULL, '集成更新', NULL, 20, '男', 1, '2026-07-16 18:30:02');
INSERT INTO `student` VALUES (141, 'TEST37E1B28F0E', NULL, NULL, NULL, '重名', NULL, NULL, NULL, 0, '2026-07-16 18:30:03');
INSERT INTO `student` VALUES (142, 'TESTF34660DDBD', NULL, NULL, NULL, '集成更新', NULL, 20, '男', 1, '2026-07-16 19:11:58');
INSERT INTO `student` VALUES (143, 'TESTC94E7CD69B', NULL, NULL, NULL, '重名', NULL, NULL, NULL, 0, '2026-07-16 19:11:58');
INSERT INTO `student` VALUES (144, 'TESTFF75D2E3E5', NULL, NULL, NULL, '集成更新', NULL, 20, '男', 1, '2026-07-16 19:15:48');
INSERT INTO `student` VALUES (145, 'TEST4E0AF67D66', NULL, NULL, NULL, '重名', NULL, NULL, NULL, 0, '2026-07-16 19:15:48');
INSERT INTO `student` VALUES (146, 'TEST4762BB5DC2', NULL, NULL, NULL, '集成更新', NULL, 20, '男', 1, '2026-07-16 19:24:11');
INSERT INTO `student` VALUES (147, 'TEST4BD52CD1F8', NULL, NULL, NULL, '重名', NULL, NULL, NULL, 0, '2026-07-16 19:24:11');

-- ----------------------------
-- Table structure for student_selected_course
-- ----------------------------
DROP TABLE IF EXISTS `student_selected_course`;
CREATE TABLE `student_selected_course`  (
  `autoID` int NOT NULL AUTO_INCREMENT COMMENT '自增序号字段',
  `studentID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '学号',
  `courseID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '课程编号',
  `score` int NULL DEFAULT NULL COMMENT '成绩',
  `isDelete` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '学生选课情况表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student_selected_course
-- ----------------------------
INSERT INTO `student_selected_course` VALUES (1, '120201080431', '00690270', 74, 0, '2022-02-17 17:52:44');
INSERT INTO `student_selected_course` VALUES (2, '120201080431', '1', 65, 0, '2022-02-17 17:52:25');
INSERT INTO `student_selected_course` VALUES (3, '23461111', '00690270', 76, 0, '2022-02-17 17:51:39');
INSERT INTO `student_selected_course` VALUES (4, '23461111', '1', 75, 0, '2022-02-17 14:40:07');
INSERT INTO `student_selected_course` VALUES (5, '23462327', '00690270', NULL, 0, '2023-05-03 20:49:17');
INSERT INTO `student_selected_course` VALUES (6, '23462327', '1', 80, 0, '2022-02-17 10:33:41');
INSERT INTO `student_selected_course` VALUES (7, '23462328', '1', 88, 0, '2022-02-17 14:42:44');

-- ----------------------------
-- Table structure for sys_class
-- ----------------------------
DROP TABLE IF EXISTS `sys_class`;
CREATE TABLE `sys_class`  (
  `classID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '班级ID--业务主键',
  `collegeID` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '所属学院',
  `className` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '班级名称',
  `isDelete` tinyint(1) NULL DEFAULT 0 COMMENT '是否被删除  0 - 未删除  1 - 已删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`classID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '班级信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_class
-- ----------------------------

-- ----------------------------
-- Table structure for sys_classinfo
-- ----------------------------
DROP TABLE IF EXISTS `sys_classinfo`;
CREATE TABLE `sys_classinfo`  (
  `autoID` int NOT NULL AUTO_INCREMENT,
  `classID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '班级ID',
  `collegeID` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '所属学院',
  `className` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '班级名称',
  `isDeleted` tinyint(1) NULL DEFAULT 0 COMMENT '是否被删除  0 - 未删除  1 - 已删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '班级信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_classinfo
-- ----------------------------
INSERT INTO `sys_classinfo` VALUES (1, '200001', '527', '软件2001班', 0, '2022-02-17 13:31:02');
INSERT INTO `sys_classinfo` VALUES (2, '200002', '527', '软件2002班', 0, '2022-02-17 13:31:02');
INSERT INTO `sys_classinfo` VALUES (3, '200011', '527', '计算2001班', 0, '2022-02-17 13:31:02');
INSERT INTO `sys_classinfo` VALUES (4, '200012', '527', '计算2002班', 0, '2022-02-17 13:31:02');
INSERT INTO `sys_classinfo` VALUES (5, '2000301', '527', '信安2001班', 0, '2022-02-17 13:31:02');
INSERT INTO `sys_classinfo` VALUES (6, '2000401', '527', '物联2001班', 0, '2022-02-17 13:31:02');

-- ----------------------------
-- Table structure for sys_college
-- ----------------------------
DROP TABLE IF EXISTS `sys_college`;
CREATE TABLE `sys_college`  (
  `collegeID` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '学院ID编码--业务主键',
  `collegeName` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '学院名称',
  `isDelete` tinyint(1) NULL DEFAULT 0 COMMENT '是否删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`collegeID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '学院表，记录学院的基本信息' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_college
-- ----------------------------

-- ----------------------------
-- Table structure for sys_department
-- ----------------------------
DROP TABLE IF EXISTS `sys_department`;
CREATE TABLE `sys_department`  (
  `departmentID` bigint NOT NULL COMMENT '部门ID：学院下属的教研室(研究所)ID',
  `parentDepartmentID` bigint NOT NULL DEFAULT 0 COMMENT '父级部门ID',
  `collegeID` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '学院ID编码--业务主键',
  `departmentName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '教研室(研究所)名称',
  `departmentType` tinyint(1) NULL DEFAULT 1 COMMENT '部门类型:\r\n1--教研室；\r\n2-研究所；\r\n3 实验中心；\r\n4-办公室；\r\n5-其他',
  `isDelete` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否被删除   0 -未被删除  1 - 被删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`departmentID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '教研室与研究所部门信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_department
-- ----------------------------

-- ----------------------------
-- Table structure for teacher
-- ----------------------------
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher`  (
  `autoID` int NOT NULL AUTO_INCREMENT,
  `teacherID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '教工号',
  `userID` varchar(22) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '对应的用户表ID',
  `departmentID` bigint NULL DEFAULT NULL COMMENT '所属的教研室(研究所)ID',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '姓名',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '电话',
  `officeAddress` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '办公地址',
  `isDelete` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否删除: 0--有效；1--已删除',
  `addTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  `updateTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`autoID`) USING BTREE,
  UNIQUE INDEX `uk_teacher_teacherID`(`teacherID` ASC) USING BTREE,
  INDEX `departmentID`(`departmentID` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 30 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teacher
-- ----------------------------
INSERT INTO `teacher` VALUES (1, '50501253', '2022022814577014', 123, '刘老师', 'wanglaowu@ncepu.edu.cm', '17666668888', '主楼E-111111', 0, '2022-02-17 12:57:10', '2026-07-15 21:02:07');
INSERT INTO `teacher` VALUES (2, '50500954', '2022022817570694', 456, '张老师', 'zhang@163.com', '13612344321', '主楼E-708办公室	0', 0, '2022-02-17 12:57:38', '2026-07-15 21:02:07');
INSERT INTO `teacher` VALUES (4, '50501239', '2022022817542497', 456, '李老师', 'li@163.com', '12344548921', '主楼E-708办公室	0', 0, '2022-04-06 11:21:08', '2026-07-15 21:02:07');
INSERT INTO `teacher` VALUES (7, '501416186', '2023060614273016', 0, 'Tom', 'tom@ncepu.edu.cn', '13512345678', '主楼F-233', 0, '2023-02-16 22:02:01', '2026-07-15 21:02:07');
INSERT INTO `teacher` VALUES (8, 'TESTC971E65DE3', '202607151958175405', NULL, '集成更新', 'update@example.com', '13800138000', NULL, 1, '2026-07-15 20:46:36', '2026-07-15 21:02:07');
INSERT INTO `teacher` VALUES (9, 'TEST24BF14064B', '202607151958175405', NULL, '重名', NULL, NULL, NULL, 0, '2026-07-15 20:46:36', '2026-07-15 21:02:07');
INSERT INTO `teacher` VALUES (10, 'TESTB9F24D616A', '202607151958175405', NULL, '集成更新', 'update@example.com', '13800138000', NULL, 1, '2026-07-15 20:46:51', '2026-07-15 21:02:07');
INSERT INTO `teacher` VALUES (11, 'TEST1EC8575CDA', '202607151958175405', NULL, '重名', NULL, NULL, NULL, 0, '2026-07-15 20:46:51', '2026-07-15 21:02:07');
INSERT INTO `teacher` VALUES (12, 'TEST15482ADFA0', '202607151958175405', NULL, '集成更新', 'update@example.com', '13800138000', NULL, 1, '2026-07-15 20:52:04', '2026-07-15 21:02:07');
INSERT INTO `teacher` VALUES (13, 'TEST07F9BAE329', '202607151958175405', NULL, '重名', NULL, NULL, NULL, 0, '2026-07-15 20:52:05', '2026-07-15 21:02:07');
INSERT INTO `teacher` VALUES (14, 'TEST2CD1783796', '202607151958175405', NULL, '集成更新', 'update@example.com', '13800138000', NULL, 1, '2026-07-15 21:09:22', '2026-07-15 21:09:22');
INSERT INTO `teacher` VALUES (15, 'TEST17957C48CF', '202607151958175405', NULL, '重名', NULL, NULL, NULL, 0, '2026-07-15 21:09:22', '2026-07-15 21:09:22');
INSERT INTO `teacher` VALUES (16, 'TEST3FC10F4AF0', '202607151958175405', NULL, '集成更新', 'update@example.com', '13800138000', NULL, 1, '2026-07-15 21:24:23', '2026-07-15 21:24:23');
INSERT INTO `teacher` VALUES (17, 'TEST1833E9906A', '202607151958175405', NULL, '重名', NULL, NULL, NULL, 0, '2026-07-15 21:24:23', '2026-07-15 21:24:23');
INSERT INTO `teacher` VALUES (18, 'TESTE38ED20E4F', '202607151958175405', NULL, '集成更新', 'update@example.com', '13800138000', NULL, 1, '2026-07-16 18:22:13', '2026-07-16 18:22:13');
INSERT INTO `teacher` VALUES (19, 'TEST0A915C21F1', '202607151958175405', NULL, '重名', NULL, NULL, NULL, 0, '2026-07-16 18:22:13', '2026-07-16 18:22:13');
INSERT INTO `teacher` VALUES (20, 'TEST16EBA1AC08', '202607151958175405', NULL, '集成更新', 'update@example.com', '13800138000', NULL, 1, '2026-07-16 18:29:13', '2026-07-16 18:29:13');
INSERT INTO `teacher` VALUES (21, 'TEST12FDB883E6', '202607151958175405', NULL, '重名', NULL, NULL, NULL, 0, '2026-07-16 18:29:13', '2026-07-16 18:29:13');
INSERT INTO `teacher` VALUES (22, 'TESTB632CEF0D9', '202607151958175405', NULL, '集成更新', 'update@example.com', '13800138000', NULL, 1, '2026-07-16 18:30:03', '2026-07-16 18:30:03');
INSERT INTO `teacher` VALUES (23, 'TESTAA4EF32BAC', '202607151958175405', NULL, '重名', NULL, NULL, NULL, 0, '2026-07-16 18:30:03', '2026-07-16 18:30:03');
INSERT INTO `teacher` VALUES (24, 'TESTCAD3FC7B7B', '202607151958175405', NULL, '集成更新', 'update@example.com', '13800138000', NULL, 1, '2026-07-16 19:11:58', '2026-07-16 19:11:58');
INSERT INTO `teacher` VALUES (25, 'TEST2BEE1B599C', '202607151958175405', NULL, '重名', NULL, NULL, NULL, 0, '2026-07-16 19:11:58', '2026-07-16 19:11:58');
INSERT INTO `teacher` VALUES (26, 'TEST21F6782659', '202607151958175405', NULL, '集成更新', 'update@example.com', '13800138000', NULL, 1, '2026-07-16 19:15:48', '2026-07-16 19:15:48');
INSERT INTO `teacher` VALUES (27, 'TEST504350DBA1', '202607151958175405', NULL, '重名', NULL, NULL, NULL, 0, '2026-07-16 19:15:48', '2026-07-16 19:15:48');
INSERT INTO `teacher` VALUES (28, 'TEST2D944FDA31', '202607151958175405', NULL, '集成更新', 'update@example.com', '13800138000', NULL, 1, '2026-07-16 19:24:11', '2026-07-16 19:24:11');
INSERT INTO `teacher` VALUES (29, 'TESTD90D3A75A4', '202607151958175405', NULL, '重名', NULL, NULL, NULL, 0, '2026-07-16 19:24:11', '2026-07-16 19:24:11');

-- ----------------------------
-- View structure for v_student_course_score
-- ----------------------------
DROP VIEW IF EXISTS `v_student_course_score`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `v_student_course_score` AS select `student`.`autoID` AS `autoID`,`student_selected_course`.`studentID` AS `studentID`,`student`.`userID` AS `userID`,`student`.`classID` AS `classID`,`student`.`collegeID` AS `collegeID`,`student`.`name` AS `studentName`,`student`.`phoneNumber` AS `phoneNumber`,`student`.`age` AS `age`,`student`.`agenda` AS `agenda`,`student`.`isDelete` AS `isDelete`,`sys_classinfo`.`className` AS `className`,`student_selected_course`.`courseID` AS `courseID`,`student_selected_course`.`score` AS `score`,`course`.`courseName` AS `courseName`,`course`.`teacherID` AS `teacherID`,`teacher`.`name` AS `teacherName`,`teacher`.`phone` AS `phone`,`teacher`.`email` AS `email` from ((((`student` join `sys_classinfo` on((`student`.`classID` = `sys_classinfo`.`classID`))) join `student_selected_course` on((`student`.`studentID` = `student_selected_course`.`studentID`))) join `course` on((`student_selected_course`.`courseID` = `course`.`courseID`))) join `teacher` on((`course`.`teacherID` = `teacher`.`teacherID`)));

SET FOREIGN_KEY_CHECKS = 1;
