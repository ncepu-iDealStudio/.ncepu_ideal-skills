# {{projectName}}

由技能 `sql-to-springboot-scaffold` 根据 `sql/{{tableName}}.sql` 生成的 Spring Boot 3 项目脚手架。

统一使用 **Controller → Service → Repository → Entity** 四层分层，Controller 只依赖 Service，Repository 只做单表数据访问，业务规则集中在 Service。

## 技术栈

| 项目 | 版本 / 说明 |
| --- | --- |
| Spring Boot | 3.2.0 |
| JDK | 17 |
| 构建 | Maven |
| 持久层 | Spring Data JPA / Hibernate |
| 参数校验 | jakarta.validation |
| 接口文档 | springdoc-openapi 2.2.0（Swagger UI） |
| 代码简化 | Lombok |
| 数据库 | MySQL 8；`h2` 仅用于本地练手 |

包名统一为 `com.security.apisecurity`。

## 环境准备（首次运行必读）

只需要装两样东西：**JDK 17** 与 **Maven 3.8+**。缺任何一个都会在 `mvn` 阶段直接报错。

### 1. 安装 JDK 17

`pom.xml` 中 `java.version=17`，用 JDK 17 即可（JDK 21 也能编译，Maven 会按 `release 17` 处理）。

**Windows**

1. 打开 <https://adoptium.net/temurin/releases/?version=17>，下载 Windows x64 的 `.msi`。
2. 安装时勾选 `Set JAVA_HOME variable` 和 `Add to PATH`。
3. 若安装包未写入环境变量，手动配置：
   - 新建系统变量 `JAVA_HOME`，例如 `D:\Java\jdk-17`；
   - 编辑系统变量 `Path`，新增 `%JAVA_HOME%\bin`。
4. **关闭并重新打开终端**，让环境变量生效。

**macOS**

```bash
brew install openjdk@17
echo 'export JAVA_HOME=$(/usr/libexec/java_home -v 17)' >> ~/.zshrc
source ~/.zshrc
```

**Linux（Ubuntu / Debian）**

```bash
sudo apt update
sudo apt install -y openjdk-17-jdk
```

**验证**

```powershell
java -version
echo $env:JAVA_HOME
```

```bash
# macOS / Linux
java -version
echo $JAVA_HOME
```

输出包含 `17.x`（或 `21.x`）即成功。若提示“找不到 java”，说明 `Path` 未生效，重开终端再试。

### 2. 安装 Maven 3.8+

模板没有自带 `mvnw`，需要本机安装 Maven。

**Windows**

1. 打开 <https://maven.apache.org/download.cgi>，下载 `apache-maven-3.9.x-bin.zip`。
2. 解压到无空格、无中文的路径，例如 `D:\apache-maven-3.9.10`。
3. 配置环境变量：
   - 新建系统变量 `M2_HOME`，值为 `D:\apache-maven-3.9.10`；
   - 编辑系统变量 `Path`，新增 `%M2_HOME%\bin`。
4. 重开终端后验证。

**macOS**

```bash
brew install maven
```

**Linux（Ubuntu / Debian）**

```bash
sudo apt install -y maven
```

**验证**

```powershell
mvn -v
```

期望输出类似：

```text
Apache Maven 3.9.10
Maven home: D:\apache-maven-3.9.10
Java version: 17.0.x
```

`Java version` 必须是 17 或以上；若显示 1.8，说明 `JAVA_HOME` 指向了旧 JDK。

### 3. 配置 Maven 镜像源（国内网络必做）

默认中央仓库在国外，首次拉依赖可能非常慢甚至超时。改用阿里云镜像：

**配置文件位置（二选一）**

| 作用范围 | 路径 |
| --- | --- |
| 当前用户（推荐） | `%USERPROFILE%\.m2\settings.xml`（Windows）、`~/.m2/settings.xml`（macOS/Linux） |
| 全局 | `${MAVEN_HOME}/conf/settings.xml` |

目录或文件不存在就新建。内容如下（若文件已存在，只把 `<mirror>` 片段插入已有 `<mirrors>` 中，不要整份覆盖）：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 https://maven.apache.org/xsd/settings-1.0.0.xsd">
    <mirrors>
        <mirror>
            <id>aliyun-central</id>
            <name>阿里云公共仓库</name>
            <url>https://maven.aliyun.com/repository/public</url>
            <mirrorOf>central</mirrorOf>
        </mirror>
    </mirrors>
</settings>
```

**验证镜像是否生效**

```powershell
mvn help:effective-settings
```

输出中出现 `aliyun-central` 即生效；也可观察首次编译时下载 URL 是否为 `maven.aliyun.com`。

> 公司内网若禁止外网直连，请改用公司私服地址（同样写在 `<mirror>` 里）。

### 4. 环境自检清单

```powershell
java -version    # 17.x 或更高
mvn -v           # 3.8+，且 Java version 指向 17+
mysql --version  # 8.x（用 H2 练手时可跳过）
```

## 项目结构

```text
{{projectStructure}}
```

## 接口说明

`server.servlet.context-path={{contextPath}}`，下表路径已带前缀。

| 方法 | 路径 | 说明 | 成功状态码 |
| --- | --- | --- | --- |
| POST | `http://localhost:{{port}}{{contextPath}}/{{resourcePath}}` | 新增 | 201 |
| GET | `http://localhost:{{port}}{{contextPath}}/{{resourcePath}}` | 分页查询 | 200 |
| GET | `http://localhost:{{port}}{{contextPath}}/{{resourcePath}}/{id}` | 查询详情 | 200（不存在 404） |
| PUT | `http://localhost:{{port}}{{contextPath}}/{{resourcePath}}/{id}` | 更新 | 200（不存在 404） |
| DELETE | `http://localhost:{{port}}{{contextPath}}/{{resourcePath}}/{id}` | 删除（软删除） | 200（不存在 404） |

