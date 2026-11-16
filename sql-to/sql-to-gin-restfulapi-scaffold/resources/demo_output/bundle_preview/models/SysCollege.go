// 【AUTO-GENERATED】
// 本文件由 sql-to-gin-restfulapi-scaffold 生成，内容可被增量更新覆盖

package models

import "time"

type SysCollegeModel struct {
	CollegeID string `gorm:"column:collegeID;type:varchar(20);primaryKey;not null;" json:"collegeID" form:"collegeID"`
	CollegeName string `gorm:"column:collegeName;type:varchar(50);default:NULL;" json:"collegeName" form:"collegeName"`
	IsDelete bool `gorm:"column:isDelete;type:tinyint(1);default:0;" json:"isDelete" form:"isDelete"`
	AddTime time.Time `gorm:"column:addTime;type:timestamp;default:CURRENT_TIMESTAMP;" json:"addTime" form:"addTime"`
}

func (m *SysCollegeModel) TableName() string {
	return "sys_college"
}
