# Router Registry Merge Strategy (V1)

## Goal

Support incremental generation without overwriting user code.

## Merge Target

- `api_1_0/__init__.py`

## Markers

Generator should only operate between marker blocks:

- `# ==AUTO_IMPORTS_START==` to `# ==AUTO_IMPORTS_END==`
- `# ==AUTO_REGISTRY_START==` to `# ==AUTO_REGISTRY_END==`

## Merge Rules

1. Keep all non-marker content unchanged.
2. In auto import block:
   - append missing blueprint imports
   - keep imports sorted by module name
   - remove duplicates
3. In auto registry block:
   - append missing registration tuples `(blueprint, prefix)`
   - keep entries sorted by endpoint/module name
   - remove duplicates
4. Do not rewrite or reorder user custom code outside marker blocks.

## Conflict Strategy

- If markers are missing: emit warning and skip merge.
- If syntax parse fails: emit warning and skip merge.
- If duplicate registrations found: keep one and warn.

## Output Diagnostics

Merge report should include:

- inserted imports count
- inserted registry entries count
- duplicate entries removed count
- skip reasons (if any)
