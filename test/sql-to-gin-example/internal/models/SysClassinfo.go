// coding: utf-8
// @Author : lryself
// @Software: GoLand

package models

import (
    "study_flask_api/utils/structs"
     "time" 
)

type SysClassinfoModel struct { 
    AutoID int `gorm:"column:autoID;primaryKey;type:int;not null;" json:"autoID" form:"autoID"`
    ClassID string `gorm:"column:classID;type:varchar(10);" json:"classID" form:"classID"`
    CollegeID string `gorm:"column:collegeID;type:varchar(20);" json:"collegeID" form:"collegeID"`
    ClassName string `gorm:"column:className;type:varchar(20);" json:"className" form:"className"`
    IsDeleted bool `gorm:"column:isDeleted;type:tinyint(1);default:0;" json:"isDeleted" form:"isDeleted"`
    AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *SysClassinfoModel) TableName() string {
    return "sys_classinfo"
}

func (m *SysClassinfoModel) GetAutoID() int {
    return m.AutoID
}

func (m *SysClassinfoModel) SetAutoID(AutoID int) {
    m.AutoID = AutoID
}

func (m *SysClassinfoModel) GetClassID() string {
    return m.ClassID
}

func (m *SysClassinfoModel) SetClassID(ClassID string) {
    m.ClassID = ClassID
}

func (m *SysClassinfoModel) GetCollegeID() string {
    return m.CollegeID
}

func (m *SysClassinfoModel) SetCollegeID(CollegeID string) {
    m.CollegeID = CollegeID
}

func (m *SysClassinfoModel) GetClassName() string {
    return m.ClassName
}

func (m *SysClassinfoModel) SetClassName(ClassName string) {
    m.ClassName = ClassName
}

func (m *SysClassinfoModel) GetIsDeleted() bool {
    return m.IsDeleted
}

func (m *SysClassinfoModel) SetIsDeleted(IsDeleted bool) {
    m.IsDeleted = IsDeleted
}

func (m *SysClassinfoModel) GetAddTime() time.Time {
    return m.AddTime
}

func (m *SysClassinfoModel) SetAddTime(AddTime time.Time) {
    m.AddTime = AddTime
}


func (m *SysClassinfoModel) GetModelMap() (map[string]interface{}, error) {
    return structs.StructToMap(m, "json")
}

func (m *SysClassinfoModel) Assign(in interface{}) {
    structs.StructAssign(m, in, "json")
}