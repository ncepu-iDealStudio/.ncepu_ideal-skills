# Provenance

This skill is adapted from **github/awesome-copilot** (`skills/openapi-to-application-java-spring-boot`).

- Source: <https://github.com/github/awesome-copilot/tree/main/skills/openapi-to-application-java-spring-boot>
- Commit read: `main` (SKILL.md SHA `3c697148951b9893dc6a4c459bde03beef663c77`)
- License of the source: MIT License (<https://github.com/github/awesome-copilot/blob/main/LICENSE>)
- The adapted material is redistributed under this repository's MIT license. Keep the attribution and this notice with any redistribution of the adapted file.

## Files adapted

| Source file in awesome-copilot | Adapted into |
|--------------------------------|--------------|
| `skills/openapi-to-application-java-spring-boot/SKILL.md` | `SKILL.md` (cross-references adapted to this repository; see Changes) |

The upstream skill is a single self-contained `SKILL.md` with no `references/`, `assets/` or `scripts/` files, so there were no companion files to copy.

## Changes

- Added a "Related skills in this repository" section pointing to the skills that actually exist here: `create-spring-boot-java-project`, `java-springboot`, `spring-security`, `spring-boot-testing`.
- The upstream version referenced two skills that are **not present in this repository**: `java-hibernate-jpa` and `java-testcontainers`. Their references were rewritten to point to the equivalent in-repo skills (`java-springboot` for Spring Data JPA/JDBC schema handling, `spring-boot-testing` for Testcontainers with `@ServiceConnection`) and to state explicitly that the upstream skills are not part of this repository.
- Added a Provenance section to `SKILL.md` and this notice.
- All technical guidance, generator configuration snippets, option notes and verification steps are otherwise unchanged from upstream.
