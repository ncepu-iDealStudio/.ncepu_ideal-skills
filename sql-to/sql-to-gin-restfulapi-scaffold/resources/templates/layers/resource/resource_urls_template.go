// 【AUTO-GENERATED】
// 本文件由 sql-to-gin-restfulapi-scaffold 生成，内容可被增量更新覆盖

package {{module_name_snake}}

import "github.com/gin-gonic/gin"

var Api *gin.RouterGroup

func {{router_init_func}}(engine *gin.RouterGroup) {
	Api = engine.Group("{{resource_slug}}")
{{routes_block}}
}
