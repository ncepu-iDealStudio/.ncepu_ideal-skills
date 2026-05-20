// coding: utf-8
// @Author : lryself
// @Software: GoLand

package teacher

import (
    "study_flask_api/utils/structs"
    "github.com/gin-gonic/gin"
    "study_flask_api/internal/globals/parser"
    "study_flask_api/internal/services"
     "time" 
)

func TeacherGetBasicHandler(c *gin.Context) {
	var err error
    
	autoID := c.Param("autoID")

	var TeacherService services.TeacherService

	err = TeacherService.Get(map[string]any{ "autoID": autoID })

	if err != nil {
		parser.JsonDBError(c, "", err)
		return
	}
	parser.JsonOK(c, "", TeacherService)
}

func TeacherGetHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
        TeacherID string `json:"teacherID" form:"teacherID"`
        UserID string `json:"userID" form:"userID"`
        DepartmentID int64 `json:"departmentID" form:"departmentID"`
        Name string `json:"name" form:"name"`
        Email string `json:"email" form:"email"`
        Phone string `json:"phone" form:"phone"`
        OfficeAddress string `json:"officeAddress" form:"officeAddress"`
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

    var TeacherService services.TeacherService
    TeacherService.Assign(Parser)
    err = TeacherService.Get(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", TeacherService)
}

func TeacherPostHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
        TeacherID string `json:"teacherID" form:"teacherID"`
        UserID string `json:"userID" form:"userID"`
        DepartmentID int64 `json:"departmentID" form:"departmentID"`
        Name string `json:"name" form:"name"`
        Email string `json:"email" form:"email"`
        Phone string `json:"phone" form:"phone"`
        OfficeAddress string `json:"officeAddress" form:"officeAddress"`
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

    var TeacherService services.TeacherService
    TeacherService.Assign(Parser)

    err = TeacherService.Add(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", TeacherService)
}

func TeacherPutHandler(c *gin.Context) {
    var err error
    
	autoID := c.Param("autoID")
    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID"`
        TeacherID string `json:"teacherID" form:"teacherID"`
        UserID string `json:"userID" form:"userID"`
        DepartmentID int64 `json:"departmentID" form:"departmentID"`
        Name string `json:"name" form:"name"`
        Email string `json:"email" form:"email"`
        Phone string `json:"phone" form:"phone"`
        OfficeAddress string `json:"officeAddress" form:"officeAddress"`
        IsDelete bool `json:"isDelete" form:"isDelete"`
        AddTime time.Time `json:"addTime" form:"addTime"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var TeacherService services.TeacherService

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }
    //不能修改业务主键
    delete(args, "autoID")

	err = TeacherService.Update(map[string]any{ "autoID": autoID }, args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", TeacherService)
}

func TeacherDeleteHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var TeacherService services.TeacherService
    TeacherService.Assign(Parser)

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    err = TeacherService.Delete(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", TeacherService)
}



// 获取列表
func TeacherGetListHandler(c *gin.Context) {
    var err error
    var TeacherService services.TeacherService

    err = c.ShouldBind(&TeacherService)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    results, err := TeacherService.GetList()
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    
    parser.JsonOK(c, "", results)
}

// 获取列表（分页）
func TeacherGetListByPage(c *gin.Context) {
    var err error

    var Parser struct {
        services.TeacherService
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