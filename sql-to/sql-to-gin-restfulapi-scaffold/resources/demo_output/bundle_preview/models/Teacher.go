// 【AUTO-GENERATED】
// 本文件由 sql-to-gin-restfulapi-scaffold 生成，内容可被增量更新覆盖

package models

import "time"

type TeacherModel struct {
	AutoID int `gorm:"column:autoID;type:int;primaryKey;not null;" json:"autoID" form:"autoID"`
	TeacherID string `gorm:"column:teacherID;type:varchar(15);not null;" json:"teacherID" form:"teacherID"`
	UserID string `gorm:"column:userID;type:varchar(22);not null;" json:"userID" form:"userID"`
	DepartmentID int64 `gorm:"column:departmentID;type:bigint;default:NULL;" json:"departmentID" form:"departmentID"`
	Name string `gorm:"column:name;type:varchar(50);not null;" json:"name" form:"name"`
	Email string `gorm:"column:email;type:varchar(100);default:NULL;" json:"email" form:"email"`
	Phone string `gorm:"column:phone;type:varchar(20);default:NULL;" json:"phone" form:"phone"`
	OfficeAddress string `gorm:"column:officeAddress;type:varchar(255);default:NULL;" json:"officeAddress" form:"officeAddress"`
	IsDelete bool `gorm:"column:isDelete;type:tinyint(1);not null;default:0;" json:"isDelete" form:"isDelete"`
	AddTime time.Time `gorm:"column:addTime;type:timestamp;not null;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
	UpdateTime time.Time `gorm:"column:updateTime;type:timestamp;not null;default:CURRENT_TIMESTAMP;" json:"updateTime" form:"updateTime"`
}

func (m *TeacherModel) TableName() string {
	return "teacher"
}
