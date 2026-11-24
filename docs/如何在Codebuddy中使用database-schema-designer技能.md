# 在 CodeBuddy 中使用 database-schema-designer 技能

> 面向第一次使用这个技能的同学。照着下面的步骤操作，你可以从一句「帮我设计个后台数据库」开始，得到一份**能直接执行的建表脚本**和一份**说清楚每张表用途的设计文档**。
>
> 全文用一个贯穿案例：**技能交换 App 的后台数据库**（用户发布技能、按分类浏览、发起交换），这也是技能文档里的示例场景。

---

## 0. 这个技能能做什么

你给它一段业务描述或一个已有库结构，它还你一套数据模型设计：

| 你提供 | 技能产出 |
| --- | --- |
| 一句话需求，如「设计一个技能交换 App 的后台数据库」 | 建表脚本 + `database-design.md` |
| 一份详细的需求规格说明书 | 只确认说明书没写清的关键点，然后出脚本 + 设计文档 |
| 已有 SQL / Prisma / Drizzle / 迁移目录 | 差异清单 + up/down 迁移文件 |

它不是一个「只画 ER 图」的技能。它的交付物是**可执行的脚本**，并且：

- 每张表、每个字段都带**业务含义注释**（不是简单重复字段类型）
- 表名用**单数**（`app_user`、`skill`），主键叫**表名 + id**（`app_user_id`），不出现裸 `id`
- 时间列统一存 UTC；状态位用整数码表 + `CHECK`，不用字符串状态
- 默认**不生成外键约束**，引用列只写 `<表名>_id`、单独建索引，删除行为写进设计文档由服务层执行
- PostgreSQL 和 MySQL 各按自己的方言出脚本；两个引擎都要时，出**两份**脚本，而不是一份「通用」脚本

它**不负责**把数据从一个数据库搬到另一个数据库，也不执行 DDL（脚本由你拿去跑）。

---

## 1. 适合哪些场景

| 场景 | 适合程度 | 说明 |
| --- | --- | --- |
| 新应用 / 新功能要建表、选主键、选索引 | 非常适合 | 这是它的主战场 |
| 做多租户设计、决定范式取舍 | 非常适合 | 会问清租户隔离方式并落进唯一约束与索引 |
| 已有库要改表、补字段 | 适合 | 先读现有定义，交付差异清单和迁移，不覆盖迁移历史 |
| 只想问「这些数据该怎么存」 | 适合 | 会按访谈规则问清关键产品决定再设计 |
| 只想把 MySQL 库迁到 PostgreSQL | 不适合 | 本技能不做数据迁移 |
| 只想生成后端接口代码 | 不适合 | 那是 `sql-to-*` 脚手架技能的活（见第 8 节配合方式） |

---

## 2. 准备工作

开始前确认本机具备：

- [ ] CodeBuddy（IDE 或插件）
- [ ] 本仓库代码（提供技能目录 `requirements_analysis/database-schema-designer/`）
- [ ] 一个放生成结果的目标项目目录
- [ ] 可选：一个数据库连接，用于验证脚本（没有也能出脚本，技能会手工逐条走查查询）

> 不需要安装额外依赖：这个技能主要是规则 + 参考文档，不跑 Python 脚本。

---

## 3. 第 1 步：新建项目目录并安装技能

### 3.1 新建空目录

新建一个专门放生成结果的项目目录，例如 `D:\work\skill-swap-db`，然后用 CodeBuddy 打开这个目录。

> 不要直接在 `ncepu_ideal-skills` 仓库里生成脚本，否则生成物和技能源码混在一起。

### 3.2 把技能复制到项目中

在 CodeBuddy 的终端里执行（把 `<本仓库路径>` 换成你机器上的实际路径）。

#### PowerShell（Windows）

```powershell
New-Item -ItemType Directory -Force -Path .codebuddy/skills | Out-Null
Copy-Item -Recurse -Force "<本仓库路径>\requirements_analysis\database-schema-designer" .codebuddy/skills/
```

例如：

```powershell
Copy-Item -Recurse -Force "D:\work\ncepu_ideal-skills\requirements_analysis\database-schema-designer" .codebuddy/skills/
```

#### Bash（macOS / Linux）

