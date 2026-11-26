# 课件开发标准流程（高等教育版）

> **所属**：TeachAnyHE 技能 · 卫星文档
> **触发时机**：开始制作课件时（Phase 全流程）
> **主文档**：[../SKILL.md](../SKILL.md)
>
> 对应 TeachAny 的 `phases/workflow.md`。保留「强制检查点工作流」骨架，移除 K-12 专属的课标检索、挂树、Hero 图 AI 生成平台链路，替换为「培养方案/教学大纲定位 + 本地 course-graph.json 生成」。

---

## 一、流程总览

```text
Phase 0  定义与检索：学生层次/专业/课程/课型，定位课程目标与知识点
Phase 1  教学骨架：问题锚点 + ABT 叙事 + 互动/评估设计
Phase 2  构建页面：复制模板，填内容，接入标准模块、公式渲染、动画/仿真
Phase 3  验证交付：运行质量检查，浏览器/命令闭环验证
Phase 4  交付：本地交付 + 可选导出（PDF/PPTX/LaTeX/LMS）
```

---

## 二、Phase 0：确定对象与目标 ⛔ CHECKPOINT

回答以下六问（结果必须落到课件结构里）：

| # | 问题 | 输出 |
| --- | --- | --- |
| 1 | 学生是谁？（年级/专业/先修基础） | 定难度、节奏、数学严谨度 |
| 2 | 先修要求是什么？ | 定是否需要前测/脚手架 |
| 3 | 学完能做什么？（对应毕业要求指标点） | 可考核的课程目标 |
| 4 | 真实场景是什么？（工程/科研/前沿） | 学习动机 |
| 5 | 学生最容易卡在哪？ | 深度理解与错误诊断点 |
| 6 | 如何验证学会？ | 练习与考核方式 |

**强制**：每个知识点登记到 `course-graph.json`（含 `prerequisites`/`leads_to`/`bloom_verbs`/`graduate_attr`）。知识体系来源：专业培养方案 → 课程教学大纲 → 教材目录。方法见 `references/higher-ed-framework.md`。

**同时探测环境并定档**：按主 `SKILL.md`「环境探测与交付档位」检查 Python 命令、TTS 引擎、网络/CDN、浏览器、模型 API 凭据，把探测结果与档位（A/B/C）及降档原因记入 `PLAN.md`。档位只决定外部依赖类模块的实现方式，不影响六问与教学设计。

## 三、Phase 1：搭建教学骨架 ⛔ CHECKPOINT

1. **ABT 叙事**：And（已知）→ But（已知解决不了）→ Therefore（本课新工具）
2. **课型判定**：新授课/复习课/习题课/专题研讨/实验课/课程设计
3. **深度理解**：五镜法选 2-3 个（看/拆/讲/比/迁）
4. **互动设计**：至少 1 个真实互动（参数滑块/推导/算法可视化/仿真）
5. **评估设计**：前测 + 后测 + 三层练习 + 三类题型组合
6. **自适应四分支**：≥2 个触发点（前测后 + 核心练习后）

**强制**：不能跳过骨架直接堆内容；每模块 1 个核心问题。

## 四、Phase 2：选择学科门类模式 ⛔ CHECKPOINT

在 `tech/design-system.md` 中确定学科门类视觉模式：

| 门类 | body class | 适用 |
| --- | --- | --- |
| 理科 | `teachanyhe-science` | 数学、物理、化学 |
| 工科 | `teachanyhe-engineering` | 计算机、通信、电气、自动化、机械 |
| 经管/文科 | `teachanyhe-econ` | 经管、文科 |

**强制**：`teachanyhe-stage` meta、`body` class、`:root` 配色三者一致，不得混用。

### ⛔ Generation Gate：内容生成前预检

生成正文前确认：

1. ✅ 六问已答，课程目标含毕业要求指标点
2. ✅ course-graph.json 已生成（至少含本课知识点及先修/后继）
3. ✅ 学科门类模式已选定
4. ✅ 已复制 `templates/course-skeleton.html`
5. ✅ 公式库（KaTeX）已引入（理工课）
6. ✅ 已确定动画/仿真方案（见 `tech/animation-toolchain.md`）

## 五、Phase 3：制作内容 ⛔ CHECKPOINT

1. 复制 `templates/course-skeleton.html`，删除 `<head>` 占位注释块
2. 填 Hero（课程标题 + 专业/课程/课型标签 + 核心问题）
3. 填课程目标（含毕业要求指标点 `graduate-attr`）
4. 填前测、知识模块 × N、综合任务、后测、拓展
5. 公式一律 KaTeX 渲染；推导用 `.derivation` 分步组件
6. 计算机类：算法可视化（步骤高亮 + 复杂度对比）
7. 通信/电气：波形/频谱/电路仿真
8. 接入标准模块：AI 助教、教师卡片、语音讲解、section hints、课程知识图谱
9. 语音讲解按档位实现：档位 A 生成 ≥3 个 `tts/*.mp3`（Edge Neural TTS），档位 B 用 Web Speech 合成，档位 C 用讲解文字稿；每个 `data-tts` 段带 `section` 映射，任何档位都保留讲解内容
10. 学术里程碑系统（章节完成度/掌握度/连续学习/综合任务完成）

### ⛔ Completeness Gate：输出完整性审查

对照 `references/baseline-rules.md` 的 19 项基线清单逐项核对，重点：

- 公式是否真渲染（无公式图片/纯文本）
- 算法是否可视化（无静态代码伪装）
- 互动是否可操作（无静态图伪装仿真）
- course-graph.json 是否齐全
- 路径是否相对引用
- 移动端是否不崩、控制台无错

## 六、Phase 4：交付与输出决策 ⛔ CHECKPOINT

见 `phases/deliverables.md`。默认本地 HTML 交付；可选导出 PDF/PPTX/LaTeX/LMS。

## 七、与 TeachAny 的对应

| TeachAny | TeachAnyHE |
| --- | --- |
| Phase 0.5 课标 node_id 检索（脚本挂树） | Phase 0 培养方案/大纲定位 + course-graph.json |
| Phase 2 学段模式（小/初/高） | Phase 2 学科门类模式（理科/工科/经管） |
| Generation Gate（Hero 图 AI 生成 + 挂树检查） | Generation Gate（公式/图谱/门类预检） |
| Completeness Gate（B-1~B-7 基线） | Completeness Gate（19 项基线） |
| Phase 4 teachany.cn 发布 | Phase 4 本地交付 + 导出 |
