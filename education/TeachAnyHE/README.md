# TeachAnyHE

**高等教育互动课件开发技能（Higher Education Edition）** — 沿袭 [TeachAny（教我学）](https://github.com/weponusa/teachany) 的「教学设计操作系统」框架，将面向对象从 K-12 换成大学本科/研究生课程，把一节课做成**有问题锚点、有推导/仿真/证明、有讲解、有评估、有知识体系映射**的互动课件。

> 本项目是 TeachAny（K-12）的高等教育迁移版，按上游要求已完成更名（Fork 必须更名），许可证延续 AGPL-3.0，详见 [License](#license)。

---

## 项目定位

TeachAnyHE 不是提示词模板，而是一套面向高校专业课程的**教学设计系统**（Agent Skill）：

| 层面 | 内容 |
| --- | --- |
| 内核（沿袭 TeachAny） | 学习闭环优先：六问、ABT 叙事、认知负荷、Mayer 多媒体原则、脚手架三级、自适应四分支、探究式学习、五镜法、Bloom 评估 |
| 对象层（换为 HE） | 专业 → 课程 → 章节 → 知识点；本科低年级/高年级/研究生三层 |
| 目标框架 | OBE 映射：知识点 → 课程目标 → 毕业要求指标点（工程教育认证/一流课程建设） |
| HE 特有强化 | KaTeX 公式强制渲染 + 分步推导组件；算法/代码可视化；信号/电路仿真；AI 助教学术诚信边界 |
| 交付方式 | 本地 HTML 交付（`file://` 可独立运行）+ 可选导出（PDF/PPTX/LaTeX/LMS），不依赖外部发布平台 |

**适用边界**：大学本科/研究生课程的互动课件。K-12 请使用原版 [teachany](https://github.com/weponusa/teachany)；企业培训不适用。

## 核心能力

- 互动课件生成：目标导向页面结构（目标→前测→模块→综合任务→后测→拓展→知识图谱）
- 课程知识图谱：本地生成 `course-graph.json`（prerequisites / leads_to / bloom_verbs / graduate_attr）
- 六种课型适配：新授课 / 复习课 / 习题课 / 专题研讨 / 实验课 / **课程设计**（高校特有）
- 九类专业课程矩阵：数学、计算机、通信、电气、自动化、机械、物理、化学、经管
- 五件套标准模块：AI 助教、教师卡片、语音讲解（按档位）、section hints、课程知识图谱
- 19 项交付基线 + 降档记录机制，保证课件完整性可核验

## 目录结构

```text
TeachAnyHE/
├── SKILL.md                        # Agent 指令主文件（决策骨架，31 KB）
├── MIGRATION.md                    # TeachAny → TeachAnyHE 完整迁移对照表
├── guides/
│   ├── assessment.md               # Bloom 评估（理工/经管双栏 + 过程性评价）
│   ├── examples.md                 # 示例库（十例：九门类 + 端到端交付）
│   ├── interaction-patterns.md     # 互动规范（公式/推导/算法可视化/仿真）
│   └── project-based.md            # 课程设计/大作业/科研训练（PBL 的 HE 形态）
├── phases/
│   ├── workflow.md                 # 4-Phase 工作流（含培养方案/大纲定位）
│   └── deliverables.md             # 交付物规范（本地交付 + 导出）
├── references/
│   ├── baseline-rules.md           # 19 项交付基线
│   └── higher-ed-framework.md      # 培养方案 / OBE / course-graph.json 框架
├── tech/
│   ├── animation-toolchain.md      # Manim / Motion Canvas / 内置 JS 仿真
│   ├── design-system.md            # 学科门类视觉（理科深蓝/工科浅灰/经管米白）
│   └── page-structure.md           # 目标导向页面结构 + teachanyhe_ 命名空间
└── templates/
    ├── course-skeleton.html        # 课件骨架（KaTeX + 推导组件 + 五件套接线）
    ├── manifest.json               # 课件元数据清单示例
    └── PLAN.md                     # 制作计划模板（六问 + 19 项基线核对表）
```

## 安装（Agent Skill）

将本目录复制或软链接到对应工具的技能目录（保持目录名 `TeachAnyHE`）：

| 工具 | 位置 |
| --- | --- |
| WorkBuddy / CodeBuddy | `~/.workbuddy/skills/TeachAnyHE/` |
| Cursor | `~/.cursor/skills/TeachAnyHE/` |
| Claude Code | `~/.claude/skills/TeachAnyHE/` |

Windows 用户把 `~` 替换为用户目录（如 `C:\Users\你的用户名\`）。整目录复制即可，技能不依赖特定 Agent 工具名，也不绑定任何外部平台。

## 跨工具适配说明

技能不假设运行环境具备某组固定工具。制作前会探测 Python、TTS 引擎、网络/CDN、浏览器、模型 API 凭据，按结果选择交付档位：

| 档位 | 条件 | 语音讲解 | 动画 | 公式 |
| --- | --- | --- | --- | --- |
| A 完整 | Python + TTS + 网络可用 | ≥3 个 mp3 + 连续播放器 | Manim / Motion Canvas | KaTeX CDN |
| B 合成 | 无 TTS 命令，有浏览器 | Web Speech 合成（明确标注） | 内嵌 Canvas/SVG | KaTeX CDN |
| C 离线 | 无网络或纯文件环境 | 讲解文字稿 | 静态 SVG 分步图 | 本地 KaTeX 或 LaTeX 源码 + 提示 |

教学设计与内容基线（六问、ABT、真实互动、练习与反馈、课程知识图谱）在任何档位都不降级；PPTX 导出是可选能力，当前工具不提供时直接跳过。降档原因与替代方案记入课件的 `PLAN.md`。

## 快速使用

在 Agent 中直接说：

> 用 TeachAnyHE 制作《信号与系统》第 4 章傅里叶变换的互动课件，本科高年级，含 AI 助教和语音讲解

或按 `SKILL.md` 的 4-Phase 工作流执行：**Phase 0** 定位培养方案与教学大纲 → **Phase 1** 六问与 ABT 教学设计 → **Phase 2** 学科适配（公式推导/算法可视化/仿真）→ **Phase 3** 构建交付（19 项基线核对）。

交付物清单：`index.html` + `manifest.json` + `course-graph.json` + `PLAN.md` + `assets/`；档位 A 另含 `tts/`（≥3 mp3），档位 B/C 不生成音频但保留讲解内容。

## 与上游 TeachAny 的关系

- **框架层不变**：学习闭环、六问、ABT、认知负荷、脚手架、自适应、探究、评估等方法完整保留。
- **K-12 专属部分移除/改造**：课标 node_id 挂树、teachany.cn 发布、历史地图/地形 3D、PhET 生活实验、游戏化成就系统等，均替换为 HE 对应物（详见 [MIGRATION.md](MIGRATION.md)）。
- 上游项目：[weponusa/teachany](https://github.com/weponusa/teachany) · 在线站点 [teachany.cn](https://www.teachany.cn/)

致谢：感谢 TeachAny 作者开源这套优秀的教学设计框架。TeachAny 与 TeachAny™/教我学™ 商标归原作者所有，本项目为其高等教育衍生版本，已按要求更名。

## License

本项目衍生自 [weponusa/teachany](https://github.com/weponusa/teachany)（非商业用途采用 AGPL-3.0 许可），故延续 **AGPL-3.0** 许可证发布。

- 非商业用途（个人教学、公立高校、学术研究、开源衍生）：遵循 AGPL-3.0
- 商业用途（SaaS、付费课程、企业培训）：需联系上游原作者获取商业许可
