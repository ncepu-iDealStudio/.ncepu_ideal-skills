# 在 CodeBuddy 插件中使用 prototype-to-taro-app 技能指南

> 面向第一次使用本技能的同学。照着从「一份原型」走到「能在微信开发者工具里点开的 Taro 小程序」，全程不需要自己写页面。
>
> 全文用一个贯穿案例：**校园技能互换小程序**（首页列表 / 详情 / 登录 / 我的）。

---

## 0. 这个技能能帮你做什么

你手上只有下面任意一种材料：

- 设计师给的**界面截图**
- 前端同学写好的**静态 HTML/CSS 原型**
- 一份写着页面清单和字段的 **PRD**

技能会把它们转成一个**可运行的 Taro 4 多端工程**（微信小程序 / 支付宝小程序 / H5 / RN），并内置：

| 内置能力 | 说明 |
| --- | --- |
| 登录 + token 持久化 | 登录页 + `Taro.setStorageSync` |
| 权限路由 | 无 token 跳登录，白名单页面免登录 |
| 请求封装 | 统一 baseURL、超时、错误码、401 跳登录 |
| 分页列表 | 下拉刷新 + 上拉加载 + 到底提示 |
| 三态渲染 | loading / empty / 有数据 |
| Mock 数据 | 后端没写好也能看到完整界面 |
| 多环境 | `config/dev.ts` / `config/prod.ts` |
| 异常捕获 | `app.onError` + 请求层兜底 |

**关键前提：技能支持两套技术栈，且不设默认值，开工前必须由你选一个。**

| 分支 | 技术栈 | 适合谁 |
| --- | --- | --- |
| **Vue3** | Taro 4 + Vue 3 + TS + Vant / Vant Weapp + Pinia | 团队熟悉 Vue，重视 UI 还原速度 |
| **React** | Taro 4 + React 18 + TS + Dva + Immer + taro-ui | 复杂业务、状态流较重的企业应用 |

两套能力对等，**选错只能重来**，所以第 4 节会重点讲怎么选。

---

## 1. 开工前的环境准备

| 依赖 | 是否必须 | 说明 |
| --- | --- | --- |
| CodeBuddy（IDE 或插件） | 必须 | 技能宿主 |
| Node.js ≥ 18 | 必须 | 跑 Taro 编译 |
| pnpm | 推荐 | 技能按 pnpm 生成流程说明；npm 也能跑 |
| Python 3.8+ | 推荐 | 三个辅助脚本（解析 / 预览 / 校验）只用标准库 |
| 微信开发者工具 | 看小程序效果必须 | 导入 `dist/` 目录 |
| 本仓库代码 | 必须 | 提供技能目录 `prototype-to-taro-app/` |

检查版本：

```powershell
node -v
pnpm -v
python --version
```

装 pnpm（可选）：

```powershell
npm i -g pnpm
```

---

## 2. 第 1 步：新建项目目录并安装技能

### 2.1 新建空目录

新建一个专门放生成结果的项目目录，例如 `D:\work\skill-swap`，然后用 CodeBuddy 打开这个目录。

> 不要在 `ncepu_ideal-skills` 仓库里直接生成项目，否则生成物会和技能源码混在一起。

### 2.2 把技能整目录复制进 `.codebuddy/skills/`

**PowerShell（Windows）**：

```powershell
New-Item -ItemType Directory -Force -Path .codebuddy/skills | Out-Null
Copy-Item -Recurse -Force "<本仓库路径>\prototype-to-taro-app" .codebuddy/skills/
```

例如：

```powershell
# 把 <本仓库路径> 换成你机器上的实际位置
Copy-Item -Recurse -Force "E:\Open_source_project\ncepu_ideal-skills\prototype-to-taro-app" .codebuddy/skills/
```

**Bash（macOS / Linux）**：

```bash
mkdir -p .codebuddy/skills
cp -r <本仓库路径>/prototype-to-taro-app .codebuddy/skills/
```

复制完的项目结构：

```text
skill-swap/
├── .codebuddy/
│   └── skills/
│       └── prototype-to-taro-app/
│           ├── SKILL.md
│           ├── README.md
│           └── resources/
└── （你自己的原型文件，下一步放这里）
```