```bash
mkdir -p .codebuddy/skills
cp -r <本仓库路径>/requirements_analysis/database-schema-designer .codebuddy/skills/
```

### 3.3 为什么要复制整个目录

这个技能是**资源驱动**的：`SKILL.md` 只写规则，真正设计时要读取 `references/` 里的规范和模板：

```text
database-schema-designer/
├── SKILL.md              # 规则主文件
├── README.md             # 技能说明
├── NOTICE / LICENSE      # 署名与许可（改编自 OneWave AI，MIT）
└── references/
    ├── interview.md      # 访谈规则与示例
    ├── postgres.md       # PostgreSQL 规范与迁移安全
    ├── mysql.md          # MySQL 规范与迁移安全
    ├── other-engines.md  # SQLite / MongoDB 规范
    ├── output-format.md  # 交付文档的结构
    └── schema-templates.md  # 两套引擎的 DDL 模板
```

只复制 `SKILL.md`，技能就读不到各引擎的规范和模板，输出会变得不可控。目录名要保持 `database-schema-designer`。

### 3.4 可选：安装到用户级

希望所有项目都能用时，安装到用户目录：

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.codebuddy\skills" | Out-Null
Copy-Item -Recurse -Force "<本仓库路径>\requirements_analysis\database-schema-designer" "$HOME\.codebuddy\skills\"
```

---

## 4. 第 2 步：确认安装成功

在目标项目根目录执行：

```powershell
Test-Path .codebuddy/skills/database-schema-designer/SKILL.md
Test-Path .codebuddy/skills/database-schema-designer/references/mysql.md
Test-Path .codebuddy/skills/database-schema-designer/references/postgres.md
```

三条都返回 `True` 才算复制完整。

然后在 CodeBuddy 中：

- 新开一个对话（或重启 IDE，让它重新扫描技能）
- 输入 `/skills`，应能看到 `database-schema-designer`
- 在「设置 → 技能 / Skills」的 Project Skills 里也能看到它

---

## 5. 第 3 步：在 CodeBuddy 中调用技能

### 5.1 怎么触发

不需要记特殊命令，直接用自然语言说需求即可。只要你的描述属于「建表 / 设计数据模型 / 选主键索引 / 改表结构 / 这些数据怎么存」，技能就会被触发。

一个典型的开场：

```text
帮我设计一个技能交换 App 的后台数据库：
用户可以发布自己会用的技能、按分类浏览、向别人发起交换。
```

### 5.2 一句话需求：会先问你几个选择题

技能会把短需求当作 **brief**，每次只问**一个会改变表结构的产品决定**，并给出针对你这个产品的选项，最后一项是「其他，我补充」。默认最多 4 轮。

例如它会这样问：

```text
在「技能交换」这个产品里，一次交换是怎么完成的？

