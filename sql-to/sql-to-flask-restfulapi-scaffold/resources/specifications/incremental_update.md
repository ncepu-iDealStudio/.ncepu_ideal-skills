# 已有项目的增量更新规范（新增表 / 表结构变更 / 表下线）

> 适用场景：目标 Flask 项目的骨架**已经生成过**，现在用户提供了新的 DDL 或修改后的 DDL。
>
> 本规范配套 `resources/config/incremental_change_policy.json` 使用。**每次增量任务开始前必须先读策略文件**。

---

## 1. 三种场景与判定

| 场景 | 判定条件 | 技能动作 |
|---|---|---|
| **新增表** | 骨架已存在，该表 7 类文件**全部不存在** | 按表生成文件 + 幂等追加注册 |
| **表结构变更** | 骨架已存在，该表**任一**文件已存在 | 先做字段级差异分析，再分层更新 |
| **表下线** | 用户明确要求移除/下线 | 只输出待删清单，**不执行删除** |

### 判定要点

- 骨架是否存在，看这四项：`manage.py`、`app/__init__.py`、`models/__init__.py`、`api_1_0/__init__.py`
- **「用户又给了一遍建表 SQL」≠ 重新建表**：只要该表文件已存在，就必须走「表结构变更」
- 一次给多张表时**逐表判定**，允许同批混用「新增表」与「表结构变更」
- 残留文件不成套（如只剩 `models/` 与 `controller/`）→ **先询问用户**补齐还是重生成

---

## 2. `alter_table`：差异识别（强制）

### 2.1 取得旧结构

按以下优先级尝试，取到即停：

1. 用户提供的旧版 `CREATE TABLE` / `CREATE VIEW`
2. 项目内 `database/*.sql` 的建表语句
3. `models/{module_name}.py` 的 `Column` 定义（解析类型、nullable、default、comment）
4. `controller/{class_name}Controller.py` 的字段使用（**仅辅助交叉校验**，不作为主依据）
5. （**仅用户同意时**）`information_schema` 查询

**取不到就问用户，禁止猜测差异。**

### 2.2 归一化后逐字段对比

比对前先做归一化，避免误报：

| 归一化项 | 处理 |
|---|---|
| 大小写、反引号 | 忽略 |
| 列顺序 | 忽略 |
| 驼峰 vs 下划线 | 视为等价（`userName` == `user_name`），**输出以 SQL 原字段名为准** |
| 类型别名 | `INT`/`INTEGER` 等同；`TINYINT(1)`/`BOOLEAN` 等同 |
| 软删 / 状态位 | **按最新 SQL 重新计算**，不沿用旧结论 |

### 2.3 输出差异清单（先给用户看，再动手）

```text
📋 结构差异：student（表）

风险等级：⚠️ HIGH（含删除列）

新增字段
  + gender  varchar(10)  性别

删除字段
  - agenda  text         日程   ⚠️ 该字段在代码中被引用 3 处

类型变更
  ~ phoneNumber  varchar(20) → varchar(500)

约束变更
  ~ isDelete  NOT NULL → NULL

标记变化
  !

注释变更
  # age  仅注释变化

确认继续？
```

**规则**：

- 差异清单必须先展示，用户确认后才动手
- `critical` / `high` 风险项**必须**逐个确认
- 出现 `removed + added` 且字段语义相近 → **先问是重命名还是删旧加新**

---

## 3. 影响面矩阵（速查）

| 变更类型 | `models/` | `controller/` | `service/` | `Resource/` + `urls.py` | `api_1_0/__init__.py` | README |
|---|---|---|---|---|---|---|
| 新增字段 | 🔄 覆盖 | 🔄 覆盖 | 📝 待办 | 📝 待办 | — | 📝 待办 |
| 删除字段 | 🔄 覆盖 | 🔄 覆盖 | 📝 待办 | 📝 待办 | — | 📝 待办 |
| 改字段类型 | 🔄 覆盖 | 🔄 覆盖 | 📝 待办 | 📝 待办 | — | 📝 待办 |
| 改可空/默认/唯一 | 🔄 覆盖 | 🔄 覆盖 | 📝 按需 | — | — | 📝 按需 |
| 主键变更 | 🔄 覆盖 | 🔄 覆盖 | 📝 待办 | 🔄 覆盖 | ⚠️ 可能变 | 📝 待办 |
| 软删字段变化 | 🔄 覆盖 | 🔄 覆盖 | 📝 **必须** | — | — | 📝 **必须** |
| 状态位增删 | 🔄 覆盖 | 🔄 覆盖 | ⚠️ 确认后追加 | 🔄 覆盖 | — | 📝 待办 |
| 视图定义变化 | 🔄 覆盖 | 🔄 覆盖 | 📝 按需 | 📝 按需 | — | 📝 按需 |

