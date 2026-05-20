# 生成企业级脚手架项目的混合 SKILL 设计方法

## 1. 背景与问题定义

在企业级后端项目中，过去常用“固定模板 + 少量参数替换”生成脚手架。该方式在稳定场景下高效，但当业务规则、技术栈、命名规范、增量演进需求变复杂时，模板模式会遇到三个核心问题：

在基于 AI 大模型进行企业级项目开发的今天，团队越来越依赖模型来提升交付效率。但“生成更快”并不等于“工程可用”。企业真实场景通常要求代码必须满足架构分层、编码规范、安全基线、可运维性和可审计性等多重约束。这意味着我们不仅要关注模型是否能生成代码，更要关注生成结果是否稳定、可控、可验证、可持续演进。

在这一背景下，Skill 技术逐步成为连接“大模型能力”和“工程治理要求”的关键约束手段。它通过规则、规范、模板和回归机制，把模型输出纳入可治理的工程流程，使“智能生成”与“规范落地”不再冲突。本项目的研究价值就在于：探索一条可复制的混合方法，让企业既能获得 AI 生产力，又能保持架构一致性与质量确定性。

1. 适配能力弱：难以覆盖多样 SQL 风格、混合命名和差异化项目约束。
2. 增量能力弱：已生成项目二次生成容易覆盖人工改动，合并风险高。
3. 质量治理弱：缺少可重复验证链路，生成结果稳定性依赖人工检查。

因此，本方案提出“混合 SKILL 设计方法”：

- 用确定性资产（规则、规范、模板）保证可控性。
- 用智能生成（上下文推理、策略编排）提升适配性。
- 用回归与快照机制保障可演进性。

---

## 2. 目标与非目标

### 2.1 目标

1. 能从 SQL DDL 生成企业级分层接口脚手架。
2. 支持首次全量生成 + 后续增量生成。
3. 具备一键回归能力（生成、校验、渲染、合并、覆盖率、快照）。
4. 通过“资产化”方式支持版本演进和团队协作。

### 2.2 非目标

1. 不追求覆盖所有 SQL 方言和极端语法。
2. 不在 V1 阶段自动生成复杂业务逻辑。
3. 不替代团队架构决策，仅提供标准化脚手架基线。

---

## 3. 设计原则

1. 规范先于实现：先定义契约和策略，再编写模板与工具。
2. 可验证优先：每次生成都可被自动校验和回归。
3. 增量安全优先：不破坏人工代码，优先合并而非覆盖。
4. 分层解耦：配置层、规范层、模板层、工具层分离。
5. 演进友好：每个资产可单独版本化与替换。

---

## 4. 与传统模板方案对比

| 维度 | 传统模板生成 | 混合 SKILL 方案 |
|---|---|---|
| 生成方式 | 固定模板替换 | 规则 + 规范 + 模板 + 工具编排 |
| 灵活性 | 中低 | 高 |
| 增量生成 | 弱，易冲突 | 强，支持合并策略 |
| 质量保障 | 依赖人工 | 可自动校验、回归、快照 |
| 维护成本 | 低起步，高后期 | 中高起步，低长期风险 |
| 团队治理 | 难统一 | 易标准化与审计 |

结论：

- 对一次性、小规模项目，传统模板仍有成本优势。
- 对企业级、长期演进项目，混合 SKILL 方案更优。

---

## 5. 混合 SKILL 总体架构

### 5.1 分层模型

1. 配置层（config）
- 命名规则、类型映射、生成档位、上下文样例。

2. 规范层（specifications）
- 代码规范、SQL 解析契约、字段渲染规则、路由合并策略。

3. 模板层（templates）
- 项目骨架模板 + 分层代码模板（model/dao/service/resource）。

4. 工具层（tools）
- 上下文生成、校验、预览、渲染、路由合并、快照比较、流水线执行。

5. 产物层（demo_output）
- context、渲染结果、manifest、回归报告、快照基线。

### 5.2 数据流

1. SQL 输入 -> 2. context 生成 -> 3. context 校验 -> 4. 生成计划预览 -> 5. 模板渲染 -> 6. 路由增量合并 -> 7. 回归报告输出 -> 8. 快照比对。

---

## 6. 关键能力设计

### 6.1 SQL 到 Context 自动抽取

