// coding: utf-8
// @Author : lryself
// @Software: GoLand

package studentSelectedCourse

import (
    "github.com/gin-gonic/gin"
)

var (
    Api *gin.RouterGroup
)

func InitStudentSelectedCourseRouterGroup(engine *gin.RouterGroup) {
    Api = engine.Group("studentSelectedCourse")
    Api.GET("", StudentSelectedCourseGetHandler)
    Api.GET(":autoID", StudentSelectedCourseGetBasicHandler)
    Api.POST("", StudentSelectedCoursePostHandler)
    Api.PUT(":autoID", StudentSelectedCoursePutHandler)
    Api.DELETE("", StudentSelectedCourseDeleteHandler)
    Api.GET("list", StudentSelectedCourseGetListHandler)
    Api.GET("list/page", StudentSelectedCourseGetListByPage)
}