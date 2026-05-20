package models

import "time"

type CourseModel struct {
	AutoID int `gorm:"column:autoID;type:int;primaryKey;not null;" json:"autoID" form:"autoID"`
	CourseID string `gorm:"column:courseID;type:varchar(20);default:NULL;" json:"courseID" form:"courseID"`
	CourseName string `gorm:"column:courseName;type:varchar(50);default:NULL;" json:"courseName" form:"courseName"`
	TeacherID string `gorm:"column:teacherID;type:varchar(15);default:NULL;" json:"teacherID" form:"teacherID"`
	Credit float64 `gorm:"column:credit;type:float;default:NULL;" json:"credit" form:"credit"`
	IsDelete bool `gorm:"column:isDelete;type:tinyint(1);default:0;" json:"isDelete" form:"isDelete"`
	AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *CourseModel) TableName() string {
	return "course"
}
