package models

import "time"

type SysDepartmentInfoModel struct {
	AutoID int64 `gorm:"column:autoID;type:bigint;primaryKey;not null;" json:"autoID" form:"autoID"`
	DepartmentID int64 `gorm:"column:departmentID;type:bigint;default:NULL;" json:"departmentID" form:"departmentID"`
	ParentDepartmentID int64 `gorm:"column:parentDepartmentID;type:bigint;not null;default:0;" json:"parentDepartmentID" form:"parentDepartmentID"`
	CollegeID string `gorm:"column:collegeID;type:varchar(20);default:NULL;" json:"collegeID" form:"collegeID"`
	DepartmentName string `gorm:"column:departmentName;type:varchar(255);default:NULL;" json:"departmentName" form:"departmentName"`
	DepartmentType bool `gorm:"column:departmentType;type:tinyint(1);default:1;" json:"departmentType" form:"departmentType"`
	IsDeleted bool `gorm:"column:isDeleted;type:tinyint(1);not null;default:0;" json:"isDeleted" form:"isDeleted"`
	AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *SysDepartmentInfoModel) TableName() string {
	return "sys_departmentInfo"
}
