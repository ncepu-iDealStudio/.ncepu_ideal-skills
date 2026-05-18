# Template Context Schema (V1.1)

## Root Object

- `project`: project-wide metadata
- `options`: generation toggles and conflict strategy
- `entities`: parsed table/view entities
- `diagnostics`: warnings and parse notes

## Key Fields

### project

- `project_name`
- `api_version_prefix`
- `run_mode_default`
- `module_style`
- `sql_source_type`
- `sql_source_path`
- `generator_name`

### options

- `first_scaffold`
- `generate_other_resource`
- `supports_batch_add`
- `auto_permission_whitelist`
- `overwrite_strategy`
- `conflict_policy`
- `security_profile`

### entity

- `entity_kind`: `table` or `view`
- `table_name_raw`
- `module_name`
- `class_name`
- `resource_slug`
- `endpoint_base`
- `url_collection`
- `url_item`
- `route_param_name`
- `primary_key_field`
- `primary_key_type`
- `supports_crud`
- `supports_query`
- `supports_other_resource`
- `has_soft_delete`
- `soft_delete_field`
- `soft_delete_active_value`
- `soft_delete_inactive_value`
- `fields`

### field

- `field_name_raw`
- `sql_type_raw`
- `sqlalchemy_type`
- `python_type`
- `nullable`
- `is_primary_key`
- `is_auto_increment`
- `is_soft_delete_field`
- `in_get_filter`
- `in_post_payload`
- `in_put_payload`

## Notes

- Route key follows SQL primary key rule.
- URL and route params use snake_case.
- Views without suitable key use collection query route only.
