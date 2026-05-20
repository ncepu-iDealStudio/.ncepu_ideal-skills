// coding: utf-8
// @Author : lryself
// @Software: GoLand

package models

import (
    "study_flask_api/utils/structs"
     "time" 
)

type AdminModel struct { 
    AutoId int `gorm:"column:auto_id;primaryKey;type:int;not null;" json:"auto_id" form:"auto_id"`
    AdminId int64 `gorm:"column:admin_id;type:bigint;" json:"admin_id" form:"admin_id"`
    UserId string `gorm:"column:user_id;type:varchar(22);" json:"user_id" form:"user_id"`
    DepartmentId int64 `gorm:"column:department_id;type:bigint;" json:"department_id" form:"department_id"`
    Name string `gorm:"column:name;type:varchar(10);" json:"name" form:"name"`
    Email string `gorm:"column:email;type:varchar(50);" json:"email" form:"email"`
    Phone string `gorm:"column:phone;type:varchar(100);" json:"phone" form:"phone"`
    OfficeAddress string `gorm:"column:office_address;type:varchar(255);" json:"office_address" form:"office_address"`
    IsDelete bool `gorm:"column:is_delete;type:tinyint(1);default:0;" json:"is_delete" form:"is_delete"`
    AddTime time.Time `gorm:"column:add_time;type:timestamp;default:CURRENT_TIMESTAMP;" json:"add_time" form:"add_time"`
}

func (m *AdminModel) TableName() string {
    return "admin"
}

func (m *AdminModel) GetAutoId() int {
    return m.AutoId
}

func (m *AdminModel) SetAutoId(AutoId int) {
    m.AutoId = AutoId
}

func (m *AdminModel) GetAdminId() int64 {
    return m.AdminId
}

func (m *AdminModel) SetAdminId(AdminId int64) {
    m.AdminId = AdminId
}

func (m *AdminModel) GetUserId() string {
    return m.UserId
}

func (m *AdminModel) SetUserId(UserId string) {
    m.UserId = UserId
}

func (m *AdminModel) GetDepartmentId() int64 {
    return m.DepartmentId
}

func (m *AdminModel) SetDepartmentId(DepartmentId int64) {
    m.DepartmentId = DepartmentId
}

func (m *AdminModel) GetName() string {
    return m.Name
}

func (m *AdminModel) SetName(Name string) {
    m.Name = Name
}

func (m *AdminModel) GetEmail() string {
    return m.Email
}

func (m *AdminModel) SetEmail(Email string) {
    m.Email = Email
}

func (m *AdminModel) GetPhone() string {
    return m.Phone
}

func (m *AdminModel) SetPhone(Phone string) {
    m.Phone = Phone
}

func (m *AdminModel) GetOfficeAddress() string {
    return m.OfficeAddress
}

func (m *AdminModel) SetOfficeAddress(OfficeAddress string) {
    m.OfficeAddress = OfficeAddress
}

func (m *AdminModel) GetIsDelete() bool {
    return m.IsDelete
}

func (m *AdminModel) SetIsDelete(IsDelete bool) {
    m.IsDelete = IsDelete
}

func (m *AdminModel) GetAddTime() time.Time {
    return m.AddTime
}

func (m *AdminModel) SetAddTime(AddTime time.Time) {
    m.AddTime = AddTime
}


func (m *AdminModel) GetModelMap() (map[string]interface{}, error) {
    return structs.StructToMap(m, "json")
}

func (m *AdminModel) Assign(in interface{}) {
    structs.StructAssign(m, in, "json")
}