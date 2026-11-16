# Output Format

Always produce the required deliverables for the chosen engine(s). Do not fold a schema script into the design document as a substitute for a standalone script. Write prose in the user's language; keep SQL and identifiers as written in the schema.

When a schema already exists, the required executable files are up/down migrations for the requested change, and `database-design.md` includes the difference list. Write a full `schema.sql` only for a new schema or when the user asks to rebuild. Do not replace an existing migration history with a greenfield script.

For MongoDB, follow [other-engines.md](other-engines.md). Deliver `schema.js` with `$jsonSchema` and indexes. Do not emit relational foreign keys.

If an output path is not specified, use:

- One engine: `schema.sql` (for MongoDB, `schema.js`)
- Both PostgreSQL and MySQL: `schema.postgres.sql` and `schema.mysql.sql`
- `database-design.md` — design document

Each schema script must follow that engine's reference: [postgres.md](postgres.md) or [mysql.md](mysql.md). Do not emit a single lowest-common-denominator script for both engines. If the user asks for one shared dialect anyway, explain what each engine would lose, then still prefer two scripts unless they insist.

When the user already has a project layout, place the files where that project keeps schema and docs. If they use an ORM, you may also add equivalent model definitions as a supplementary file. Do not replace the required files with ORM models unless the user asks for that.

Omit design-document sections that do not apply (for example, scaling notes for a small internal tool).

## 1. Schema script

A complete, executable script for one engine and version, in dependency order.

- PostgreSQL: extensions, tables, constraints, indexes, triggers, and row-level security when it applies.
- MySQL: `ENGINE=InnoDB`, `DEFAULT CHARSET=utf8mb4` and an explicit collation on every table, constraints, indexes, and `ON UPDATE CURRENT_TIMESTAMP(6)` or triggers. Do not emit Postgres-only syntax (`timestamptz`, `uuidv7()`, partial `CREATE INDEX ... WHERE`, `EXECUTE FUNCTION`, `GENERATED ... AS IDENTITY` as a habit).

Put explanatory comments above non-obvious constraints, indexes, and `ON DELETE` choices. If migrations are also requested, add up/down scripts as extra files (separate files per engine when targeting both); they do not replace the schema script(s).

## 2. Design document (`database-design.md`)

Use this structure. When targeting both engines, keep one document, put engine-specific types and index syntax in the column/index tables or a short note under each table, and add the **Engine differences** section.

````markdown
# [Domain] database design - [Engine and version, or "PostgreSQL and MySQL"]

## Assumptions
- [Product decisions the user chose, and decisions taken from a specification without asking]
- [Assumptions for decisions that were not asked because the cap was reached]
- [Volumes, tenancy, engine defaults, and anything else inferred rather than stated]

## ERD
```mermaid
erDiagram
  ...
```

## Relationship overview
- [Each relationship in one line: tables, cardinality, and the foreign key, including join tables for N:M]

## Tables

### `table_name` (short title)
- **Purpose:** [What this table stores and why it exists]
- **Columns:**

  | Column | Type | Meaning | Constraints |
  |---|---|---|---|
  | ... | ... | ... | ... |

  When targeting both engines, use split type cells such as `timestamptz` (PostgreSQL) / `DATETIME(6)` (MySQL).

- **Keys:** [Primary key, unique keys, and natural keys]
- **Relationships:**
  - [Cardinality and the related table, the FK columns, and ON DELETE]
- **Indexes:** [Each index and the query it serves; for MySQL, state the generated-column or composite substitute for any partial index used in PostgreSQL]
- **Notes:** [Soft delete, tenancy, RLS or MySQL tenancy enforcement, or other caveats that belong to this table]

(Repeat one subsection per table or collection.)

## Query-to-index map
| Query | Served by |
|---|---|

## Design decisions
- [Key type, why, and the PostgreSQL / MySQL form]
- [Each deliberate denormalization, and the query it serves]
- [ON DELETE choices that are not obvious]
- [Soft delete vs hard delete, and where]

## Engine differences
[Only when targeting both engines. List type, index, tenancy, and migration differences. Omit when there is a single engine.]

## Schema script
- File: `schema.sql` (or `schema.postgres.sql` and `schema.mysql.sql`)

## Migrations
[Only if requested or clearly needed. Otherwise omit.]

```sql
-- up
```
```sql
-- down (mark destructive steps)
```

## Verification
- [What was run: DDL applied on the target engine(s), EXPLAIN results for key queries]
- [Or: "Not executed; reviewed by hand"]

## Later, if needed
- [Partitioning trigger point, read replicas, archival, caching]
````

Every table or collection in the schema script must have a subsection under **Tables**. Do not leave a table documented only in the ERD or the SQL comments.
