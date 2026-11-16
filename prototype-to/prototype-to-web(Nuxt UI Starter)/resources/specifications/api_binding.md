# 已有工程：按接口文档对接真实数据

适用：目标目录**已经是**本技能生成的 Nuxt UI Starter 工程（或同结构工程），用户提供接口文档，要求页面改用真实数据。

从零生成工程、按原型图新增列表页，都不走本文。本文也不实现后端。

---

## 1. 先判定，再动手

骨架已存在，当目录里**同时**有：

- `nuxt.config.ts`（modules 含 `@nuxt/ui`）
- `app/services/`，且其中有 `*Service.ts`

没有 service 层就停。不要在 `app/pages/` 或 `app/composables/` 里写 `$fetch` / `fetch(`。

| 场景 | 判定 | 动作 |
| --- | --- | --- |
| **对接已有方法** | 页面已经通过某个 service 方法取数 | 用文档匹配该方法，在该方法内映射并切换 |
| **文档多出接口** | 文档有写接口、详情接口，但工程没有对应页面或方法 | 不生成页面，不新增方法。列入本次未对接 |
| **文档对不上** | 路径、字段或包络无法唯一对应 | 停下来问，不猜 |

一次只对接用户这次给出的文档所覆盖的方法。未提到的方法保持 `useMock = true`。

---

## 2. 接受的文档，以及先读什么

不要求用户把文档转成某一种格式。以下都可以：

- OpenAPI / Swagger 的 JSON 或 YAML
- Markdown、Apifox 导出
- 用户粘贴的「方法 + 路径 + 请求参数 + 响应示例」

对每个**已经存在**的 service 方法，只提取这些信息：

| 项 | 用途 |
| --- | --- |
| HTTP 方法与路径 | 替换该方法里的 `$fetch` 地址 |
| 查询参数 / 路径参数 | 仅当页面已经把对应参数传给该方法 |
| 响应字段 | 映射到该方法已经返回的页面类型 |
| 包络 | 是否为 `{ code, data, message }` 或文档写明的其他外壳 |
| 鉴权头 | 文档写明才加，例如 `Authorization` |

先列页面真正用到的字段（组件 props、模板绑定），再和响应字段配对。文档里页面用不到的字段不映射到类型上。

---

## 3. 禁止事项

- 禁止再复制 `resources/templates/project_structure/`
- 禁止改 `app.config.ts`、无关页面、无关组件
- 禁止把后端字段名写进页面或卡片组件
- 禁止引入 axios、Pinia，或其他 HTTP 客户端。继续用 Nuxt 内置 `$fetch`
- 禁止为了接一个请求头去新建登录页、刷新令牌或通用拦截器
- 禁止把接口文档当成页面清单，顺手加栏目或新页面
- 禁止在路径、字段或包络仍有歧义时关掉 `useMock`

---

## 4. 适配只写在对应的 service 里

页面继续调用原来的 composable，composable 继续调用原来的 service 方法，返回类型保持不变。

下面以 `getSkills(): Promise<Skill[]>` 为例。文档中的列表项字段是 `skill_id`、`skill_name`、`publisher_name`，外壳是 `{ code, data, message }`。

```ts
interface SkillListResponse {
  code: number
  message: string
  data: Array<{
    skill_id: string
    skill_name: string
    publisher_name: string
    avatar_url?: string
    tag_list?: string[]
    created_at?: string
  }>
}

const useMockSkills = false
/** 成功码以接口文档为准，不要沿用示例里的 0。 */
const SUCCESS_CODE = 0

export const skillService = {
  async getSkills(fetcher: typeof $fetch = $fetch, apiBase = ''): Promise<Skill[]> {
    if (useMockSkills) {
      await delay(300)
      return mockSkills
    }
    const raw = await fetcher<SkillListResponse>(`${apiBase}/skills`, {
      // 文档写明 Authorization 时才加。凭证读取方式也以文档为准；文档没写就不要猜。
      headers: { Authorization: `Bearer ${accessToken}` }
    })
    if (raw.code !== SUCCESS_CODE) {
      throw new Error(raw.message || '加载失败')
    }
    return raw.data.map(row => ({
      id: row.skill_id,
      title: row.skill_name,
      userName: row.publisher_name,
      avatar: row.avatar_url ?? '',
      tags: row.tag_list ?? [],
      createdAt: row.created_at ?? ''
    }))
  }
}
```

要点：

- `fetcher` 和 `apiBase` 由列表 composable 传入：`useRequestFetch()` 与 `useRuntimeConfig().public.apiBase`。service 里不要再写一份基地址
- 原始响应类型按**这份文档**命名，不替换页面正在用的 `Skill`
- `SUCCESS_CODE` 按文档填写。文档没写成功值时停下来问，不要沿用示例里的 `0`
- 请求头只加文档写明的那一个。示例里的 `accessToken` 表示文档已经说明的凭证；文档没写它从哪来，就删掉 `headers` 并停下来问。不要为这个变量新做登录页
- 同一文件里还有未对接的方法时，用该方法自己的开关（如 `useMockSkills`），不要用一个文件级开关把其他方法一起关掉
- 缺少的可选展示字段用空字符串或空数组，让现有空态和缺图占位继续生效。缺少页面必需字段（如列表项 `id`、主标题）时停下来问

---

## 5. 分页、筛选、详情

- 页面已经有「加载更多」或分页控件，并且文档有对应查询参数时，把参数加到**现有** service 方法上。composable 继续向页面暴露原来的 `items`
- 页面没有分页或筛选交互时，不因为文档里有 `page`、`keyword` 就新做控件
- 文档有详情接口，但工程没有详情页、也没有 `getXxxById` 之类的现有方法时，不新增详情页

---

## 6. 停下来问

遇到下面任一情况，先问用户，不写对接代码：

- 现有方法在文档里找不到唯一的路径
- 同一方法能对上多个路径
- 页面主字段在响应里没有对应字段
- 响应包络有两种以上解释
- 文档要求鉴权，但没写请求头名称，或没写凭证从哪里来
- 成功 `code` 的取值没有写明

能对上的方法可以先做。对不上的方法保持 mock，并在结果里列出原因。

---

## 7. 改完怎么汇报

说明：

- 哪些方法已切换到真实请求（路径、原始字段 → 页面字段）
- 哪些方法仍走 mock，以及原因
- 文档里有、但这次没有接的接口
- 页面和 composable 的调用方式没有改
