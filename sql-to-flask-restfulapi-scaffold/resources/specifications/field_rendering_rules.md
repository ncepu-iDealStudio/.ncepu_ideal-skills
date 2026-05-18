# Field Rendering Rules (V1)

## Goal

Define deterministic rendering for SQL columns into Flask-SQLAlchemy model field lines.

## Rendering Order

Render field attributes in this fixed order:

1. name
2. SQLAlchemy type
3. primary_key
4. nullable
5. default/server_default
6. comment (as info)

## Template Output Pattern

Use this standard line pattern:

`{field_name} = db.Column({sqlalchemy_type}, primary_key={primary_key}, nullable={nullable}{default_part}{info_part})`

## Rules

1. `field_name` keeps SQL raw column name to preserve compatibility.
2. `sqlalchemy_type` comes from `type_mappings.json`.
3. `primary_key` is true only for SQL primary key columns.
4. `nullable` is false when SQL has NOT NULL; otherwise true.
5. `default_part`:
   - literal default -> `, default=<value>`
   - SQL function/default expression -> `, server_default=db.FetchedValue()`
6. `info_part`:
   - if comment exists -> `, info="<comment>"`
   - else omit

## Soft Delete Guidance

If column name is in configured soft-delete candidates:

- keep as normal model field
- controller handles filtering and delete behavior

## Example

Input column:

- name: `isDelete`
- type: `tinyint(1)`
- default: `0`
- comment: `是否删除`

Rendered line:

`isDelete = db.Column(db.Integer, primary_key=False, nullable=True, default=0, info="是否删除")`
