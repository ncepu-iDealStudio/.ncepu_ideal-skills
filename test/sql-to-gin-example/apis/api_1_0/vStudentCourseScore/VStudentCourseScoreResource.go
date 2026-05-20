// coding: utf-8
// @Author : lryself
// @Software: GoLand

package vStudentCourseScore

import (
    "study_flask_api/utils/structs"
    "github.com/gin-gonic/gin"
    "study_flask_api/internal/globals/parser"
    "study_flask_api/internal/services"
    
)


func VStudentCourseScoreGetHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID"`
        StudentID string `json:"studentID" form:"studentID"`
        UserID string `json:"userID" form:"userID"`
        ClassID string `json:"classID" form:"classID"`
        CollegeID string `json:"collegeID" form:"collegeID"`
        StudentName string `json:"studentName" form:"studentName"`
        PhoneNumber string `json:"phoneNumber" form:"phoneNumber"`
        Age int `json:"age" form:"age"`
        Agenda string `json:"agenda" form:"agenda"`
        IsDelete bool `json:"isDelete" form:"isDelete"`
        ClassName string `json:"className" form:"className"`
        CourseID string `json:"courseID" form:"courseID"`
        Score int `json:"score" form:"score"`
        CourseName string `json:"courseName" form:"courseName"`
        TeacherID string `json:"teacherID" form:"teacherID"`
        TeacherName string `json:"teacherName" form:"teacherName"`
        Phone string `json:"phone" form:"phone"`
        Email string `json:"email" form:"email"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

	args, err := structs.StructToMap(Parser, "json")
	if err != nil {
		parser.JsonParameterIllegal(c, "", err)
		return
	}

    var VStudentCourseScoreService services.VStudentCourseScoreService
    VStudentCourseScoreService.Assign(Parser)
    err = VStudentCourseScoreService.Get(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", VStudentCourseScoreService)
}



// 获取列表
func VStudentCourseScoreGetListHandler(c *gin.Context) {
    var err error
    var VStudentCourseScoreService services.VStudentCourseScoreService

    err = c.ShouldBind(&VStudentCourseScoreService)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    results, err := VStudentCourseScoreService.GetList()
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    
    parser.JsonOK(c, "", results)
}

// 获取列表（分页）
func VStudentCourseScoreGetListByPage(c *gin.Context) {
    var err error

    var Parser struct {
        services.VStudentCourseScoreService
        parser.ListParser
    }

    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    results, count, err := Parser.GetListByPage(Parser.ListParser)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }

    parser.JsonOK(c, "", results, map[string]any{
        "totalCount": count,
        "totalPage":  int(count) / Parser.Size + 1,
    })
}