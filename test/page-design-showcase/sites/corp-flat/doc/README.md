# 云枢智能 · 设计综述（状态恢复入口）

## 需求摘要
> 我们公司做工业物联网，需要一个正式的官网，要有首页、产品列表、产品详情、关于我们和联系方式。

## Requirement Model
- site：云枢智能 / zh-CN / 企业对外官网与产品门户 / 制造业客户与合作伙伴
- pages：index.html（home）、list.html（list）、detail.html（detail）、about.html（about）、contact.html（contact）、404.html（error）
- content：领域：工业物联网；模型：product（products）、notice（notices）
- design：扁平质感（flat-material）— 对外正式门户且强调产品；flat-material 的阴影分层与现代产品感最贴合，避免暗色控制台气质

## design_statement
- position：正式但不老派的工业物联网公司门户，不是电商，也不是控制台
- focus：首页第一眼落在深蓝实底 hero 的主张句，往下是三条能力卡与真实数字背书
- device：白色卡片 + 浅阴影分层替代边框，滚动淡入只有一种，不做霓虹与扫描线
- banned：不做浮动装饰球、不做伪造的实时产线仪表盘、不写"赋能未来"式空话、不把产品页做成促销页

## 采用的设计包
已复制到 `doc/design/flat-material.md`。

## 页面进度
- [x] index.html · home · 云枢智能 · 工业物联网产品与方案
- [x] list.html · list · 产品中心 · 云枢智能
- [x] detail.html · detail · 云枢边缘网关 EG-210 · 云枢智能
- [x] about.html · about · 关于我们 · 云枢智能
- [x] contact.html · contact · 联系我们 · 云枢智能
- [x] 404.html · error · 页面不存在 · 云枢智能

## 后续拆解提示
所有重复区域已标注 data-component / data-collection / data-slot，删除全部 data-* 后仍是合法语义 HTML。
