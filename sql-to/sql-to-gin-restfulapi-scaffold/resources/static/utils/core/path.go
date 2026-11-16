package core

import "os"

// PathExists returns whether path exists on disk.
func PathExists(path string) bool {
	_, err := os.Stat(path)
	return err == nil || !os.IsNotExist(err)
}
