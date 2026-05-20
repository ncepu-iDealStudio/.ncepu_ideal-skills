package models



type StudentModel struct {
	AutoID int `gorm:"column:autoID;primaryKey;type:int;not null;" json:"autoID" form:"autoID"`
	StudentID string `gorm:"column:studentID;type:varchar(20);" json:"studentID" form:"studentID"`
}

func (m *StudentModel) TableName() string {
	return "student"
}
