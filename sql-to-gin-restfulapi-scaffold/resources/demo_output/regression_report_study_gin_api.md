# Step 7 Regression Report (sql-to-gin-restfulapi-scaffold)

Date: 2026-05-20

## Scope

This report validates current skill assets against the target SQL baseline in test/study_flask_api.sql and current toolchain behavior.

## Evidence Inputs

- SQL baseline: test/study_flask_api.sql
- Example context: sql-to-gin-restfulapi-scaffold/resources/config/template_context_example.json
- Generated full context: sql-to-gin-restfulapi-scaffold/resources/demo_output/generated_context_study_flask_api.json
- Router merge target: sql-to-gin-restfulapi-scaffold/resources/templates/project_structure/apis/api_1_0/urls.go
- Router merge preview target: sql-to-gin-restfulapi-scaffold/resources/demo_output/urls_merge_preview.go

## Executed Checks

1. Context schema validation
2. Generation plan preview
3. Bundle preview rendering
4. SQL table/view baseline extraction
5. Soft-delete candidate name scan
6. Router merge idempotence check
7. Context coverage comparison against SQL baseline
8. SQL-to-context automatic extraction
9. Full registry merge completeness

## Results

### 1) Context schema validation

- Status: PASS
- Output: Context validation passed.

### 2) Generation plan preview

- Status: PASS
- Output summary:
  - entities: 11
  - planned files: 54
  - tables: 10
  - views: 1

### 3) Bundle preview rendering

- Status: PASS
- Output summary:
  - bundle files: 11
  - manifest generated:
    - sql-to-gin-restfulapi-scaffold/resources/demo_output/bundle_preview/manifest.json

### 4) SQL baseline extraction

- Status: PASS
- Extracted from SQL:
  - tables: 10
  - views: 1
  - total entities: 11

Tables:
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

Views:
- v_student_course_score

### 5) Soft-delete naming coverage

- Status: PARTIAL PASS
- Found in SQL from configured candidates:
  - isDelete
  - is_delete
- Not found in this SQL baseline (but supported by config):
  - is_deleted
  - isDeleted

### 6) Router merge idempotence

- Status: PASS
- Re-run merge output:
  - inserted_imports_count: 0
  - inserted_registry_entries_count: 0
  - duplicate_imports_removed_count: 0
  - duplicate_registry_entries_removed_count: 0
- Conclusion: merge is stable for repeated execution.

### 7) Coverage vs baseline

- Status: PASS
- SQL baseline entities: 11
- Context entities: 11
- Coverage by generated full context: 100.00%

Interpretation:
- SQL-to-context automation is now wired and working.
- Current toolchain supports full baseline scope for this SQL input.

### 8) SQL-to-context automatic extraction

- Status: PASS
- Tool:
  - sql-to-gin-restfulapi-scaffold/resources/tools/generate_context_from_sql.py
- Output:
  - tables: 10
  - views: 1
  - entities: 11
  - generated file:
    - sql-to-gin-restfulapi-scaffold/resources/demo_output/generated_context_study_flask_api.json

### 9) Full registry merge completeness

- Status: PASS
- Method:
  - run merge on isolated preview file (no overwrite of main template)
- Output summary:
  - inserted_imports_count: 9
  - inserted_registry_entries_count: 9

Note:
- Main template already contained 2 entries (student and v_student_course_score).
- After merge preview, total imports and total Init calls are both 11.

### 10) One-command pipeline execution

- Status: PASS
- Tool:
  - sql-to-gin-restfulapi-scaffold/resources/tools/run_regression_pipeline.py
- Output artifacts:
  - sql-to-gin-restfulapi-scaffold/resources/demo_output/pipeline_report.json
- Key summary from latest run:
  - all steps ok: true
  - sql_entities: 11
  - context_entities: 11
  - coverage_percent: 100.0

### 11) Snapshot regression guard

- Status: PASS
- Tool:
  - sql-to-gin-restfulapi-scaffold/resources/tools/check_snapshots.py
- Snapshot files:
  - sql-to-gin-restfulapi-scaffold/resources/demo_output/snapshots/generated_context_study_flask_api.snapshot.json
  - sql-to-gin-restfulapi-scaffold/resources/demo_output/snapshots/bundle_manifest.snapshot.json
- Latest compare mode result:
  - context snapshot: match
  - manifest snapshot: match

## Regression Verdict

- Toolchain correctness (validation/preview/render/merge): PASS
- Functional coverage against full SQL baseline: PASS (11/11)

## Next Actions

1. Add stricter SQL type inference for view fields (currently defaults to string when source metadata is unavailable).
2. Add parser diagnostics for unsupported DDL fragments into generated context diagnostics.
3. Add regression command wrapper (single entry script) to run validate/preview/render/merge in one command.
4. Add minimal golden snapshot tests for generated_context_study_flask_api.json and bundle manifest.
