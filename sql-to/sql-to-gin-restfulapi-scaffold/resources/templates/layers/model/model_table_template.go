// 【AUTO-GENERATED】
// 本文件由 sql-to-gin-restfulapi-scaffold 生成，内容可被增量更新覆盖

package models

{{imports_block}}

type {{entity_name}}Model struct {
{{fields_block}}
}

func (m *{{entity_name}}Model) TableName() string {
	return "{{table_name_raw}}"
}
