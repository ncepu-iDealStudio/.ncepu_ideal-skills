// coding: utf-8
// @Author : lryself
// @Software: GoLand

package student

import (
    "github.com/gin-gonic/gin"
)

var (
    Api *gin.RouterGroup
)

func InitStudentRouterGroup(engine *gin.RouterGroup) {
    Api = engine.Group("student")
    Api.GET("", StudentGetHandler)
    Api.GET(":autoID", StudentGetBasicHandler)
    Api.POST("", StudentPostHandler)
    Api.PUT(":autoID", StudentPutHandler)
    Api.DELETE("", StudentDeleteHandler)
    Api.GET("list", StudentGetListHandler)
    Api.GET("list/page", StudentGetListByPage)
}