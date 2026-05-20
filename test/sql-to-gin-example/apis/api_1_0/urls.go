// coding: utf-8
// @Author : lryself
// @Software: GoLand

package api_1_0

import (
    "github.com/gin-gonic/gin"
    "study_flask_api/apis/api_1_0/admin"
    "study_flask_api/apis/api_1_0/course"
    "study_flask_api/apis/api_1_0/courseArrangement"
    "study_flask_api/apis/api_1_0/ssoUser"
    "study_flask_api/apis/api_1_0/student"
    "study_flask_api/apis/api_1_0/studentSelectedCourse"
    "study_flask_api/apis/api_1_0/sysClassinfo"
    "study_flask_api/apis/api_1_0/sysCollegeinfo"
    "study_flask_api/apis/api_1_0/sysDepartmentinfo"
    "study_flask_api/apis/api_1_0/teacher"
    "study_flask_api/apis/api_1_0/vStudentCourseScore"
)

var (
    Api *gin.RouterGroup
)

func InitAPIRouter(engine *gin.Engine) {
    Api = engine.Group("api")
    Api.Any("version", GetVersion)

    admin.InitAdminRouterGroup(Api)
    course.InitCourseRouterGroup(Api)
    courseArrangement.InitCourseArrangementRouterGroup(Api)
    ssoUser.InitSsoUserRouterGroup(Api)
    student.InitStudentRouterGroup(Api)
    studentSelectedCourse.InitStudentSelectedCourseRouterGroup(Api)
    sysClassinfo.InitSysClassinfoRouterGroup(Api)
    sysCollegeinfo.InitSysCollegeinfoRouterGroup(Api)
    sysDepartmentinfo.InitSysDepartmentinfoRouterGroup(Api)
    teacher.InitTeacherRouterGroup(Api)
    vStudentCourseScore.InitVStudentCourseScoreRouterGroup(Api)
}