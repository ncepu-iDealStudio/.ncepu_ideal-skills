package services

import (
	"{{module_name}}/internal/dao"
	"{{module_name}}/internal/globals/database"
	"{{module_name}}/internal/globals/parser"
)

type {{entity_name}}Service struct {
	dao.{{entity_name}}Dao
}

func (m *{{entity_name}}Service) GetList() ([]{{entity_name}}Service, error) {
	mysqlManager := database.GetMysqlClient()
	results := []{{entity_name}}Service{}
	rows, err := mysqlManager.Table(m.TableName()).Where(m).Rows()
	if err != nil {
		return results, err
	}
	defer rows.Close()
	for rows.Next() {
		var result {{entity_name}}Service
		err = mysqlManager.ScanRows(rows, &result)
		if err != nil {
			return results, err
		}
		results = append(results, result)
	}
	return results, nil
}

func (m *{{entity_name}}Service) GetListByPage(p parser.ListParser) ([]{{entity_name}}Service, int64, error) {
	mysqlManager := database.GetMysqlClient()
	results := []{{entity_name}}Service{}
	var count int64 = 0

	rows, err := mysqlManager.Table(m.TableName()).Where(m).Count(&count).Limit(p.Size).Offset((p.Page-1)*p.Size).Order(p.Order).Rows()
	if err != nil {
		return results, 0, err
	}
	defer rows.Close()
	for rows.Next() {
		var result {{entity_name}}Service
		err = mysqlManager.ScanRows(rows, &result)
		if err != nil {
			return results, 0, err
		}
		results = append(results, result)
	}
	return results, count, nil
}
