# Router Registry Merge Strategy (V1)

## Goal

Support incremental generation without overwriting user code.

## Merge Targets

- apis/api_1_0/urls.go
- apis/api_1_0/{resource}/urls.go

## Markers

Generator should only operate between marker blocks when markers exist:

- // ==AUTO_IMPORTS_START== to // ==AUTO_IMPORTS_END==
- // ==AUTO_REGISTRY_START== to // ==AUTO_REGISTRY_END==

When markers do not exist, strategy falls back to append-only safe insertion.

## Merge Rules

1. Keep all non-marker content unchanged.
2. In auto import block:
   - append missing package imports
   - keep imports sorted by module name
   - remove duplicates
3. In auto registry block:
   - append missing InitXxxRouterGroup calls
   - keep entries sorted by resource/module name
   - remove duplicates
4. Do not rewrite or reorder user custom code outside marker blocks.

## Conflict Strategy

- If markers are missing: warning and fallback append-only insertion.
- If syntax parse fails: warning and skip merge.
- If duplicate registrations found: keep one and warn.

## Output Diagnostics

Merge report should include:

- inserted imports count
- inserted registry entries count
- duplicate entries removed count
- skip reasons (if any)
