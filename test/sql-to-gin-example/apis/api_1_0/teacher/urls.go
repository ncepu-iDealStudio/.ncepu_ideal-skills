// coding: utf-8
// @Author : lryself
// @Software: GoLand

package teacher

import (
    "github.com/gin-gonic/gin"
)

var (
    Api *gin.RouterGroup
)

func InitTeacherRouterGroup(engine *gin.RouterGroup) {
    Api = engine.Group("teacher")
    Api.GET("", TeacherGetHandler)
    Api.GET(":autoID", TeacherGetBasicHandler)
    Api.POST("", TeacherPostHandler)
    Api.PUT(":autoID", TeacherPutHandler)
    Api.DELETE("", TeacherDeleteHandler)
    Api.GET("list", TeacherGetListHandler)
    Api.GET("list/page", TeacherGetListByPage)
}