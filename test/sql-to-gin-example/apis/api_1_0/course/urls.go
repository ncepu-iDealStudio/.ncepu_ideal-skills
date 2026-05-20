// coding: utf-8
// @Author : lryself
// @Software: GoLand

package course

import (
    "github.com/gin-gonic/gin"
)

var (
    Api *gin.RouterGroup
)

func InitCourseRouterGroup(engine *gin.RouterGroup) {
    Api = engine.Group("course")
    Api.GET("", CourseGetHandler)
    Api.GET(":autoID", CourseGetBasicHandler)
    Api.POST("", CoursePostHandler)
    Api.PUT(":autoID", CoursePutHandler)
    Api.DELETE("", CourseDeleteHandler)
    Api.GET("list", CourseGetListHandler)
    Api.GET("list/page", CourseGetListByPage)
}