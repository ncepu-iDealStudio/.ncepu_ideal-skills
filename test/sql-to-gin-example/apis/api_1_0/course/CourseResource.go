// coding: utf-8
// @Author : lryself
// @Software: GoLand

package course

import (
    "study_flask_api/utils/structs"
    "github.com/gin-gonic/gin"
    "study_flask_api/internal/globals/parser"
    "study_flask_api/internal/services"
     "time" 
)

func CourseGetBasicHandler(c *gin.Context) {
	var err error
    
	autoID := c.Param("autoID")

	var CourseService services.CourseService

	err = CourseService.Get(map[string]any{ "autoID": autoID })

	if err != nil {
		parser.JsonDBError(c, "", err)
		return
	}
	parser.JsonOK(c, "", CourseService)
}

func CourseGetHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
        CourseID string `json:"courseID" form:"courseID"`
        CourseName string `json:"courseName" form:"courseName"`
        TeacherID string `json:"teacherID" form:"teacherID"`
        Credit float32 `json:"credit" form:"credit"`
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

    var CourseService services.CourseService
    CourseService.Assign(Parser)
    err = CourseService.Get(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", CourseService)
}

func CoursePostHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
        CourseID string `json:"courseID" form:"courseID"`
        CourseName string `json:"courseName" form:"courseName"`
        TeacherID string `json:"teacherID" form:"teacherID"`
        Credit float32 `json:"credit" form:"credit"`
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

    var CourseService services.CourseService
    CourseService.Assign(Parser)

    err = CourseService.Add(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", CourseService)
}

func CoursePutHandler(c *gin.Context) {
    var err error
    
	autoID := c.Param("autoID")
    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID"`
        CourseID string `json:"courseID" form:"courseID"`
        CourseName string `json:"courseName" form:"courseName"`
        TeacherID string `json:"teacherID" form:"teacherID"`
        Credit float32 `json:"credit" form:"credit"`
        IsDelete bool `json:"isDelete" form:"isDelete"`
        AddTime time.Time `json:"addTime" form:"addTime"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var CourseService services.CourseService

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }
    //不能修改业务主键
    delete(args, "autoID")

	err = CourseService.Update(map[string]any{ "autoID": autoID }, args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", CourseService)
}

func CourseDeleteHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var CourseService services.CourseService
    CourseService.Assign(Parser)

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    err = CourseService.Delete(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", CourseService)
}



// 获取列表
func CourseGetListHandler(c *gin.Context) {
    var err error
    var CourseService services.CourseService

    err = c.ShouldBind(&CourseService)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    results, err := CourseService.GetList()
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    
    parser.JsonOK(c, "", results)
}

// 获取列表（分页）
func CourseGetListByPage(c *gin.Context) {
    var err error

    var Parser struct {
        services.CourseService
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