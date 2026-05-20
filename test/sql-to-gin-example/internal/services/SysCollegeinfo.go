// coding: utf-8
// @Author : lryself
// @Software: GoLand

package services

import (
    "study_flask_api/internal/dao"
    "study_flask_api/internal/globals/database"
    "study_flask_api/internal/globals/parser"
)

type SysCollegeinfoService struct {
    dao.SysCollegeinfoDao
}

func (m *SysCollegeinfoService) GetList() ([]SysCollegeinfoService, error) {
    mysqlManager := database.GetMysqlClient()
    results := []SysCollegeinfoService{}

    rows, err := mysqlManager.Table(m.TableName()).Where("IsDeleted", false).Where(m).Rows()
    defer rows.Close()
    if err != nil {
        return results, err
    }
    for rows.Next() {
        var result SysCollegeinfoService
        err = mysqlManager.ScanRows(rows, &result)
        if err != nil {
            return results, err
        }
        results = append(results, result)
    }
    return results, nil
}


func (m *SysCollegeinfoService) GetListByPage(p parser.ListParser) ([]SysCollegeinfoService, int64, error) {
    mysqlManager := database.GetMysqlClient()
    results := []SysCollegeinfoService{}
    var count int64 = 0

    rows, err := mysqlManager.Table(m.TableName()).Where("IsDeleted", false).Where(m).Count(&count).Limit(p.Size).Offset((p.Page - 1) * p.Size).Order(p.Order).Rows()
    defer rows.Close()
    if err != nil {
        return results, 0, err
    }
    for rows.Next() {
        var result SysCollegeinfoService
        err = mysqlManager.ScanRows(rows, &result)
        if err != nil {
            return results, 0, err
        }
        results = append(results, result)
    }
    return results, count, nil
}