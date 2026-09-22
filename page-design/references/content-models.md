# Content Models（内容模型）

内容模型描述页面里装什么数据，与设计无关。V1 预置 4 种常用模型；不预置几十种，其余按需建模。

## 预置模型

### article（文章/资讯）

| 字段 | 说明 | data-slot |
|------|------|-----------|
| title | 标题 | post.title |
| summary | 摘要 | post.summary |
| url | 链接 | post.url |
| cover | 封面图 | post.cover |
| author | 作者 | post.author |
| publishedAt | 发布日期（time datetime） | post.date |
| category | 分类 | post.category |
| tags | 标签 | post.tags |
| body | 正文（仅 detail 页） | — |

### product（产品）

name / model / summary / image / specifications（表格）/ certifications

### person（人物）

name / title（职称）/ avatar / bio / affiliation / links

### notice（通知公告）

title / publisher / publishedAt / category / body

## 按需建模规则

预置之外（论文 paper、课程 course、项目 project、设备 device……）：

1. 从学生需求推导**必要字段**（宁少勿多，每页卡片显示 3–5 个字段为宜）
2. 字段名用英文 camelCase，作为 data-slot 的键（如 `paper.venue`）
3. 建好的模型登记进 site-manifest.json 的 `collections`，含字段清单与 `"sample": true`
4. detail 页可展示更多字段，list 卡片只展示关键字段

## 样例数据纪律

- **必须生成真实感样例数据**：标题像真标题、日期在合理区间、人名像真人、正文有 2–3 段成文内容（不得 lorem ipsum）
- 样例数据服务于两个目的：原型演示效果 + 后续拆解时的结构参照
- 与学生真实信息冲突时一律用虚构数据；manifest 中 `contentSample.generated: true` 全局声明
- 不得编造可被误认为真实机构的数据（如真实公司名+假新闻），用明显虚构但自然的名称
