package routers

import (
	"{{module_name}}/apis/api_1_0"

	"github.com/gin-gonic/gin"
)

func InitRouter(engine *gin.Engine) {
	api_1_0.InitAPIRouter(engine)
}