所有响应都经过 `ApiResponse` 包装：

```json
{
  "success": true,
  "message": "操作成功",
  "data": { },
  "timestamp": "2026-01-01T12:00:00"
}
```

### 请求 / 响应示例

`POST http://localhost:{{port}}{{contextPath}}/{{resourcePath}}`

```json
{{requestExample}}
```

`GET http://localhost:{{port}}{{contextPath}}/{{resourcePath}}?page=0&size=20&sortBy=createTime&sortDir=desc`

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `page` | `0` | 页码，**从 0 开始** |
| `size` | `20` | 每页条数 |
| `sortBy` | `createTime` | 排序字段（Java 属性名） |
| `sortDir` | `desc` | `asc` / `desc` |

## 接口文档（Swagger）访问地址

应用启动成功后（控制台出现 `Tomcat started on port(s): {{port}} (http)`），用浏览器打开：

| 用途 | 完整地址 |
| --- | --- |
| **Swagger UI（推荐，可直接调试）** | <http://localhost:{{port}}{{contextPath}}/swagger-ui.html> |
| Swagger UI 重定向后的实际页面 | <http://localhost:{{port}}{{contextPath}}/swagger-ui/index.html> |
| OpenAPI JSON | <http://localhost:{{port}}{{contextPath}}{{apiDocsPath}}> |
| OpenAPI YAML | <http://localhost:{{port}}{{contextPath}}{{apiDocsPath}}.yaml> |

**注意事项**

- 必须带上下文路径 `{{contextPath}}`，否则 404。
- 改了 `server.port` 要同步换端口，改了 context-path 要同步换前缀。
- 本项目 `springdoc.api-docs.path={{apiDocsPath}}`，不是 springdoc 默认的 `/v3/api-docs`。
- 打开 404 时检查：`pom.xml` 是否有 `springdoc-openapi-starter-webmvc-ui`、`springdoc.swagger-ui.enabled=true`、启动日志是否有 springdoc 报错。
- 当前安全配置未启用，Swagger 与接口均无需 token；启用 `SecurityConfig` 后 `/api-docs/**`、`/swagger-ui/**` 已放行。

## 配置说明

`src/main/resources/application.properties` 关键配置：

```properties
server.port={{port}}
server.servlet.context-path={{contextPath}}

spring.datasource.url=jdbc:mysql://localhost:3306/{{databaseName}}?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true
spring.datasource.username=${DB_USERNAME:{{dbUsername}}}
spring.datasource.password=${DB_PASSWORD:{{dbPassword}}}

spring.jpa.hibernate.ddl-auto=none
```

数据库账号密码支持环境变量 `DB_USERNAME` / `DB_PASSWORD` 覆盖，避免明文入库。

## 快速开始

```bash
# 1. 建库建表
mysql -u {{dbUsername}} -p -e "CREATE DATABASE IF NOT EXISTS {{databaseName}} DEFAULT CHARSET utf8mb4;"
mysql -u {{dbUsername}} -p {{databaseName}} < sql/{{tableName}}.sql

# 2. 编译
mvn clean install -DskipTests

# 3. 启动
mvn spring-boot:run
```

启动后打开 Swagger：<http://localhost:{{port}}{{contextPath}}/swagger-ui.html>

### 没有 MySQL 时用 H2 练手

```properties
spring.datasource.url=jdbc:h2:mem:demo;MODE=MySQL;DB_CLOSE_DELAY=-1
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.H2Dialect
```

内存库重启即清空，只用于验证接口。

## DTO 设计说明

### {{className}}Request（请求 DTO）

只包含业务字段。以下字段由后端自动管理，**不会**出现在请求 DTO 中：

| 字段 | 原因 |
| --- | --- |
| `id` | 数据库自动生成 |
| `status` / `state` | 后端默认值管理 |
| 软删除字段 | 后端自动维护 |
| `create_time` / `update_time` | `@PrePersist` / `@PreUpdate` 自动填充 |

### {{className}}Response（响应 DTO）

包含全部展示字段，不含 `password`、`token` 等敏感字段。

## 软删除机制

表存在软删除字段时：

- `delete()`：把软删除字段置为 `true` 并保存，数据仍在库中
- 详情 / 更新：查询条件附加“未删除”，已删除记录视为不存在（404）
- 列表 / 搜索：固定附加“未删除”条件

## 安全配置说明（暂未启用）

安全骨架（`SecurityConfig`、`JwtUtils`、`AuthTokenFilter`、`AuthEntryPointJwt`、`UserDetailsServiceImpl`）已生成，但 `pom.xml` 中相关依赖处于注释状态，且依赖尚未生成的 `User` / `UserRepository`，因此文件放在 `security-placeholder/`，不参与编译。

启用步骤：

1. 打开 `pom.xml` 中被注释的安全依赖；
2. 把 `security-placeholder/` 下文件移入 `src/main/java/com/security/apisecurity/` 对应包；
3. 补齐 `User` / `UserRepository`；
4. 配置 `jwt.secret`（≥32 字符 Base64）与 `jwt.expiration`；
5. 重启后接口默认要求 `Authorization: Bearer <token>`。

## 增量新增其它表

```text
请使用 sql-to-springboot-scaffold 技能，为 sql/{{nextTableName}}.sql 做增量生成。
要求：只生成该表相关文件；路由用复数；已存在的 Service 不要覆盖。
```

每张表固定产出 6 个文件：Entity、Repository、Request DTO、Response DTO、Service、Controller。
