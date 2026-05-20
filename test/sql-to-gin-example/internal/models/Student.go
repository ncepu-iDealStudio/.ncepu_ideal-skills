// coding: utf-8
// @Author : lryself
// @Software: GoLand

package models

import (
    "study_flask_api/utils/structs"
     "time" 
)

type StudentModel struct { 
    AutoID int `gorm:"column:autoID;primaryKey;type:int;not null;" json:"autoID" form:"autoID"`
    StudentID string `gorm:"column:studentID;type:varchar(20);" json:"studentID" form:"studentID"`
    UserID string `gorm:"column:userID;type:varchar(22);" json:"userID" form:"userID"`
    ClassID string `gorm:"column:classID;type:varchar(10);" json:"classID" form:"classID"`
    CollegeID string `gorm:"column:collegeID;type:varchar(20);" json:"collegeID" form:"collegeID"`
    Name string `gorm:"column:name;type:varchar(20);" json:"name" form:"name"`
    PhoneNumber string `gorm:"column:phoneNumber;type:varchar(500);" json:"phoneNumber" form:"phoneNumber"`
    Age int `gorm:"column:age;type:int;" json:"age" form:"age"`
    Agenda string `gorm:"column:agenda;type:varchar(10);" json:"agenda" form:"agenda"`
    IsDelete bool `gorm:"column:isDelete;type:tinyint(1);default:0;" json:"isDelete" form:"isDelete"`
    AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *StudentModel) TableName() string {
    return "student"
}

func (m *StudentModel) GetAutoID() int {
    return m.AutoID
}

func (m *StudentModel) SetAutoID(AutoID int) {
    m.AutoID = AutoID
}

func (m *StudentModel) GetStudentID() string {
    return m.StudentID
}

func (m *StudentModel) SetStudentID(StudentID string) {
    m.StudentID = StudentID
}

func (m *StudentModel) GetUserID() string {
    return m.UserID
}

func (m *StudentModel) SetUserID(UserID string) {
    m.UserID = UserID
}

func (m *StudentModel) GetClassID() string {
    return m.ClassID
}

func (m *StudentModel) SetClassID(ClassID string) {
    m.ClassID = ClassID
}

func (m *StudentModel) GetCollegeID() string {
    return m.CollegeID
}

func (m *StudentModel) SetCollegeID(CollegeID string) {
    m.CollegeID = CollegeID
}

func (m *StudentModel) GetName() string {
    return m.Name
}

func (m *StudentModel) SetName(Name string) {
    m.Name = Name
}

func (m *StudentModel) GetPhoneNumber() string {
    return m.PhoneNumber
}

func (m *StudentModel) SetPhoneNumber(PhoneNumber string) {
    m.PhoneNumber = PhoneNumber
}

func (m *StudentModel) GetAge() int {
    return m.Age
}

func (m *StudentModel) SetAge(Age int) {
    m.Age = Age
}

func (m *StudentModel) GetAgenda() string {
    return m.Agenda
}

func (m *StudentModel) SetAgenda(Agenda string) {
    m.Agenda = Agenda
}

func (m *StudentModel) GetIsDelete() bool {
    return m.IsDelete
}

func (m *StudentModel) SetIsDelete(IsDelete bool) {
    m.IsDelete = IsDelete
}

func (m *StudentModel) GetAddTime() time.Time {
    return m.AddTime
}

func (m *StudentModel) SetAddTime(AddTime time.Time) {
    m.AddTime = AddTime
}


func (m *StudentModel) GetModelMap() (map[string]interface{}, error) {
    return structs.StructToMap(m, "json")
}

func (m *StudentModel) Assign(in interface{}) {
    structs.StructAssign(m, in, "json")
}