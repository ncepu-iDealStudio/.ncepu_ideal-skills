package core

// Must panics when err is not nil.
func Must(err error) {
	if err != nil {
		panic(err)
	}
}

// Handle invokes handler when err is not nil.
func Handle(err error, handler func(error)) {
	if err != nil && handler != nil {
		handler(err)
	}
}

// Ignore returns whether err is nil; useful for concise guard checks.
func Ignore(err error) bool {
	return err == nil
}
