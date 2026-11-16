// 【AUTO-GENERATED】
// 本文件由 sql-to-gin-restfulapi-scaffold 生成，内容可被增量更新覆盖

package models

import "time"

type SysDepartmentModel struct {
	DepartmentID int64 `gorm:"column:departmentID;type:bigint;primaryKey;not null;" json:"departmentID" form:"departmentID"`
	ParentDepartmentID int64 `gorm:"column:parentDepartmentID;type:bigint;not null;default:0;" json:"parentDepartmentID" form:"parentDepartmentID"`
	CollegeID string `gorm:"column:collegeID;type:varchar(20);default:NULL;" json:"collegeID" form:"collegeID"`
	DepartmentName string `gorm:"column:departmentName;type:varchar(255);default:NULL;" json:"departmentName" form:"departmentName"`
	DepartmentType bool `gorm:"column:departmentType;type:tinyint(1);default:1;" json:"departmentType" form:"departmentType"`
	IsDelete bool `gorm:"column:isDelete;type:tinyint(1);not null;default:0;" json:"isDelete" form:"isDelete"`
	AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *SysDepartmentModel) TableName() string {
	return "sys_department"
}
