// coding: utf-8
// @Author : lryself
// @Software: GoLand

package dao
import (
    "errors"
    "study_flask_api/internal/globals/database"
    "study_flask_api/internal/models"
)

type VStudentCourseScoreDao struct {
    models.VStudentCourseScoreModel
}

func (m *VStudentCourseScoreDao) Get(args map[string]any) error {
	mysqlManager := database.GetMysqlClient()
	return mysqlManager.Where(args).Take(m).Error
}

func (m *VStudentCourseScoreDao) Add(args map[string]any) error {
    mysqlManager := database.GetMysqlClient()
    err := m.Get(args)
    if err == nil {
        return errors.New("数据已存在")
    }
    return mysqlManager.Create(&m).Error
}

func (m *VStudentCourseScoreDao) Update(query map[string]any, args map[string]any) error {
    mysqlManager := database.GetMysqlClient()
    err := m.Get(query)
    if err != nil {
        return err
    }
    return mysqlManager.Model(&m).Updates(args).Error
}

func (m *VStudentCourseScoreDao) Delete(args map[string]any) error {
    mysqlManager := database.GetMysqlClient()
    err := m.Get(args)
    if err != nil {
        return err
    }
    return mysqlManager.Model(&m).Delete(&m).Error
}