1. 双方互相确认后，各自把技能标记成已交换（需要一张交换记录表）
2. 只是留言联系，平台不记录交换完成
3. 由发布者手动下架技能
4. 其他，我补充
```

注意它问的是**产品问题**，不会问你「主键用 bigint 还是 uuid」「要不要建索引」这类技术问题——那些由它按引擎规范决定。

> 想跳过访谈，直接说「直接设计」。技能会把没问到的内容写成假设，然后给出脚本和设计文档。

### 5.3 详细规格说明书：只确认缺口

如果你已经写好 PRD 或需求规格说明书，把文件一起给 CodeBuddy：

```text
先读一下 @requirements.md，用 database-schema-designer 为我设计数据库。
```

技能会先通读说明书，已经写明的功能不再追问，只确认「说明书没写清、而且不同答案会增减表或关系」的点，默认最多 2 轮；没有这种缺口就直接开始设计。

### 5.4 引擎怎么选

引擎是技能会问的关键问题之一。判断规则：

| 你的后续计划 | 选哪个引擎 |
| --- | --- |
| 只是设计数据模型，还没定 | PostgreSQL（默认），并写进假设 |
| 接下来要用本仓库的 `sql-to-*` 生成后端 | **必须 MySQL** |
| 两个引擎都要 | 出两份脚本：`schema.postgres.sql` + `schema.mysql.sql` |
| Supabase | 先看项目主版本，再决定能否用 PostgreSQL 18 语法 |

> 这条很重要：`sql-to-fastapi`、`sql-to-flask`、`sql-to-gin`、`sql-to-springboot` 吃的是 MySQL `CREATE TABLE`，不要把 PostgreSQL 脚本交给它们。

---

## 6. 你会拿到什么

以技能交换 App、只做 MySQL 为例：

```text
skill-swap-db/
├── schema.sql            # 可执行建表脚本（每张表、每个字段都有中文注释）
└── database-design.md    # 假设、ERD、关系说明、每张表的用途与索引
```

`database-design.md` 里会写清：

- 访谈中跳过的点，采用了什么**假设**
- 实体关系（1:1 / 1:N / N:M）和主要查询
- 每张表的用途、字段含义、键、关系、索引
- 引用列的 `ON DELETE` 意图（由服务层执行，脚本里没有外键约束）

两个引擎都要时，会变成 `schema.postgres.sql` + `schema.mysql.sql`，设计文档里多一节「Engine differences」说明差异。

已有库改造时，交付的是**差异清单 + up/down 迁移文件**，不会用一份全新的 `schema.sql` 覆盖迁移历史。

### 生成后怎么验证

技能会尽量验证脚本：有数据库就在本机或 Docker 里跑一遍、插几行数据、用 `EXPLAIN` 看关键查询是否用上索引；没有数据库就手工逐条走查应用会实际执行的 SQL。你可以再自己确认：

```sql
-- 语法能不能过
SOURCE schema.sql;

-- 关键查询是否走了索引
EXPLAIN SELECT * FROM skill WHERE category_id = 1 AND status = 1 ORDER BY created_at DESC;
```

---

## 7. 与 sql-to-* 脚手架技能配合

这两个技能是上下游关系，经常串起来用：

```text
database-schema-designer（出 schema.mysql.sql）
   → sql-to-fastapi-restfulapi-scaffold（读 MySQL CREATE TABLE）
   → 生成 Model / Schema / Repository / Service / Resource
```

在第 5.4 节就要告诉技能「接下来要用 `sql-to-*` 生成后端」，它会自动选 MySQL 并说明原因。拿到 `schema.mysql.sql` 后，把它交给 CodeBuddy：

```text
用 sql-to-fastapi-restfulapi-scaffold 技能，读取 @schema.mysql.sql，
生成 Flask/FastAPI 分层脚手架代码。
```

> `database-schema-designer` 不会替你执行 DDL，也不会生成后端代码；`sql-to-*` 也不会执行 DDL。建表这件事由你在目标数据库上完成。

---

## 8. 常见问题

**问：技能一直追问，能不能少问几轮？**

答：短需求默认最多 4 轮，详细规格说明书最多 2 轮，这是技能的上限。想直接出结果就说「直接设计」，它会用假设补齐。

**问：为什么脚本里没有 `FOREIGN KEY`？**

答：这是刻意设计。技能只声明引用列（如 `category_id`）并单独建索引，把 `ON DELETE` 意图写进设计文档，由服务层执行。只有你明确要求时才补外键迁移。

**问：能不能只生成一份「通用」脚本，两个数据库都能跑？**

答：不能，技能会拒绝这种做法。PostgreSQL 和 MySQL 的类型、时间语义、索引能力差异很大，一份「最低公共分母」脚本在两边都不理想。

**问：字段注释有什么用？**

答：注释写的是字段的业务含义（存什么、单位、取值范围），不是重复字段类型。它是交付物的一部分：没有注释的表或字段会被技能视为缺陷。

**问：装错了目录名怎么办？**

答：把目录名改回 `database-schema-designer`，重启 CodeBuddy 让技能重新扫描。

---

## 9. 参考资料与署名

- 技能本体：`requirements_analysis/database-schema-designer/`
- 本技能改编自 [OneWave AI 的 database-schema-designer](https://github.com/OneWave-AI/claude-skills/tree/main/database-schema-designer)（MIT License，Copyright (c) 2025 OneWave AI），署名与修改说明见技能目录里的 `NOTICE` 和 `LICENSE`。
- 本仓库的使用约定见 [README.md](../README.md)。