### 2.3 为什么必须整目录复制

技能是**资源驱动**的：`SKILL.md` 只写规则，真正生成代码时要读：

```text
prototype-to-taro-app/
├── SKILL.md
└── resources/
    ├── config/           # 命名规则、依赖基线、设计 token
    ├── specifications/   # 原型解析契约、双框架代码范式
    ├── templates/        # 工程骨架（shared / vue3 / react）
    ├── tools/            # 解析、预览、校验脚本
    └── demo_output/      # 两套完整示例（可删，不影响生成）
```

只复制 `SKILL.md`，技能读不到模板就会「自由发挥」，生成结果不可控。

> 💡 `resources/demo_output/` 是示例产物，只用于对照参考。嫌体积大可以删，但**建议第一次留着**——生成结果跑不通时可以拿它对比。

### 2.4 可选：装到用户级（所有项目可用）

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.codebuddy\skills" | Out-Null
Copy-Item -Recurse -Force "<本仓库路径>\prototype-to-taro-app" "$HOME\.codebuddy\skills\"
```

---

## 3. 第 2 步：确认技能装好了

### 3.1 查文件

在项目根目录执行，三条都返回 `True` 才算复制完整：

```powershell
Test-Path .codebuddy/skills/prototype-to-taro-app/SKILL.md
Test-Path .codebuddy/skills/prototype-to-taro-app/resources/templates/vue3
Test-Path .codebuddy/skills/prototype-to-taro-app/resources/tools/validate_project.py
```

### 3.2 在 CodeBuddy 里确认

1. 新开一个对话，或重启 IDE 让它重新扫描技能
2. 在 CodeBuddy 里输入 `/skills`，列表里应出现 `prototype-to-taro-app`
3. 「设置 → 技能 / Skills → Project Skills」中同样能看到它

**名字出现在列表里 = 安装成功。**

也可以直接问一句：

```text
我现在有哪些可用的技能？列出和「原型转 Taro 小程序」相关的。
```

---

## 4. 第 3 步：准备原型材料

### 4.1 三种输入，选一种即可

| 输入类型 | 效果 | 适合 |
| --- | --- | --- |
| **HTML/CSS 原型** | 最好，可用脚本自动解析出页面、组件、字段 | 有前端原型 |
| **截图** | 好，AI 直接读图还原布局与配色 | 只有设计稿 |
| **PRD 页面清单** | 一般，需要你补充字段和交互 | 早期项目 |

### 4.2 在项目里建原型目录

```text
skill-swap/
├── prototype/
│   ├── index.html        # 首页原型（或 home.png / 设计稿截图）
│   ├── detail.html       # 详情页
│   └── pages.md          # 可选：PRD 页面清单
└── .codebuddy/skills/
```

### 4.3 原型写得越「语义化」，生成越准

解析脚本靠 class 名和中文文本做启发式推断，所以：

- 用 `card` / `tag` / `avatar` / `empty` 这类语义化 class，组件会被正确识别
- 用 `list` / `form` / `detail` / `grid` 这类词，布局类型判定更准
- 主色用 `#2B6DE5` 这种 6 位 hex 写在样式里，脚本会取出现频次最高的那个
- 页面标题写进 `<title>` 或 `<h1>`

### 4.4 用脚本先解析一遍（可选但推荐）

HTML 原型可以直接跑解析器，产出 `proto_context.json`，比让 AI 纯看图更可控：

```powershell
cd .codebuddy/skills/prototype-to-taro-app
python resources/tools/parse_prototype.py ../../../prototype/index.html `
  --out ../../../prototype/proto_context.json `
  --project skill-swap `
  --title "技能互换" `
  --framework vue3 `
  --targets weapp,h5
