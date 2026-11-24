# md-prd-to-html-prototype 多端多页原型技能增强设计

- 日期：2026-11-16
- 状态：设计已确认，待用户审查规格
- 范围：对 `md-prd-to-html-prototype` 技能做架构级增强

## 1. 背景与目标

### 1.1 现状

- 技能本体仅 `md-prd-to-html-prototype/SKILL.md`（70 行），无 README、脚本、模板或规范层。
- 当前行为：读取本地 Markdown 需求文档，生成**一个**内联 CSS/JS 的单文件 HTML 原型，固定写到源 MD 同级目录，命名为 `原型-{系统名称}.html`。
- 现有 SKILL.md 存在内部矛盾：声称"完全离线、无外部资源"，却强制使用 Tailwind CSS CDN。
- 另有一份副本 `.workbuddy/skills/md-prd-to-html-prototype/SKILL.md`（81 行），前 70 行与根目录版一致，多出一节"与 modern-web-guidance 叠加"。两份均被 git 跟踪；README 与 README.en.md 仅登记 `.workbuddy` 副本。

### 1.2 优化需求（原文 6 点）

1. 针对用户输入的 md 格式系统需求设计文档，生成需要的静态页面原型。
2. 根据需求分析文档，系统可能需要前台、后台、甚至移动端原型；让用户选择先生成哪个端。
3. 用户选端后，进一步询问生成单页原型还是多静态页原型。
4. 用户选择后执行生成，分文件夹存放：前台 `www/`、后台 `admin/`、移动端 `app/`。
5. 原型页面含 HTML+CSS+JS，除模拟数据外还需实现交互示例效果。
6. 最终原型均可通过本地浏览器直接打开查看与操作。

### 1.3 已确认的设计决策

| # | 决策点 | 结论 |
|---|--------|------|
| D1 | 输出根目录 | 生成前由用户指定一个"原型根目录"，三端为其子目录；支持后续分次续写 |
| D2 | 单页 / 多页定义 | 单页 = 一个 HTML 含全部视图（菜单切换）；多静态页 = 每页独立 HTML + 真实 `href` 跳转 + `index.html` 入口 |
| D3 | 样式依赖 | 完全离线：手写精简 CSS 与 JS 全部内联，不用 CDN、无外部字体/图片 |
| D4 | 候选端识别 | 技能先分析 MD，按角色/页面列出候选端让用户勾选并指定"先生成哪个" |
| D5 | 跨端状态 | 在原型根目录写 `_原型说明.md`，记录系统名、角色、数据字典、端与页面清单、Mock 约定、生成历史；后续先读再续写 |
| D6 | 交互深度 | 在现有四类基础上扩展：页间跳转、表单必填校验、状态切换、列表增改删的 Mock 联动 |
| D7 | 组织方案 | 方案 C：`SKILL.md` 主干 + `references/` 三份规范 + `scripts/` 校验器与单测 + README |

## 2. 架构与文件布局

```
md-prd-to-html-prototype/                # canonical 版本（根目录）
├── SKILL.md                            # 主干：触发条件 + 6 步工作流 + 决策门（约 120 行）
├── README.md                           # 人读说明（当前缺失，补齐）
├── references/
│   ├── output-contract.md              # 目录契约：www/admin/app、命名、index、_原型说明.md
│   ├── interaction-contract.md         # 离线 HTML 骨架 + 交互清单 + Mock 数据规范
│   └── intake-and-state.md             # 端识别问题 + [NEEDS CLARIFICATION] + 状态文件格式
└── scripts/
    ├── validate_prototype.py           # 纯标准库校验器（exit 0/1/2）
    └── test_validate_prototype.py      # 校验器单测
```

**副本同步策略：**

