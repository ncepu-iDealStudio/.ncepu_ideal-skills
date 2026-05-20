package main

import (
	"study_flask_api/cmd"
	"study_flask_api/utils/message"

	initialization "study_flask_api/init"
)

func main() {
	waitGroup := initialization.Init()

	// 执行cmd
	cmd.Execute()
	message.Println("系统已全部初始化完成！")

	// 退出系统
	waitGroup.Wait()
	message.Exit()
}
