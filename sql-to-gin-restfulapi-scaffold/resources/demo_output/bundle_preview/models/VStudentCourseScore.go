package models



type VStudentCourseScoreModel struct {
	AutoID string `gorm:"column:autoID;type:varchar(255);" json:"autoID" form:"autoID"`
	StudentID string `gorm:"column:studentID;type:varchar(255);" json:"studentID" form:"studentID"`
	UserID string `gorm:"column:userID;type:varchar(255);" json:"userID" form:"userID"`
	ClassID string `gorm:"column:classID;type:varchar(255);" json:"classID" form:"classID"`
	CollegeID string `gorm:"column:collegeID;type:varchar(255);" json:"collegeID" form:"collegeID"`
	StudentName string `gorm:"column:studentName;type:varchar(255);" json:"studentName" form:"studentName"`
	PhoneNumber string `gorm:"column:phoneNumber;type:varchar(255);" json:"phoneNumber" form:"phoneNumber"`
	Age string `gorm:"column:age;type:varchar(255);" json:"age" form:"age"`
	Agenda string `gorm:"column:agenda;type:varchar(255);" json:"agenda" form:"agenda"`
	IsDelete string `gorm:"column:isDelete;type:varchar(255);" json:"isDelete" form:"isDelete"`
	ClassName string `gorm:"column:className;type:varchar(255);" json:"className" form:"className"`
	CourseID string `gorm:"column:courseID;type:varchar(255);" json:"courseID" form:"courseID"`
	Score string `gorm:"column:score;type:varchar(255);" json:"score" form:"score"`
	CourseName string `gorm:"column:courseName;type:varchar(255);" json:"courseName" form:"courseName"`
	TeacherID string `gorm:"column:teacherID;type:varchar(255);" json:"teacherID" form:"teacherID"`
	TeacherName string `gorm:"column:teacherName;type:varchar(255);" json:"teacherName" form:"teacherName"`
	Phone string `gorm:"column:phone;type:varchar(255);" json:"phone" form:"phone"`
	Email string `gorm:"column:email;type:varchar(255);" json:"email" form:"email"`
}

func (m *VStudentCourseScoreModel) TableName() string {
	return "v_student_course_score"
}
