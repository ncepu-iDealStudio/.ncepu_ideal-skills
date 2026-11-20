# database-schema-designer

从自然语言或已有库结构，设计 PostgreSQL、MySQL、SQLite 或 MongoDB 的数据模型。一句话需求会先用少量选项问清会改变表结构的产品决定；详细规格说明书则只确认没写清的点。PostgreSQL 与 MySQL 各用自己的写法，可以只做一种，也可以两种各出一份脚本。

改编自 [OneWave AI 的 database-schema-designer](https://github.com/OneWave-AI/claude-skills/tree/main/database-schema-designer)（MIT）。署名见 `NOTICE` 和 `LICENSE`。

## 什么时候用

- 新应用或新功能要建表、选主键、选索引、做多租户
- 已有 SQL、Prisma、Drizzle 或迁移目录，要改表而不是另起一套
- 用户只描述了业务，问「这些数据该怎么存」

本技能不负责把数据从一个数据库产品搬到另一个。

## 怎么和用户把需求谈清楚

先看输入有多完整，不先问用户要多深的访谈。

一句话需求，例如「帮我设计一个技能交换 app 的后台数据库」，每次只问一个会改变表结构的产品决定，并给出针对这个产品的选项，最后一项是「其他，我补充」。默认最多 4 轮。人群、交换方式这类问题要拆开问，不要第一条消息就把所有问题列完。

用户另外给了详细的需求规格说明书时，先读说明书。已经写明的功能不再追问。只确认说明书没写清、而且不同答案会增减表或关系的点。默认最多 2 轮；没有这种缺口就直接设计。

用户说「直接设计」就不再提问，把没问到的内容写成假设，然后给出建表脚本和设计文档。`shallow` / `medium` / `deep` 只在用户自己说出这些词时才加问查询量、保留和合规。

## 交付什么

新建库：

- 一种引擎：`schema.sql`（MongoDB 为 `schema.js`）
- PostgreSQL 和 MySQL 都要：`schema.postgres.sql` 与 `schema.mysql.sql`
- `database-design.md`：假设、关系、每张表的用途和索引

已有库：先读现有定义，交付差异清单和 up/down 迁移。只有用户明确要求重建时才给全量 `schema.sql`。

## 引擎注意

- 未知引擎且问完仍不知道时，默认 PostgreSQL，并写进假设。接下来要用本仓库的 `sql-to-fastapi`、`sql-to-flask`、`sql-to-gin` 或 `sql-to-springboot` 生成后端时，改为 MySQL：那些技能吃的是 MySQL `CREATE TABLE`，而且不执行 DDL。不要把 PostgreSQL 脚本交给它们。
- Supabase 不等于 PostgreSQL 18。先看项目的主版本，再决定能不能用 `uuidv7()`。`auth.uid()` 只写在 Supabase 的行级安全策略里。
- MySQL 没有部分索引。用生成列代替时，查询必须按该列过滤和排序。`utf8mb4_0900_ai_ci` 的唯一约束同时忽略大小写和重音，和 PostgreSQL 的 `lower(email)` 不一样。
- MongoDB 按访问模式嵌入或引用，不写关系型外键。

## 装到 AI 工具

把本目录整份复制到工具的 skills 目录，目录名保持 `database-schema-designer`。需要带上 `SKILL.md` 和 `references/`。

- Cursor：`.cursor/skills/database-schema-designer/`
- Claude Code：`.claude/skills/database-schema-designer/`
