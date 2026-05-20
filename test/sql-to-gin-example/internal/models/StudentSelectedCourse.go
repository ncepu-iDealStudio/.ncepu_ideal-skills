// coding: utf-8
// @Author : lryself
// @Software: GoLand

package models

import (
    "study_flask_api/utils/structs"
     "time" 
)

type StudentSelectedCourseModel struct { 
    AutoID int `gorm:"column:autoID;primaryKey;type:int;not null;" json:"autoID" form:"autoID"`
    StudentID string `gorm:"column:studentID;type:varchar(20);not null;" json:"studentID" form:"studentID"`
    CourseID string `gorm:"column:courseID;type:varchar(15);not null;" json:"courseID" form:"courseID"`
    Score int `gorm:"column:score;type:int;" json:"score" form:"score"`
    IsDelete bool `gorm:"column:isDelete;type:tinyint(1);default:0;" json:"isDelete" form:"isDelete"`
    AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *StudentSelectedCourseModel) TableName() string {
    return "student_selected_course"
}

func (m *StudentSelectedCourseModel) GetAutoID() int {
    return m.AutoID
}

func (m *StudentSelectedCourseModel) SetAutoID(AutoID int) {
    m.AutoID = AutoID
}

func (m *StudentSelectedCourseModel) GetStudentID() string {
    return m.StudentID
}

func (m *StudentSelectedCourseModel) SetStudentID(StudentID string) {
    m.StudentID = StudentID
}

func (m *StudentSelectedCourseModel) GetCourseID() string {
    return m.CourseID
}

func (m *StudentSelectedCourseModel) SetCourseID(CourseID string) {
    m.CourseID = CourseID
}

func (m *StudentSelectedCourseModel) GetScore() int {
    return m.Score
}

func (m *StudentSelectedCourseModel) SetScore(Score int) {
    m.Score = Score
}

func (m *StudentSelectedCourseModel) GetIsDelete() bool {
    return m.IsDelete
}

func (m *StudentSelectedCourseModel) SetIsDelete(IsDelete bool) {
    m.IsDelete = IsDelete
}

func (m *StudentSelectedCourseModel) GetAddTime() time.Time {
    return m.AddTime
}

func (m *StudentSelectedCourseModel) SetAddTime(AddTime time.Time) {
    m.AddTime = AddTime
}


func (m *StudentSelectedCourseModel) GetModelMap() (map[string]interface{}, error) {
    return structs.StructToMap(m, "json")
}

func (m *StudentSelectedCourseModel) Assign(in interface{}) {
    structs.StructAssign(m, in, "json")
}