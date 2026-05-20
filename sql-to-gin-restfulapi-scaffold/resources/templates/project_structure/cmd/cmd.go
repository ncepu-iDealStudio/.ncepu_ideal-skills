package cmd

import (
	"{{module_name}}/apis"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var rootCmd = &cobra.Command{
	Use:   "{{project_name}}",
	Short: "{{project_name}} service",
	PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
		viper.SetConfigName("config")
		viper.AddConfigPath("./configs")
		viper.SetConfigType("yaml")
		return viper.ReadInConfig()
	},
	RunE: func(cmd *cobra.Command, args []string) error {
		return apis.StartHttp()
	},
}

func Execute() {
	_ = rootCmd.Execute()
}
