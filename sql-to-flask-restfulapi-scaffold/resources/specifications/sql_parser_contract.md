# SQL Parser Contract (V1)

## Supported DDL

V1 supports common MySQL DDL only:

- CREATE TABLE
- CREATE VIEW
- Primary key
- Default value
- Column/table comments

## Unsupported Syntax Handling

Unsupported or unrecognized syntax should:

1. be skipped
2. be recorded in diagnostics warnings

## Primary Key Rule

Route key uses the SQL-defined primary key directly.

- If primary key is autoID/auto_id, use it
- If business key should be used, it must be defined as primary key in DDL

## View Rule

For views without clear primary key/business key:

- generate collection query routes only
- do not generate item route or CRUD write operations

## Output Diagnostics

Parser output must include:

- parsed entities count
- skipped statements count
- warning list with reason and SQL snippet
