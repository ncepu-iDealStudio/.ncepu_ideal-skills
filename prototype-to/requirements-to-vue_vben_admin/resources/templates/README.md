# 模板说明

本目录是从**真实 vben5 仓库验证通过**的产物中提取的可复用模板。
生成时复制并替换占位符，不要原样拷贝（含示例业务语义）。

| 文件 | 用途 | 需替换的占位 |
| --- | --- | --- |
| `routes/route_module_template.ts` | 一级模块路由文件 | 模块名、path、icon、order、children |
| `views/crud_list_template.vue` | CRUD 列表页 | 标题、API 函数名、字段 |
| `views/crud_data_template.ts` | 列定义 + 表单 schema | 字段名、标签、组件类型 |
| `views/crud_form_template.vue` | 新增/编辑抽屉 | API 函数名 |
| `views/dashboard_list_template.vue` | 数据看板页 | 卡片指标、图表轴与数据 |
| `api/api_module_template.ts` | API 模块 | namespace 名、路径、字段类型 |

## 关键约束（来自真实仓库验证）

1. UI 组件从 **`ant-design-vue`** 导入（web-antd），不是 `antdv-next`
2. `VbenTableAction` 从 **`@vben/common-ui`** 导入，不是 `#/adapter/vxe-table`
3. 路由文件放 `src/router/routes/modules/`，**不要改** `routes/index.ts`
4. 所有跨目录引用用 **`#/`** 别名
