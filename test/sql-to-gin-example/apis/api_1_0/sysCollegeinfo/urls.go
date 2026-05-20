// coding: utf-8
// @Author : lryself
// @Software: GoLand

package sysCollegeinfo

import (
    "github.com/gin-gonic/gin"
)

var (
    Api *gin.RouterGroup
)

func InitSysCollegeinfoRouterGroup(engine *gin.RouterGroup) {
    Api = engine.Group("sysCollegeinfo")
    Api.GET("", SysCollegeinfoGetHandler)
    Api.GET(":autoID", SysCollegeinfoGetBasicHandler)
    Api.POST("", SysCollegeinfoPostHandler)
    Api.PUT(":autoID", SysCollegeinfoPutHandler)
    Api.DELETE("", SysCollegeinfoDeleteHandler)
    Api.GET("list", SysCollegeinfoGetListHandler)
    Api.GET("list/page", SysCollegeinfoGetListByPage)
}