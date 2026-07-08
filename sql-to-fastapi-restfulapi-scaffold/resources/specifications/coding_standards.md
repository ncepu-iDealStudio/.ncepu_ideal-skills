# SQL-to-FastAPI-Scaffold 代码规范

## 1. 概述

本文档定义了 SQL-to-FastAPI-Scaffold 生成代码时应遵循的规范和最佳实践。

## 2. 格式规范

### 2.1 缩进与空格

- 使用 4 个空格进行缩进
- 不使用 Tab 字符
- 行尾不留多余空格
- 文件末尾保留一个空行

### 2.2 行宽

- 最大行宽 120 字符
- 超过行宽时合理换行

### 2.3 空行

- 模块级函数或类之间留 2 个空行
- 类内部的方法之间留 1 个空行
- 函数或方法内部逻辑块之间留 1 个空行

### 2.4 导入顺序

导入应按以下顺序分组，组之间留一个空行：

1. 标准库导入
2. 第三方库导入
3. 本地模块导入

示例：

```python
# 标准库
from typing import List, Optional
from datetime import datetime

# 第三方库
from sqlalchemy import Column, String
from pydantic import BaseModel

# 本地模块
from models.base import BaseModel
from schemas.response import SuccessResponse
```

## 3. 命名规范

### 3.1 类名

- 使用大驼峰命名法（PascalCase）
- 首字母大写
- 不使用下划线分隔

### 3.2 函数与方法名

- 使用蛇形命名法（snake_case）
- 全小写
- 用下划线分隔单词

### 3.3 常量

- 使用全大写下划线分隔（UPPER_SNAKE_CASE）
- 在模块顶部定义

### 3.4 私有成员

- 使用单下划线前缀（_private_member）
- 表示非公开接口

## 4. 文档字符串规范

### 4.1 模块文档字符串

每个模块文件顶部应有模块文档字符串：

```python
"""
模块功能描述

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""
```

### 4.2 类文档字符串

每个类应有类文档字符串：

```python
class ClassName(BaseModel):
    """
    类功能描述
    """
```

### 4.3 方法文档字符串

每个公共方法应有方法文档字符串：

```python
def method_name(self, param: Type) -> ReturnType:
    """
    方法功能描述
    """
```

### 4.4 语言要求

所有文档字符串使用中文。

## 5. SQLAlchemy 模型规范

### 5.1 继承关系

所有模型必须继承 `BaseModel`：

```python
from models.base import BaseModel

class ModelName(BaseModel):
    pass
```

### 5.2 表名

- 使用 `__tablename__` 属性定义表名
- 表名使用蛇形命名法
- 与数据库表名保持一致

### 5.3 字段定义

- 字段名使用蛇形命名法
- 字段定义使用 `Column`
- 必须包含 `comment` 参数说明字段用途
- 约束顺序：`primary_key` → `nullable` → `unique` → `default` → `comment`

### 5.4 外键与关系

- 外键字段命名格式：`{related_table}_id`
- 关系属性命名格式：`{related_table}`
- 使用 `relationship` 定义关系

## 6. Pydantic Schema 规范

### 6.1 基础模型

- `{ClassName}Base`：包含业务字段，不包含主键
- 字段必填使用 `...`，可选使用 `None`

### 6.2 创建模型

- `{ClassName}Create`：继承 Base，添加主键字段
- 包含完整的示例数据

### 6.3 更新模型

- `{ClassName}Update`：所有字段使用 `Optional`
- 设置 `extra = "forbid"` 防止批量赋值
- 不包含主键字段

### 6.4 响应模型

- `{ClassName}Response`：包含所有字段 + `is_delete` + `add_time`
- 设置 `from_attributes = True`
- 包含完整示例

### 6.5 字段验证器

- 使用 `@validator` 装饰器
- 验证器命名格式：`validate_{field_name}`
- 处理 `None` 值情况

## 7. FastAPI Resource 规范

### 7.1 路由前缀

- 使用 `APIRouter(prefix="/{resource_singular}")`（路由前缀使用**单数**）
- 文件夹命名使用单数：`api/v1/{resource_singular}/{resource_singular}Resource.py`
- tags 使用中文说明

### 7.2 端点方法

- GET /：获取列表，分页
- GET /{id}：获取详情
- POST /：创建
- PUT /{id}：更新
- DELETE /{id}：软删除

### 7.3 装饰器与依赖

**必须添加**：
- 所有端点必须添加 `@handle_service_exceptions` 装饰器
- 所有端点必须包含 `container: ServiceContainer = Depends(ServiceContainer)` 依赖

