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

 Date: 17/07/2026 12:10:32
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
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户账号信息表（登录中心）' ROW_FORMAT = Dynamic;

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
-- View structure for v_student_course_score
-- ----------------------------
DROP VIEW IF EXISTS `v_student_course_score`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `v_student_course_score` AS select `student`.`autoID` AS `autoID`,`student_selected_course`.`studentID` AS `studentID`,`student`.`userID` AS `userID`,`student`.`classID` AS `classID`,`student`.`collegeID` AS `collegeID`,`student`.`name` AS `studentName`,`student`.`phoneNumber` AS `phoneNumber`,`student`.`age` AS `age`,`student`.`agenda` AS `agenda`,`student`.`isDelete` AS `isDelete`,`sys_classinfo`.`className` AS `className`,`student_selected_course`.`courseID` AS `courseID`,`student_selected_course`.`score` AS `score`,`course`.`courseName` AS `courseName`,`course`.`teacherID` AS `teacherID`,`teacher`.`name` AS `teacherName`,`teacher`.`phone` AS `phone`,`teacher`.`email` AS `email` from ((((`student` join `sys_classinfo` on((`student`.`classID` = `sys_classinfo`.`classID`))) join `student_selected_course` on((`student`.`studentID` = `student_selected_course`.`studentID`))) join `course` on((`student_selected_course`.`courseID` = `course`.`courseID`))) join `teacher` on((`course`.`teacherID` = `teacher`.`teacherID`)));

SET FOREIGN_KEY_CHECKS = 1;