```

注意 `--framework` 必填，不写会直接报错：

```text
error: the following arguments are required: --framework
```

生成的 `proto_context.json` 是**初稿**，重点看 `diagnostics.need_confirm`，把里面列的待确认项补上（页面跳转关系、是否需要 tabBar、空态样式等）。

---

## 5. 第 4 步：发起生成（最关键）

### 5.1 先回答框架选择

技能第一步一定会问你：

```text
请确认用哪个框架生成：
[A] Vue3 + TS（推荐给熟悉 Vue 的团队，UI 还原快）
[B] React + TS（适合复杂业务、状态流较重的企业应用）
```

**必须明确回答，不要说"你看着办"。** 因为：

- 页面文件后缀不同（`.vue` vs `.tsx`）
- 入口不同（`app.ts` vs `app.tsx`）
- 状态管理不同（Pinia vs Dva）
- UI 库不同（Vant vs taro-ui）

一个工程**只能有一种**写法，混用会编译失败。

### 5.2 提示词模板（Vue3 分支）

```text
请使用 prototype-to-taro-app 技能，根据 prototype/ 下的原型生成 Taro 小程序工程。

【前置确认】
- 框架：Vue3 + TS（Vant + Pinia）
- 目标平台：微信小程序 + H5
- 需要登录与权限路由：是
- 需要暗黑模式：否

【工程信息】
- 工程名：skill-swap
- 应用标题：技能互换
- appid：先留占位，我后面自己填

【页面清单】
1. pages/home/index      首页，列表，tab
2. pages/detail/index    详情页，展示单条
3. pages/login/index     登录页，免登录白名单
4. pages/mine/index      我的，tab

【要求】
1) 每个页面必须有 index.config.ts，并在 app.config.ts 的 pages 中注册；
2) 列表页做三态渲染（loading / empty / 有数据）+ 下拉刷新 + 上拉加载；
3) 请求统一走 services/request.ts，页面禁止直接调用 Taro.request；
4) src/mock/ 下造与真实接口同形状的 mock 数据，列表至少 10 条，含超长文本与空数组边界；
5) 生成后运行 resources/tools/validate_project.py 自检，确保 0 错误；
6) 注释与界面文案用中文。
```

### 5.3 提示词模板（React 分支）

把「前置确认」改成：

```text
- 框架：React + TS（taro-ui + Dva + Immer）
```

其余保持不变。页面仍然是 `pages/home/index.tsx`，状态放 `src/models/`。

### 5.4 只有截图时怎么写

```text
请使用 prototype-to-taro-app 技能，根据 prototype/home.png、prototype/detail.png 生成 Taro 小程序工程。
框架选 Vue3，目标平台微信小程序。
按截图还原布局、配色和间距，先用 mock 数据，字段名先用合理英文命名并在最后列出待确认项。
```

### 5.5 点名技能更稳

装了多个技能时，**在提示词里直接写技能名**，别指望自动匹配。

---

## 6. 生成过程中会发生什么

正常流程里，Agent 应该依次做这些事——如果它跳过第 2、3 步直接写代码，**停下来纠正它**：

1. 读 `SKILL.md`
2. 读 `resources/config/`（命名规则、依赖基线、设计 token）
3. 读 `resources/specifications/`（原型解析契约、双框架范式）
4. （HTML 输入）跑 `parse_prototype.py` 得到 `proto_context.json`
5. 跑 `preview_plan.py` 确认要生成哪些文件
6. 从 `resources/templates/{vue3|react}/` + `shared/` 复制骨架，替换占位符
7. 逐页生成页面、store/model、service、mock
8. 跑 `validate_project.py` 自检

替换的占位符只有这几个：

| 占位符 | 含义 | 示例 |
| --- | --- | --- |
| `{{project_name}}` | 工程名（kebab-case） | `skill-swap` |
| `{{app_title}}` | 小程序显示名 | `技能互换` |
| `{{appid}}` | 小程序 appid | `touristappid`（占位） |
| `{{primary_color}}` | 主色 | `#2B6DE5` |
| `{{framework}}` | `vue3` 或 `react` | `vue3` |
| `{{build_date}}` | 构建日期 | 自动填 |

生成完成后，Agent 会输出一段类似这样的总结：

