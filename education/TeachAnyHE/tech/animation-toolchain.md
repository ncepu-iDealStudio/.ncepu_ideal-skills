# 动画与仿真工具分层（高等教育版）

> **所属**：TeachAnyHE 技能 · 卫星文档
> **触发时机**：Phase 2/3 选择动画与仿真工具时
> **主文档**：[../SKILL.md](../SKILL.md)
>
> 对应 TeachAny 的动画工具栈（TeachAny 仓库的 `tech/stack.md` / `tech/ai-multimodal.md`，其动画部分已并入本文档）。高等教育动画以「数学推导可视化、算法流程、信号/电路仿真」为主，去掉 K-12 的 PhET 生活化实验。

---

## 一、工具分层总览

| 内容类型 | 首选工具 | 次选 | 输出形式 |
| --- | --- | --- | --- |
| 数学推导/证明 | Manim | 逐步展开 HTML | `assets/*.mp4` 或内嵌 |
| 函数图像/几何 | Manim / 内置 Canvas | GeoGebra | mp4 / 内嵌 |
| 算法流程 | Motion Canvas | 内置 SVG/Canvas | mp4 / 内嵌 |
| 信号波形/频谱 | 内置 JS（Canvas） | 引用 Python 结果 | 内嵌 |
| 电路/系统仿真 | 内置 JS 引擎 | 引用 Python/Jupyter | 内嵌 |
| 数据可视化 | Chart.js / 内置 SVG | matplotlib | 内嵌 / 图片 |

## 二、选择规则

1. **需要交互（学生调参观察）→ 内嵌 JS**：数学函数图、信号波形/频谱、电路仿真，优先内置 Canvas/SVG 实时交互，而非导出视频。
2. **需要演示（固定推导/流程）→ 导出视频**：数学推导、算法执行过程，用 Manim / Motion Canvas 导出 mp4。
3. **数据图表 → Chart.js**：复杂度对比、性能曲线、实验结果。

## 三、数学推导可视化（Manim）

典型场景：梯度下降的等高线下降动画、极限/导数的几何意义、傅里叶变换的频谱逼近。

```bash
# 安装与渲染命令
pip install manim
manim render -pql gradient_descent.py GradientDescent   # 低质量预览
manim render -pqh gradient_descent.py GradientDescent   # 高质量导出
```

```python
# 示例：Manim 绘制梯度下降等高线
from manim import *
class GradientDescent(Scene):
    def construct(self):
        # 绘制等高线 f(x,y)，叠加负梯度方向箭头与迭代点轨迹
        ...
```

**交付**：导出 `assets/gradient-descent.mp4`，在课件中 `<video>` 内嵌或提供下载。

**降级**：Manim/Python 环境缺失或渲染失败 → 退回内嵌 Canvas/SVG 实时交互（见「二、选择规则」第 1 条），不阻塞课件交付。

## 四、算法流程可视化（Motion Canvas / 内置 JS）

典型场景：排序/查找/图遍历的逐步执行、二叉搜索树的插入删除、复杂度对比。

**优先内置 JS 实时交互**：数组条 + 当前比较位置高亮 + 复杂度对比表，学生可「点下一步」或「自动播放」。比静态 mp4 更适合教学。

```html
<div class="algo-viz" data-algo="quick-sort">
  <div class="algo-bars"><!-- 数组条 --></div>
  <div class="algo-step-info"><!-- 当前步骤说明 --></div>
  <button data-action="next">下一步</button>
  <table class="complexity"><!-- 复杂度对比 --></table>
</div>
```

## 五、信号/电路仿真（内置 JS）

典型场景：时域波形 ↔ 频谱双视图、RC 充放电、采样定理混叠演示、滤波器幅频响应。

**内置 JS 引擎**：参数滑块（改变信号时长/幅度/频率/R-C 参数）+ 实时更新 Canvas 波形/频谱。核心是「控制变量三元组」：改变什么/保持不变/测量什么。

## 六、与 TeachAny 的对应

| TeachAny | TeachAnyHE |
| --- | --- |
| PhET 生活化实验（溢水杯/跷跷板） | 内置 JS 工程仿真（波形/频谱/电路/函数图） |
| Manim（数学推导） | Manim（数学推导/证明/函数图） |
| Motion Canvas（算法流程） | Motion Canvas / 内置 JS（算法可视化） |
| GeoGebra | GeoGebra（保留，几何/函数图） |
| 数据图表 | Chart.js / matplotlib |
