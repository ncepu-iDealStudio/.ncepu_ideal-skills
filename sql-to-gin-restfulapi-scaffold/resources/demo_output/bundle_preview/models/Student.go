package models

import "time"

type StudentModel struct {
	AutoID int `gorm:"column:autoID;type:int;primaryKey;not null;" json:"autoID" form:"autoID"`
	StudentID string `gorm:"column:studentID;type:varchar(20);not null;" json:"studentID" form:"studentID"`
	UserID string `gorm:"column:userID;type:varchar(22);default:NULL;" json:"userID" form:"userID"`
	ClassID string `gorm:"column:classID;type:varchar(10);default:NULL;" json:"classID" form:"classID"`
	CollegeID string `gorm:"column:collegeID;type:varchar(20);default:NULL;" json:"collegeID" form:"collegeID"`
	Name string `gorm:"column:name;type:varchar(20);not null;" json:"name" form:"name"`
	PhoneNumber string `gorm:"column:phoneNumber;type:varchar(500);default:NULL;" json:"phoneNumber" form:"phoneNumber"`
	Age int `gorm:"column:age;type:int;default:NULL;" json:"age" form:"age"`
	Gender string `gorm:"column:gender;type:varchar(10);default:NULL;" json:"gender" form:"gender"`
	IsDelete bool `gorm:"column:isDelete;type:tinyint(1);not null;default:0;" json:"isDelete" form:"isDelete"`
	AddTime time.Time `gorm:"column:addTime;type:datetime;not null;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *StudentModel) TableName() string {
	return "student"
}
