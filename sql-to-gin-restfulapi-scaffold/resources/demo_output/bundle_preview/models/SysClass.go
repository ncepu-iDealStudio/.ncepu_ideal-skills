package models

import "time"

type SysClassModel struct {
	ClassID string `gorm:"column:classID;type:varchar(10);primaryKey;not null;" json:"classID" form:"classID"`
	CollegeID string `gorm:"column:collegeID;type:varchar(20);default:NULL;" json:"collegeID" form:"collegeID"`
	ClassName string `gorm:"column:className;type:varchar(20);default:NULL;" json:"className" form:"className"`
	IsDelete bool `gorm:"column:isDelete;type:tinyint(1);default:0;" json:"isDelete" form:"isDelete"`
	AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *SysClassModel) TableName() string {
	return "sys_class"
}
