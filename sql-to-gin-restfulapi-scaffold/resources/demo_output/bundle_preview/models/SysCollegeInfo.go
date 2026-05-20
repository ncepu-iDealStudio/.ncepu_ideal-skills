package models

import "time"

type SysCollegeInfoModel struct {
	AutoID int64 `gorm:"column:autoID;type:bigint;primaryKey;not null;" json:"autoID" form:"autoID"`
	CollegeID string `gorm:"column:collegeID;type:varchar(20);default:NULL;" json:"collegeID" form:"collegeID"`
	CollegeName string `gorm:"column:collegeName;type:varchar(50);default:NULL;" json:"collegeName" form:"collegeName"`
	IsDelete bool `gorm:"column:isDelete;type:tinyint(1);default:0;" json:"isDelete" form:"isDelete"`
	AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *SysCollegeInfoModel) TableName() string {
	return "sys_collegeInfo"
}
