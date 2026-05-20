package api_1_0

import (
	"github.com/gin-gonic/gin"
	// ==AUTO_IMPORTS_START==
	admin "study_flask_api/apis/api_1_0/admin"
	course "study_flask_api/apis/api_1_0/course"
	course_arrangement "study_flask_api/apis/api_1_0/course_arrangement"
	sso_user "study_flask_api/apis/api_1_0/sso_user"
	student "study_flask_api/apis/api_1_0/student"
	student_selected_course "study_flask_api/apis/api_1_0/student_selected_course"
	sys_classInfo "study_flask_api/apis/api_1_0/sys_class_info"
	sys_collegeInfo "study_flask_api/apis/api_1_0/sys_college_info"
	sys_departmentInfo "study_flask_api/apis/api_1_0/sys_department_info"
	teacher "study_flask_api/apis/api_1_0/teacher"
	v_student_course_score "study_flask_api/apis/api_1_0/v_student_course_score"
	// ==AUTO_IMPORTS_END==
)

var Api *gin.RouterGroup

func InitAPIRouter(engine *gin.Engine) {
	Api = engine.Group("api")
	// ==AUTO_REGISTRY_START==
	admin.InitAdminRouterGroup(Api)
	course.InitCourseRouterGroup(Api)
	course_arrangement.InitCourseArrangementRouterGroup(Api)
	sso_user.InitSsoUserRouterGroup(Api)
	student.InitStudentRouterGroup(Api)
	student_selected_course.InitStudentSelectedCourseRouterGroup(Api)
	sys_classInfo.InitSysClassInfoRouterGroup(Api)
	sys_collegeInfo.InitSysCollegeInfoRouterGroup(Api)
	sys_departmentInfo.InitSysDepartmentInfoRouterGroup(Api)
	teacher.InitTeacherRouterGroup(Api)
	v_student_course_score.InitVStudentCourseScoreRouterGroup(Api)
	// ==AUTO_REGISTRY_END==
}
