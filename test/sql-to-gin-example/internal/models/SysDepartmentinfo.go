// coding: utf-8
// @Author : lryself
// @Software: GoLand

package models

import (
    "study_flask_api/utils/structs"
     "time" 
)

type SysDepartmentinfoModel struct { 
    AutoID int64 `gorm:"column:autoID;primaryKey;type:bigint;not null;" json:"autoID" form:"autoID"`
    DepartmentID int64 `gorm:"column:departmentID;type:bigint;" json:"departmentID" form:"departmentID"`
    ParentDepartmentID int64 `gorm:"column:parentDepartmentID;type:bigint;not null;default:0;" json:"parentDepartmentID" form:"parentDepartmentID"`
    CollegeID string `gorm:"column:collegeID;type:varchar(20);" json:"collegeID" form:"collegeID"`
    DepartmentName string `gorm:"column:departmentName;type:varchar(255);" json:"departmentName" form:"departmentName"`
    DepartmentType bool `gorm:"column:departmentType;type:tinyint(1);default:1;" json:"departmentType" form:"departmentType"`
    IsDeleted bool `gorm:"column:isDeleted;type:tinyint(1);not null;default:0;" json:"isDeleted" form:"isDeleted"`
    AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *SysDepartmentinfoModel) TableName() string {
    return "sys_departmentinfo"
}

func (m *SysDepartmentinfoModel) GetAutoID() int64 {
    return m.AutoID
}

func (m *SysDepartmentinfoModel) SetAutoID(AutoID int64) {
    m.AutoID = AutoID
}

func (m *SysDepartmentinfoModel) GetDepartmentID() int64 {
    return m.DepartmentID
}

func (m *SysDepartmentinfoModel) SetDepartmentID(DepartmentID int64) {
    m.DepartmentID = DepartmentID
}

func (m *SysDepartmentinfoModel) GetParentDepartmentID() int64 {
    return m.ParentDepartmentID
}

func (m *SysDepartmentinfoModel) SetParentDepartmentID(ParentDepartmentID int64) {
    m.ParentDepartmentID = ParentDepartmentID
}

func (m *SysDepartmentinfoModel) GetCollegeID() string {
    return m.CollegeID
}

func (m *SysDepartmentinfoModel) SetCollegeID(CollegeID string) {
    m.CollegeID = CollegeID
}

func (m *SysDepartmentinfoModel) GetDepartmentName() string {
    return m.DepartmentName
}

func (m *SysDepartmentinfoModel) SetDepartmentName(DepartmentName string) {
    m.DepartmentName = DepartmentName
}

func (m *SysDepartmentinfoModel) GetDepartmentType() bool {
    return m.DepartmentType
}

func (m *SysDepartmentinfoModel) SetDepartmentType(DepartmentType bool) {
    m.DepartmentType = DepartmentType
}

func (m *SysDepartmentinfoModel) GetIsDeleted() bool {
    return m.IsDeleted
}

func (m *SysDepartmentinfoModel) SetIsDeleted(IsDeleted bool) {
    m.IsDeleted = IsDeleted
}

func (m *SysDepartmentinfoModel) GetAddTime() time.Time {
    return m.AddTime
}

func (m *SysDepartmentinfoModel) SetAddTime(AddTime time.Time) {
    m.AddTime = AddTime
}


func (m *SysDepartmentinfoModel) GetModelMap() (map[string]interface{}, error) {
    return structs.StructToMap(m, "json")
}

func (m *SysDepartmentinfoModel) Assign(in interface{}) {
    structs.StructAssign(m, in, "json")
}