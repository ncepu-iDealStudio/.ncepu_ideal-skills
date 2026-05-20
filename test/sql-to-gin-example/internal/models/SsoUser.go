// coding: utf-8
// @Author : lryself
// @Software: GoLand

package models

import (
    "study_flask_api/utils/structs"
     "time" 
)

type SsoUserModel struct { 
    AutoID int64 `gorm:"column:autoID;primaryKey;type:bigint;not null;" json:"autoID" form:"autoID"`
    UserID string `gorm:"column:userID;type:varchar(22);" json:"userID" form:"userID"`
    Account string `gorm:"column:account;type:varchar(255);" json:"account" form:"account"`
    Password string `gorm:"column:password;type:varchar(255);" json:"password" form:"password"`
    UserType bool `gorm:"column:userType;type:tinyint(1);" json:"userType" form:"userType"`
    Status bool `gorm:"column:status;type:tinyint(1);" json:"status" form:"status"`
    AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *SsoUserModel) TableName() string {
    return "sso_user"
}

func (m *SsoUserModel) GetAutoID() int64 {
    return m.AutoID
}

func (m *SsoUserModel) SetAutoID(AutoID int64) {
    m.AutoID = AutoID
}

func (m *SsoUserModel) GetUserID() string {
    return m.UserID
}

func (m *SsoUserModel) SetUserID(UserID string) {
    m.UserID = UserID
}

func (m *SsoUserModel) GetAccount() string {
    return m.Account
}

func (m *SsoUserModel) SetAccount(Account string) {
    m.Account = Account
}

func (m *SsoUserModel) GetPassword() string {
    return m.Password
}

func (m *SsoUserModel) SetPassword(Password string) {
    m.Password = Password
}

func (m *SsoUserModel) GetUserType() bool {
    return m.UserType
}

func (m *SsoUserModel) SetUserType(UserType bool) {
    m.UserType = UserType
}

func (m *SsoUserModel) GetStatus() bool {
    return m.Status
}

func (m *SsoUserModel) SetStatus(Status bool) {
    m.Status = Status
}

func (m *SsoUserModel) GetAddTime() time.Time {
    return m.AddTime
}

func (m *SsoUserModel) SetAddTime(AddTime time.Time) {
    m.AddTime = AddTime
}


func (m *SsoUserModel) GetModelMap() (map[string]interface{}, error) {
    return structs.StructToMap(m, "json")
}

func (m *SsoUserModel) Assign(in interface{}) {
    structs.StructAssign(m, in, "json")
}