- 根目录版本为 canonical。
- `.workbuddy/skills/md-prd-to-html-prototype/` 副本保留其"与 modern-web-guidance 叠加"节，其余内容与 canonical 同步；同步时该叠加节更新为反映多端/多页场景的表述（仍保持离线与内联约束不变）。
- README.md 与 README.en.md 中该技能的描述、安装位置、结构树条目同步更新：登记根目录 canonical 与 `.workbuddy` 安装副本两处。
- `modern-web-guidance/README.md` 中相关条目仅在该技能文件结构变化需要时更新；本设计不强制改动其内容。

**职责边界（SRP）：**

- `SKILL.md`：编排流程、提出决策问题、指定何时读哪份 reference、指定何时运行校验脚本。不重复具体格式规范。
- `references/*`：单一主题的详细契约，供 AI 按需读取。
- `scripts/validate_prototype.py`：唯一可执行的硬约束检查点，只做校验，不生成、不修改产物。
- `_原型说明.md`：跨调用状态载体，由技能读写，不由校验器写。

## 3. 工作流与决策门

`SKILL.md` 定义 6 步工作流，包含 4 个决策门：

```
步骤 1 确认输入
  - 询问并确认：本地 MD 路径 + 原型根目录路径（D1）
  - 读取 MD 全文，解析：系统名称、目标角色、页面清单、字段、按钮/弹窗、表格列、筛选条件、交互
  - 门①：若页面或字段信息缺失 → 输出 [NEEDS CLARIFICATION] 清单并停止，不生成
步骤 2 分析候选端
  - 按角色与页面判断 www / admin / app 中哪些与该系统相关
  - 门②：列出候选端，让用户勾选要生成的端，并指定"本次先生成哪个端"
步骤 3 选择生成模式
  - 门③：让用户二选一：单页（一个 HTML 内多视图切换） or 多静态页（每页 HTML + index.html）
步骤 4 读取/建立状态
  - 若 <原型根>/_原型说明.md 存在 → 读取并续写；否则按 intake-and-state.md 新建
步骤 5 生成
  - 只在用户本次选中的端目录下产出 HTML；同步更新 _原型说明.md
  - 遵循 interaction-contract.md 的离线与交互要求
步骤 6 自检与交付
  - 运行 python <技能>/scripts/validate_prototype.py <原型根> --expect-side <端> --mode <single|multi>
  - 输出摘要：原型文件路径、本次生成端、页面清单、已实现交互、待确认业务点
```

**关键规则：**

- 每次调用**只生成一个端**（用户本次选中的端），其余端留待后续调用，实现"分次续写"。
- 三端目录名固定为 `www/`、`admin/`、`app/`，且仅位于用户指定的原型根目录下。
- 步骤 2 与步骤 3 的问题**每次都必须问**，即使状态文件里已有记录；状态文件只用于复用分析结论与数据约定，不跳过用户确认。

## 4. 输出目录与状态文件契约

```
<用户指定的原型根目录>/
├── _原型说明.md
├── www/       # 前台（仅当生成过前台时存在）
│   ├── index.html                     # 多页模式：导航入口；单页模式：唯一主文件
│   └── pages/*.html                   # 多页模式：每页一个 HTML
├── admin/     # 后台管理（仅当生成过后台时存在）
└── app/       # 移动端（仅当生成过移动端时存在）
```

**_原型说明.md 必含小节：**

1. 系统名称与一句话定位
2. 目标角色清单
3. 候选端与已生成端（含生成时间）
4. 页面清单（按端分组，标注单页/多页模式）
5. 数据字典与 Mock 数据约定（字段名、类型、示例值、状态枚举）
6. 待确认业务点（[NEEDS CLARIFICATION] 汇总）
7. 生成历史（每次调用：时间、端、模式、产出文件）

**多页模式内部链接规则：**所有本地 `href` 必须指向实际存在的 HTML 文件；`index.html` 必须存在并链接到该端所有页面。

## 5. 离线 HTML 与交互契约

### 5.1 页面骨架（每个 HTML 必须满足）

