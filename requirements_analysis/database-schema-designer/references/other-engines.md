# Other Engines

For PostgreSQL, use [postgres.md](postgres.md). For MySQL 8.x / 9.x (InnoDB), use [mysql.md](mysql.md). Those two engines are first-class in this skill.

This file covers only SQLite and MongoDB. SQLite still follows the relational workflow, with the type and pragma rules below. MongoDB does not: skip relational keys, foreign keys, and `ON DELETE`, and shape the schema from access patterns.

## SQLite

- Declare tables `STRICT` so column types are enforced.
- Foreign keys are off by default: run `PRAGMA foreign_keys = ON;` on every connection.
- `INTEGER PRIMARY KEY` is an alias for the rowid and the fastest key.
- Store timestamps as ISO 8601 `TEXT` in UTC or as Unix epoch `INTEGER`; pick one and be consistent.
- Partial and expression indexes are supported.
- `ALTER TABLE` is limited (no dropping constraints); many changes need the create-copy-rename pattern.
- Use WAL mode (`PRAGMA journal_mode = WAL;`) for concurrent readers.

## MongoDB

- Design from access patterns: list the queries, then shape documents so each common query reads one document or one index range.
- Embed when data is read together, owned by the parent, and bounded (order line items). Reference when data is shared, updated independently, or grows without limit (comments on a popular post).
- Documents are capped at 16 MB; unbounded arrays are the usual way to hit it.
- Enforce shape with `$jsonSchema` validators on the collection (see [schema-templates.md](schema-templates.md)).
- Compound index order follows the ESR rule: equality fields, then sort fields, then range fields.
- Multi-document transactions exist but cost more; a schema that needs them for common writes is often better modeled with embedding.
- Denormalized copies (a user's name on each post) need an update path; document which copies are allowed to go stale.
