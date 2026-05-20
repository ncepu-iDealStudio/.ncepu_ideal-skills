// coding: utf-8
// @Author : lryself
// @Software: GoLand

package student

import (
    "study_flask_api/utils/structs"
    "github.com/gin-gonic/gin"
    "study_flask_api/internal/globals/parser"
    "study_flask_api/internal/services"
     "time" 
)

func StudentGetBasicHandler(c *gin.Context) {
	var err error
    
	autoID := c.Param("autoID")

	var StudentService services.StudentService

	err = StudentService.Get(map[string]any{ "autoID": autoID })

	if err != nil {
		parser.JsonDBError(c, "", err)
		return
	}
	parser.JsonOK(c, "", StudentService)
}

func StudentGetHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
        StudentID string `json:"studentID" form:"studentID"`
        UserID string `json:"userID" form:"userID"`
        ClassID string `json:"classID" form:"classID"`
        CollegeID string `json:"collegeID" form:"collegeID"`
        Name string `json:"name" form:"name"`
        PhoneNumber string `json:"phoneNumber" form:"phoneNumber"`
        Age int `json:"age" form:"age"`
        Agenda string `json:"agenda" form:"agenda"`
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

    var StudentService services.StudentService
    StudentService.Assign(Parser)
    err = StudentService.Get(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", StudentService)
}

func StudentPostHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
        StudentID string `json:"studentID" form:"studentID"`
        UserID string `json:"userID" form:"userID"`
        ClassID string `json:"classID" form:"classID"`
        CollegeID string `json:"collegeID" form:"collegeID"`
        Name string `json:"name" form:"name"`
        PhoneNumber string `json:"phoneNumber" form:"phoneNumber"`
        Age int `json:"age" form:"age"`
        Agenda string `json:"agenda" form:"agenda"`
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

    var StudentService services.StudentService
    StudentService.Assign(Parser)

    err = StudentService.Add(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", StudentService)
}

func StudentPutHandler(c *gin.Context) {
    var err error
    
	autoID := c.Param("autoID")
    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID"`
        StudentID string `json:"studentID" form:"studentID"`
        UserID string `json:"userID" form:"userID"`
        ClassID string `json:"classID" form:"classID"`
        CollegeID string `json:"collegeID" form:"collegeID"`
        Name string `json:"name" form:"name"`
        PhoneNumber string `json:"phoneNumber" form:"phoneNumber"`
        Age int `json:"age" form:"age"`
        Agenda string `json:"agenda" form:"agenda"`
        IsDelete bool `json:"isDelete" form:"isDelete"`
        AddTime time.Time `json:"addTime" form:"addTime"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var StudentService services.StudentService

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }
    //不能修改业务主键
    delete(args, "autoID")

	err = StudentService.Update(map[string]any{ "autoID": autoID }, args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", StudentService)
}

func StudentDeleteHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var StudentService services.StudentService
    StudentService.Assign(Parser)

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    err = StudentService.Delete(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", StudentService)
}



// 获取列表
func StudentGetListHandler(c *gin.Context) {
    var err error
    var StudentService services.StudentService

    err = c.ShouldBind(&StudentService)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    results, err := StudentService.GetList()
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    
    parser.JsonOK(c, "", results)
}

// 获取列表（分页）
func StudentGetListByPage(c *gin.Context) {
    var err error

    var Parser struct {
        services.StudentService
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