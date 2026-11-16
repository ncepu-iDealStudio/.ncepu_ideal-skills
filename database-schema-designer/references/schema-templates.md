# Schema Templates

Two complete worked examples of the same domain: PostgreSQL 18 and MySQL 8.4 (InnoDB). Adapt names and types to the domain.

- PostgreSQL 17 or earlier: replace `uuidv7()` with `gen_random_uuid()` or an app-generated UUIDv7.
- MySQL: generate UUIDv7 in the app and store `UUID_TO_BIN(uuid, 0)`. There is no built-in `uuidv7()`.

## Contents
- Worked example: multi-tenant project tracker (PostgreSQL 18)
- The same example in MySQL 8.4 (InnoDB)
- Row-level security (PostgreSQL)
- Text ERD
- Migration with rollback (PostgreSQL)
- Migration with rollback (MySQL)
- MongoDB collection with validation

## Worked example: multi-tenant project tracker (PostgreSQL 18)

```sql
-- Shared trigger function: keep updated_at current on every UPDATE
CREATE OR REPLACE FUNCTION set_updated_at() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at := now();
  RETURN NEW;
END;
$$;

CREATE TABLE orgs (
  id         uuid PRIMARY KEY DEFAULT uuidv7(),
  name       text NOT NULL CHECK (char_length(name) BETWEEN 1 AND 200),
  slug       text NOT NULL UNIQUE,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE users (
  id         uuid PRIMARY KEY DEFAULT uuidv7(),
  email      text NOT NULL,
  full_name  text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);
-- Case-insensitive uniqueness; also serves lookups by lower(email)
CREATE UNIQUE INDEX users_email_lower_key ON users (lower(email));

CREATE TABLE org_members (
  org_id     uuid NOT NULL REFERENCES orgs (id) ON DELETE CASCADE,
  user_id    uuid NOT NULL REFERENCES users (id) ON DELETE CASCADE,
  role       text NOT NULL DEFAULT 'member' CHECK (role IN ('owner', 'admin', 'member')),
  created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (org_id, user_id)
);
-- The PK serves "members of an org"; this serves "orgs for a user"
CREATE INDEX idx_org_members_user ON org_members (user_id);

CREATE TABLE projects (
  id         uuid PRIMARY KEY DEFAULT uuidv7(),
  org_id     uuid NOT NULL REFERENCES orgs (id) ON DELETE CASCADE,
  name       text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (org_id, name),
  UNIQUE (id, org_id)          -- target for the composite FK from tasks
);

CREATE TABLE tasks (
  id          uuid PRIMARY KEY DEFAULT uuidv7(),
  org_id      uuid NOT NULL,
  project_id  uuid NOT NULL,
  assignee_id uuid REFERENCES users (id) ON DELETE SET NULL,
  title       text NOT NULL CHECK (char_length(title) BETWEEN 1 AND 500),
  status      text NOT NULL DEFAULT 'todo' CHECK (status IN ('todo', 'in_progress', 'done')),
  due_at      timestamptz,
  created_at  timestamptz NOT NULL DEFAULT now(),
  updated_at  timestamptz NOT NULL DEFAULT now(),
  -- Keeps tasks.org_id consistent with the project's org
  FOREIGN KEY (project_id, org_id) REFERENCES projects (id, org_id) ON DELETE CASCADE
);
-- Main screen: open tasks for a project by due date
CREATE INDEX idx_tasks_project_due_open ON tasks (project_id, due_at) WHERE status <> 'done';
-- "My tasks" view and the ON DELETE SET NULL from users
CREATE INDEX idx_tasks_assignee ON tasks (assignee_id) WHERE assignee_id IS NOT NULL;
-- RLS policies filter by org
CREATE INDEX idx_tasks_org ON tasks (org_id);

CREATE TRIGGER orgs_updated_at     BEFORE UPDATE ON orgs     FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER users_updated_at    BEFORE UPDATE ON users    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER projects_updated_at BEFORE UPDATE ON projects FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER tasks_updated_at    BEFORE UPDATE ON tasks    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

Query-to-index map for this schema:

| Query | Served by |
|---|---|
| Open tasks for a project by due date | `idx_tasks_project_due_open` (partial) |
| Tasks assigned to me | `idx_tasks_assignee` |
| Members of an org | `org_members` primary key `(org_id, user_id)` |
| Orgs a user belongs to | `idx_org_members_user` |
| Look up user by email | `users_email_lower_key` (query with `lower(email) = lower($1)`) |
| Project by name within an org | `UNIQUE (org_id, name)` |


## The same example in MySQL 8.4 (InnoDB)

UUIDv7 values are supplied by the app and stored as `BINARY(16)` with `UUID_TO_BIN(uuid, 0)`. `updated_at` uses `ON UPDATE CURRENT_TIMESTAMP(6)` instead of a trigger. There are no partial indexes: open-task sorting uses a stored generated column.

```sql
CREATE TABLE orgs (
  id         BINARY(16) NOT NULL,
  name       VARCHAR(200) NOT NULL,
  slug       VARCHAR(100) NOT NULL,
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (id),
  UNIQUE KEY orgs_slug_key (slug),
  CONSTRAINT orgs_name_len CHECK (CHAR_LENGTH(name) BETWEEN 1 AND 200)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE users (
  id         BINARY(16) NOT NULL,
  email      VARCHAR(255) NOT NULL,
  full_name  VARCHAR(200) NULL,
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (id),
  UNIQUE KEY users_email_key (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- UNIQUE (email) is case-insensitive under utf8mb4_0900_ai_ci

CREATE TABLE org_members (
  org_id     BINARY(16) NOT NULL,
  user_id    BINARY(16) NOT NULL,
  role       VARCHAR(20) NOT NULL DEFAULT 'member',
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (org_id, user_id),
  KEY idx_org_members_user (user_id),
  CONSTRAINT org_members_org_id_fkey FOREIGN KEY (org_id) REFERENCES orgs (id) ON DELETE CASCADE,
  CONSTRAINT org_members_user_id_fkey FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
  CONSTRAINT org_members_role_check CHECK (role IN ('owner', 'admin', 'member'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- PK (org_id, user_id) already covers the org_id foreign key; idx_org_members_user serves "orgs for a user"

CREATE TABLE projects (
  id         BINARY(16) NOT NULL,
  org_id     BINARY(16) NOT NULL,
  name       VARCHAR(200) NOT NULL,
  created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (id),
  UNIQUE KEY projects_org_name_key (org_id, name),
  UNIQUE KEY projects_id_org_key (id, org_id),
  CONSTRAINT projects_org_id_fkey FOREIGN KEY (org_id) REFERENCES orgs (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE tasks (
  id          BINARY(16) NOT NULL,
  org_id      BINARY(16) NOT NULL,
  project_id  BINARY(16) NOT NULL,
  assignee_id BINARY(16) NULL,
  title       VARCHAR(500) NOT NULL,
  status      VARCHAR(20) NOT NULL DEFAULT 'todo',
  due_at      DATETIME(6) NULL,
  created_at  DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  updated_at  DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  -- NULL when done. Query: WHERE project_id = ? AND due_sort_key IS NOT NULL ORDER BY due_sort_key
  -- InnoDB still indexes the NULL rows; status <> 'done' ORDER BY due_at does not use this index
  due_sort_key DATETIME(6) GENERATED ALWAYS AS (IF(status = 'done', NULL, due_at)) STORED,
  PRIMARY KEY (id),
  KEY idx_tasks_project_due_open (project_id, due_sort_key),
  KEY idx_tasks_assignee (assignee_id),
  KEY idx_tasks_org (org_id),
  CONSTRAINT tasks_title_len CHECK (CHAR_LENGTH(title) BETWEEN 1 AND 500),
  CONSTRAINT tasks_status_check CHECK (status IN ('todo', 'in_progress', 'done')),
  CONSTRAINT tasks_project_org_fkey FOREIGN KEY (project_id, org_id) REFERENCES projects (id, org_id) ON DELETE CASCADE,
  CONSTRAINT tasks_assignee_id_fkey FOREIGN KEY (assignee_id) REFERENCES users (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

Query-to-index map for this schema:

| Query | Served by |
|---|---|
| Open tasks for a project by due date | `idx_tasks_project_due_open` on `(project_id, due_sort_key)`, only when the query is `WHERE project_id = ? AND due_sort_key IS NOT NULL ORDER BY due_sort_key`. `WHERE status <> 'done' ORDER BY due_at` does not use this index for the filter or the sort. InnoDB still stores the `NULL` entries. |
| Tasks assigned to me | `idx_tasks_assignee` (InnoDB may also use this for `ON DELETE SET NULL`) |
| Members of an org | `org_members` primary key `(org_id, user_id)` |
| Orgs a user belongs to | `idx_org_members_user` |
| Look up user by email | `users_email_key` (case-insensitive under `utf8mb4_0900_ai_ci`) |
| Project by name within an org | `projects_org_name_key` |

MySQL has no row-level security. Enforce `org_id` membership in the application, or with views that filter on a session variable. Index `org_id` as above so those checks stay cheap.

Engine differences in this pair of scripts:

- Open-task lookup: PostgreSQL filters `status <> 'done'` on a partial index. MySQL must filter and sort `due_sort_key`. The done rows remain in the MySQL index.
- Email uniqueness: PostgreSQL `lower(email)` folds case and keeps accents distinct. MySQL `utf8mb4_0900_ai_ci` folds case and accents, so `jose` and `josé` cannot both exist.
- Primary keys: PostgreSQL 18 `uuidv7()` versus app-generated UUIDv7 stored with `UUID_TO_BIN(uuid, 0)`. On PostgreSQL 17 or earlier, do not copy the `uuidv7()` default from this example.

## Row-level security (PostgreSQL)

Needed whenever clients reach the database directly (always on Supabase).

```sql
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

-- Members of the task's org can read and write its tasks.
-- current_setting('app.user_id') is set per request by the app; on Supabase use (select auth.uid()).
CREATE POLICY tasks_member_access ON tasks
  FOR ALL
  USING (EXISTS (
    SELECT 1 FROM org_members m
    WHERE m.org_id = tasks.org_id
      AND m.user_id = (select current_setting('app.user_id', true)::uuid)
  ))
  WITH CHECK (EXISTS (
    SELECT 1 FROM org_members m
    WHERE m.org_id = tasks.org_id
      AND m.user_id = (select current_setting('app.user_id', true)::uuid)
  ));
```

Repeat for each tenant-scoped table. Policies that only allow reads need just `USING`; split `FOR ALL` into per-operation policies when roles differ (for example only `owner`/`admin` may delete).

## Text ERD

```
orgs  ──1:N──  projects  ──1:N──  tasks
orgs  ──N:M──  users     (via org_members, with role)
users ──1:N──  tasks     (assignee, optional)
```

Or as Mermaid, which renders on GitHub:

```mermaid
erDiagram
  orgs ||--o{ org_members : has
  users ||--o{ org_members : joins
  orgs ||--o{ projects : owns
  projects ||--o{ tasks : contains
  users |o--o{ tasks : "assigned to"
```

## Migration with rollback (PostgreSQL)

Keep each migration small, and put `CONCURRENTLY` index builds in their own migration because they cannot run inside a transaction.

```sql
-- migrations/0007_add_task_priority.up.sql
BEGIN;
SET LOCAL lock_timeout = '5s';
ALTER TABLE tasks
  ADD COLUMN priority smallint NOT NULL DEFAULT 2 CHECK (priority BETWEEN 1 AND 4);
COMMIT;

-- migrations/0008_index_task_priority.up.sql  (no transaction)
CREATE INDEX CONCURRENTLY idx_tasks_project_priority_open
  ON tasks (project_id, priority) WHERE status <> 'done';
```

```sql
-- migrations/0008_index_task_priority.down.sql  (no transaction)
DROP INDEX CONCURRENTLY IF EXISTS idx_tasks_project_priority_open;

-- migrations/0007_add_task_priority.down.sql
-- Destructive: drops priority values. Back up first if they matter.
BEGIN;
SET LOCAL lock_timeout = '5s';
ALTER TABLE tasks DROP COLUMN IF EXISTS priority;
COMMIT;
```

If a `CREATE INDEX CONCURRENTLY` fails partway, it leaves an `INVALID` index; drop it and retry.


## Migration with rollback (MySQL)

Keep each migration small. Prefer `ALGORITHM=INSTANT` or `ALGORITHM=INPLACE, LOCK=NONE`. There is no `CREATE INDEX CONCURRENTLY`.

```sql
-- migrations/0007_add_task_priority.up.sql
SET lock_wait_timeout = 5;
ALTER TABLE tasks
  ADD COLUMN priority SMALLINT NOT NULL DEFAULT 2,
  ALGORITHM=INSTANT;

ALTER TABLE tasks
  ADD CONSTRAINT tasks_priority_check CHECK (priority BETWEEN 1 AND 4),
  ALGORITHM=INPLACE, LOCK=NONE;

-- migrations/0008_index_task_priority.up.sql
ALTER TABLE tasks
  ADD INDEX idx_tasks_project_priority_open (project_id, priority),
  ALGORITHM=INPLACE, LOCK=NONE;
```

```sql
-- migrations/0008_index_task_priority.down.sql
ALTER TABLE tasks
  DROP INDEX idx_tasks_project_priority_open,
  ALGORITHM=INPLACE, LOCK=NONE;

-- migrations/0007_add_task_priority.down.sql
-- Destructive: drops priority values. Back up first if they matter.
SET lock_wait_timeout = 5;
ALTER TABLE tasks
  DROP CONSTRAINT tasks_priority_check,
  ALGORITHM=INPLACE, LOCK=NONE;

ALTER TABLE tasks
  DROP COLUMN priority,
  ALGORITHM=INPLACE, LOCK=NONE;
```

If InnoDB refuses `INSTANT` or `INPLACE, LOCK=NONE` on a large table, stop and use gh-ost or pt-online-schema-change; do not silently run a table-copy `ALGORITHM=COPY`.

## MongoDB collection with validation

Design from access patterns: embed data read together and bounded in size, reference data that is shared or grows without limit.

```javascript
db.createCollection("tasks", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["orgId", "projectId", "title", "status", "createdAt"],
      properties: {
        orgId:     { bsonType: "objectId" },
        projectId: { bsonType: "objectId" },
        title:     { bsonType: "string", minLength: 1, maxLength: 500 },
        status:    { enum: ["todo", "in_progress", "done"] },
        assignee:  {  // embedded snapshot for list views; source of truth is users
          bsonType: "object",
          properties: { userId: { bsonType: "objectId" }, name: { bsonType: "string" } }
        },
        dueAt:     { bsonType: "date" },
        createdAt: { bsonType: "date" }
      }
    }
  }
});

// Equality, then sort, then range (the ESR rule)
db.tasks.createIndex({ projectId: 1, status: 1, dueAt: 1 });
db.tasks.createIndex({ "assignee.userId": 1, dueAt: 1 });
```
