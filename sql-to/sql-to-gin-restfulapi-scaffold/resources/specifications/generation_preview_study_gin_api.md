# Generation Preview for test/api_security_demo-20260717.sql (V1)

## Input

- SQL source: test/api_security_demo-20260717.sql
- Target style: Gin + GORM layered scaffold

## Expected Entities

Tables (11 expected):

- admin
- course
- course_arrangement
- sso_user
- student
- student_selected_course
- sys_class
- sys_classinfo
- sys_college
- sys_department
- teacher

Views (1 expected):

- v_student_course_score

> 说明：实体清单以 `test/api_security_demo-20260717.sql` 为准。旧版基线
> `test/study_flask_api.sql` 使用驼峰表名（`sys_classInfo` 等）且已移除；
> 当前基线为全小写 snake_case 表名，并多出 `sys_class` 一张表。

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
