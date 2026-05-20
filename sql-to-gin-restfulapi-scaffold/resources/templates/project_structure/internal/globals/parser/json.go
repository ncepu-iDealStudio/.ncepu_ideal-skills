package parser

import (
	"errors"
	"net/http"

	"{{module_name}}/internal/globals/codes"

	"github.com/gin-gonic/gin"
)

func JsonOK(c *gin.Context, msg string, data interface{}, others ...map[string]any) {
	if msg == "" {
		msg = "成功!"
	}
	backMap := gin.H{
		"code":    codes.OK,
		"message": msg,
		"data":    data,
	}
	for _, other := range others {
		for k, v := range other {
			backMap[k] = v
		}
	}
	c.JSON(http.StatusOK, backMap)
}

func JsonParameterIllegal(c *gin.Context, msg string, err error) {
	if msg == "" {
		msg = "参数非法!"
	}
	c.JSON(http.StatusOK, gin.H{
		"code":    codes.ParameterIllegal,
		"message": msg,
		"err":     err.Error(),
	})
}

func JsonDBError(c *gin.Context, msg string, err error) {
	if err != nil && err.Error() == "record not found" {
		if msg == "" {
			msg = "无数据!"
		}
		c.JSON(http.StatusOK, gin.H{
			"code":    codes.NotData,
			"message": msg,
			"err":     err.Error(),
		})
		return
	}
	if msg == "" {
		msg = "数据库错误!"
	}
	if err == nil {
		err = errors.New(msg)
	}
	c.JSON(http.StatusOK, gin.H{
		"code":    codes.DBError,
		"message": msg,
		"err":     err.Error(),
	})
}
