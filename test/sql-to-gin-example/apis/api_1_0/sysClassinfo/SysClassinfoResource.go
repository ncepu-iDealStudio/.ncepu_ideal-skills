// coding: utf-8
// @Author : lryself
// @Software: GoLand

package sysClassinfo

import (
    "study_flask_api/utils/structs"
    "github.com/gin-gonic/gin"
    "study_flask_api/internal/globals/parser"
    "study_flask_api/internal/services"
     "time" 
)

func SysClassinfoGetBasicHandler(c *gin.Context) {
	var err error
    
	autoID := c.Param("autoID")

	var SysClassinfoService services.SysClassinfoService

	err = SysClassinfoService.Get(map[string]any{ "autoID": autoID })

	if err != nil {
		parser.JsonDBError(c, "", err)
		return
	}
	parser.JsonOK(c, "", SysClassinfoService)
}

func SysClassinfoGetHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
        ClassID string `json:"classID" form:"classID"`
        CollegeID string `json:"collegeID" form:"collegeID"`
        ClassName string `json:"className" form:"className"`
        IsDeleted bool `json:"isDeleted" form:"isDeleted"`
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

    var SysClassinfoService services.SysClassinfoService
    SysClassinfoService.Assign(Parser)
    err = SysClassinfoService.Get(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SysClassinfoService)
}

func SysClassinfoPostHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
        ClassID string `json:"classID" form:"classID"`
        CollegeID string `json:"collegeID" form:"collegeID"`
        ClassName string `json:"className" form:"className"`
        IsDeleted bool `json:"isDeleted" form:"isDeleted"`
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

    var SysClassinfoService services.SysClassinfoService
    SysClassinfoService.Assign(Parser)

    err = SysClassinfoService.Add(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SysClassinfoService)
}

func SysClassinfoPutHandler(c *gin.Context) {
    var err error
    
	autoID := c.Param("autoID")
    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID"`
        ClassID string `json:"classID" form:"classID"`
        CollegeID string `json:"collegeID" form:"collegeID"`
        ClassName string `json:"className" form:"className"`
        IsDeleted bool `json:"isDeleted" form:"isDeleted"`
        AddTime time.Time `json:"addTime" form:"addTime"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var SysClassinfoService services.SysClassinfoService

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }
    //不能修改业务主键
    delete(args, "autoID")

	err = SysClassinfoService.Update(map[string]any{ "autoID": autoID }, args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SysClassinfoService)
}

func SysClassinfoDeleteHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var SysClassinfoService services.SysClassinfoService
    SysClassinfoService.Assign(Parser)

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    err = SysClassinfoService.Delete(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SysClassinfoService)
}



// 获取列表
func SysClassinfoGetListHandler(c *gin.Context) {
    var err error
    var SysClassinfoService services.SysClassinfoService

    err = c.ShouldBind(&SysClassinfoService)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    results, err := SysClassinfoService.GetList()
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    
    parser.JsonOK(c, "", results)
}

// 获取列表（分页）
func SysClassinfoGetListByPage(c *gin.Context) {
    var err error

    var Parser struct {
        services.SysClassinfoService
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