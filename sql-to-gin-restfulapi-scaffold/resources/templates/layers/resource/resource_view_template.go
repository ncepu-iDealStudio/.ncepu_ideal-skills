package {{module_name_snake}}

import (
	"github.com/gin-gonic/gin"
	"{{module_name}}/internal/globals/parser"
	"{{module_name}}/internal/services"
)

func {{entity_name}}GetListHandler(c *gin.Context) {
	var svc services.{{entity_name}}Service
	err := c.ShouldBind(&svc)
	if err != nil {
		parser.JsonParameterIllegal(c, "", err)
		return
	}
	parser.JsonOK(c, "", svc)
}
