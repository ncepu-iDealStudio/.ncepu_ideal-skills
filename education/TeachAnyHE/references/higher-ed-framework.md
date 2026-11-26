# 高等教育知识体系与培养方案框架（对应 TeachAny 的课标/知识树）

高等教育没有统一课标 node_id。TeachAnyHE 用「专业培养方案 → 课程教学大纲 → 教材章节 → 知识点」四级体系替代 K-12 的「学段 → 学科 → 单元 → 知识点」，并叠加 OBE 目标映射。

## 1. 四级知识体系

```text
专业培养方案（major）
  └─ 课程（course）
       └─ 章节（chapter）
            └─ 知识点（node，含先修/后继/Bloom 目标/毕业要求指标点）
```

| 层级 | 来源 | 关键字段 |
| --- | --- | --- |
| 专业 | 培养方案 | 培养目标、毕业要求（1-12 条）、课程体系 |
| 课程 | 教学大纲 | 课程目标、知识点清单、学时、考核方式 |
| 章节 | 教材目录 | 章节目录、重难点 |
| 知识点 | 教材+大纲 | definition、prerequisites、leads_to、bloom_verbs、graduate_attr |

## 2. OBE 目标映射（成果导向）

每个知识点应尽量标注支撑的**毕业要求指标点**，实现「知识点 → 课程目标 → 毕业要求」的可追溯链条。

**示例（《数据结构》二叉搜索树）**：

```json
{
  "node": "二叉搜索树",
  "course_objective": "掌握树形结构的存储与查找算法，能分析其时间复杂度",
  "graduate_attr": "毕业要求3-2：能针对复杂工程问题设计算法并进行复杂度分析"
}
```

**设计课件时的 OBE 检查**：

1. 本知识点的课程目标是什么？（不是「讲完」而是「学生会做什么」）
2. 支撑哪条毕业要求指标点？
3. 用什么题型/任务能观察到该能力的达成？
4. 前后测是否能量化目标达成度？

## 3. 课程知识图谱（course-graph.json）

每个课件目录放一份 `course-graph.json`，结构如下：

```json
{
  "major": "计算机科学与技术",
  "course": "数据结构",
  "chapter": "第5章 树与二叉树",
  "nodes": [
    {
      "id": "ds-tree-basic",
      "name": "树的定义与性质",
      "prerequisites": ["ds-linear-list"],
      "leads_to": ["ds-tree-bst", "ds-tree-traversal"],
      "bloom_verbs": ["understand"],
      "graduate_attr": "毕业要求1-1",
      "definition": "n个结点的有限集合，n=0为空树"
    },
    {
      "id": "ds-tree-bst",
      "name": "二叉搜索树",
      "prerequisites": ["ds-tree-basic"],
      "leads_to": ["ds-avl", "ds-rbtree"],
      "bloom_verbs": ["apply", "analyze"],
      "graduate_attr": "毕业要求3-2",
      "definition": "左子树所有结点值小于根、右子树所有结点值大于根的二叉树"
    }
  ]
}
```

**用途**：① 驱动自适应分支（prerequisites 判定 review-prereq）；② 课件内知识图谱模块渲染；③ 间隔重复复习队列；④ 跨课件掌握度共享。

**生成方法**：可让 AI 依据教学大纲/教材目录直接产出 JSON（结构见上）；也可用脚本从「章节-知识点」简表批量生成：

```python
# scripts/build-course-graph.py：从知识点列表生成 course-graph.json
import json
graph = {
  "major": "计算机科学与技术", "course": "数据结构", "chapter": "第5章 树与二叉树",
  "nodes": [
    {"id":"ds-tree-basic","name":"树的定义与性质","prerequisites":["ds-linear-list"],
     "leads_to":["ds-tree-bst"],"bloom_verbs":["understand"],
     "graduate_attr":"毕业要求1-1","definition":"n个结点的有限集合"}
  ]
}
json.dump(graph, open("course-graph.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
```

生成后用 `python -m json.tool course-graph.json` 校验合法性（输出为空即通过）。

## 4. 各专业课程群（示例目录，覆盖示例替换范围）

| 门类 | 代表课程 |
| --- | --- |
| 数学类 | 高等数学、线性代数、概率论与数理统计、数学分析、常微分方程、数值分析、最优化方法、运筹学、图论、抽象代数 |
| 计算机类 | 数据结构、算法设计与分析、操作系统、计算机网络、计算机组成原理、数据库系统、编译原理、离散数学、机器学习、人工智能 |
| 通信类 | 信号与系统、通信原理、数字信号处理、信息论与编码、电磁场与电磁波、通信网络、无线通信 |
| 电气类 | 电路分析、模拟电子技术、数字电子技术、电机学、电力系统分析、自动控制原理、电力电子技术 |
| 自动化类 | 自动控制原理、现代控制理论、过程控制、机器人学、智能控制 |
| 物理类 | 大学物理、理论力学、电动力学、量子力学、热力学与统计物理、固体物理 |
| 化学类 | 无机化学、有机化学、分析化学、物理化学、结构化学、化工原理 |
| 机械类 | 理论力学、材料力学、机械原理、机械设计、流体力学 |
| 经管类 | 微观经济学、宏观经济学、计量经济学、运筹学、管理信息系统、金融工程 |

## 5. 与 TeachAny 的对应

| TeachAny | TeachAnyHE |
| --- | --- |
| 学段（小学/初中/高中） | 学位层次（本科低年级/高年级/研究生） |
| 学科（数理化生史地语英IT） | 专业课程群（数学/计算机/通信/电气/自动化/机械/物理/化学/经管，共 9 类） |
| 课标 node_id + 知识树 | 培养方案 + 教学大纲 + course-graph.json |
| 课标「探究」关键词强制探究 | 大纲/培养方案「实验/设计/研讨」强制对应课型 |
| PBL 路径 → ext 挂树 | 课程设计/项目 → 独立项目页 |
