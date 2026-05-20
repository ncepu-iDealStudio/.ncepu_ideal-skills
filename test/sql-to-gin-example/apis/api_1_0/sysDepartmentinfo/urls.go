// coding: utf-8
// @Author : lryself
// @Software: GoLand

package sysDepartmentinfo

import (
    "github.com/gin-gonic/gin"
)

var (
    Api *gin.RouterGroup
)

func InitSysDepartmentinfoRouterGroup(engine *gin.RouterGroup) {
    Api = engine.Group("sysDepartmentinfo")
    Api.GET("", SysDepartmentinfoGetHandler)
    Api.GET(":autoID", SysDepartmentinfoGetBasicHandler)
    Api.POST("", SysDepartmentinfoPostHandler)
    Api.PUT(":autoID", SysDepartmentinfoPutHandler)
    Api.DELETE("", SysDepartmentinfoDeleteHandler)
    Api.GET("list", SysDepartmentinfoGetListHandler)
    Api.GET("list/page", SysDepartmentinfoGetListByPage)
}