目标：把 SQL 解析结果转换为统一中间语义（context），作为所有模板与工具的唯一输入。

收益：

1. 统一语义入口，避免模板直接耦合 SQL 细节。
2. 支持后续扩展更多输入源（DDL 文本、数据库元数据、迁移脚本）。

### 6.2 增量合并机制

目标：在不破坏人工代码的前提下更新路由注册。

策略：

1. marker 区域内自动维护 import 与 registry。
2. 去重、排序、幂等执行。
3. 缺少 marker 时输出告警并跳过/降级。

### 6.3 一键回归流水线

目标：单命令触发完整链路，保证每次变更可验证。

流水线步骤建议：

1. 生成 context
2. 校验 context
3. 预览生成计划
4. 渲染预览产物
5. 路由合并预演
6. 覆盖率计算
7. 快照校验

### 6.4 快照防回归

目标：将关键产物（context、manifest）基线化，避免无感变更。

策略：

1. compare 模式：检测差异并失败。
2. update 模式：在预期变更场景刷新快照。

---

## 7. 质量门禁（Quality Gates）

建议将以下门禁作为“可发布”条件：

1. context 校验通过。
2. 一键流水线全步骤通过。
3. 覆盖率达到目标阈值（当前基线 100%）。
4. 快照比较通过。
5. 回归报告生成且状态为 PASS。

---

## 8. 版本策略与协作规范

### 8.1 版本策略

1. SKILL 版本：语义化版本（如 V1.0 / V1.1）。
2. 规则与模板版本可独立演进。
3. 每次版本升级必须附带回归报告。

### 8.2 协作规范

1. 先改 specifications，再改 templates/tools。
2. 任何生成行为改动都要更新快照和报告。
3. 禁止直接绕过流水线合并重大变更。

---

## 9. 能力成熟度模型（建议）

### L1 模板可用
- 仅支持固定模板替换。

### L2 规则化生成
- 引入命名和类型映射规则。

### L3 可验证生成
- 有校验、预览、可重复产物。

### L4 可演进生成
- 增量合并、幂等、快照防回归。

### L5 平台化生成
- 多栈复用、策略中心化、治理可视化、组织级推广。

当前建议评估：

- `sql-to-gin-restfulapi-scaffold` 已达到 L4，具备向 L5 演进基础。

---

## 10. 风险与应对

1. 风险：解析精度不足（尤其 view 字段类型推断）
- 应对：引入更强类型推断与诊断输出。

2. 风险：规则和模板漂移
- 应对：规范先行、快照校验、流水线门禁。

3. 风险：资产增多导致维护复杂
- 应对：分层目录、版本策略、变更清单模板化。

---

## 11. 未来趋势与建议

### 11.1 趋势判断

1. 从“模板中心”走向“语义上下文中心”。
2. 从“代码生成”走向“可治理生成（合规、审计、回归）”。
3. 从“单项目工具”走向“组织级工程资产平台”。

下面对这三条趋势做进一步解释。

#### 趋势 1：从“模板中心”走向“语义上下文中心”

什么是“模板中心”：

- 以模板文件为主，输入参数通常较少（如表名、字段名、作者）。
- 模板直接决定输出结构，业务语义主要“硬编码”在模板逻辑中。

什么是“语义上下文中心”：

- 先把输入（如 SQL、规范、命名规则）转换成统一的中间语义对象（context / IR）。
- 模板只是 context 的渲染器，语义决策（例如软删除、主键策略、分页策略）由 context 和规则层决定。

简单例子：

- 模板中心做法：在 `resource_table_template.go` 里写大量 `if field == isDelete` 的判断。
- 语义中心做法：先在 context 中标记 `has_soft_delete=true`、`soft_delete_field=isDelete`，模板只读取这些标记渲染代码。

价值：

1. 可维护：规则变更时优先改 context 生成逻辑，而不是改几十个模板。
2. 可扩展：同一份 context 可同时渲染 Gin、FastAPI、SpringBoot 等不同栈。
3. 可测试：context 可单独校验与快照，不依赖最终代码渲染结果才能发现问题。

#### 趋势 2：从“代码生成”走向“可治理生成”

“可治理生成”不是只看“生成出来了没有”，而是看“是否可控、可追踪、可验证、可审计”。

“可治理生成”通常包含以下能力：

