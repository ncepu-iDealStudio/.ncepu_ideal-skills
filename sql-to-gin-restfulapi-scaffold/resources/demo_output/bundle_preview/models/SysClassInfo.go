package models

import "time"

type SysClassInfoModel struct {
	AutoID int `gorm:"column:autoID;type:int;primaryKey;not null;" json:"autoID" form:"autoID"`
	ClassID string `gorm:"column:classID;type:varchar(10);default:NULL;" json:"classID" form:"classID"`
	CollegeID string `gorm:"column:collegeID;type:varchar(20);default:NULL;" json:"collegeID" form:"collegeID"`
	ClassName string `gorm:"column:className;type:varchar(20);default:NULL;" json:"className" form:"className"`
	IsDeleted bool `gorm:"column:isDeleted;type:tinyint(1);default:0;" json:"isDeleted" form:"isDeleted"`
	AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *SysClassInfoModel) TableName() string {
	return "sys_classInfo"
}
