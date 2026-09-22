# 林述 · 设计综述（状态恢复入口）

## 需求摘要
> 我想做一个简单的个人主页，介绍自己，放几个我做过的项目就行，好看一点。

## Requirement Model
- site：林述 / zh-CN / 个人介绍与作品展示 / 课程老师与同学
- pages：index.html（home）、list.html（list）、about.html（about）、404.html（error）
- content：领域：个人主页；模型：自建 projects（title, summary, url, year）
- design：毛玻璃（glassmorphism）— 学生只要"好看一点"且页面极简；glassmorphism 是强风格包，此处内容量小、单页为主，风险可控且最贴合诉求

## design_statement
- position：一张个人名片式的主页，不是博客，也不是简历长页
- focus：首屏第一眼落在彩色渐变背景上的那块磨砂玻璃卡片与人名
- device：彩色渐变底 + 半透明磨砂浮层，只有悬浮上浮一种动效
- banned：不做背景视频、不做鼠标跟随光效、不做滚动视差、玻璃层不超过两层

## 采用的设计包
已复制到 `doc/design/glassmorphism.md`。

## 页面进度
- [x] index.html · home · 林述 · 个人主页
- [x] list.html · list · 项目 · 林述
- [x] about.html · about · 关于 · 林述
- [x] 404.html · error · 页面不存在 · 林述

## 后续拆解提示
所有重复区域已标注 data-component / data-collection / data-slot，删除全部 data-* 后仍是合法语义 HTML。
