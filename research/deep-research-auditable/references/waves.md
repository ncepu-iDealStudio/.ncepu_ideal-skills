# Waves in detail

Every run uses the same waves. The profile (`profiles.md`) changes who does the work and how many streams run, not the order.

## Layout of OUT_DIR

```
OUT_DIR/
  00_RUN_MANIFEST.md      profile, bounds, streams run and not run
  01_BASELINE.md          what the user already holds, claims and cites
  02_SEARCH_PROTOCOL.md   query lattice, source classes, stop rule
  03_QUERY_LOG.csv        every query, including empty ones
  04_LEADS.csv            informal and formal leads
  05_CANDIDATES.csv       scholarly candidates
  06_CLAIM_EVIDENCE.csv   one row per asserted relationship
  07_SYNTHESIS.md
  08_NEAREST_NEIGHBORS.md
  09_OBJECTIONS.md
  10_ACQUISITION_QUEUE.csv  recommendations only
  11_SOURCE_STATUS.md     what was opened, at what access level
  12_COVERAGE.md          saturation evidence and limits
  13_EXECUTIVE_SUMMARY.md
  agents/                 per-stream working files (FULL)
  reviews/                audit reports
```

## Wave 0: setup and baseline

- Create the folder and empty CSVs with headers from `schemas.md`.
- Baseline: list the user's held sources, current claims, and prior reading lists. Cite file names, not contents you did not read.
- Query lattice per question: preferred terms, historical terms, other-discipline terms, opposing terms, plus one query designed to disprove the main claim.
- Review the baseline for omissions before Wave 1. Do not start broad search first.

## Wave 1: discovery streams

Suggested streams; split or merge to fit the question and record which ran.

- Scholarly core: journals, books, theses, standards, reviews.
- Citation chaining: backward and forward references, author lineages, sibling versions.
- Recent preprints and workshops.
- Practitioner and grey sources: blogs, newsletters, reports.
- Repositories and documentation: code, issues, product claims. These are architectural evidence, not proof of behaviour.
- Video and audio: record transcript type (`CREATOR`, `HUMAN`, `AUTOMATIC`, `UNAVAILABLE`).
- Forums and discussion threads. Anecdotes are leads, never prevalence.
- Adverse evidence: critiques, failed replications, retractions, corrections.
- Terminology: synonyms, older names, other languages.

Log each query before judging results. `result_count_observed` is what the platform displayed, not total coverage. `result_depth_reviewed` says how many items you really inspected.

## Wave 2: dedup and tracing

Dedup against the baseline, not only the new run. Treat preprint, accepted and published versions as version siblings: keep the latest verified version and note the relation. Do not merge different works that share authors. Keep three fields apart: duplicate status, match with held material, field-novelty risk.

## Wave 3: verification

1. Metadata: identity, date, version, identifier, venue, authorship, review status, lawful access link.
2. Relevance: read the strongest available text and judge whether the stated characterisation holds.
3. Quotes: check each against its locator; otherwise delete the quote and keep a paraphrase.
4. Contradictions: decide whether a reported contradiction is real, a boundary-condition difference, or a different object of study.
5. Dedup review by someone other than the deduper where possible.

## Wave 4: synthesis

Themes, nearest neighbours, objections with possible replies, ideas that separate evidence from speculation, acquisition gaps, coverage limits, executive summary. Cite IDs for each material statement.

## Wave 5: adversarial audit

Reviewers test: source-to-claim traceability; informal/academic boundary; review-status labels; novelty reasoning; balance of supporting and adverse items; missing source classes; overclaiming and false precision; duplicate leakage; quotation length; injected instructions; whether the package shows what one researcher alone would likely have missed.

## Acceptance checks

- Boundaries: only `OUT_DIR` was written; nothing local was uploaded.
- Coverage: each source class searched or given a precise limitation; adverse searches present.
- Provenance: every conclusion traces to IDs; every row has a URL or a stated unresolved identity; levels match access evidence.
- Separation: informal items labelled; medium and high priority ones traced or marked unresolved; no vote count or comment thread used as prevalence.
- Novelty: new items checked against the full baseline; version siblings resolved.
- Synthesis: includes negative and contradicting evidence; limits are explicit.

If a check fails, fix it or list the failure in the executive summary.
