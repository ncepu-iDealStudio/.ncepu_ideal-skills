# SQL-to-Gin-RESTfulAPI Code Standards

## Scope

This document defines V1 coding standards for generated Gin RESTful projects.

## Naming

- Go package folders: snake_case
- URL paths: snake_case
- URL path params: snake_case
- Struct names: PascalCase
- Keep SQL field names as-is where possible to preserve compatibility

## Layering

Generated code follows these layers:

- internal/models
- internal/dao
- internal/services
- apis/api_1_0

## Generated API Style

- Handlers use Gin context with explicit bind and error return handling
- Service layer encapsulates business query and pagination methods
- DAO layer encapsulates CRUD persistence details
- Model layer owns GORM tags and table binding metadata

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
- err

## Pagination

- Page default: 1
- Size default: 10
- Size max: 100
- Order default: empty string

## Soft Delete

If soft delete field exists (is_delete, is_deleted, isDelete, isDeleted):

- get/update must filter out deleted rows by default
- delete should perform soft delete

## Conflict Strategy (Incremental)

- Merge API registration files
- Skip existing entity files
- Emit warnings for skipped files

## Formatting and Build

- Generated Go code should be gofmt-compatible
- Imports should be deterministic and deduplicated
- Do not generate unused imports in final output
