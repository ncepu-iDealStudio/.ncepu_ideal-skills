package api_1_0

import (
	"github.com/gin-gonic/gin"
	// ==AUTO_IMPORTS_START==
	student "study_flask_api/apis/api_1_0/student"
	v_student_course_score "study_flask_api/apis/api_1_0/v_student_course_score"
	// ==AUTO_IMPORTS_END==
)

var Api *gin.RouterGroup

func InitAPIRouter(engine *gin.Engine) {
	Api = engine.Group("api")
	// ==AUTO_REGISTRY_START==
	student.InitStudentRouterGroup(Api)
	v_student_course_score.InitVStudentCourseScoreRouterGroup(Api)
	// ==AUTO_REGISTRY_END==
}
