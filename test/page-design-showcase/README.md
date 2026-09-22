# page-design-showcase

`page-design` 的产出示例，分两部分。

## gallery/

设计包与配色的预览画廊，入口是 `gallery/index.html`。

- 9 个设计包的实景预览页，同一套内容在不同视觉体系下的呈现
- `palette-compare.html`：三套自定配色的色卡与角色分工
- `pressure-heat.html` / `pressure-twilight.html` / `pressure-garden.html`：三套自定配色的成稿页面
- `thermal-anomaly/`：热异常页的历史版本与截图存档，供对照回溯

## sites/

四个端到端生成的完整站点，每个都是标准的 `doc/` + `template/` 结构，且 `validate.py` 零错误通过。

| 目录 | 场景 | 设计包 | 页面 |
|---|---|---|---|
| blog-swiss | 个人博客 | swiss-minimal | 6 |
| corp-flat | 公司门户 | flat-material | 6 |
| showcase-aurora | 动态设计作品集 | tech-aurora | 5 |
| homepage-glass | 个人主页 | glassmorphism | 4 |

`generate-sites.cjs` 是这四个站点的生成脚本，重跑可在原地重建。

素材均为演示用样例内容，不对应任何真实机构、产品或人物。
