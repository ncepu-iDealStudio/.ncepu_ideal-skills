package models

import "time"

type SsoUserModel struct {
	AutoID int64 `gorm:"column:autoID;type:bigint;primaryKey;not null;" json:"autoID" form:"autoID"`
	UserID string `gorm:"column:userID;type:varchar(22);default:NULL;" json:"userID" form:"userID"`
	Account string `gorm:"column:account;type:varchar(255);default:NULL;" json:"account" form:"account"`
	Password string `gorm:"column:password;type:varchar(255);default:NULL;" json:"password" form:"password"`
	UserType bool `gorm:"column:userType;type:tinyint(1);default:NULL;" json:"userType" form:"userType"`
	Status bool `gorm:"column:status;type:tinyint(1);default:NULL;" json:"status" form:"status"`
	AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *SsoUserModel) TableName() string {
	return "sso_user"
}
