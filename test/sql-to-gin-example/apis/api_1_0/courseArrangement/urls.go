// coding: utf-8
// @Author : lryself
// @Software: GoLand

package courseArrangement

import (
    "github.com/gin-gonic/gin"
)

var (
    Api *gin.RouterGroup
)

func InitCourseArrangementRouterGroup(engine *gin.RouterGroup) {
    Api = engine.Group("courseArrangement")
    Api.GET("", CourseArrangementGetHandler)
    Api.GET(":autoID", CourseArrangementGetBasicHandler)
    Api.POST("", CourseArrangementPostHandler)
    Api.PUT(":autoID", CourseArrangementPutHandler)
    Api.DELETE("", CourseArrangementDeleteHandler)
    Api.GET("list", CourseArrangementGetListHandler)
    Api.GET("list/page", CourseArrangementGetListByPage)
}