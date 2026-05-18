# Study Flask API - Spring Boot RESTful API

基于 SQL 表结构自动生成的 Spring Boot RESTful API 项目

## 技术栈

- **Spring Boot**: 3.2.0
- **Java**: 17
- **Spring Data JPA**: 数据持久层
- **Spring Validation**: 数据验证
- **Lombok**: 简化代码
- **SpringDoc OpenAPI**: API 文档 (Swagger)
- **MySQL**: 数据库

## 项目结构

```
src/main/java/com/security/apisecurity/
├── ApiSecurityApplication.java          # 应用入口
├── config/                               # 配置类
├── controller/                           # REST 控制器
│   ├── AdminController.java
│   ├── CourseController.java
│   ├── CourseArrangementController.java
│   ├── SsoUserController.java
│   ├── StudentController.java
│   ├── StudentSelectedCourseController.java
│   ├── SysClassInfoController.java
│   ├── SysCollegeInfoController.java
│   ├── SysDepartmentInfoController.java
│   └── TeacherController.java
├── dto/
│   ├── request/                          # 请求 DTO
│   │   ├── AdminRequest.java
│   │   ├── CourseRequest.java
│   │   ├── CourseArrangementRequest.java
│   │   ├── SsoUserRequest.java
│   │   ├── StudentRequest.java
│   │   ├── StudentSelectedCourseRequest.java
│   │   ├── SysClassInfoRequest.java
│   │   ├── SysCollegeInfoRequest.java
│   │   ├── SysDepartmentInfoRequest.java
│   │   └── TeacherRequest.java
│   └── response/                         # 响应 DTO
│       ├── AdminResponse.java
│       ├── ApiResponse.java
│       ├── CourseResponse.java
│       ├── CourseArrangementResponse.java
│       ├── SsoUserResponse.java
│       ├── StudentResponse.java
│       ├── StudentSelectedCourseResponse.java
│       ├── SysClassInfoResponse.java
│       ├── SysCollegeInfoResponse.java
│       ├── SysDepartmentInfoResponse.java
│       └── TeacherResponse.java
├── entity/                               # JPA 实体
│   ├── Admin.java
│   ├── Course.java
│   ├── CourseArrangement.java
│   ├── SsoUser.java
│   ├── Student.java
│   ├── StudentSelectedCourse.java
│   ├── SysClassInfo.java
│   ├── SysCollegeInfo.java
│   ├── SysDepartmentInfo.java
│   └── Teacher.java
├── exception/                            # 异常处理
│   ├── AccessDeniedException.java
│   ├── BadRequestException.java
│   ├── GlobalExceptionHandler.java
│   └── ResourceNotFoundException.java
├── repository/                           # 数据访问层
│   ├── AdminRepository.java
│   ├── CourseRepository.java
│   ├── CourseArrangementRepository.java
│   ├── SsoUserRepository.java
│   ├── StudentRepository.java
│   ├── StudentSelectedCourseRepository.java
│   ├── SysClassInfoRepository.java
│   ├── SysCollegeInfoRepository.java
│   ├── SysDepartmentInfoRepository.java
│   └── TeacherRepository.java
└── service/                              # 业务逻辑层
    ├── AdminService.java
    ├── CourseService.java
    ├── CourseArrangementService.java
    ├── SsoUserService.java
    ├── StudentService.java
    ├── StudentSelectedCourseService.java
    ├── SysClassInfoService.java
    ├── SysCollegeInfoService.java
    ├── SysDepartmentInfoService.java
    └── TeacherService.java
```

## API 接口列表

基础路径: `/api/v1`

### Admin (管理员)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /admins | 创建管理员 |
| GET | /admins | 获取管理员列表（分页） |
| GET | /admins/{id} | 获取管理员详情 |
| PUT | /admins/{id} | 更新管理员 |
| DELETE | /admins/{id} | 删除管理员（软删除） |

### Course (课程)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /courses | 创建课程 |
| GET | /courses | 获取课程列表（分页） |
| GET | /courses/{id} | 获取课程详情 |
| PUT | /courses/{id} | 更新课程 |
| DELETE | /courses/{id} | 删除课程（软删除） |

### CourseArrangement (课程安排)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /course-arrangements | 创建课程安排 |
| GET | /course-arrangements | 获取课程安排列表（分页） |
| GET | /course-arrangements/{id} | 获取课程安排详情 |
| PUT | /course-arrangements/{id} | 更新课程安排 |
| DELETE | /course-arrangements/{id} | 删除课程安排（软删除） |