```text
✅ 已生成 Taro 工程：skill-swap（Vue3 分支）
📁 config/ src/pages/(4) src/store/ src/services/ src/mock/
🎨 已还原：首页 / 详情 / 登录 / 我的；下拉刷新、上拉加载、登录跳转
▶️ pnpm install → pnpm dev:weapp → 微信开发者工具打开 dist/
⚠️ 待确认：小程序 appid、列表真实字段
```

---

## 7. 三个辅助脚本速查

脚本都在 `.codebuddy/skills/prototype-to-taro-app/resources/tools/` 下，只用标准库，`python 脚本路径` 直接跑。

### 7.1 `parse_prototype.py`：HTML → proto_context.json

```text
python resources/tools/parse_prototype.py <原型.html> [选项]

  --out        输出路径，默认 proto_context.json
  --project    工程名（kebab-case），默认 prototype-app
  --title      应用标题，不填则从 <title>/<h1> 提取
  --framework  vue3 | react（必填）
  --targets    目标平台，逗号分隔：weapp,h5,alipay,rn
  --page-name  页面名，默认 index
```

### 7.2 `preview_plan.py`：先看会生成哪些文件

```powershell
python resources/tools/preview_plan.py proto_context.json
```

输出工程名、框架、页面清单、**计划生成的文件列表**、以及待确认项。

> ⚠️ 这个脚本读不到 `project.framework` 时会退回 `vue3`。所以 `proto_context.json` 里一定要有 `"framework": "vue3"` 或 `"react"`。

### 7.3 `validate_project.py`：生成后自检

```powershell
python resources/tools/validate_project.py ./skill-swap
python resources/tools/validate_project.py ./skill-swap --json
```

只做静态检查，**不需要 Node 环境**；退出码 0 表示无阻断性错误。12 项检查：

| 检查项 | 失败常见原因 |
| --- | --- |
| `config/index.ts` 声明 framework | 占位符 `{{framework}}` 没替换 |
| `src/app.config.ts` 存在 | 骨架没复制全 |
| 入口文件与框架匹配 | Vue3 却生成了 `app.tsx` |
| 页面已在 `app.config.ts` 注册 | 新建了目录但忘了注册（**页面点不进去的首要原因**） |
| 每个页面有 `index.config.ts` | 标题会变成默认值 |
| 未混用两套框架写法 | Vue3 工程里出现 `.tsx` 页面 |
| 存在统一请求封装 | 缺 `services/request.ts` |
| 页面未直接 `Taro.request` | 页面里直接发了请求 |
| 状态管理目录符合框架 | Vue3 该有 `store/`，React 该有 `models/` |
| tabBar 配置合法 | 数量不在 2-5，或指向未注册页面 |
| 存在类型定义 | 缺 `types/index.ts` |
| 列表页有三态渲染 | 只有 loading，没有 empty |

---

## 8. 第 5 步：检查生成结果

### 8.1 应该是这样的目录

```text
skill-swap/
├── config/
│   ├── index.ts            # framework: 'vue3'
│   ├── dev.ts / prod.ts
├── src/
│   ├── app.ts              # Vue3 入口（React 为 app.tsx）
│   ├── app.config.ts       # pages / tabBar / window
│   ├── app.scss
│   ├── pages/
│   │   ├── home/  index.vue + index.config.ts + index.scss
│   │   ├── detail/ login/ mine/
│   ├── components/Empty.vue
│   ├── store/index.ts + modules/{user,skill}.ts   # React 为 models/
│   ├── services/request.ts + modules/{auth,skill}.ts
│   ├── mock/skill.mock.ts
│   ├── styles/variables.scss
│   └── types/index.ts
├── project.config.json
├── package.json
├── tsconfig.json
└── babel.config.js
```

### 8.2 手动核对清单

- [ ] `config/index.ts` 里 `framework` 是 `vue3` 或 `react`，不是 `{{framework}}`
- [ ] 4 个页面都出现在 `app.config.ts` 的 `pages` 数组中
- [ ] 每个页面目录都有 `index.config.ts`（有标题）
- [ ] 页面后缀统一：全 `.vue` 或全 `.tsx`，没有混着来
- [ ] 列表页有 loading / empty / 有数据三态
- [ ] 请求都走 `services/request.ts`，页面里搜不到 `Taro.request`
- [ ] mock 列表 ≥ 10 条，含超长文本和空数组场景
- [ ] `appid` 是占位值，等你自己填

