// coding: utf-8
// @Author : lryself
// @Software: GoLand

package models

import (
    "study_flask_api/utils/structs"
     "time" 
)

type TeacherModel struct { 
    AutoID int `gorm:"column:autoID;primaryKey;type:int;not null;" json:"autoID" form:"autoID"`
    TeacherID string `gorm:"column:teacherID;type:varchar(15);" json:"teacherID" form:"teacherID"`
    UserID string `gorm:"column:userID;type:varchar(22);" json:"userID" form:"userID"`
    DepartmentID int64 `gorm:"column:departmentID;MUL;type:bigint;" json:"departmentID" form:"departmentID"`
    Name string `gorm:"column:name;type:varchar(10);" json:"name" form:"name"`
    Email string `gorm:"column:email;type:varchar(50);" json:"email" form:"email"`
    Phone string `gorm:"column:phone;type:varchar(15);" json:"phone" form:"phone"`
    OfficeAddress string `gorm:"column:officeAddress;type:varchar(255);" json:"officeAddress" form:"officeAddress"`
    IsDelete bool `gorm:"column:isDelete;type:tinyint(1);default:0;" json:"isDelete" form:"isDelete"`
    AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *TeacherModel) TableName() string {
    return "teacher"
}

func (m *TeacherModel) GetAutoID() int {
    return m.AutoID
}

func (m *TeacherModel) SetAutoID(AutoID int) {
    m.AutoID = AutoID
}

func (m *TeacherModel) GetTeacherID() string {
    return m.TeacherID
}

func (m *TeacherModel) SetTeacherID(TeacherID string) {
    m.TeacherID = TeacherID
}

func (m *TeacherModel) GetUserID() string {
    return m.UserID
}

func (m *TeacherModel) SetUserID(UserID string) {
    m.UserID = UserID
}

func (m *TeacherModel) GetDepartmentID() int64 {
    return m.DepartmentID
}

func (m *TeacherModel) SetDepartmentID(DepartmentID int64) {
    m.DepartmentID = DepartmentID
}

func (m *TeacherModel) GetName() string {
    return m.Name
}

func (m *TeacherModel) SetName(Name string) {
    m.Name = Name
}

func (m *TeacherModel) GetEmail() string {
    return m.Email
}

func (m *TeacherModel) SetEmail(Email string) {
    m.Email = Email
}

func (m *TeacherModel) GetPhone() string {
    return m.Phone
}

func (m *TeacherModel) SetPhone(Phone string) {
    m.Phone = Phone
}

func (m *TeacherModel) GetOfficeAddress() string {
    return m.OfficeAddress
}

func (m *TeacherModel) SetOfficeAddress(OfficeAddress string) {
    m.OfficeAddress = OfficeAddress
}

func (m *TeacherModel) GetIsDelete() bool {
    return m.IsDelete
}

func (m *TeacherModel) SetIsDelete(IsDelete bool) {
    m.IsDelete = IsDelete
}

func (m *TeacherModel) GetAddTime() time.Time {
    return m.AddTime
}

func (m *TeacherModel) SetAddTime(AddTime time.Time) {
    m.AddTime = AddTime
}


func (m *TeacherModel) GetModelMap() (map[string]interface{}, error) {
    return structs.StructToMap(m, "json")
}

func (m *TeacherModel) Assign(in interface{}) {
    structs.StructAssign(m, in, "json")
}