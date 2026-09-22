# 砚田笔记 · 设计综述（状态恢复入口）

## 需求摘要
> 我想做一个个人博客，写技术笔记和读书感想，要干净一点，能放文章列表和文章页。

## Requirement Model
- site：砚田笔记 / zh-CN / 个人写作与技术笔记 / 同学、同行与未来雇主
- pages：index.html（home）、list.html（list）、post.html（detail）、about.html（about）、contact.html（contact）、404.html（error）
- content：领域：个人写作；模型：article（posts）
- design：瑞士极简（swiss-minimal）— 学生要求"干净"，且内容是长文阅读；swiss-minimal 的纯白网格与单强调色最适合文字密集场景

## design_statement
- position：一个安静的阅读型个人博客，不是作品集，也不是门户
- focus：首页第一眼落在标题下那句自述，紧接着是三张最近文章卡片
- device：纯白网格 + 单一红色强调线 + 零圆角，不用卡片阴影堆叠与渐变
- banned：不做粒子背景、不做卡片套卡片、不放头像墙、不写"赋能/极致"式标语

## 采用的设计包
已复制到 `doc/design/swiss-minimal.md`。

## 页面进度
- [x] index.html · home · 砚田笔记 · 写字的地方
- [x] list.html · list · 全部文章 · 砚田笔记
- [x] post.html · detail · 用三十行 CSS 做一套网格系统 · 砚田笔记
- [x] about.html · about · 关于 · 砚田笔记
- [x] contact.html · contact · 联系 · 砚田笔记
- [x] 404.html · error · 页面不存在 · 砚田笔记

## 后续拆解提示
所有重复区域已标注 data-component / data-collection / data-slot，删除全部 data-* 后仍是合法语义 HTML。