### 8.3 发现不对，怎么让它改

不要自己动手，直接指出问题让它重做：

```text
pages/mine/index 没有在 app.config.ts 的 pages 里注册，请补上；
另外 pages/ 下的页面后缀混用了 .vue 和 .tsx，请统一成 .vue（本工程是 Vue3 分支）。
```

改完再跑一次 `validate_project.py`。

---

## 9. 第 6 步：把它跑起来

### 9.1 安装依赖

```powershell
cd skill-swap
pnpm install
```

依赖版本基线见 `resources/config/dependency_baseline.json`，Taro 为 4.x。

### 9.2 编译微信小程序

```powershell
pnpm dev:weapp
```

终端出现 `Compiled successfully` 后：

1. 打开**微信开发者工具**
2. 「导入项目」→ 目录选 `skill-swap/dist`
3. AppID 处填你自己的，或点「测试号」
4. 勾选「不校验合法域名」（因为还在用 mock）

> `project.config.json` 里的 `appid` 只是占位（默认 `touristappid`），必须换成你自己的，否则真机预览受限。

### 9.3 编译 H5（最快看效果）

```powershell
pnpm dev:h5
```

浏览器打开终端提示的地址（通常 `http://localhost:10086`）。**第一次验收建议先看 H5**，不用装微信开发者工具。

### 9.4 其他平台

```powershell
pnpm dev:alipay     # 支付宝小程序
pnpm build:weapp    # 生产构建
pnpm type-check     # 只跑类型检查
```

RN 端 Taro 4 需额外配置，首次不建议直接上。

### 9.5 看到什么算成功

| 现象 | 说明 |
| --- | --- |
| 首页出现 10 条 mock 卡片 | mock 生效 |
| 下拉能看到刷新动画 | 分页/刷新接好了 |
| 点卡片进详情 | 路由跳转正确 |
| 清掉 storage 后自动跳登录 | 权限路由生效 |
| 列表置空显示「暂无数据」 | 空态渲染通过 |

---

## 10. 常见问题

### 10.1 技能没被调用

- 提示词里**点名**：`请使用 prototype-to-taro-app 技能`
- 确认 `.codebuddy/skills/prototype-to-taro-app/SKILL.md` 存在
- 新开对话或重启 IDE 重新扫描

### 10.2 报「找不到模板 / 读不到 resources」

只复制了 `SKILL.md`。回到第 2 步用 `Copy-Item -Recurse` / `cp -r` **整目录复制**，再跑 3.1 的三条 `Test-Path`。

### 10.3 它没问我框架就开始了

这是本技能最严重的问题。直接打断：

```text
请先停下来，问我选 Vue3 还是 React，再开始生成。
```

如果已经生成了一半，最省事的做法是**删掉重来**——两套写法混在一个工程里，越改越乱。

### 10.4 页面生成了，但点不进去

99% 是没在 `app.config.ts` 的 `pages` 里注册。Taro 只会编译注册过的页面。

### 10.5 页面标题不对

缺 `index.config.ts`，或里面的 `navigationBarTitleText` 没写。

### 10.6 样式在小程序里全乱了

- Taro 默认 `designWidth: 750`，写 `px` 会按 750 设计稿换算，别把 H5 的 `px` 直接搬进来
- 小程序不支持部分 CSS 选择器（如 `*`、属性选择器）
- 用了 Vant 时注意是 **Vant Weapp**，不是 H5 版 Vant

### 10.7 主包超过 2MB

微信主包上限 2MB。把静态图片放 CDN 或分包，`src/mock/` 里的长文本别塞大图 base64。

### 10.8 想换成真实接口了

**不用改页面，也不用改 `request.ts`**。`services/request.ts` 里的地址来自编译期常量：

```ts
// src/services/request.ts
declare const TARO_APP_API: string
export const BASE_URL = TARO_APP_API || 'https://api.example.com'
```

所以要改的是多环境配置：

