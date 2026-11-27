# Run manifest: <RUN_ID>

## Identity

- Run ID: `<UTC timestamp>`
- Questions: <1 to 5 questions>
- Output folder: `<OUT_DIR>`
- Profile: `FULL` or `SCOPED` (exactly one)
- Bounds: agent cap `<n>`, time or query budget `<n>`, excluded source classes `<list>`

## Streams

| Stream | Run? | Reason |
|---|---|---|
| scholarly core | yes | central to Q1 |
| adverse evidence | yes | required in every run |
| video and audio | no | profile bound; listed as a limitation |

Example phrasing for a SCOPED run: "Two streams ran. The nine others were not run because this pass is a bounded check of one claim. Their absence is a profile limitation, not a finding."

## Baseline summary

<What the user already holds and claims. File names only.>

## Status log

| Time (UTC) | Wave | Note |
|---|---|---|
| | 0 | setup done |

## Open items at close

<Unresolved failures, if any. "None" only if the acceptance checks all passed.>