1. 合规（Compliance）
- 是否遵循组织编码规范、安全规范、命名规范。
- 示例：统一响应结构、敏感字段处理、鉴权中间件基线。

2. 审计（Auditability）
- 生成过程是否可追踪：输入是什么、规则版本是什么、输出了什么。
- 示例：输出生成清单、冲突告警、跳过原因和统计报告。

3. 回归（Regression Safety）
- 同样输入是否稳定输出；改动后是否造成非预期差异。
- 示例：一键流水线 + 快照校验（context、manifest）+ 覆盖率统计。

4. 变更可控（Change Control）
- 增量更新是否安全，是否避免覆盖人工改动。
- 示例：marker 区域增量合并、幂等执行、冲突保护策略。

一句话总结：

- 代码生成关注“产出速度”。
- 可治理生成关注“产出质量 + 生命周期可控性”。

#### 趋势 3：从“单项目工具”走向“组织级工程资产平台”

“单项目工具”的典型特征：

- 只服务某一个项目或某一类脚手架。
- 规则和模板散落在项目内，难复用、难统一。

“组织级工程资产平台”的核心要素：

1. 资产标准化
- 统一规则模型（命名、类型、分页、软删除等）。
- 统一规范模型（解析契约、合并契约、质量门禁）。

2. 多栈复用能力
- 同一语义层支持多技术栈渲染（Gin/FastAPI/SpringBoot 等）。

3. 版本与发布机制
- 规则、模板、工具独立版本化。
- 发布前统一回归，发布后可回滚。

4. 平台级质量门禁
- CI 中内置校验、快照、覆盖率、报告上传。

5. 可观测与可审计
- 每次生成有记录：输入版本、输出摘要、差异报告、失败原因。

6. 组织协同机制
- 架构组维护标准资产，业务组在标准范围内扩展。
- 通过规范评审和变更流程保证一致性。

可落地的演进路径（建议）：

1. 先做“单 Skill 闭环”（你当前已基本完成）。
2. 再抽象“跨 Skill 共用资产层”（规则、规范、流水线）。
3. 最后平台化：统一门户、版本治理、可视化报表与权限控制。

#### 术语与仓库落点映射（便于学习）

| 术语 | 含义 | 在当前仓库中的落点（示例） | 建议阅读顺序 |
|---|---|---|---|
| 语义上下文（context / IR） | 将 SQL 与规则解析后的统一中间语义输入 | `sql-to-gin-restfulapi-scaffold/resources/demo_output/generated_context_study_flask_api.json`、`resources/config/template_context_example.json` | 先看 context 字段结构，再看模板如何消费 |
| 规则层（config） | 命名、类型、生成档位等策略配置 | `resources/config/naming_rules.json`、`resources/config/type_mappings.json`、`resources/config/generation_profiles.json` | 先看命名规则，再看类型映射 |
| 规范层（specifications） | 解析契约、合并策略、质量约束 | `resources/specifications/sql_parser_contract.md`、`resources/specifications/router_registry_merge_strategy.md` | 先看 parser contract，再看 merge strategy |
| 模板层（templates） | 把 context 渲染成目标代码 | `resources/templates/project_structure/`、`resources/templates/layers/` | 先看 project_structure，再看 layers |
| 工具层（tools） | 负责生成、校验、预览、合并、回归 | `resources/tools/generate_context_from_sql.py`、`validate_template_context.py`、`run_regression_pipeline.py` | 先看 generate，再看 pipeline |
| 可治理生成 | 合规、审计、回归、变更可控的生成体系 | `resources/demo_output/regression_report_study_gin_api.md`、`resources/demo_output/pipeline_report.json` | 先看 pipeline report，再看 regression report |
| 快照防回归 | 关键产物基线化并自动比对 | `resources/tools/check_snapshots.py`、`resources/demo_output/snapshots/` | 先看 compare 模式，再看 update 模式 |
| 组织级工程资产平台 | 跨项目复用规则/规范/模板/流水线能力的平台化形态 | 当前仓库中的多 Skill 目录（FastAPI/Flask/Gin/SpringBoot）与根 README 总览 | 先看单 Skill 闭环，再看跨 Skill 共性 |

#### 推荐学习路径（30-60 分钟）

1. 先运行一键流水线，建立全局认知：
	- `python sql-to-gin-restfulapi-scaffold/resources/tools/run_regression_pipeline.py`
