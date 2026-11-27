# Profiles

Declare exactly one profile in `00_RUN_MANIFEST.md` before Wave 1.

## FULL: parallel agents

For agent runtimes that can run several workers. Every Wave 1 stream you list is dispatched; you may split streams but not drop ones you named.

- One controller delegates, merges and reports. It does not search itself.
- Each worker gets: task ID, read set, one output file it exclusively owns, dependencies, required evidence, completion criteria, and an explicit ban on touching the user's own files.
- Workers write only their own file under `agents/`. A merge step writes the shared ledgers.
- Verifiers are different workers from discoverers wherever possible.
- Reviewers report; owners of the affected file correct.
- Use the smallest worker capability that does the task. Mechanical setup needs no strong model; synthesis and final audit do.

## SCOPED: one agent or one chat

For a single assistant in a single conversation, or a bounded mid-project pass. The manifest must name: streams run, streams not run and why, a query or time budget, and the output folder.

- Run waves sequentially, one stream at a time, finishing the log of each before the next.
- Role separation becomes sequential self-review: after discovery, change posture and verify as if someone else had written the leads. Re-open sources rather than trusting your earlier notes.
- Pick the two or three streams that bear most on the central claims, and always include the adverse-evidence stream.
- If the chat cannot browse or write files, produce the CSVs and markdown inline, mark every item `DISCOVERED` unless you really opened it, and say that no search was run if none was.
- Coverage gaps from a narrower profile are profile-scoped limitations, not hidden failures. State them in `12_COVERAGE.md`.

## Choosing

| Situation | Profile |
|---|---|
| Opening a large project, many claims, several source classes | FULL |
| Spot check of one claim, a deadline, or a chat-only tool | SCOPED |
| Unsure | SCOPED, then widen if saturation is not reached |
