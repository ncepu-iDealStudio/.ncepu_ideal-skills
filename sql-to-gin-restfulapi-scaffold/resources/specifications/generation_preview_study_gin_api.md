# Generation Preview for test/study_flask_api.sql (V1)

## Input

- SQL source: test/study_flask_api.sql
- Target style: Gin + GORM layered scaffold

## Expected Entities

Tables (10 expected):

- admin
- course
- course_arrangement
- sso_user
- student
- student_selected_course
- sys_classInfo
- sys_collegeInfo
- sys_departmentInfo
- teacher

Views (1 expected):

- v_student_course_score

## Expected Generated Outputs (First Scaffold)

Project skeleton:

- main.go
- cmd/
- apis/
- internal/
- configs/
- utils/
- go.mod

Per table (CRUD layers):

- internal/models/{Entity}.go
- internal/dao/{Entity}.go
- internal/services/{Entity}.go
- apis/api_1_0/{resource}/urls.go
- apis/api_1_0/{resource}/{Entity}Resource.go

Per view (query only):

- internal/models/{Entity}.go
- internal/services/{Entity}.go
- apis/api_1_0/{resource}/urls.go
- apis/api_1_0/{resource}/{Entity}Resource.go

Registry updates:

- apis/api_1_0/urls.go import list
- apis/api_1_0/urls.go InitXXRouterGroup call list

## Validation Focus

- mixed naming style compatibility (snake_case + camelCase)
- soft-delete detection coverage
- pagination defaults and caps
- view read-only enforcement
- duplicate registry prevention in incremental runs
