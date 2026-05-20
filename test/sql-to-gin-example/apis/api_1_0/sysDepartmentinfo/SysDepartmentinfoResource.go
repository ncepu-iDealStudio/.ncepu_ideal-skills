// coding: utf-8
// @Author : lryself
// @Software: GoLand

package sysDepartmentinfo

import (
    "study_flask_api/utils/structs"
    "github.com/gin-gonic/gin"
    "study_flask_api/internal/globals/parser"
    "study_flask_api/internal/services"
     "time" 
)

func SysDepartmentinfoGetBasicHandler(c *gin.Context) {
	var err error
    
	autoID := c.Param("autoID")

	var SysDepartmentinfoService services.SysDepartmentinfoService

	err = SysDepartmentinfoService.Get(map[string]any{ "autoID": autoID })

	if err != nil {
		parser.JsonDBError(c, "", err)
		return
	}
	parser.JsonOK(c, "", SysDepartmentinfoService)
}

func SysDepartmentinfoGetHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int64 `json:"autoID" form:"autoID" binding:"required"`
        DepartmentID int64 `json:"departmentID" form:"departmentID"`
        ParentDepartmentID int64 `json:"parentDepartmentID" form:"parentDepartmentID"`
        CollegeID string `json:"collegeID" form:"collegeID"`
        DepartmentName string `json:"departmentName" form:"departmentName"`
        DepartmentType bool `json:"departmentType" form:"departmentType"`
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

    var SysDepartmentinfoService services.SysDepartmentinfoService
    SysDepartmentinfoService.Assign(Parser)
    err = SysDepartmentinfoService.Get(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SysDepartmentinfoService)
}

func SysDepartmentinfoPostHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int64 `json:"autoID" form:"autoID" binding:"required"`
        DepartmentID int64 `json:"departmentID" form:"departmentID"`
        ParentDepartmentID int64 `json:"parentDepartmentID" form:"parentDepartmentID"`
        CollegeID string `json:"collegeID" form:"collegeID"`
        DepartmentName string `json:"departmentName" form:"departmentName"`
        DepartmentType bool `json:"departmentType" form:"departmentType"`
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

    var SysDepartmentinfoService services.SysDepartmentinfoService
    SysDepartmentinfoService.Assign(Parser)

    err = SysDepartmentinfoService.Add(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SysDepartmentinfoService)
}

func SysDepartmentinfoPutHandler(c *gin.Context) {
    var err error
    
	autoID := c.Param("autoID")
    var Parser struct { 
        AutoID int64 `json:"autoID" form:"autoID"`
        DepartmentID int64 `json:"departmentID" form:"departmentID"`
        ParentDepartmentID int64 `json:"parentDepartmentID" form:"parentDepartmentID"`
        CollegeID string `json:"collegeID" form:"collegeID"`
        DepartmentName string `json:"departmentName" form:"departmentName"`
        DepartmentType bool `json:"departmentType" form:"departmentType"`
        IsDeleted bool `json:"isDeleted" form:"isDeleted"`
        AddTime time.Time `json:"addTime" form:"addTime"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var SysDepartmentinfoService services.SysDepartmentinfoService

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }
    //不能修改业务主键
    delete(args, "autoID")

	err = SysDepartmentinfoService.Update(map[string]any{ "autoID": autoID }, args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SysDepartmentinfoService)
}

func SysDepartmentinfoDeleteHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoID int64 `json:"autoID" form:"autoID" binding:"required"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var SysDepartmentinfoService services.SysDepartmentinfoService
    SysDepartmentinfoService.Assign(Parser)

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    err = SysDepartmentinfoService.Delete(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", SysDepartmentinfoService)
}



// 获取列表
func SysDepartmentinfoGetListHandler(c *gin.Context) {
    var err error
    var SysDepartmentinfoService services.SysDepartmentinfoService

    err = c.ShouldBind(&SysDepartmentinfoService)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    results, err := SysDepartmentinfoService.GetList()
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    
    parser.JsonOK(c, "", results)
}

// 获取列表（分页）
func SysDepartmentinfoGetListByPage(c *gin.Context) {
    var err error

    var Parser struct {
        services.SysDepartmentinfoService
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