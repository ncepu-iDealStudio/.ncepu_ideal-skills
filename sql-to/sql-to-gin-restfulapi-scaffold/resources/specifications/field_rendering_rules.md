# Field Rendering Rules (V1)

## Goal

Define deterministic rendering of model fields and parser bind fields for Gin scaffold output.

## Model Field Rule

Render Go struct fields using this order:

1. Go field name
2. Go type
3. gorm tag
4. json tag
5. form tag

Expected format:

FieldName Type `gorm:"..." json:"..." form:"..."`

## Type Rule

- SQL numeric types map to Go numeric types from type_mappings.json
- SQL date/time types map to time.Time and add time import
- tinyint(1), bool, boolean map to bool

## Nullability Rule

- V1 uses value types by default for stable code generation
- nullable metadata is preserved for future pointer-type extension

## Payload Participation Rule

- Primary key field:
  - in_post_payload: false when auto increment
  - in_put_payload: false
- Soft-delete field:
  - in_post_payload: false
  - in_put_payload: false
- Normal business field:
  - in_get_filter: true
  - in_post_payload: true
  - in_put_payload: true

## Soft Delete Rule

If a field is recognized as soft-delete candidate:

- mark is_soft_delete_field = true
- use inactive value as default query filter
- delete action sets active value

## Comment Rule

- SQL field comments should be preserved in context metadata
- V1 does not force comment emission into Go code comments
