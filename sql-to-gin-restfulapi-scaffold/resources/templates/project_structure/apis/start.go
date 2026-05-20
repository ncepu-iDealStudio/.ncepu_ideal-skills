package apis

import (
	"fmt"
	"{{module_name}}/internal/settings"

	"github.com/spf13/viper"
)

func StartHttp() error {
	engine, err := settings.InitGinEngine()
	if err != nil {
		return err
	}
	return engine.Run(fmt.Sprintf("%s:%s", viper.GetString("system.host"), viper.GetString("system.port")))
}