2. 再看 context 产物，理解“语义中心”输入长什么样：
	- `resources/demo_output/generated_context_study_flask_api.json`
3. 对照模板层，理解“同一语义如何渲染代码”：
	- `resources/templates/project_structure/` + `resources/templates/layers/`
4. 查看回归与快照报告，理解“可治理生成”如何落地：
	- `resources/demo_output/pipeline_report.json`
	- `resources/demo_output/regression_report_study_gin_api.md`
5. 最后回到规范层，理解“为什么这样设计”：
	- `resources/specifications/*.md`

#### 常见误区与纠偏建议

1. 误区：把“模板”当成语义层
- 现象：在模板里堆大量业务判断（主键、软删除、分页、视图只读等）。
- 问题：模板可读性急剧下降，跨栈复用困难，改一条规则要改多处模板。
- 建议：把判断前移到 context 生成与规则层，模板只负责渲染。

2. 误区：只关注“生成成功”，忽略“生成可验证”
- 现象：能出代码就算完成，没有固定验证链路。
- 问题：后续改动引入回归时不易发现，质量波动大。
- 建议：将 `run_regression_pipeline.py` 作为默认入口，并把失败视为阻断信号。

3. 误区：增量生成直接覆盖文件
- 现象：二次生成时覆盖已有注册文件或人工改动。
- 问题：高冲突风险，团队信任成本高。
- 建议：坚持 marker 区域合并策略，非 marker 区域只读；保留冲突诊断输出。

4. 误区：快照机制被“无脑 update”
- 现象：每次差异都直接 `--update`，不做变化审查。
- 问题：把真实回归问题掩盖成“正常更新”。
- 建议：默认 compare，只有“预期变更 + 评审通过”才允许 update。

5. 误区：规范文档长期不更新
- 现象：实现已变，specifications 未同步，文档与行为脱节。
- 问题：新人难以理解系统边界，维护出现隐性分叉。
- 建议：实行“先改规范，再改实现”的变更顺序，并在回归报告中记录版本差异。

6. 误区：把单 Skill 成功等同于平台化完成
- 现象：一个 Skill 跑通后就尝试快速复制到所有栈，缺少共性抽象。
- 问题：重复建设，资产碎片化，维护成本攀升。
- 建议：先抽象跨 Skill 共用能力（context schema、merge 策略、快照策略），再规模化推广。

### 11.2 实施建议

1. 继续坚持“确定性模板 + 智能推理”的混合路线。
2. 保持一键流水线作为发布前置门禁。
3. 将快照机制纳入常规开发流程。
4. 逐步将同类 Skill（FastAPI/Flask/SpringBoot）对齐到同一治理模型。

---

## 12. 开源使用 FAQ 与贡献指南

### 12.1 FAQ（面向首次接触者）

1. 问：这个 Skill 是不是只能处理 `study_flask_api.sql`？
- 答：不是。该 SQL 只是回归基线样例。只要输入 SQL 满足当前 parser contract 的支持范围，都可以生成 context 并进入渲染链路。

2. 问：为什么强调先看 context，而不是先看模板？
- 答：因为当前方法是“语义上下文中心”。模板是渲染层，真正的生成决策在 context 和规则层完成。

3. 问：我只想快速看效果，最短命令是什么？
- 答：优先执行 `python sql-to-gin-restfulapi-scaffold/resources/tools/run_regression_pipeline.py`，可一次性得到完整链路验证和报告。

4. 问：快照 compare 失败就一定是 bug 吗？
- 答：不一定。可能是预期变更，也可能是非预期回归。建议先查看差异来源，再决定是否执行 `--update`。

5. 问：为什么不建议直接改模板解决所有问题？
- 答：因为规则和语义应该沉淀在 config/spec/context 侧。把语义判断长期堆在模板里会导致维护成本急剧上升。

### 12.2 排错路径（建议按顺序执行）

1. 第一步：先跑一键流水线
- 命令：`python sql-to-gin-restfulapi-scaffold/resources/tools/run_regression_pipeline.py`
- 目标：快速定位是 context、模板渲染、路由合并还是快照环节失败。

2. 第二步：看 pipeline 报告中的失败步骤
- 文件：`sql-to-gin-restfulapi-scaffold/resources/demo_output/pipeline_report.json`
- 目标：确认失败阶段和错误摘要。

