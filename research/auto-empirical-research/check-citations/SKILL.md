---
name: check-citations
description: >-
  Check BibTeX citation metadata against Crossref, Semantic Scholar, and OpenAlex. Use for 核查参考文献、检查 BibTeX、验证 DOI or 排查编造引用. Distinguishes unavailable sources from completed searches without a match.
---

# check-citations

Check citation metadata before submission; flags are leads for manual review, not proof that a reference was fabricated. Run the script from the installed skill directory or use its absolute path. Do not send confidential titles or identifiers to external APIs without authorization. If shell or network access is unavailable, offer an offline formatting review and label it as such.

## When to Use

- After writing or editing a `.bib` file with AI assistance
- Before submitting a paper, thesis, or report
- When reviewing AI-generated literature sections
- As a CI/CD check in LaTeX manuscript pipelines
- When auditing existing bibliographies for dead or fabricated references

## Background

- 6-55% of AI-generated citations are fabricated (varies by model/domain)
- 100+ hallucinated references found in NeurIPS 2025 accepted papers
- Universities increasingly treat fake citations as academic misconduct
- Three hallucination types: **fully fabricated**, **chimeric** (real title + wrong authors), **modified real** (slightly altered metadata)

## Usage

### Quick Check (Single File)

```bash
python scripts/citation_checker.py references.bib
```

### Check All `.bib` Files in a Directory

```bash
python scripts/citation_checker.py path/to/report/
```

### JSON Output (CI/CD Pipelines)

```bash
python scripts/citation_checker.py references.bib --json
```

### Verbose Mode (Debug API Responses)

```bash
python scripts/citation_checker.py references.bib --verbose
```

## How It Works

### Cascading Multi-Source Verification

Each citation is checked against three independent databases:

| Source | Coverage | Strength |
|--------|----------|----------|
| CrossRef | 140M+ DOI-registered works | Best for journal/conference papers with DOIs |
| Semantic Scholar | 200M+ papers | Best author disambiguation, arXiv coverage |
| OpenAlex | 240M+ works | Broadest coverage, fully open |

**Verification logic:**
- Found in 2+ sources with matching title → **verified** (high confidence)
- Found in 1 source only → **suspicious** (manual check recommended)
- All three searches completed, no match → **not_found** (not proof of fabrication)
- No matches and at least one lookup failed → **unverified** (retry or check manually); `source_errors` identifies failures even when another source matched

### Chimeric Detection

When a citation's title matches a real paper but the authors don't overlap at all, it's flagged as a possible **chimeric hallucination** — the most dangerous type because the title looks real on Google Scholar.

### Red Flag Heuristics

- Invalid DOI format (doesn't start with `10.xxxx/`)
- Suspiciously generic title patterns ("A Comprehensive Survey of...")
- Future publication year
- Missing author or year fields
- Single-word author names (incomplete metadata)

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All citations verified |
| 1 | At least one citation not found, or invalid input path |
| 2 | Suspicious citations, with no `not_found` or `unverified` |
| 3 | At least one incomplete verification, with no `not_found` |

## Dependencies

Python 3.9+ and outbound HTTPS; no third-party Python packages. On Windows, use `python` or `py -3`. The script uses public endpoints, subject to provider availability and rate limits. `--json` keeps diagnostic messages off stdout.

## Accuracy (Tested)

| Category | Result | Description |
|----------|--------|-------------|
| Known-good | 9/10 (90%) | Famous ML papers (Vaswani, Devlin, Brown, He, etc.) |
| Known-bad | 10/10 (100%) | Fabricated papers with plausible titles |
| Chimeric | 5/5 (100%) | Real titles with wrong authors |
| **False positive rate** | **10%** | 1 miss: unpublished tech report without DOI |
| **False negative rate** | **0%** | No fake paper was ever verified |

These are upstream results on a small historical sample; they do not guarantee correctness for other citations.

## Limitations

- Papers without DOI that have many derivatives (e.g., BERT without DOI) may not be found via title search alone — always include DOIs when available
- Semantic Scholar free tier rate-limits at ~100 requests/5 minutes — batch verification is slower
- Cannot verify papers behind paywalls or not indexed in any of the three databases
- Book chapters, technical reports, and grey literature have lower coverage

## Integration with LaTeX Workflows

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
python3 scripts/citation_checker.py references.bib
```

### GitHub Actions

```yaml
- name: Check citations
  run: python scripts/citation_checker.py references.bib --json > citation_report.json
```
