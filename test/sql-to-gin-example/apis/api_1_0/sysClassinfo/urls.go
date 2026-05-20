// coding: utf-8
// @Author : lryself
// @Software: GoLand

package sysClassinfo

import (
    "github.com/gin-gonic/gin"
)

var (
    Api *gin.RouterGroup
)

func InitSysClassinfoRouterGroup(engine *gin.RouterGroup) {
    Api = engine.Group("sysClassinfo")
    Api.GET("", SysClassinfoGetHandler)
    Api.GET(":autoID", SysClassinfoGetBasicHandler)
    Api.POST("", SysClassinfoPostHandler)
    Api.PUT(":autoID", SysClassinfoPutHandler)
    Api.DELETE("", SysClassinfoDeleteHandler)
    Api.GET("list", SysClassinfoGetListHandler)
    Api.GET("list/page", SysClassinfoGetListByPage)
}