3. 第三步：按失败类型分治
- context 相关失败：检查 `generate_context_from_sql.py` 输出与 `validate_template_context.py` 报错。
- 渲染相关失败：检查 `render_preview_bundle.py` 与模板变量是否匹配。
- 路由合并失败：检查 `router_registry_merge_strategy.md` 与 marker 区域是否完整。
- 快照失败：先 compare 审查差异，再在“预期变更”前提下 update。

4. 第四步：回看规范是否同步
- 重点文件：`resources/specifications/*.md`
- 目标：避免出现“实现变了，但规范没变”的隐性分叉。

5. 第五步：必要时缩小输入复现
- 建议做法：只保留一个 table 或一个 view 的最小 SQL 片段，先打通链路后再恢复全量输入。

### 12.3 贡献者最小流程（面向开源协作）

1. 先阅读顺序
- `README.md` -> 本文档 -> `resources/specifications/` -> `resources/tools/`。

2. 提交变更前必做
- 运行一键流水线并确认通过。
- 若产物有预期变化，提供差异说明并更新快照。
- 在 PR 描述中写清“改动点、影响面、回归结果”。

3. 建议的 PR 类型
- 规则改进：仅改 config/spec，并附示例。
- 模板改进：说明输入 context 及预期渲染差异。
- 工具改进：给出失败场景、修复思路、回归证据。

4. 不建议的提交方式
- 未跑回归直接提交。
- 快照失败后直接 update 但无差异解释。
- 只改实现不改规范，导致行为无法审计。

### 12.4 开源 FAQ 速查表（一页版）

适用场景：

- 新贡献者首次进入仓库时的“最短路径”操作清单。

快速动作（按顺序）：

1. 看入口文档
- `README.md`

2. 跑一次完整验证
- `python sql-to-gin-restfulapi-scaffold/resources/tools/run_regression_pipeline.py`

3. 看结果文件
- `sql-to-gin-restfulapi-scaffold/resources/demo_output/pipeline_report.json`

4. 理解输入语义
- `sql-to-gin-restfulapi-scaffold/resources/demo_output/generated_context_study_flask_api.json`

5. 理解输出来源
- `sql-to-gin-restfulapi-scaffold/resources/templates/project_structure/`
- `sql-to-gin-restfulapi-scaffold/resources/templates/layers/`

常见问题速答：

1. 看到快照差异怎么办？
- 先 compare 诊断差异来源；确认是预期变更后再 update。

2. 改规则还是改模板？
- 先看是否属于“语义决策”。语义决策优先改 config/spec/context；模板只做渲染。

3. 回归通过但代码看起来不理想怎么办？
- 先补规范或规则，再调整模板；避免直接在生成产物上人工修补作为长期方案。

4. 如何判断变更是否可合并？
- 满足质量门禁：流水线通过、快照可解释、变更说明完整。

### 12.5 贡献者 PR 模板示例（四段式）

建议在 PR 描述中使用以下结构：

```markdown
## 1) 问题
- 当前行为：
- 预期行为：
- 影响范围：

## 2) 方案
- 变更文件：
- 设计取舍：
- 兼容性说明：

## 3) 验证
- 执行命令：
	- python sql-to-gin-restfulapi-scaffold/resources/tools/run_regression_pipeline.py
- 结果摘要：
	- pipeline_report: PASS/FAIL
	- snapshot compare: PASS/FAIL
	- 覆盖率：xx%

## 4) 影响面
- 对已有 Skill 的影响：
- 对文档/规范的影响：
- 是否需要更新快照：是/否（原因）
```

推荐补充项：

1. 若变更 parser contract，请附最小 SQL 复现片段。
2. 若变更模板渲染，请附关键产物 diff 摘要。
3. 若变更快照，请附“为什么是预期变化”的一句话解释。

---

## 13. 结论

对于“生成企业级接口脚手架项目”这一类 Skill，采用混合 SKILL 设计方法是合理且面向未来的路线。

其核心价值不在“生成了多少代码”，而在于：

1. 能否稳定生成。
2. 能否安全增量演进。
3. 能否被自动验证与治理。

从这个标准看，当前方案具备较好的工程落地性，可作为后续同类 Skill 的参考基线。