图例：🔄 可覆盖 ｜ 📝 只输出待办（不覆盖）｜ ⚠️ 需用户确认 ｜ — 不动

### 3.1 三条最容易出事的同步规则

漏一条就会运行期报错：

#### 规则一：状态位「同进同退」

`Controller` 的状态更新入口、`Resource` 的路由、`Service` 的业务校验**必须同步**。

若 `Service` 需要补业务校验（如"停用前检查关联数据"）：

```text
1. 展示待追加的代码片段
2. 取得用户明确同意
3. 只追加到 service 文件的业务逻辑区
4. 用户不确认 → 报告中写明「状态接口缺少业务校验」
```

#### 规则二：软删字段要改三处

- `models/`：字段定义（可覆盖）
- `controller/`：`get`/`update` 的过滤条件、`delete` 的软删分支（可覆盖）
- `service/`：**手写文件里的跨表查询条件**（只能列待办）

> Service 里任何写了 `is_delete == 0` 的查询都要跟着改。这是最容易漏的地方。

#### 规则三：主键变更会穿透所有层

主键影响：`models` 定义 → `controller` 方法参数 → `Resource` 路径参数 → `urls.py` 的 `url_item` 模板 → 前端契约。

**必须全链路核对**，不能只改 model。

---

## 4. 文件归属与覆盖规则

| 文件 | 标记 | 覆盖策略 |
|---|---|---|
| `models/{module_name}.py` | `【AUTO-GENERATED】` | 直接覆盖 |
| `controller/{class_name}Controller.py` | `【AUTO-GENERATED】` | 重生成标准 CRUD 方法，**保留手写方法** |
| `service/{class_name}Service.py` | `【HAND-WRITTEN】` | **绝不覆盖**，输出待办 |
| `api_1_0/{slug}Resource/{slug}Resource.py` | `【AUTO-GENERATED】` | 重生成 CRUD，保留自定义路由 |
| `api_1_0/{slug}Resource/{slug}OtherResource.py` | `【HAND-WRITTEN 占位】` | **绝不覆盖** |
| `api_1_0/{slug}Resource/urls.py` | `【AUTO-GENERATED】` | 直接覆盖 |
| `api_1_0/{slug}Resource/__init__.py` | `【AUTO-GENERATED】` | 直接覆盖 |
| `api_1_0/__init__.py` | marker 区块 | 幂等追加 |
| `app/`、`config/`、`utils/`、`static/` | 无标记 | **完全不碰** |

**判定补充**：文件存在但**没有** `【AUTO-GENERATED】` 标记 → 视为用户已手改，**禁止覆盖**。

### 4.1 确需向 Service 追加代码时

```text
⚠️ 需要向手写文件追加代码

文件：service/StudentService.py
原因：新增 status 字段，需要停用前的关联校验

将追加以下内容（仅追加，不修改已有代码）：

────────────────────────────────
    def change_status(self, pk, status):
        """变更学生状态（脚手架追加）"""
        if status == 0:
            # 停用前校验
            ...
────────────────────────────────

确认追加？(yes/no)
```

---

## 5. `add_table`：注册与幂等（强制）

新表必须在 `api_1_0/__init__.py` 注册，否则蓝图不生效、路由 404。

### 5.1 注册位置

```python
# ==AUTO_IMPORTS_START==
from api_1_0.studentResource import student_blueprint
# ← 在 END 之前追加
# ==AUTO_IMPORTS_END==

ROUTER_REGISTRY = [
    # ==AUTO_REGISTRY_START==
    (student_blueprint, "/api_1_0"),
    # ← 在 END 之前追加
    # ==AUTO_REGISTRY_END==
]
```