**可选依赖（根据业务需求）**：
- `current_user: dict = Depends(get_current_user)` - 需要认证的端点添加（如管理后台）
- 公开接口（如登录、注册、公共数据查询）不需要添加认证依赖

### 7.4 OpenAPI 文档

- 必须设置 `summary` 和 `description`
- 必须设置 `response_model`
- 必须设置 `status_code`

## 8. Service 层规范

### 8.1 类定义

每个资源对应一个独立的 Service 类，直接注入 `db: Session`：

```python
from typing import Dict
from sqlalchemy.orm import Session

from models.{{table_name}} import {{ClassName}}
from schemas.{{table_name}} import {{ClassName}}Create, {{ClassName}}Update, {{ClassName}}Response


class {{ClassName}}Service:
    """
    {{table_comment}}服务类
    """

    def __init__(self, db: Session):
        self.db = db
```

### 8.2 方法规范

#### create

1. 检查主键唯一性
2. 检查外键存在性
3. 创建对象
4. 提交事务
5. 清除缓存
6. 返回响应模型

#### get_list

1. 构建查询（过滤 `is_delete = False`）
2. 计算总数
3. 分页查询
4. 转换为响应模型

#### get_detail

1. 查询对象
2. 检查存在性
3. 返回响应模型

#### update

1. 查询对象
2. 检查存在性
3. 检查外键
4. 更新字段
5. 提交事务
6. 清除缓存
7. 返回响应模型

#### delete

1. 查询对象
2. 检查存在性
3. 软删除（设置 `is_delete = True`）
4. 提交事务
5. 清除缓存

### 8.3 错误处理

使用 `utils.custom_exceptions` 中的异常类：

```python
from utils.custom_exceptions import BadRequestException, NotFoundException

# 抛出400错误
raise BadRequestException("{{table_comment}}已存在")

# 抛出404错误
raise NotFoundException("{{table_comment}}不存在")
```

### 8.4 缓存管理

数据修改后调用缓存清除方法：

```python
from core.cache import clear_cache

clear_cache()
```

## 9. 安全规范

### 9.1 输入验证

- 所有用户输入必须通过 Pydantic Schema 验证
- 敏感字段使用适当的验证器

### 9.2 批量赋值保护

- Update 模型必须设置 `extra = "forbid"`
- 不允许未定义的字段被赋值

### 9.3 敏感数据脱敏

- 手机号、邮箱等敏感字段提供 `masked_*` 属性
- 不在响应中返回原始敏感数据

### 9.4 认证与授权

**根据业务场景选择是否需要认证**：
- 管理后台类接口：需要认证，添加 `Depends(get_current_user)`
- 公开接口（登录、注册、公共查询等）：不需要认证

**需要认证时的规范**：
- 通过 `get_current_user` 获取当前用户
- 执行操作时记录 `current_user_id`
- 在 Service 层的 create/update/delete 方法中传入 current_user_id

### 9.5 SQL 注入防护

- 使用 SQLAlchemy ORM，不拼接 SQL
- 参数化查询

## 10. 性能规范

### 10.1 缓存

- 数据修改后调用 `self._clear_cache()`
- 合理使用缓存提高性能

### 10.2 分页

- 列表查询必须分页
- 默认分页大小 20，最大 100

### 10.3 查询优化

- 使用索引字段查询
- 避免 N+1 查询问题

## 11. 错误处理规范

### 11.1 错误类型

- `handle_service_exceptions`：统一处理服务层异常
- 错误信息使用中文
- 错误信息清晰具体

### 11.2 错误响应

- 使用统一的响应格式
- 包含错误代码和错误信息

## 12. 示例SQL规范

### 12.1 CREATE TABLE 语句

- 每个字段必须有 `COMMENT`
- 主键使用 `PRIMARY KEY`
- 非空字段使用 `NOT NULL`
- 唯一约束使用 `UNIQUE`
- 默认值使用 `DEFAULT`
- 外键约束使用 `FOREIGN KEY ... REFERENCES ...`

示例：

```sql
CREATE TABLE student (
    student_id VARCHAR(20) PRIMARY KEY COMMENT '学生ID',
    user_id VARCHAR(22) COMMENT '用户ID',
    class_id VARCHAR(10) COMMENT '班级ID',
    name VARCHAR(100) NOT NULL COMMENT '学生姓名',
    phone VARCHAR(20) COMMENT '手机号',
    email VARCHAR(100) UNIQUE COMMENT '邮箱',
    age INT DEFAULT 0 COMMENT '年龄',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (user_id) REFERENCES sso_user(user_id),
    FOREIGN KEY (class_id) REFERENCES sys_class(class_id)
) COMMENT='学生表';
```
