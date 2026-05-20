// coding: utf-8
// @Author : lryself
// @Software: GoLand

package models

import (
    "study_flask_api/utils/structs"
    
)

type VStudentCourseScoreModel struct { 
    AutoID int `gorm:"column:autoID;type:int;not null;default:0;" json:"autoID" form:"autoID"`
    StudentID string `gorm:"column:studentID;type:varchar(20);not null;" json:"studentID" form:"studentID"`
    UserID string `gorm:"column:userID;type:varchar(22);" json:"userID" form:"userID"`
    ClassID string `gorm:"column:classID;type:varchar(10);" json:"classID" form:"classID"`
    CollegeID string `gorm:"column:collegeID;type:varchar(20);" json:"collegeID" form:"collegeID"`
    StudentName string `gorm:"column:studentName;type:varchar(20);" json:"studentName" form:"studentName"`
    PhoneNumber string `gorm:"column:phoneNumber;type:varchar(500);" json:"phoneNumber" form:"phoneNumber"`
    Age int `gorm:"column:age;type:int;" json:"age" form:"age"`
    Agenda string `gorm:"column:agenda;type:varchar(10);" json:"agenda" form:"agenda"`
    IsDelete bool `gorm:"column:isDelete;type:tinyint(1);default:0;" json:"isDelete" form:"isDelete"`
    ClassName string `gorm:"column:className;type:varchar(20);" json:"className" form:"className"`
    CourseID string `gorm:"column:courseID;type:varchar(15);not null;" json:"courseID" form:"courseID"`
    Score int `gorm:"column:score;type:int;" json:"score" form:"score"`
    CourseName string `gorm:"column:courseName;type:varchar(50);" json:"courseName" form:"courseName"`
    TeacherID string `gorm:"column:teacherID;type:varchar(15);" json:"teacherID" form:"teacherID"`
    TeacherName string `gorm:"column:teacherName;type:varchar(10);" json:"teacherName" form:"teacherName"`
    Phone string `gorm:"column:phone;type:varchar(15);" json:"phone" form:"phone"`
    Email string `gorm:"column:email;type:varchar(50);" json:"email" form:"email"`
}

func (m *VStudentCourseScoreModel) TableName() string {
    return "v_student_course_score"
}

func (m *VStudentCourseScoreModel) GetAutoID() int {
    return m.AutoID
}

func (m *VStudentCourseScoreModel) SetAutoID(AutoID int) {
    m.AutoID = AutoID
}

func (m *VStudentCourseScoreModel) GetStudentID() string {
    return m.StudentID
}

func (m *VStudentCourseScoreModel) SetStudentID(StudentID string) {
    m.StudentID = StudentID
}

func (m *VStudentCourseScoreModel) GetUserID() string {
    return m.UserID
}

func (m *VStudentCourseScoreModel) SetUserID(UserID string) {
    m.UserID = UserID
}

func (m *VStudentCourseScoreModel) GetClassID() string {
    return m.ClassID
}

func (m *VStudentCourseScoreModel) SetClassID(ClassID string) {
    m.ClassID = ClassID
}

func (m *VStudentCourseScoreModel) GetCollegeID() string {
    return m.CollegeID
}

func (m *VStudentCourseScoreModel) SetCollegeID(CollegeID string) {
    m.CollegeID = CollegeID
}

func (m *VStudentCourseScoreModel) GetStudentName() string {
    return m.StudentName
}

func (m *VStudentCourseScoreModel) SetStudentName(StudentName string) {
    m.StudentName = StudentName
}

func (m *VStudentCourseScoreModel) GetPhoneNumber() string {
    return m.PhoneNumber
}

func (m *VStudentCourseScoreModel) SetPhoneNumber(PhoneNumber string) {
    m.PhoneNumber = PhoneNumber
}

func (m *VStudentCourseScoreModel) GetAge() int {
    return m.Age
}

func (m *VStudentCourseScoreModel) SetAge(Age int) {
    m.Age = Age
}

func (m *VStudentCourseScoreModel) GetAgenda() string {
    return m.Agenda
}

func (m *VStudentCourseScoreModel) SetAgenda(Agenda string) {
    m.Agenda = Agenda
}

func (m *VStudentCourseScoreModel) GetIsDelete() bool {
    return m.IsDelete
}

func (m *VStudentCourseScoreModel) SetIsDelete(IsDelete bool) {
    m.IsDelete = IsDelete
}

func (m *VStudentCourseScoreModel) GetClassName() string {
    return m.ClassName
}

func (m *VStudentCourseScoreModel) SetClassName(ClassName string) {
    m.ClassName = ClassName
}

func (m *VStudentCourseScoreModel) GetCourseID() string {
    return m.CourseID
}

func (m *VStudentCourseScoreModel) SetCourseID(CourseID string) {
    m.CourseID = CourseID
}

func (m *VStudentCourseScoreModel) GetScore() int {
    return m.Score
}

func (m *VStudentCourseScoreModel) SetScore(Score int) {
    m.Score = Score
}

func (m *VStudentCourseScoreModel) GetCourseName() string {
    return m.CourseName
}

func (m *VStudentCourseScoreModel) SetCourseName(CourseName string) {
    m.CourseName = CourseName
}

func (m *VStudentCourseScoreModel) GetTeacherID() string {
    return m.TeacherID
}

func (m *VStudentCourseScoreModel) SetTeacherID(TeacherID string) {
    m.TeacherID = TeacherID
}

func (m *VStudentCourseScoreModel) GetTeacherName() string {
    return m.TeacherName
}

func (m *VStudentCourseScoreModel) SetTeacherName(TeacherName string) {
    m.TeacherName = TeacherName
}

func (m *VStudentCourseScoreModel) GetPhone() string {
    return m.Phone
}

func (m *VStudentCourseScoreModel) SetPhone(Phone string) {
    m.Phone = Phone
}

func (m *VStudentCourseScoreModel) GetEmail() string {
    return m.Email
}

func (m *VStudentCourseScoreModel) SetEmail(Email string) {
    m.Email = Email
}


func (m *VStudentCourseScoreModel) GetModelMap() (map[string]interface{}, error) {
    return structs.StructToMap(m, "json")
}

func (m *VStudentCourseScoreModel) Assign(in interface{}) {
    structs.StructAssign(m, in, "json")
}