package models

import "time"

type AdminModel struct {
	AutoId int `gorm:"column:auto_id;type:int;primaryKey;not null;" json:"auto_id" form:"auto_id"`
	AdminId int64 `gorm:"column:admin_id;type:bigint;default:NULL;" json:"admin_id" form:"admin_id"`
	UserId string `gorm:"column:user_id;type:varchar(22);default:NULL;" json:"user_id" form:"user_id"`
	DepartmentId int64 `gorm:"column:department_id;type:bigint;default:NULL;" json:"department_id" form:"department_id"`
	Name string `gorm:"column:name;type:varchar(10);default:NULL;" json:"name" form:"name"`
	Email string `gorm:"column:email;type:varchar(50);default:NULL;" json:"email" form:"email"`
	Phone string `gorm:"column:phone;type:varchar(100);default:NULL;" json:"phone" form:"phone"`
	OfficeAddress string `gorm:"column:office_address;type:varchar(255);default:NULL;" json:"office_address" form:"office_address"`
	IsDelete bool `gorm:"column:is_delete;type:tinyint(1);default:0;" json:"is_delete" form:"is_delete"`
	AddTime time.Time `gorm:"column:add_time;type:timestamp;default:CURRENT_TIMESTAMP;" json:"add_time" form:"add_time"`
}

func (m *AdminModel) TableName() string {
	return "admin"
}