- `<!DOCTYPE html>`、`lang="zh-CN"`、`<meta name="viewport">`、有意义的 `<title>`。
- 全部 CSS 写在 `<style>` 内，全部 JS 写在 `<script>` 内。
- 禁止：CDN 链接、`<link rel="stylesheet">`、`<script src=...>`、外部字体、外部图片 URL。
- 图标使用 Unicode 字符或内联 SVG。
- Mock 数据以 JS 对象/数组写在 `<script>` 中，字段贴近业务场景。

### 5.2 必须实现的交互

1. 导航：单页模式用菜单切换视图；多页模式用真实 `<a href>` 跳转，且 `index.html` 可达所有页面。
2. 弹窗：新增/编辑 modal 的打开与关闭。
3. 表格：筛选 + 重置。
4. 表单：提交时必填校验与提示。
5. 状态：状态标签可切换（如"待处理 → 已通过"）。
6. Mock 联动：列表的新增/编辑/删除真实改动内存数据并刷新表格。
7. 操作反馈：提交成功 toast。

### 5.3 移动端（`app/`）额外约束

- 固定 375px 宽度手机视口居中展示。
- 底部 Tab 栏导航。
- 卡片式列表替代宽表格。
- 仍满足全部离线约束，双击可打开。

### 5.4 与设计包技能的关系

写弹窗、表单、表格、键盘操作前，`.workbuddy` 副本按既有叠加节先检索 `modern-web-guidance`；检索结果只用于改进交互细节，不改变本技能的"单端/多端、单页/多页、完全内联、低保真"约束。canonical 根目录版保持自包含，不硬编码该叠加步骤（避免安装位置耦合）。

## 6. 校验脚本设计

**文件：** `scripts/validate_prototype.py`，Python 3 标准库实现，无第三方依赖。

**用法：**

```
python scripts/validate_prototype.py <原型根目录> [--expect-side www|admin|app] [--mode single|multi]
```

**退出码：** 0 = 全部通过；1 = 存在校验错误；2 = 用法错误（参数缺失、路径不存在）。

**校验项：**

1. 目录层：`<原型根>/_原型说明.md` 存在；若给了 `--expect-side`，只允许该端目录存在变化；只接受 `www`/`admin`/`app` 三个端目录名。
2. HTML 结构：每个 HTML 含 DOCTYPE、`lang="zh-CN"`、viewport、非空 `<title>`。
3. 离线：无 `http://` 或 `https://` 外链；无 `<link rel="stylesheet">`；无 `<script src=...>`；无外部字体/图片 URL。
4. 资源内联：有 `<style>` 与 `<script>`；检测到 Mock 数据标识（如 `const MOCK_` 或等价 JS 数据结构）。
5. 多页模式（当 `--mode multi`）：`index.html` 存在；所有本地 `href` 指向存在的 HTML 文件，无断链。
6. 交互最低保证：存在 modal、filter/reset、toast、必填校验（`required` 或等价）相关实现标记。
7. 状态文件：`_原型说明.md` 记录了本次生成的端与页面。

**错误报告格式：** 逐条输出 `[ERROR] <相对路径>: <问题>` 到 stdout，便于 AI 读取后修正；全部通过时输出 `OK: N checks passed`。

## 7. 测试策略

- `scripts/test_validate_prototype.py`：用 `tempfile` 构造干净样例与各类违规样例（外链、断链、缺 style/script、缺状态文件、错误端目录），断言退出码 0/1/2 与错误文本。使用 `unittest`（标准库），不引入 pytest 依赖。
- 端到端手工验证：用一份示例 MD 走完整流程，生成单页/多页各一端，浏览器打开确认可交互；再运行校验器确认通过。
- 不新增仓库级测试目录改动；测试文件随技能放在 `scripts/` 下。

## 8. 范围外（不做）

- 不实现真实后端、真实鉴权或数据持久化。
- 不引入高保真视觉设计或设计包选择机制。
- 不改动 `prd-html-skill`、`common-website-design` 等其他技能。
- 不新增 Python 第三方依赖；校验器仅用标准库。
- 不在一次调用中生成多个端（保持"每次一端"的分次续写模型）。
