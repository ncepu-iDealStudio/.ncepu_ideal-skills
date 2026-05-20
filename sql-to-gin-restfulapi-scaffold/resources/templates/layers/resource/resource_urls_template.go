package {{module_name_snake}}

import "github.com/gin-gonic/gin"

var Api *gin.RouterGroup

func {{router_init_func}}(engine *gin.RouterGroup) {
	Api = engine.Group("{{resource_slug}}")
{{routes_block}}
}
