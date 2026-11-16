package database

import (
	"sync"

	"github.com/spf13/viper"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var (
	mysqlClient *gorm.DB
	once        sync.Once
)

func GetMysqlClient() *gorm.DB {
	once.Do(func() {
		db, err := gorm.Open(mysql.Open(viper.GetString("database.mysql_dsn")), &gorm.Config{})
		if err != nil {
			panic(err)
		}
		mysqlClient = db
	})
	return mysqlClient
}