### SsoUser (用户账号)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /sso-users | 创建用户账号 |
| GET | /sso-users | 获取用户账号列表（分页） |
| GET | /sso-users/{id} | 获取用户账号详情 |
| PUT | /sso-users/{id} | 更新用户账号 |
| DELETE | /sso-users/{id} | 删除用户账号（硬删除） |

### Student (学生)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /students | 创建学生 |
| GET | /students | 获取学生列表（分页） |
| GET | /students/{id} | 获取学生详情 |
| PUT | /students/{id} | 更新学生 |
| DELETE | /students/{id} | 删除学生（软删除） |

### StudentSelectedCourse (学生选课)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /student-selected-courses | 创建学生选课记录 |
| GET | /student-selected-courses | 获取学生选课列表（分页） |
| GET | /student-selected-courses/{id} | 获取学生选课详情 |
| PUT | /student-selected-courses/{id} | 更新学生选课 |
| DELETE | /student-selected-courses/{id} | 删除学生选课（软删除） |

### SysClassInfo (班级信息)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /sys-classes | 创建班级 |
| GET | /sys-classes | 获取班级列表（分页） |
| GET | /sys-classes/{id} | 获取班级详情 |
| PUT | /sys-classes/{id} | 更新班级 |
| DELETE | /sys-classes/{id} | 删除班级（软删除） |

### SysCollegeInfo (学院信息)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /sys-colleges | 创建学院 |
| GET | /sys-colleges | 获取学院列表（分页） |
| GET | /sys-colleges/{id} | 获取学院详情 |
| PUT | /sys-colleges/{id} | 更新学院 |
| DELETE | /sys-colleges/{id} | 删除学院（软删除） |

### SysDepartmentInfo (部门信息)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /sys-departments | 创建部门 |
| GET | /sys-departments | 获取部门列表（分页） |
| GET | /sys-departments/{id} | 获取部门详情 |
| PUT | /sys-departments/{id} | 更新部门 |
| DELETE | /sys-departments/{id} | 删除部门（软删除） |

### Teacher (教师)

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /teachers | 创建教师 |
| GET | /teachers | 获取教师列表（分页） |
| GET | /teachers/{id} | 获取教师详情 |
| PUT | /teachers/{id} | 更新教师 |
| DELETE | /teachers/{id} | 删除教师（软删除） |

## API 使用示例

### 创建记录

```bash
curl -X POST http://localhost:8080/api/v1/students \
  -H "Content-Type: application/json" \
  -d '{
    "studentId": "20230001",
    "name": "张三",
    "classId": "CS2023",
    "collegeId": "CS",
    "age": 20,
    "agenda": "男",
    "phoneNumber": "13800138000"
  }'
```

### 获取列表

```bash
curl -X GET "http://localhost:8080/api/v1/students?page=0&size=20&sortBy=addTime&sortDir=desc"
```

### 获取详情

```bash
curl -X GET http://localhost:8080/api/v1/students/1
```

### 更新记录

```bash
curl -X PUT http://localhost:8080/api/v1/students/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "李四",
    "age": 21
  }'
```

### 删除记录

```bash
curl -X DELETE http://localhost:8080/api/v1/students/1
```

## 统一响应格式

```json
{
  "code": 200,
  "message": "Success",
  "data": { ... }
}
```

错误响应：

```json
{
  "code": 404,
  "message": "Student not found with autoId: 1",
  "data": null
}
```

## 配置说明

数据库配置在 `src/main/resources/application.properties`:

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/study_flask_api
spring.datasource.username=root
spring.datasource.password=123456
```

## 快速开始

1. 确保 MySQL 数据库已安装并运行
2. 创建数据库 `study_flask_api`
3. 修改 `application.properties` 中的数据库配置
4. 运行以下命令启动项目：

```bash
mvn spring-boot:run
```

或打包后运行：

```bash
mvn clean package
java -jar target/api-security-demo-0.0.1-SNAPSHOT.jar
```

5. 访问 Swagger UI: http://localhost:8080/api/v1/swagger-ui.html
6. 访问 API Docs: http://localhost:8080/api/v1/api-docs

## DTO 设计说明

### Request DTO
- 包含业务字段
- 排除自动管理字段（主键、创建时间、软删除字段等）
- 包含验证注解

### Response DTO
- 包含所有展示字段
- 排除敏感字段（密码等）

## 软删除机制

以下表使用软删除：
- Admin (is_delete)
- Course (isDelete)
- CourseArrangement (isDelete)
- Student (isDelete)
- StudentSelectedCourse (isDelete)
- SysClassInfo (isDeleted)
- SysCollegeInfo (isDelete)
- SysDepartmentInfo (isDeleted)
- Teacher (isDelete)

以下表使用硬删除：
- SsoUser (无软删除字段)
