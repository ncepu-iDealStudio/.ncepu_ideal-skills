# 本地检索工具契约（Local Search Contract）

本文件是 `resources/tools/mwg.py` 与 `resources/tools/build_index.py` 的**行为约定**，
也是把上游 `SKILL.md` 工作流从 `npx modern-web-guidance@latest` 迁移到本地工具时的
**唯一映射依据**。实现者（AI 智能体）与工具之间按此契约交互。

## 1. 为什么需要本地工具

上游技能依赖 `npx -y modern-web-guidance@latest ...`：

- 需要**联网**从 npm 拉取包（离线/沙箱环境会超时）；
- 会向 Google 发送**匿名遥测**（安装量、检索词、retrieve 的 guide id）；
- CLI 源码（`modern-web.mjs`）**不在上游仓库里**，无法审计或随本仓库分发。

本技能改为**随仓库自带的零依赖 Python 工具**：

- 完全离线、仅用 Python 标准库、无遥测、可审计；
- 指南全文 `resources/guides/` 随仓库分发，检索基于本地索引；
- 上游 CLI 的 `search` / `retrieve` / `list` 三个核心能力一一对应。

## 2. 文件职责

| 文件 | 角色 | 是否可重建 |
| :--- | :--- | :--- |
| `resources/guides/**/*.md` | 209 份指南**原文**（CC-BY 4.0），内容源，永不手工修改 | 否（源） |
| `resources/guides_index.json` | 派生索引：`id / category / path / title / summary / keywords` | 是 |
| `resources/tools/build_index.py` | 扫描 `guides/` 重建索引 | 工具 |
| `resources/tools/mwg.py` | 本地检索 CLI：`search / retrieve / list / categories` | 工具 |

> 索引是**派生文件**：更新、增删或翻译指南后，必须重跑 `build_index.py`。
> 检索结果以索引为准，但 `retrieve` 永远从 `guides/` 读取最新全文。

## 3. 命令契约

所有命令在技能目录 `modern-web-guidance/` 下执行（也可用绝对路径调用 `mwg.py`）：

```sh
python3 resources/tools/mwg.py search "<2-5 词查询>" [-n 8] [--json]
python3 resources/tools/mwg.py retrieve "<id>[,<id>...]"
python3 resources/tools/mwg.py list [分类] [--json]
python3 resources/tools/mwg.py categories
python3 resources/tools/build_index.py        # 重建索引
```

### `search`
- **输入**：一个 2–5 词、动作导向、**单一** Web 平台能力或 UI 模式的查询。
  - 省略框架名（React/Vue/Tailwind）与业务名词（产品、路由、文件名）。
  - 多特性任务拆成多次 `search`。
  - 把领域意图翻译成隐含的 UI 原语："删除前确认" → `"confirmation modal dialog"`。
- **中文查询**：`mwg.py` 内置中文→英文同义词映射（`ZH_MAP`），可直接用中文检索；
  英文查询同样有效。
- **输出**：按相关度排序的 `[{id, category, title, summary, score}]`（默认 8 条）。
- **退出码**：`0` 有结果，`2` 无结果（此时按 SKILL.md 第 1 步策略**改写一次查询**再搜，
  或用 `list` 浏览主题），其他为参数/索引错误。
- **判定**：按 `title` 与 `summary` 判断是否匹配；命中就直接 `retrieve`，**不要**再 `list`。

### `retrieve`
- **输入**：一个或多个逗号分隔的 `id`（`id` = 指南文件名去掉 `.md`）。
- **输出**：对应指南**全文**（不截断），并在开头附一行
  `<!-- id | category | source: 相对路径 -->` 便于溯源；多个 id 之间用分隔线隔开。
- **退出码**：`0` 成功；`1` 有 id 不存在或文件缺失（错误信息列出已知 id 的查看方式）。
- **大文件**：全文一次性输出。若终端输出被截断，改用文件读取工具直接读
  `resources/guides/<path>`（从索引的 `path` 字段得到），不要用 `head`/`cat` 截断后臆断。

### `list` / `categories`
- `categories` 列出 17 个分类及计数；`list [分类]` 列出该分类下全部 `id → title`。
- 用于「广泛 UI 审计」或 `search` 两次改写仍无结果时浏览目录。

## 4. 上游命令 → 本地命令映射

阅读指南时，正文里常出现形如
`npx -y modern-web-guidance@latest retrieve "<id>"` 的交叉引用。
**这些引用一律按下表在本地执行，禁止联网调用 npx**：

