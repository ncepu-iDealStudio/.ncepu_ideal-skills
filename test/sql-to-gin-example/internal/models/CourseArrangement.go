// coding: utf-8
// @Author : lryself
// @Software: GoLand

package models

import (
    "study_flask_api/utils/structs"
     "time" 
)

type CourseArrangementModel struct { 
    AutoID int `gorm:"column:autoID;primaryKey;type:int;not null;" json:"autoID" form:"autoID"`
    CourseID string `gorm:"column:courseID;type:varchar(20);" json:"courseID" form:"courseID"`
    TermID string `gorm:"column:termID;type:varchar(50);" json:"termID" form:"termID"`
    ClassTime string `gorm:"column:classTime;type:varchar(20);" json:"classTime" form:"classTime"`
    Count int `gorm:"column:count;type:int;" json:"count" form:"count"`
    IsDelete bool `gorm:"column:isDelete;type:tinyint(1);default:0;" json:"isDelete" form:"isDelete"`
    AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *CourseArrangementModel) TableName() string {
    return "course_arrangement"
}

func (m *CourseArrangementModel) GetAutoID() int {
    return m.AutoID
}

func (m *CourseArrangementModel) SetAutoID(AutoID int) {
    m.AutoID = AutoID
}

func (m *CourseArrangementModel) GetCourseID() string {
    return m.CourseID
}

func (m *CourseArrangementModel) SetCourseID(CourseID string) {
    m.CourseID = CourseID
}

func (m *CourseArrangementModel) GetTermID() string {
    return m.TermID
}

func (m *CourseArrangementModel) SetTermID(TermID string) {
    m.TermID = TermID
}

func (m *CourseArrangementModel) GetClassTime() string {
    return m.ClassTime
}

func (m *CourseArrangementModel) SetClassTime(ClassTime string) {
    m.ClassTime = ClassTime
}

func (m *CourseArrangementModel) GetCount() int {
    return m.Count
}

func (m *CourseArrangementModel) SetCount(Count int) {
    m.Count = Count
}

func (m *CourseArrangementModel) GetIsDelete() bool {
    return m.IsDelete
}

func (m *CourseArrangementModel) SetIsDelete(IsDelete bool) {
    m.IsDelete = IsDelete
}

func (m *CourseArrangementModel) GetAddTime() time.Time {
    return m.AddTime
}

func (m *CourseArrangementModel) SetAddTime(AddTime time.Time) {
    m.AddTime = AddTime
}


func (m *CourseArrangementModel) GetModelMap() (map[string]interface{}, error) {
    return structs.StructToMap(m, "json")
}

func (m *CourseArrangementModel) Assign(in interface{}) {
    structs.StructAssign(m, in, "json")
}