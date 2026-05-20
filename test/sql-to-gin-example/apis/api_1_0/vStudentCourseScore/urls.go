// coding: utf-8
// @Author : lryself
// @Software: GoLand

package vStudentCourseScore

import (
    "github.com/gin-gonic/gin"
)

var (
    Api *gin.RouterGroup
)

func InitVStudentCourseScoreRouterGroup(engine *gin.RouterGroup) {
    Api = engine.Group("vStudentCourseScore")
    Api.GET("", VStudentCourseScoreGetHandler)
    
    Api.GET("list", VStudentCourseScoreGetListHandler)
    Api.GET("list/page", VStudentCourseScoreGetListByPage)
}