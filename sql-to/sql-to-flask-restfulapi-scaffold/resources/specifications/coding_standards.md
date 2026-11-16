# SQL-to-Flask-RESTfulAPI Code Standards

## Scope

This document defines V1 coding standards for generated Flask RESTful projects.

## Naming

- Python modules: snake_case
- URL paths: snake_case
- URL path params: snake_case
- Class names: PascalCase
- Keep SQL field names as-is where possible to preserve compatibility

## Layering

Generated code follows these layers:

- models
- controller
- service
- api_1_0

## Response Contract

All API responses should follow:

- code
- message
- data
- totalCount
- totalPage

Error response minimum fields:

- code
- message
- data

## Pagination

- Page default: 1
- Size default: 10
- Size max: 100

## Soft Delete

If soft delete field exists (`is_delete`, `is_deleted`, `isDelete`, `isDeleted`):

- get/update must filter out deleted rows by default
- delete should perform soft delete

## Conflict Strategy (Incremental)

- Merge registration files
- Skip existing entity files
- Emit warnings for skipped files

## Dependencies

Use exact dependency versions in requirements.txt for deterministic debugging.
