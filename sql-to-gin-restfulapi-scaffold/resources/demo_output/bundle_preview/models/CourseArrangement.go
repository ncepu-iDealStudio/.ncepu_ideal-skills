package models

import "time"

type CourseArrangementModel struct {
	AutoID int `gorm:"column:autoID;type:int;primaryKey;not null;" json:"autoID" form:"autoID"`
	CourseID string `gorm:"column:courseID;type:varchar(20);default:NULL;" json:"courseID" form:"courseID"`
	TermID string `gorm:"column:termID;type:varchar(50);default:NULL;" json:"termID" form:"termID"`
	ClassTime string `gorm:"column:classTime;type:varchar(20);default:NULL;" json:"classTime" form:"classTime"`
	Count int `gorm:"column:count;type:int;default:NULL;" json:"count" form:"count"`
	IsDelete bool `gorm:"column:isDelete;type:tinyint(1);default:0;" json:"isDelete" form:"isDelete"`
	AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *CourseArrangementModel) TableName() string {
	return "course_arrangement"
}
