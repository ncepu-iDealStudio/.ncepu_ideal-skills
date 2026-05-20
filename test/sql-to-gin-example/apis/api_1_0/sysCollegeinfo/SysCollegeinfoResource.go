// coding: utf-8
// @Author : lryself
// @Software: GoLand

package sysCollegeinfo

import (
    "study_flask_api/utils/structs"
    "github.com/gin-gonic/gin"
    "study_flask_api/internal/globals/parser"
    "study_flask_api/internal/services"
     "time" 
)

func SysCollegeinfoGetBasicHandler(c *gin.Context) {
	var err error
    
	autoID := c.Param("autoID")

	var SysCollegeinfoService services.SysCollegeinfoService

	err = SysCollegeinfoService.Get(map[string]any{ "autoID": autoID })

	if err != nil {
		parser.JsonDBError(c, "", err)
		return
	}
	parser.JsonOK(c, "", SysCollegeinfoService)
}

func SysCollegeinfoGetHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int64 `json:"autoID" form:"autoID" binding:"required"`
        CollegeID string `json:"collegeID" form:"collegeID"`
        CollegeName string `json:"collegeName" form:"collegeName"`
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

    var SysCollegeinfoService services.SysCollegeinfoService
    SysCollegeinfoService.Assign(Parser)
    err = SysCollegeinfoService.Get(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SysCollegeinfoService)
}

func SysCollegeinfoPostHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int64 `json:"autoID" form:"autoID" binding:"required"`
        CollegeID string `json:"collegeID" form:"collegeID"`
        CollegeName string `json:"collegeName" form:"collegeName"`
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

    var SysCollegeinfoService services.SysCollegeinfoService
    SysCollegeinfoService.Assign(Parser)

    err = SysCollegeinfoService.Add(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SysCollegeinfoService)
}

func SysCollegeinfoPutHandler(c *gin.Context) {
    var err error
    
	autoID := c.Param("autoID")
    var Parser struct { 
        AutoID int64 `json:"autoID" form:"autoID"`
        CollegeID string `json:"collegeID" form:"collegeID"`
        CollegeName string `json:"collegeName" form:"collegeName"`
        IsDelete bool `json:"isDelete" form:"isDelete"`
        AddTime time.Time `json:"addTime" form:"addTime"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var SysCollegeinfoService services.SysCollegeinfoService

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }
    //不能修改业务主键
    delete(args, "autoID")

	err = SysCollegeinfoService.Update(map[string]any{ "autoID": autoID }, args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SysCollegeinfoService)
}

func SysCollegeinfoDeleteHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int64 `json:"autoID" form:"autoID" binding:"required"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var SysCollegeinfoService services.SysCollegeinfoService
    SysCollegeinfoService.Assign(Parser)

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    err = SysCollegeinfoService.Delete(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SysCollegeinfoService)
}



// 获取列表
func SysCollegeinfoGetListHandler(c *gin.Context) {
    var err error
    var SysCollegeinfoService services.SysCollegeinfoService

    err = c.ShouldBind(&SysCollegeinfoService)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    results, err := SysCollegeinfoService.GetList()
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    
    parser.JsonOK(c, "", results)
}

// 获取列表（分页）
func SysCollegeinfoGetListByPage(c *gin.Context) {
    var err error

    var Parser struct {
        services.SysCollegeinfoService
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