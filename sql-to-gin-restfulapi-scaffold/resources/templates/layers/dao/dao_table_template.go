package dao

import (
	"errors"
	"{{module_name}}/internal/globals/database"
	"{{module_name}}/internal/models"
)

type {{entity_name}}Dao struct {
	models.{{entity_name}}Model
}

func (m *{{entity_name}}Dao) Get(args map[string]any) error {
	mysqlManager := database.GetMysqlClient()
	return mysqlManager.Where(args).Take(m).Error
}

func (m *{{entity_name}}Dao) Add(args map[string]any) error {
	mysqlManager := database.GetMysqlClient()
	err := m.Get(args)
	if err == nil {
		return errors.New("数据已存在")
	}
	return mysqlManager.Create(&m).Error
}

func (m *{{entity_name}}Dao) Update(query map[string]any, args map[string]any) error {
	mysqlManager := database.GetMysqlClient()
	err := m.Get(query)
	if err != nil {
		return err
	}
	return mysqlManager.Model(&m).Updates(args).Error
}

func (m *{{entity_name}}Dao) Delete(args map[string]any) error {
	mysqlManager := database.GetMysqlClient()
	err := m.Get(args)
	if err != nil {
		return err
	}
	return mysqlManager.Model(&m).Delete(&m).Error
}
