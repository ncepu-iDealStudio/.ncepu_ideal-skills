// coding: utf-8
// @Author : lryself
// @Software: GoLand

package admin

import (
    "study_flask_api/utils/structs"
    "github.com/gin-gonic/gin"
    "study_flask_api/internal/globals/parser"
    "study_flask_api/internal/services"
     "time" 
)

func AdminGetBasicHandler(c *gin.Context) {
	var err error
    
	auto_id := c.Param("auto_id")

	var AdminService services.AdminService

	err = AdminService.Get(map[string]any{ "auto_id": auto_id })

	if err != nil {
		parser.JsonDBError(c, "", err)
		return
	}
	parser.JsonOK(c, "", AdminService)
}

func AdminGetHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoId int `json:"auto_id" form:"auto_id" binding:"required"`
        AdminId int64 `json:"admin_id" form:"admin_id"`
        UserId string `json:"user_id" form:"user_id"`
        DepartmentId int64 `json:"department_id" form:"department_id"`
        Name string `json:"name" form:"name"`
        Email string `json:"email" form:"email"`
        Phone string `json:"phone" form:"phone"`
        OfficeAddress string `json:"office_address" form:"office_address"`
        IsDelete bool `json:"is_delete" form:"is_delete"`
        AddTime time.Time `json:"add_time" form:"add_time"`
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

    var AdminService services.AdminService
    AdminService.Assign(Parser)
    err = AdminService.Get(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", AdminService)
}

func AdminPostHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoId int `json:"auto_id" form:"auto_id" binding:"required"`
        AdminId int64 `json:"admin_id" form:"admin_id"`
        UserId string `json:"user_id" form:"user_id"`
        DepartmentId int64 `json:"department_id" form:"department_id"`
        Name string `json:"name" form:"name"`
        Email string `json:"email" form:"email"`
        Phone string `json:"phone" form:"phone"`
        OfficeAddress string `json:"office_address" form:"office_address"`
        IsDelete bool `json:"is_delete" form:"is_delete"`
        AddTime time.Time `json:"add_time" form:"add_time"`
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

    var AdminService services.AdminService
    AdminService.Assign(Parser)

    err = AdminService.Add(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", AdminService)
}

func AdminPutHandler(c *gin.Context) {
    var err error
    
	auto_id := c.Param("auto_id")
    var Parser struct { 
        AutoId int `json:"auto_id" form:"auto_id"`
        AdminId int64 `json:"admin_id" form:"admin_id"`
        UserId string `json:"user_id" form:"user_id"`
        DepartmentId int64 `json:"department_id" form:"department_id"`
        Name string `json:"name" form:"name"`
        Email string `json:"email" form:"email"`
        Phone string `json:"phone" form:"phone"`
        OfficeAddress string `json:"office_address" form:"office_address"`
        IsDelete bool `json:"is_delete" form:"is_delete"`
        AddTime time.Time `json:"add_time" form:"add_time"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var AdminService services.AdminService

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }
    //不能修改业务主键
    delete(args, "auto_id")

	err = AdminService.Update(map[string]any{ "auto_id": auto_id }, args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", AdminService)
}

func AdminDeleteHandler(c *gin.Context) {
    var err error

    var Parser struct { 
        AutoId int `json:"auto_id" form:"auto_id" binding:"required"`
    }
    err = c.ShouldBind(&Parser)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    var AdminService services.AdminService
    AdminService.Assign(Parser)

    args, err := structs.StructToMap(Parser, "json")
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    err = AdminService.Delete(args)
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    parser.JsonOK(c, "", AdminService)
}



// 获取列表
func AdminGetListHandler(c *gin.Context) {
    var err error
    var AdminService services.AdminService

    err = c.ShouldBind(&AdminService)
    if err != nil {
        parser.JsonParameterIllegal(c, "", err)
        return
    }

    results, err := AdminService.GetList()
    if err != nil {
        parser.JsonDBError(c, "", err)
        return
    }
    
    parser.JsonOK(c, "", results)
}

// 获取列表（分页）
func AdminGetListByPage(c *gin.Context) {
    var err error

    var Parser struct {
        services.AdminService
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