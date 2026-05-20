// coding: utf-8
// @Author : lryself
// @Software: GoLand

package models

import (
    "study_flask_api/utils/structs"
     "time" 
)

type SysCollegeinfoModel struct { 
    AutoID int64 `gorm:"column:autoID;primaryKey;type:bigint;not null;" json:"autoID" form:"autoID"`
    CollegeID string `gorm:"column:collegeID;type:varchar(20);" json:"collegeID" form:"collegeID"`
    CollegeName string `gorm:"column:collegeName;type:varchar(50);" json:"collegeName" form:"collegeName"`
    IsDelete bool `gorm:"column:isDelete;type:tinyint(1);default:0;" json:"isDelete" form:"isDelete"`
    AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *SysCollegeinfoModel) TableName() string {
    return "sys_collegeinfo"
}

func (m *SysCollegeinfoModel) GetAutoID() int64 {
    return m.AutoID
}

func (m *SysCollegeinfoModel) SetAutoID(AutoID int64) {
    m.AutoID = AutoID
}

func (m *SysCollegeinfoModel) GetCollegeID() string {
    return m.CollegeID
}

func (m *SysCollegeinfoModel) SetCollegeID(CollegeID string) {
    m.CollegeID = CollegeID
}

func (m *SysCollegeinfoModel) GetCollegeName() string {
    return m.CollegeName
}

func (m *SysCollegeinfoModel) SetCollegeName(CollegeName string) {
    m.CollegeName = CollegeName
}

func (m *SysCollegeinfoModel) GetIsDelete() bool {
    return m.IsDelete
}

func (m *SysCollegeinfoModel) SetIsDelete(IsDelete bool) {
    m.IsDelete = IsDelete
}

func (m *SysCollegeinfoModel) GetAddTime() time.Time {
    return m.AddTime
}

func (m *SysCollegeinfoModel) SetAddTime(AddTime time.Time) {
    m.AddTime = AddTime
}


func (m *SysCollegeinfoModel) GetModelMap() (map[string]interface{}, error) {
    return structs.StructToMap(m, "json")
}

func (m *SysCollegeinfoModel) Assign(in interface{}) {
    structs.StructAssign(m, in, "json")
}