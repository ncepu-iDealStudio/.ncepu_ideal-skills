// coding: utf-8
// @Author : lryself
// @Software: GoLand

package admin

import (
    "github.com/gin-gonic/gin"
)

var (
    Api *gin.RouterGroup
)

func InitAdminRouterGroup(engine *gin.RouterGroup) {
    Api = engine.Group("admin")
    Api.GET("", AdminGetHandler)
    Api.GET(":auto_id", AdminGetBasicHandler)
    Api.POST("", AdminPostHandler)
    Api.PUT(":auto_id", AdminPutHandler)
    Api.DELETE("", AdminDeleteHandler)
    Api.GET("list", AdminGetListHandler)
    Api.GET("list/page", AdminGetListByPage)
}