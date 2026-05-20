package settings

import (
	"{{module_name}}/apis/routers"

	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
)

func InitGinEngine() (*gin.Engine, error) {
	gin.SetMode(viper.GetString("system.mode"))
	engine := gin.Default()
	routers.InitRouter(engine)
	return engine, nil
}
