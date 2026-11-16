package core

import "strings"

// SnakeToUpperCamel converts snake_case text to UpperCamelCase.
func SnakeToUpperCamel(s string) string {
	if s == "" {
		return s
	}
	parts := strings.Split(s, "_")
	for i := range parts {
		if parts[i] == "" {
			continue
		}
		parts[i] = strings.ToUpper(parts[i][:1]) + strings.ToLower(parts[i][1:])
	}
	return strings.Join(parts, "")
}

// SnakeToLowerCamel converts snake_case text to lowerCamelCase.
func SnakeToLowerCamel(s string) string {
	up := SnakeToUpperCamel(s)
	if up == "" {
		return up
	}
	return strings.ToLower(up[:1]) + up[1:]
}
