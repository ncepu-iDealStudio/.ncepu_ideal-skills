/*
 Navicat Premium Dump SQL

 Source Server         : 8.140.241.248
 Source Server Type    : MySQL
 Source Server Version : 80027 (8.0.27)
 Source Host           : 8.140.241.248:13306
 Source Schema         : study_flask_api

 Target Server Type    : MySQL
 Target Server Version : 80027 (8.0.27)
 File Encoding         : 65001

 Date: 11/05/2026 10:22:11
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `auto_id` int NOT NULL AUTO_INCREMENT,
  `admin_id` bigint DEFAULT NULL COMMENT '管理员用户ID',
  `user_id` varchar(22) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '对应的用户表ID',
  `department_id` bigint DEFAULT NULL COMMENT '所属的部门)ID',
  `name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '姓名',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '电话',
  `office_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '办公地址',
  `is_delete` tinyint(1) DEFAULT '0' COMMENT '是否删除',
  `add_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`auto_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course` (
  `autoID` int NOT NULL AUTO_INCREMENT,
  `courseID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '课程编号',
  `courseName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '课程名称',
  `teacherID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '任课教师编号',
  `credit` float DEFAULT NULL COMMENT '学分',
  `isDelete` tinyint(1) DEFAULT '0' COMMENT '是否删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='课程基本信息表';

-- ----------------------------
-- Table structure for course_arrangement
-- ----------------------------
DROP TABLE IF EXISTS `course_arrangement`;
CREATE TABLE `course_arrangement` (
  `autoID` int NOT NULL AUTO_INCREMENT COMMENT '自增序号',
  `courseID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '课程编号',
  `termID` varchar(50) DEFAULT NULL COMMENT '学期ID',
  `classTime` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '上课时间：1-2；3-4；5-6；7-8；',
  `count` int DEFAULT NULL COMMENT '课程容量-可选人数',
  `isDelete` tinyint(1) DEFAULT '0' COMMENT '是否删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='课程安排表';

-- ----------------------------
-- Table structure for sso_user
-- ----------------------------
DROP TABLE IF EXISTS `sso_user`;
CREATE TABLE `sso_user` (
  `autoID` bigint NOT NULL AUTO_INCREMENT,
  `userID` varchar(22) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '用户ID',
  `account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '登录账号-默认为手机号',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '密码',
  `userType` tinyint(1) DEFAULT NULL COMMENT '账号类型：1--学生；2--老师；3--管理人员',
  `status` tinyint(1) DEFAULT NULL COMMENT '账号的状态：1--可用；0--锁定',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户账号信息表';

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `autoID` int NOT NULL AUTO_INCREMENT COMMENT '自增字段',
  `studentID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '学号，业务主键',
  `userID` varchar(22) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '对应的用户表ID',
  `classID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '所属班级ID',
  `collegeID` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '所属学院',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '学生姓名',
  `phoneNumber` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '手机号码',
  `age` int DEFAULT NULL COMMENT '年龄',
  `agenda` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '性别',
  `isDelete` tinyint(1) DEFAULT '0' COMMENT '是否删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='学生基本信息表';

-- ----------------------------
-- Table structure for student_selected_course
-- ----------------------------
DROP TABLE IF EXISTS `student_selected_course`;
CREATE TABLE `student_selected_course` (
  `autoID` int NOT NULL AUTO_INCREMENT COMMENT '自增序号字段',
  `studentID` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '学号',
  `courseID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '课程编号',
  `score` int DEFAULT NULL COMMENT '成绩',
  `isDelete` tinyint(1) DEFAULT '0' COMMENT '是否删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='学生选课情况表';

-- ----------------------------
-- Table structure for sys_classInfo
-- ----------------------------
DROP TABLE IF EXISTS `sys_classInfo`;
CREATE TABLE `sys_classInfo` (
  `autoID` int NOT NULL AUTO_INCREMENT,
  `classID` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '班级ID',
  `collegeID` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '所属学院',
  `className` varchar(20) DEFAULT NULL COMMENT '班级名称',
  `isDeleted` tinyint(1) DEFAULT '0' COMMENT '是否被删除  0 - 未删除  1 - 已删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='班级信息表';

-- ----------------------------
-- Table structure for sys_collegeInfo
-- ----------------------------
DROP TABLE IF EXISTS `sys_collegeInfo`;
CREATE TABLE `sys_collegeInfo` (
  `autoID` bigint NOT NULL AUTO_INCREMENT,
  `collegeID` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '学院ID编码--业务主键',
  `collegeName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '学院名称',
  `isDelete` tinyint(1) DEFAULT '0' COMMENT '是否删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb3 COMMENT='学院表，记录学院/系信息，学生-导师-秘书通过学院进行关联';

-- ----------------------------
-- Table structure for sys_departmentInfo
-- ----------------------------
DROP TABLE IF EXISTS `sys_departmentInfo`;
CREATE TABLE `sys_departmentInfo` (
  `autoID` bigint NOT NULL AUTO_INCREMENT,
  `departmentID` bigint DEFAULT NULL COMMENT '学院下属的教研室(研究所)ID',
  `parentDepartmentID` bigint NOT NULL DEFAULT '0' COMMENT '父级部门ID',
  `collegeID` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '学院ID编码--业务主键',
  `departmentName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '教研室(研究所)名称',
  `departmentType` tinyint(1) DEFAULT '1' COMMENT '部门类型:\r\n1--教研室；\r\n2-研究所；\r\n3 实验中心；\r\n4-办公室；\r\n5-其他',
  `isDeleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否被删除   0 -未被删除  1 - 被删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='教研室与研究所信息表';

-- ----------------------------
-- Table structure for teacher
-- ----------------------------
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher` (
  `autoID` int NOT NULL AUTO_INCREMENT,
  `teacherID` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '教工号',
  `userID` varchar(22) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '对应的用户表ID',
  `departmentID` bigint DEFAULT NULL COMMENT '所属的教研室(研究所)ID',
  `name` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '姓名',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '电话',
  `officeAddress` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '办公地址',
  `isDelete` tinyint(1) DEFAULT '0' COMMENT '是否删除',
  `addTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录添加时间',
  PRIMARY KEY (`autoID`) USING BTREE,
  KEY `departmentID` (`departmentID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- View structure for v_student_course_score
-- ----------------------------
DROP VIEW IF EXISTS `v_student_course_score`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `v_student_course_score` AS select `student`.`autoID` AS `autoID`,`student_selected_course`.`studentID` AS `studentID`,`student`.`userID` AS `userID`,`student`.`classID` AS `classID`,`student`.`collegeID` AS `collegeID`,`student`.`name` AS `studentName`,`student`.`phoneNumber` AS `phoneNumber`,`student`.`age` AS `age`,`student`.`agenda` AS `agenda`,`student`.`isDelete` AS `isDelete`,`sys_classInfo`.`className` AS `className`,`student_selected_course`.`courseID` AS `courseID`,`student_selected_course`.`score` AS `score`,`course`.`courseName` AS `courseName`,`course`.`teacherID` AS `teacherID`,`teacher`.`name` AS `teacherName`,`teacher`.`phone` AS `phone`,`teacher`.`email` AS `email` from ((((`student` join `sys_classInfo` on((`student`.`classID` = `sys_classInfo`.`classID`))) join `student_selected_course` on((`student`.`studentID` = `student_selected_course`.`studentID`))) join `course` on((`student_selected_course`.`courseID` = `course`.`courseID`))) join `teacher` on((`course`.`teacherID` = `teacher`.`teacherID`)));

SET FOREIGN_KEY_CHECKS = 1;