```ts
// config/dev.ts
defineConstants: {
  TARO_APP_API: '"https://dev-api.your-domain.com"',
}

// config/prod.ts
defineConstants: {
  TARO_APP_API: '"https://api.your-domain.com"',
}
```

再把页面里读 mock 的地方换成 `services/modules/xxx.ts` 的真实函数（`request.ts` 已统一处理 token 注入、`{ code, message, data }` 解包、401 跳登录）。因为页面只依赖 service 层，**页面结构不用动**。

### 10.9 React 分支里出现了 `.vue`

混用了。让 Agent 统一成 `.tsx`，并同步把 `models/` 的 Dva 写法补齐。

### 10.10 生成完想加一个页面

做**增量生成**，不要重建工程：

```text
请使用 prototype-to-taro-app 技能，在现有工程 skill-swap 上新增 pages/order-list/index 页面。
要求：只新增该页面相关文件，注册到 app.config.ts；不要改动 services/request.ts、store/ 和已有页面。
```

---

## 11. 附录

### A. 双框架差异速查（生成时最易出错）

| 维度 | Vue3 分支 | React 分支 |
| --- | --- | --- |
| 页面文件 | `index.vue` | `index.tsx` |
| 入口 | `app.ts`（createApp） | `app.tsx`（Provider 包裹 Dva store） |
| 组件写法 | `<script setup>` | 函数组件 + Hooks |
| 状态 | Pinia `defineStore` | Dva model（namespace/state/effects/reducers） |
| 读状态 | `storeToRefs(useUserStore())` | `useSelector((s) => s.user)` |
| 改状态 | 直接改变量 | `dispatch({ type: 'user/setToken' })` |
| UI 库 | Vant / Vant Weapp | taro-ui |
| 生命周期 | `onShow` / `onLoad` | `useDidShow` / `useLoad` |

### B. 命名规范

| 对象 | 规则 | 示例 |
| --- | --- | --- |
| 页面目录 | kebab-case | `pages/order-list/` |
| 页面文件 | `index.vue` / `index.tsx` | — |
| 页面配置 | `index.config.ts` | — |
| 组件 | PascalCase 文件 | `OrderCard.vue` |
| Store（Vue3） | `use<Name>Store` | `useUserStore` |
| Model（React） | 小写 | `user` |
| Service 函数 | camelCase | `getOrderList` |
| 类型 | PascalCase | `OrderItem` |

### C. 和其它「原型转应用」技能怎么分工

| 技能 | 目标平台 | 技术栈 | 什么时候选 |
| --- | --- | --- | --- |
| **`prototype-to-taro-app`（本技能）** | 小程序 / H5 / RN | Taro（Vue3 或 React） | 小程序优先，或多端含 RN |
| `prototype-to-app-uniappx` | App / 小程序 / H5 | uni-app x | 要原生 App 且接受 Vue 语法 |
| `prototype-to-flutter-app` | Android / iOS / Web | Flutter | 只做 App |

### D. 更多资料

| 内容 | 路径 |
| --- | --- |
| 技能定义（AI 读的规则） | `.codebuddy/skills/prototype-to-taro-app/SKILL.md` |
| 技能说明（人读的） | `.codebuddy/skills/prototype-to-taro-app/README.md` |
| 双框架代码范式对照 | `resources/specifications/framework_patterns.md` |
| 原型解析契约 | `resources/specifications/prototype_parser_contract.md` |
| 依赖版本基线 | `resources/config/dependency_baseline.json` |
| 完整示例产物 | `resources/demo_output/skill-swap-vue3/`、`skill-swap-react/` |
| Taro 官方文档 | <https://docs.taro.zone/> |

---

## 一句话总结

```text
建空项目 → 整目录复制技能到 .codebuddy/skills/ → 准备原型
→ 明确选 Vue3 或 React → 点名技能生成 → 跑 validate_project.py
→ 核对 pages 注册与后缀统一 → pnpm install → pnpm dev:h5 / dev:weapp
```

先让一个页面（首页列表）跑通，再补详情、登录、我的——比一次性生成 10 个页面好排查得多。