| 上游（原文中出现的） | 本地等价命令 |
| :--- | :--- |
| `npx -y modern-web-guidance@latest search "<q>" [--skill-version …]` | `python3 resources/tools/mwg.py search "<q>"` |
| `npx -y modern-web-guidance@latest retrieve "<id>"` | `python3 resources/tools/mwg.py retrieve "<id>"` |
| `npx -y modern-web-guidance@latest list` | `python3 resources/tools/mwg.py list` |
| `npx -y modern-web-guidance@latest legacy-scan <path> --json` | **不提供**（依赖上游未开源的确定性规则库，见第 6 节） |
| `set-allow-origin-trials` / `set-allow-volatile-features` / `.mwgrc` | **不提供**（上游按 Baseline 对实验特性做 retrieve 门禁，见第 5 节） |

## 5. 浏览器支持 / 实验特性策略

上游对「Origin Trial」「volatile 特性」有 `retrieve` 门禁（需 `.mwgrc` 解锁）。
本地工具**不做门禁**，因为本仓库分发的指南是上游 v1.0.0 的公开快照，不含被门禁隐藏的内容。
实现者仍需遵守通用策略（见 `SKILL.md`「浏览器支持与回退」）：

- 默认假定 **Baseline Widely available** 特性无需回退；
- 非 Widely available 特性**必须**按指南的「Fallback strategies」章节给出轻量回退，
  除非用户在 `AGENTS.md` / `CLAUDE.md` 里声明了自定义浏览器支持策略；
- 指南里逐条列出的 Baseline 状态与浏览器版本是判断依据。

## 6. 不提供的能力与边界

- **`legacy-scan`**：依赖上游未开源的确定性遗留规则库；本技能不移植。
  用户要求「全库现代化扫描」时，改用 `list` 人工圈定相关指南 + 逐文件核对。
- **语义/向量检索**：本地用「关键词加权 + 前缀 + 中文同义词映射」近似，
  不追求上游离线 embedding 的语义召回；因此 `search` 查询务必用**具体的 HTML/CSS/UI 名词**。
- **框架适配**：指南是原生 HTML/CSS/JS；迁移到框架时保留现代特性，不要退回旧写法
  （具体见 `SKILL.md`「框架适配」）。

## 7. 索引格式（`guides_index.json`）

```json
{
  "meta": {
    "schema_version": 1,
    "generated_at": "YYYY-MM-DD",
    "source": "GoogleChrome/modern-web-guidance @ <commit>",
    "guide_count": 209,
    "guides_dir": "resources/guides"
  },
  "categories": { "css": 18, "performance": 26, "...": "..." },
  "guides": [
    {
      "id": "light-dismiss-a-dialog",
      "category": "ui-behaviors",
      "path": "ui-behaviors/light-dismiss-a-dialog.md",
      "title": "Light-Dismiss a Dialog",
      "summary": "Modern modal dialogs often support ...",
      "keywords": ["light", "dismiss", "dialog", "closedby", "..."]
    }
  ]
}
```

- `id` 全局唯一、等于文件名（去掉 `.md`）；`path` 是相对 `guides/` 的 POSIX 路径。
- `title` 取首个 Markdown 标题，`summary` 取第一段正文，`keywords` 由标题/各级标题/摘要/
  id/分类名分词去重得到（去停用词、保留技术缩写如 INP/LCP/CLS）。
- 字段可读性优先；`mwg.py` 只读这些字段，不依赖任何外部库。

## 8. 更新指南后的操作流程

1. 用上游新版 `skills/modern-web-guidance/guides/` 覆盖本地 `resources/guides/`
   （保持英文原文，除非决定翻译——翻译需在 `ATTRIBUTION.md` 声明「已修改」）。
2. 重跑 `python3 resources/tools/build_index.py`。
3. 核对 `guide_count` 与分类计数；抽样 `search` / `retrieve` 验证。
4. 更新 `ATTRIBUTION.md` 顶部的 commit 与版本号。
5. 如上游 `SKILL.md` 工作流有变化，评估是否需要同步本技能 `SKILL.md`。

## 9. 验收清单

- [ ] `guide_count` 与 `resources/guides/` 下 `.md` 文件数一致
- [ ] 每个索引条目的 `path` 对应真实存在的文件
- [ ] `search "light dismiss dialog"` 首条为 `light-dismiss-a-dialog`
- [ ] `retrieve "dialog"` 输出非空且包含 `# Dialog` 标题
- [ ] 中文查询（如「暗色」「响应式表格」「通行密钥」）能返回相关结果
- [ ] `retrieve "不存在的 id"` 以退出码 1 报错
- [ ] 全程无网络请求、无遥测