### 5.2 幂等要求

- 追加前检查该 blueprint 是否**已存在**于 `ROUTER_REGISTRY`
- 同一份 SQL 重复生成 → **零 diff**
- `__init__.py` 里的 marker 被删除或改写 → **不自动修改文件**，输出待办并告警

---

## 6. 数据库迁移边界

技能**不做**：

- 执行任何 DDL
- 改写 `database/` 下的 SQL
- 接入 Alembic 等迁移框架
- 删除或修改数据

技能**要做**：

- 在报告中给出 MySQL `ddl_hint`
- 提示发布顺序：
  - **加列** → 先 DDL，后发代码（旧代码不认识新列，不影响）
  - **删列** → 先发代码（不再引用该列），后 DDL
  - **改类型** → 视兼容性，必要时双写过渡
- 提示备份与回滚

---

## 7. 执行顺序（`alter_table`）

```text
1. 判定模式（确认是 alter_table）
        ↓
2. 取旧结构 → 归一化 → 逐字段比对 → 输出差异清单
        ↓
3. 用户确认（high/critical 必确认）
        ↓
4. 按影响面矩阵逐层更新
   ├─ 覆盖：models / controller / resource / urls
   ├─ 追加：api_1_0/__init__.py（幂等）
   └─ 待办：service / OtherResource / README
        ↓
5. 输出报告（含 DDL 建议与待办清单）
        ↓
6. 用户执行 DDL（技能不执行）
        ↓
7. 验证
```

---

## 8. 验证清单

```bash
# 1) 导入自检（最易暴露 blueprint 缺失、循环导入）
python -c "from app import create_app; app = create_app('develop')"

# 2) 路由自检
flask routes | grep <resource_slug>

# 3) 全量回归
pytest -q

# 4) 变化字段最小冒烟
#    POST 写入 → GET 详情 → PUT 更新 → DELETE

# 5) 幂等自检：同一 SQL 再跑一次，确认零 diff
```

---

## 9. 变更报告模板（输出给用户）

```markdown
## ✅ 增量更新完成：student（表结构变更）

### 运行模式
`alter_table`（骨架已存在，models/student.py 等 7 个文件已存在）

### 结构差异
| 类型 | 字段 | 详情 | 风险 |
|---|---|---|---|
| 新增 | gender | varchar(10) | low |
| 删除 | agenda | text | **high** ⚠️ |
| 类型变更 | phoneNumber | varchar(20)→(500) | medium |

### 文件更新
| 文件 | 动作 |
|---|---|
| models/student.py | 🔄 已覆盖 |
| controller/StudentController.py | 🔄 已重生成 CRUD |
| api_1_0/__init__.py | ✅ 无变化（路由未变） |
| service/StudentService.py | 📝 待办（见下） |
| README.md | 📝 待办 |

### 人工待办
1. `service/StudentService.py` 第 42 行：跨表查询中的 `isDelete == 0` 需确认字段名
2. 全局搜索 `agenda`，移除 3 处引用（清单见附）
3. `README.md` 字段表补 `gender`

### DDL 建议
```sql
ALTER TABLE student ADD COLUMN gender varchar(10) COMMENT '性别';
ALTER TABLE student MODIFY COLUMN phoneNumber varchar(500) COMMENT '手机号码';
-- ⚠️ agenda 删除需先完成代码清理
```

**发布顺序**：先执行 ADD/MODIFY，验证通过后再执行 DROP COLUMN。

### 验证结果
- ✅ 导入自检通过
- ✅ 路由自检通过（`/api_1_0/student` 存在）
- ⚠️ 回归测试待用户执行（需先完成待办）
```

---

## 10. 与既有策略的关系

| 既有机制 | 在增量场景下的处理 |
|---|---|
| `generation_profiles.json` | 仍用于决定生成档位，不影响增量判定 |
| `router_registry_merge_strategy.md` | 增量的注册幂等**沿用**该文档的 marker 规则 |
| 文件冲突策略（跳过已存在实体文件） | **被本规范细化**：不再一律跳过，改为按文件归属分级处理 |
| `field_rendering_rules.md` | 渲染单个字段时仍遵循，本规范只管"哪些字段要重渲染" |
