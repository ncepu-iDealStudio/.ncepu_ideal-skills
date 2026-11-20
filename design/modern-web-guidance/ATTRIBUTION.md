# 来源与许可声明

本技能项目的指南内容并非原创，而是移植自 Google Chrome 团队维护的开源项目
[GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance)。
本仓库仅对「驱动层」（`SKILL.md`、`README.md`、检索工具、规范文档）做了中文改写与
本地化改造，**`resources/guides/` 下的 209 份指南为上游原文的逐字副本**。

## 来源信息

- 上游仓库：https://github.com/GoogleChrome/modern-web-guidance
- 源码仓库：https://github.com/GoogleChrome/modern-web-guidance-src
- 官方文档：https://developer.chrome.com/docs/modern-web-guidance
- 移植版本：v1.0.0（Release v1.0.0）
- 移植 commit：`4dd968349e54ca45a05dd5c818fb035c9054b022`（2026-11-10）
- 移植范围：`skills/modern-web-guidance/guides/` 全部 209 份 Markdown 指南（17 个分类）
- 维护方：由 Google Chrome、Microsoft Edge、Mozilla Firefox 与 MDN 团队，联合 Web 开发社区共同维护

## 许可

依据上游 `README.md` 的「License」章节：

- **软件代码**（本项目的 `resources/tools/*.py`、示例片段）采用
  [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)。
  `resources/guides/` 中指南内嵌的代码示例同属上游软件代码，按 Apache-2.0 使用。
- **文档与指南内容**（`resources/guides/` 下全部 Markdown）采用
  [Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/)。
  署名对象为 GoogleChrome/modern-web-guidance 及其贡献者（见上文来源信息）。

> 说明：本技能对上游指南**未做内容修改**（保留英文原文），仅新增了本地检索索引与
> 中文驱动文档。若后续对指南做翻译、删改或增补，需在此处注明「已修改」并保留本声明。

## 与上游的关系与差异

| 项目 | 上游 | 本项目 |
| :--- | :--- | :--- |
| 指南检索 | `npx modern-web-guidance@latest search/retrieve`（联网、离线语义模型、带遥测） | 本地 `resources/tools/mwg.py`（零依赖、完全离线、无遥测、基于关键词加权索引） |
| 路由器 | 英文 `SKILL.md`（90 行） | 中文 `SKILL.md`，工作流对齐但面向本仓库 |
| 交叉引用 | 指南内 `npx -y modern-web-guidance@latest retrieve "<id>"` | 阅读时映射为 `python3 resources/tools/mwg.py retrieve "<id>"`，见 `resources/specifications/local_search_contract.md` |
| 遗留代码扫描 | `legacy-scan`（依赖上游未开源的规则库） | 不提供 |
| Chrome 扩展技能包 | `skills/chrome-extensions` | 不纳入（本次仅移植主技能） |

## 更新指南

指南内容会随 Web 平台演进而更新。同步上游最新版的方法见
[README.md「更新指南」](README.md#更新指南)。更新后请同步修订本文件顶部的 commit 与版本号。
