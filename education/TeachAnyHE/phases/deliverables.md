# 输出物要求与交付标准（高等教育版）

> **所属**：TeachAnyHE 技能 · 卫星文档
> **触发时机**：Phase 4 交付时
> **主文档**：[../SKILL.md](../SKILL.md)
>
> 对应 TeachAny 的 `phases/deliverables.md`。高等教育无 teachany.cn 平台，交付以「本地 HTML + 可选导出」为主。

---

## 一、输出层级

| 层级 | 内容 | 必选性 |
| --- | --- | --- |
| **L1** | 互动课件（HTML，单文件/目录自包含） | 必选，不可跳过 |
| **L2** | 教学动画 / 仿真（Manim / Motion Canvas / 内置 JS） | 默认必选，自动执行 |
| **L3** | AI 语音讲解（≥3 个 mp3，Edge Neural TTS） | 默认必选，多引擎自动回退 |

## 二、L1 — 互动课件（必选）

- `index.html` 可独立运行（`file://` 协议双击即用）
- 含 `manifest.json`（课程/专业/课型/知识点清单）
- 含 `course-graph.json`（知识点先修/后继/Bloom/毕业要求指标点）
- 公式 KaTeX 渲染（理工课）；算法/代码可视化（计算机课）
- 标准模块齐全：AI 助教、教师卡片、TTS、section hints、课程知识图谱
- 前测 + 后测 + 至少 3 层 Bloom 覆盖
- 学术里程碑系统（非游戏化）

## 三、L2 — 教学动画/仿真（默认必选）

按 `tech/animation-toolchain.md` 选择工具：

| 内容 | 工具 |
| --- | --- |
| 数学推导/函数图 | Manim |
| 算法流程 | Motion Canvas / 内置 JS |
| 波形/频谱/电路仿真 | 内置 JS 引擎 / 引用 Python 结果 |

**交付**：动画导出为 `assets/*.mp4` 或内嵌 Canvas/SVG 实时仿真（优先内嵌，交互性更强）。

## 四、L3 — AI 语音讲解（默认必选）

- 用 Edge Neural TTS（命令行工具 `edge-tts`）生成 ≥3 个 `tts/*.mp3`
- 每个 `data-tts` 段落带 `section` 映射
- 禁用 Web Speech API 金属音交付
- 提供连续音频播放器（连续播放 + 正文 data-tts 段落高亮）

**生成命令**（首选 edge-tts，Python 包）：

```bash
pip install edge-tts
edge-tts --voice zh-CN-XiaoxiaoNeural --text "本段讲解文本" --write-media tts/section1.mp3
```

**多引擎回退链**：edge-tts → gTTS（`gtts-cli`）→ 本地 espeak-ng；仍失败且重试 ≥2 次（间隔 ≥30 秒）→ 记录豁免原因（具体报错）与后续补齐步骤。

## 五、可选导出

| 格式 | 工具/方法 | 适用 |
| --- | --- | --- |
| PDF | `window.print()` / 无头浏览器 | 讲义、教学资料 |
| PPTX | 结合 pptx 技能 | 课堂演示 |
| LaTeX 讲义 | 手写/模板 | 数学、理论课配套讲义 |
| LMS 包 | SCORM / 页面包 | 学习通/雨课堂/Canvas/Moodle |

**注意**：导出前先检测环境有无导出工具/权限；无则退回本地 HTML 交付，不假设能生成。

**转换细节**：
- PDF：`window.print()` 配合 `@media print`（隐藏悬浮按钮），或 headless 浏览器 `--print-to-pdf`。
- PPTX：用 `@skill:pptx` / `html2pptx` 转演示文稿，一个模块对应一张幻灯片。
- LaTeX：将 `.formula-box` / `.derivation` 提取为 `theorem`/`proof` 环境，产出配套讲义。
- LMS：导出 SCORM 1.2/2004 或静态页面包，导入学习通/雨课堂/Canvas/Moodle。

## 六、交付标准（制作交付）

交付前必须满足：

- 已补齐 AI 助教、连续音频播放器（≥3 个真实 mp3）、课程知识图谱三模块
- 通过质检（公式渲染、路径、互动可用性）
- 关键资源存在：`index.html`、`manifest.json`、`course-graph.json`、`PLAN.md`、`assets/`、`tts/`（或豁免记录）
- 控制台无错误、核心互动可用、移动端不崩
- 交付摘要说明：是否导出其他格式；若未导出，给出本地路径与知识点清单

**质检命令**（交付前逐项跑）：

```bash
cd "$COURSE_DIR"
python -m json.tool manifest.json    > /dev/null && echo "manifest.json 合法"
python -m json.tool course-graph.json > /dev/null && echo "course-graph.json 合法"
python -m http.server 8000            # 浏览器打开 http://localhost:8000 检查控制台报错与互动可用性
# 无头浏览器脚本检查（可选，Playwright）：收集 page.on('console') 报错 + 移动端视口截图
```

## 七、与 TeachAny 的对应

| TeachAny | TeachAnyHE |
| --- | --- |
| teachany.cn 发布闭环 + GitHub 挂树 | 本地 HTML 交付 + 导出（PDF/PPTX/LaTeX/LMS） |
| L1 互动课件（挂树） | L1 互动课件（course-graph.json） |
| L2 教学动画（PhET/Manim/Motion Canvas） | L2 动画/仿真（Manim/Motion Canvas/内置 JS） |
| L3 AI 语音（Edge-TTS 浏览器合成） | L3 AI 语音（Edge Neural TTS + 多引擎回退） |
