// 【AUTO-GENERATED】
// 本文件由 sql-to-gin-restfulapi-scaffold 生成，内容可被增量更新覆盖

package models

import "time"

type StudentSelectedCourseModel struct {
	AutoID int `gorm:"column:autoID;type:int;primaryKey;not null;" json:"autoID" form:"autoID"`
	StudentID string `gorm:"column:studentID;type:varchar(20);not null;" json:"studentID" form:"studentID"`
	CourseID string `gorm:"column:courseID;type:varchar(15);not null;" json:"courseID" form:"courseID"`
	Score int `gorm:"column:score;type:int;default:NULL;" json:"score" form:"score"`
	IsDelete bool `gorm:"column:isDelete;type:tinyint(1);default:0;" json:"isDelete" form:"isDelete"`
	AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *StudentSelectedCourseModel) TableName() string {
	return "student_selected_course"
}
