// coding: utf-8
// @Author : lryself
// @Software: GoLand

package studentSelectedCourse

import (
    "study_flask_api/utils/structs"
    "github.com/gin-gonic/gin"
    "study_flask_api/internal/globals/parser"
    "study_flask_api/internal/services"
     "time" 
)

func StudentSelectedCourseGetBasicHandler(c *gin.Context) {
	var err error
    
	autoID := c.Param("autoID")

	var StudentSelectedCourseService services.StudentSelectedCourseService

	err = StudentSelectedCourseService.Get(map[string]any{ "autoID": autoID })

	if err != nil {
		parser.JsonDBError(c, "", err)
		return
	}
	parser.JsonOK(c, "", StudentSelectedCourseService)
}

func StudentSelectedCourseGetHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
        StudentID string `json:"studentID" form:"studentID"`
        CourseID string `json:"courseID" form:"courseID"`
        Score int `json:"score" form:"score"`
        IsDelete bool `json:"isDelete" form:"isDelete"`
        AddTime time.Time `json:"addTime" form:"addTime"`
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

    var StudentSelectedCourseService services.StudentSelectedCourseService
    StudentSelectedCourseService.Assign(Parser)
    err = StudentSelectedCourseService.Get(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", StudentSelectedCourseService)
}

func StudentSelectedCoursePostHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
        StudentID string `json:"studentID" form:"studentID"`
        CourseID string `json:"courseID" form:"courseID"`
        Score int `json:"score" form:"score"`
        IsDelete bool `json:"isDelete" form:"isDelete"`
        AddTime time.Time `json:"addTime" form:"addTime"`
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

    var StudentSelectedCourseService services.StudentSelectedCourseService
    StudentSelectedCourseService.Assign(Parser)

    err = StudentSelectedCourseService.Add(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", StudentSelectedCourseService)
}

func StudentSelectedCoursePutHandler(c *gin.Context) {
    var err error
    
	autoID := c.Param("autoID")
    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID"`
        StudentID string `json:"studentID" form:"studentID"`
        CourseID string `json:"courseID" form:"courseID"`
        Score int `json:"score" form:"score"`
        IsDelete bool `json:"isDelete" form:"isDelete"`
        AddTime time.Time `json:"addTime" form:"addTime"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var StudentSelectedCourseService services.StudentSelectedCourseService

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }
    //不能修改业务主键
    delete(args, "autoID")

	err = StudentSelectedCourseService.Update(map[string]any{ "autoID": autoID }, args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", StudentSelectedCourseService)
}

func StudentSelectedCourseDeleteHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var StudentSelectedCourseService services.StudentSelectedCourseService
    StudentSelectedCourseService.Assign(Parser)

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    err = StudentSelectedCourseService.Delete(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", StudentSelectedCourseService)
}



// 获取列表
func StudentSelectedCourseGetListHandler(c *gin.Context) {
    var err error
    var StudentSelectedCourseService services.StudentSelectedCourseService

    err = c.ShouldBind(&StudentSelectedCourseService)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    results, err := StudentSelectedCourseService.GetList()
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    
    parser.JsonOK(c, "", results)
}

// 获取列表（分页）
func StudentSelectedCourseGetListByPage(c *gin.Context) {
    var err error

    var Parser struct {
        services.StudentSelectedCourseService
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