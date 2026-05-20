# Template Context Schema (V1)

## Root

Context object contains:

- project
- options
- entities
- diagnostics

## project

Required fields:

- project_name: string
- module_name: string
- generator_name: string
- api_group: string
- api_version_package: string
- sql_source_type: string (file | text)
- sql_source_path: string

## options

Required fields:

- first_scaffold: boolean
- overwrite_strategy: string (merge | skip | overwrite)
- conflict_policy: string (warn | fail)
- security_profile: string (minimal | standard | secure)
- generate_view_resource: boolean
- supports_batch_add: boolean

## entities[]

Common fields:

- entity_kind: string (table | view)
- table_name_raw: string
- module_name: string
- entity_name: string
- resource_slug: string
- router_init_func: string
- url_collection: string
- url_item: string
- route_param_name: string
- primary_key_field: string
- primary_key_type: string
- supports_crud: boolean
- supports_query: boolean
- has_soft_delete: boolean
- fields: array

### fields[]

Required fields:

- field_name_raw: string
- go_field_name: string
- sql_type_raw: string
- gorm_type: string
- go_type: string
- gorm_tag: string
- json_tag: string
- form_tag: string
- nullable: boolean
- is_primary_key: boolean
- is_auto_increment: boolean
- is_soft_delete_field: boolean
- default_value: any
- comment: string
- in_get_filter: boolean
- in_post_payload: boolean
- in_put_payload: boolean

## diagnostics

Required fields:

- parse_errors: string[]
- fallback_warnings: string[]
- conflict_warnings: string[]
