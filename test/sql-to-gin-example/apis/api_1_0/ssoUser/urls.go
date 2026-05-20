// coding: utf-8
// @Author : lryself
// @Software: GoLand

package ssoUser

import (
    "github.com/gin-gonic/gin"
)

var (
    Api *gin.RouterGroup
)

func InitSsoUserRouterGroup(engine *gin.RouterGroup) {
    Api = engine.Group("ssoUser")
    Api.GET("", SsoUserGetHandler)
    Api.GET(":autoID", SsoUserGetBasicHandler)
    Api.POST("", SsoUserPostHandler)
    Api.PUT(":autoID", SsoUserPutHandler)
    Api.DELETE("", SsoUserDeleteHandler)
    Api.GET("list", SsoUserGetListHandler)
    Api.GET("list/page", SsoUserGetListByPage)
}