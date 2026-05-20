// coding: utf-8
// @Author : lryself
// @Software: GoLand

package ssoUser

import (
    "study_flask_api/utils/structs"
    "github.com/gin-gonic/gin"
    "study_flask_api/internal/globals/parser"
    "study_flask_api/internal/services"
     "time" 
)

func SsoUserGetBasicHandler(c *gin.Context) {
	var err error
    
	autoID := c.Param("autoID")

	var SsoUserService services.SsoUserService

	err = SsoUserService.Get(map[string]any{ "autoID": autoID })

	if err != nil {
		parser.JsonDBError(c, "", err)
		return
	}
	parser.JsonOK(c, "", SsoUserService)
}

func SsoUserGetHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int64 `json:"autoID" form:"autoID" binding:"required"`
        UserID string `json:"userID" form:"userID"`
        Account string `json:"account" form:"account"`
        Password string `json:"password" form:"password"`
        UserType bool `json:"userType" form:"userType"`
        Status bool `json:"status" form:"status"`
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

    var SsoUserService services.SsoUserService
    SsoUserService.Assign(Parser)
    err = SsoUserService.Get(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SsoUserService)
}

func SsoUserPostHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int64 `json:"autoID" form:"autoID" binding:"required"`
        UserID string `json:"userID" form:"userID"`
        Account string `json:"account" form:"account"`
        Password string `json:"password" form:"password"`
        UserType bool `json:"userType" form:"userType"`
        Status bool `json:"status" form:"status"`
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

    var SsoUserService services.SsoUserService
    SsoUserService.Assign(Parser)

    err = SsoUserService.Add(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SsoUserService)
}

func SsoUserPutHandler(c *gin.Context) {
    var err error
    
	autoID := c.Param("autoID")
    var Parser struct { 
        AutoID int64 `json:"autoID" form:"autoID"`
        UserID string `json:"userID" form:"userID"`
        Account string `json:"account" form:"account"`
        Password string `json:"password" form:"password"`
        UserType bool `json:"userType" form:"userType"`
        Status bool `json:"status" form:"status"`
        AddTime time.Time `json:"addTime" form:"addTime"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var SsoUserService services.SsoUserService

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }
    //不能修改业务主键
    delete(args, "autoID")

	err = SsoUserService.Update(map[string]any{ "autoID": autoID }, args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SsoUserService)
}

func SsoUserDeleteHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int64 `json:"autoID" form:"autoID" binding:"required"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var SsoUserService services.SsoUserService
    SsoUserService.Assign(Parser)

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    err = SsoUserService.Delete(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SsoUserService)
}



// 获取列表
func SsoUserGetListHandler(c *gin.Context) {
    var err error
    var SsoUserService services.SsoUserService

    err = c.ShouldBind(&SsoUserService)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    results, err := SsoUserService.GetList()
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    
    parser.JsonOK(c, "", results)
}

// 获取列表（分页）
func SsoUserGetListByPage(c *gin.Context) {
    var err error

    var Parser struct {
        services.SsoUserService
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