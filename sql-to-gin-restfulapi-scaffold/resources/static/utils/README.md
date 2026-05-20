This directory stores reusable runtime utility assets for generated Gin projects.

Current scope:
- core/path.go: path existence helper
- core/errors.go: generic error handling helpers
- core/case.go: snake_case to camelCase helpers
- core/struct_map.go: reflection helpers for struct-map and tag-based assignment

Design rule:
- Keep only low-coupling and dependency-light helpers here.
- Project-specific helpers (logging pipeline, message queue, auth workflow) should stay in target projects or optional profiles.
