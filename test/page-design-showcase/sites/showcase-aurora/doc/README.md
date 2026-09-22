# 光年计划 · 设计综述（状态恢复入口）

## 需求摘要
> 我想要一个高大上的作品集网站，展示我的动态设计和视觉作品，要有动画效果，看起来很酷。

## Requirement Model
- site：光年计划 / zh-CN / 视觉作品集与动态设计展示 / 创意机构、招聘方与同行
- pages：index.html（landing）、list.html（list）、detail.html（detail）、about.html（about）、404.html（error）
- content：领域：视觉/动态设计；模型：自建 works（title, summary, cover, url, year）
- design：极光科技（tech-aurora）— 学生明确要"高大上 + 动画"，tech-aurora 是唯一允许视差与霓虹渐变的包，其余包无法承载该气质

## design_statement
- position：一个以动态视觉为主角的作品集，不是简历页，也不是模板站
- focus：首屏第一眼落在渐变标题与下方的三张作品卡，视差只出现在中段一处
- device：深色渐变 + 霓虹紫青双色 + 滚动淡入与分组错开进入，视差用 sticky 纯 CSS 实现
- banned：不做全屏粒子雨、不做鼠标跟随光斑、不做自动播放轮播、不让首屏内容先隐藏再淡入

## 采用的设计包
已复制到 `doc/design/tech-aurora.md`。

## 页面进度
- [x] index.html · landing · 光年计划 · 动态视觉作品集
- [x] list.html · list · 全部作品 · 光年计划
- [x] detail.html · detail · 光年计划 · 主视觉 · 光年计划
- [x] about.html · about · 关于 · 光年计划
- [x] 404.html · error · 页面不存在 · 光年计划

## 后续拆解提示
所有重复区域已标注 data-component / data-collection / data-slot，删除全部 data-* 后仍是合法语义 HTML。
