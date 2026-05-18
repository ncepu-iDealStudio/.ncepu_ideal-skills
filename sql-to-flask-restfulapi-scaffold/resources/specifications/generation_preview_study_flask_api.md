# Generation Preview (study_flask_api.sql)

## Input

- SQL file: `test/study_flask_api.sql`
- Target style: Flask + Flask-RESTful layered scaffold

## Parsed Entities

### Tables (10)

1. admin
2. course
3. course_arrangement
4. sso_user
5. student
6. student_selected_course
7. sys_classInfo
8. sys_collegeInfo
9. sys_departmentInfo
10. teacher

### Views (1)

1. v_student_course_score

## Planned Generation Output

### Project skeleton (first scaffold)

- manage.py
- app/
- api_1_0/
- models/
- controller/
- service/
- config/
- utils/
- requirements.txt

### Per-table files (7 each)

- models/{module_name}.py
- controller/{ClassName}Controller.py
- service/{ClassName}Service.py
- api_1_0/{resource_slug}Resource/__init__.py
- api_1_0/{resource_slug}Resource/{resource_slug}Resource.py
- api_1_0/{resource_slug}Resource/{resource_slug}OtherResource.py
- api_1_0/{resource_slug}Resource/urls.py

Estimated table files: 10 x 7 = 70

### Per-view files (6 each)

- models/{module_name}.py (read-only mapping)
- controller/{ClassName}Controller.py (query only)
- service/{ClassName}Service.py
- api_1_0/{resource_slug}Resource/__init__.py
- api_1_0/{resource_slug}Resource/{resource_slug}OtherResource.py
- api_1_0/{resource_slug}Resource/urls.py (collection query route)

Estimated view files: 1 x 6 = 6

### Registry merge update

- api_1_0/__init__.py
- import block merge
- registry tuple merge

## Rule Reminders

- Route key uses SQL primary key directly.
- URL and route params use snake_case.
- Soft-deleted rows are filtered by default in get/update when soft-delete field exists.
- Incremental mode merges registry, skips existing entity files, and emits warnings.
