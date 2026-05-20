package models

{{imports_block}}

type {{entity_name}}Model struct {
{{fields_block}}
}

func (m *{{entity_name}}Model) TableName() string {
	return "{{table_name_raw}}"
}
