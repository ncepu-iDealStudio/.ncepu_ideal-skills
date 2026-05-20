package models

import "time"

type TeacherModel struct {
	AutoID int `gorm:"column:autoID;type:int;primaryKey;not null;" json:"autoID" form:"autoID"`
	TeacherID string `gorm:"column:teacherID;type:varchar(15);default:NULL;" json:"teacherID" form:"teacherID"`
	UserID string `gorm:"column:userID;type:varchar(22);default:NULL;" json:"userID" form:"userID"`
	DepartmentID int64 `gorm:"column:departmentID;type:bigint;default:NULL;" json:"departmentID" form:"departmentID"`
	Name string `gorm:"column:name;type:varchar(10);default:NULL;" json:"name" form:"name"`
	Email string `gorm:"column:email;type:varchar(50);default:NULL;" json:"email" form:"email"`
	Phone string `gorm:"column:phone;type:varchar(15);default:NULL;" json:"phone" form:"phone"`
	OfficeAddress string `gorm:"column:officeAddress;type:varchar(255);default:NULL;" json:"officeAddress" form:"officeAddress"`
	IsDelete bool `gorm:"column:isDelete;type:tinyint(1);default:0;" json:"isDelete" form:"isDelete"`
	AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *TeacherModel) TableName() string {
	return "teacher"
}
