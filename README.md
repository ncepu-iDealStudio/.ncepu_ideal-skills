# ncepu_ideal-skills

企业级服务端项目技能（Skills）集合仓库。  
当前已落地第一个可用技能：`sql-to-fastapi-scaffold`，用于从 SQL 表结构快速生成基于 FastAPI 的分层项目代码。

English version: [README.en.md](README.en.md)

## 项目目标

- 统一沉淀团队在后端工程化中的可复用技能。
- 将“规范 + 模板 + 配置”封装为可调用的 Skill，降低项目搭建与重复开发成本。
- 逐步形成可扩展的技能库：一个仓库，多个领域技能（数据库、API、架构、工程化等）。

## 当前技能清单

### 1) sql-to-fastapi-scaffold（已实现）

位置：`sql-to-fastapi-scaffold/`

能力概述：

- 解析 SQL `CREATE TABLE` 语句
- 生成 FastAPI 分层代码（Model / Schema / Resource / Service）
- 首次生成时可产出完整项目骨架；后续增表可按表增量生成代码
- 支持软删除/硬删除自动策略
- 内置类型映射、命名规则、字段验证与敏感字段脱敏规则

详细说明见：

- 技能说明：`sql-to-fastapi-scaffold/README.md`
- 技能配置：`sql-to-fastapi-scaffold/SKILL.md`

## 仓库结构

```text
ncepu_ideal-skills/
├── README.md
├── README.en.md
├── docs/
│   └── Trea中使用skill配置.md
├── sql-to-fastapi-scaffold/
│   ├── README.md
│   ├── SKILL.md
│   └── resources/
│       ├── config/
│       │   ├── naming_rules.json
│       │   └── type_mappings.json
│       ├── specifications/
│       │   └── coding_standards.md
│       └── templates/
│           ├── project_structure/
│           └── layers/
└── test/
	└── sql-to-fastapi-example/
```

说明：

- `sql-to-fastapi-scaffold/resources/`：技能核心资源（模板、规则、规范）
- `test/sql-to-fastapi-example/`：技能生成结果示例与验证样例
- `docs/`：使用说明与配套文档

## 快速开始

### 1) 使用技能

将包含 `CREATE TABLE` 的 SQL 输入给技能，要求生成 FastAPI 接口项目。

示例（简化）：

```sql
CREATE TABLE student (
	studentID VARCHAR(20) PRIMARY KEY COMMENT '学号',
	name VARCHAR(100) NOT NULL COMMENT '学生姓名',
	age INT COMMENT '年龄',
	is_deleted BOOLEAN DEFAULT FALSE COMMENT '是否删除'
);
```

### 2) 运行生成的示例项目（参考）

示例目录：`test/sql-to-fastapi-example/`

```bash
cd test/sql-to-fastapi-example
pip install -r requirements.txt
uvicorn start:app --reload
```

默认访问：

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### 3) 在 Trae 中配置技能

参考文档：`docs/Trea中使用skill配置.md`

## 设计理念

本仓库采用“资源驱动”设计：

- 通过模板驱动代码结构（`resources/templates/`）
- 通过配置驱动规则映射（`resources/config/`）
- 通过规范约束输出质量（`resources/specifications/`）

这种方式可以让技能具备：

- 可维护：规则集中、可追踪
- 可扩展：新增技能互不影响
- 可复用：同一技能可服务多个业务场景

## 未来规划

- 新增更多面向企业后端的技能（脚手架、治理、工程化等）
- 完善技能验证样例与回归测试
- 建立统一技能命名、版本与文档规范

## 贡献指南

欢迎提交新的 Skill 或改进现有 Skill。

建议流程：

1. Fork 本仓库并新建分支
2. 在独立目录中实现新 Skill（包含 `SKILL.md`、`README.md`、`resources/`）
3. 补充对应示例到 `test/`
4. 更新根 README 的技能清单与说明
5. 发起 Pull Request

## 许可证

当前仓库未声明许可证文件。建议补充 `LICENSE` 后再对外分发。
