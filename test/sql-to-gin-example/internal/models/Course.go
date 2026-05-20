// coding: utf-8
// @Author : lryself
// @Software: GoLand

package models

import (
    "study_flask_api/utils/structs"
     "time" 
)

type CourseModel struct { 
    AutoID int `gorm:"column:autoID;primaryKey;type:int;not null;" json:"autoID" form:"autoID"`
    CourseID string `gorm:"column:courseID;type:varchar(20);" json:"courseID" form:"courseID"`
    CourseName string `gorm:"column:courseName;type:varchar(50);" json:"courseName" form:"courseName"`
    TeacherID string `gorm:"column:teacherID;type:varchar(15);" json:"teacherID" form:"teacherID"`
    Credit float32 `gorm:"column:credit;type:float;" json:"credit" form:"credit"`
    IsDelete bool `gorm:"column:isDelete;type:tinyint(1);default:0;" json:"isDelete" form:"isDelete"`
    AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *CourseModel) TableName() string {
    return "course"
}

func (m *CourseModel) GetAutoID() int {
    return m.AutoID
}

func (m *CourseModel) SetAutoID(AutoID int) {
    m.AutoID = AutoID
}

func (m *CourseModel) GetCourseID() string {
    return m.CourseID
}

func (m *CourseModel) SetCourseID(CourseID string) {
    m.CourseID = CourseID
}

func (m *CourseModel) GetCourseName() string {
    return m.CourseName
}

func (m *CourseModel) SetCourseName(CourseName string) {
    m.CourseName = CourseName
}

func (m *CourseModel) GetTeacherID() string {
    return m.TeacherID
}

func (m *CourseModel) SetTeacherID(TeacherID string) {
    m.TeacherID = TeacherID
}

func (m *CourseModel) GetCredit() float32 {
    return m.Credit
}

func (m *CourseModel) SetCredit(Credit float32) {
    m.Credit = Credit
}

func (m *CourseModel) GetIsDelete() bool {
    return m.IsDelete
}

func (m *CourseModel) SetIsDelete(IsDelete bool) {
    m.IsDelete = IsDelete
}

func (m *CourseModel) GetAddTime() time.Time {
    return m.AddTime
}

func (m *CourseModel) SetAddTime(AddTime time.Time) {
    m.AddTime = AddTime
}


func (m *CourseModel) GetModelMap() (map[string]interface{}, error) {
    return structs.StructToMap(m, "json")
}

func (m *CourseModel) Assign(in interface{}) {
    structs.StructAssign(m, in, "json")
}