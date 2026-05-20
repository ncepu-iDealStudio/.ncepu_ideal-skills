// coding: utf-8
// @Author : lryself
// @Software: GoLand

package courseArrangement

import (
    "study_flask_api/utils/structs"
    "github.com/gin-gonic/gin"
    "study_flask_api/internal/globals/parser"
    "study_flask_api/internal/services"
     "time" 
)

func CourseArrangementGetBasicHandler(c *gin.Context) {
	var err error
    
	autoID := c.Param("autoID")

	var CourseArrangementService services.CourseArrangementService

	err = CourseArrangementService.Get(map[string]any{ "autoID": autoID })

	if err != nil {
		parser.JsonDBError(c, "", err)
		return
	}
	parser.JsonOK(c, "", CourseArrangementService)
}

func CourseArrangementGetHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
        CourseID string `json:"courseID" form:"courseID"`
        TermID string `json:"termID" form:"termID"`
        ClassTime string `json:"classTime" form:"classTime"`
        Count int `json:"count" form:"count"`
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

    var CourseArrangementService services.CourseArrangementService
    CourseArrangementService.Assign(Parser)
    err = CourseArrangementService.Get(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", CourseArrangementService)
}

func CourseArrangementPostHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
        CourseID string `json:"courseID" form:"courseID"`
        TermID string `json:"termID" form:"termID"`
        ClassTime string `json:"classTime" form:"classTime"`
        Count int `json:"count" form:"count"`
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

    var CourseArrangementService services.CourseArrangementService
    CourseArrangementService.Assign(Parser)

    err = CourseArrangementService.Add(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", CourseArrangementService)
}

func CourseArrangementPutHandler(c *gin.Context) {
    var err error
    
	autoID := c.Param("autoID")
    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID"`
        CourseID string `json:"courseID" form:"courseID"`
        TermID string `json:"termID" form:"termID"`
        ClassTime string `json:"classTime" form:"classTime"`
        Count int `json:"count" form:"count"`
        IsDelete bool `json:"isDelete" form:"isDelete"`
        AddTime time.Time `json:"addTime" form:"addTime"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var CourseArrangementService services.CourseArrangementService

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }
    //不能修改业务主键
    delete(args, "autoID")

	err = CourseArrangementService.Update(map[string]any{ "autoID": autoID }, args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", CourseArrangementService)
}

func CourseArrangementDeleteHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int `json:"autoID" form:"autoID" binding:"required"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var CourseArrangementService services.CourseArrangementService
    CourseArrangementService.Assign(Parser)

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    err = CourseArrangementService.Delete(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", CourseArrangementService)
}



// 获取列表
func CourseArrangementGetListHandler(c *gin.Context) {
    var err error
    var CourseArrangementService services.CourseArrangementService

    err = c.ShouldBind(&CourseArrangementService)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    results, err := CourseArrangementService.GetList()
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    
    parser.JsonOK(c, "", results)
}

// 获取列表（分页）
func CourseArrangementGetListByPage(c *gin.Context) {
    var err error

    var Parser struct {
        services.CourseArrangementService
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