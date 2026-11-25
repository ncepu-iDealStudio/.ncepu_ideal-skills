#!/usr/bin/env python3
"""
Citation Checker — Multi-Source Verification for Academic Reports.

Prevents AI-hallucinated citations from reaching submission.
Uses a cascading verification pipeline: CrossRef → Semantic Scholar → OpenAlex.

Background:
- 6-55% of AI-generated citations are fabricated (varies by model/domain)
- 100+ hallucinated refs found in NeurIPS 2025 accepted papers
- Universities increasingly treat fake citations as academic misconduct
- Three hallucination types: fully fabricated, chimeric (blended), modified real

Usage:
    # Check a single .bib file
    python citation_checker.py references.bib

    # Check all .bib files in a directory
    python citation_checker.py path/to/report/

    # Output as JSON (for CI pipelines)
    python citation_checker.py references.bib --json

    # Verbose mode (show API responses)
    python citation_checker.py references.bib --verbose

Requires Python 3.9+ (standard library only) and access to the public API endpoints.
"""

import re
import sys
import json
import time
import urllib.parse
from http.client import HTTPException
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class BibEntry:
    key: str
    entry_type: str
    title: str
    authors: str
    year: str
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    raw: str = ""
    line_number: int = 0
    file_path: str = ""


@dataclass
class VerificationResult:
    entry: BibEntry
    status: str  # "verified", "suspicious", "not_found", "unverified"
    confidence: float  # 0.0 - 1.0
    sources_checked: list[str] = field(default_factory=list)
    sources_found: list[str] = field(default_factory=list)
    best_match_title: Optional[str] = None
    best_match_similarity: float = 0.0
    notes: list[str] = field(default_factory=list)
    red_flags: list[str] = field(default_factory=list)
    source_errors: dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# BibTeX Parser
# ---------------------------------------------------------------------------

def parse_bib_file(filepath: Path) -> list[BibEntry]:
    """Parse a .bib file and extract entries."""
    entries = []
    content = filepath.read_text(encoding="utf-8", errors="replace")
    # Match @type{key, ... }
    entry_pattern = re.compile(
        r"@(\w+)\{([^,\s]+)\s*,(.+?)\n\}",
        re.DOTALL,
    )

    for match in entry_pattern.finditer(content):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        body = match.group(3)
        line_number = content[: match.start()].count("\n") + 1

        # Skip @comment, @string, @preamble
        if entry_type in ("comment", "string", "preamble"):
            continue

        title = _extract_field(body, "title")
        authors = _extract_field(body, "author")
        year = _extract_field(body, "year")
        doi = _extract_field(body, "doi")
        arxiv_id = _extract_field(body, "eprint") or _extract_field(
            body, "arxiv"
        )

        if not title:
            continue  # Can't verify without title

        entries.append(
            BibEntry(
                key=key,
                entry_type=entry_type,
                title=_clean_latex(title),
                authors=_clean_latex(authors) if authors else "",
                year=year or "",
                doi=doi,
                arxiv_id=arxiv_id,
                raw=match.group(0),
                line_number=line_number,
                file_path=str(filepath),
            )
        )

    return entries


def _extract_field(body: str, field_name: str) -> Optional[str]:
    """Extract a field value from BibTeX body."""
    pattern = re.compile(
        rf"{field_name}\s*=\s*[\{{\"](.+?)[\}}\"]",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(body)
    if match:
        value = match.group(1).strip()
        # Handle nested braces
        value = re.sub(r"\{([^}]*)\}", r"\1", value)
        return value
    return None


def _clean_latex(text: str) -> str:
    """Remove LaTeX commands from text."""
    text = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", text)
    text = re.sub(r"[{}]", "", text)
    text = re.sub(r"\\.", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------------------------------------------------------
# Similarity
# ---------------------------------------------------------------------------

def title_similarity(a: str, b: str) -> float:
    """Compute normalized token-overlap similarity between two titles."""
    if not a or not b:
        return 0.0
    tokens_a = set(a.lower().split())
    tokens_b = set(b.lower().split())
    # Remove common stop words
    stop = {"the", "a", "an", "of", "for", "in", "on", "to", "and", "with", "by", "from", "is", "are", "at"}
    tokens_a -= stop
    tokens_b -= stop
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union)


def author_overlap(entry_authors: str, found_authors: str) -> float:
    """Check if author last names overlap between BibTeX entry and API result."""
    if not entry_authors or not found_authors:
        return 0.0

    def extract_last_names(text: str) -> set[str]:
        lower = text.lower().strip()
        names = set()

        if re.search(r"\band\b", lower):
            # BibTeX format: "Last, First and Last, First"
            people = re.split(r"\band\b", lower)
            for person in people:
                person = person.strip()
                if not person:
                    continue
                if "," in person:
                    # "Last, First" → take before comma
                    last = person.split(",")[0].strip().split()[-1]
                    names.add(last)
                else:
                    # "First Last" → take last word
                    words = person.split()
                    if words:
                        names.add(words[-1])
        else:
            # API format: "First Last, First Last" (comma-separated)
            people = lower.split(",")
            for person in people:
                person = person.strip()
                if not person:
                    continue
                words = person.split()
                if len(words) >= 2:
                    names.add(words[-1])
                elif words:
                    names.add(words[0])

        return names

    entry_names = extract_last_names(entry_authors)
    found_names = extract_last_names(found_authors)

    if not entry_names or not found_names:
        return 0.0

    overlap = entry_names & found_names
    return len(overlap) / max(len(entry_names), 1)


# ---------------------------------------------------------------------------
# API Clients (Cascading: CrossRef → Semantic Scholar → OpenAlex)
# ---------------------------------------------------------------------------

HEADERS = {
    "User-Agent": "citation-checker/1.0 (academic-report-verification)"
}


def fetch_json(url: str, timeout: int, retry_429: bool = False) -> dict:
    request = Request(url, headers={**HEADERS, "Accept": "application/json"})
    while True:
        try:
            with urlopen(request, timeout=timeout) as response:
                data = json.load(response)
            if not isinstance(data, dict):
                raise ValueError("Expected a JSON object")
            return data
        except HTTPError as exc:
            exc.close()
            if exc.code != 429 or not retry_429:
                raise
            retry_429 = False
            time.sleep(5)


def title_candidates(title: str) -> list[str]:
    _, _, subtitle = title.partition(":")
    return [title, subtitle.strip()] if len(subtitle.split()) >= 4 else [title]


def crossref_match(data: dict, similarity: float = 1.0, doi: str = "") -> dict:
    return {
        "title": (data.get("title") or [""])[0],
        "authors": ", ".join(f"{a.get('given', '')} {a.get('family', '')}" for a in data.get("author", [])),
        "doi": doi or data.get("DOI", ""),
        "year": str(data.get("published-print", data.get("published-online", {})).get("date-parts", [[""]])[0][0]),
        "similarity": similarity,
    }


def check_crossref(entry: BibEntry) -> Optional[dict]:
    if entry.doi:
        doi = urllib.parse.quote(entry.doi, safe="/")
        try:
            data = fetch_json(f"https://api.crossref.org/works/{doi}", timeout=10)
        except HTTPError as exc:
            if exc.code != 404:
                raise
        else:
            return crossref_match(data["message"], doi=entry.doi)

    for title in title_candidates(entry.title):
        query = urllib.parse.urlencode({"query.title": title, "rows": 5})
        data = fetch_json(f"https://api.crossref.org/works?{query}", timeout=15)
        for item in data["message"]["items"]:
            similarity = title_similarity(entry.title, (item.get("title") or [""])[0])
            if similarity > 0.6:
                return crossref_match(item, similarity)
    return None


def check_semantic_scholar(entry: BibEntry) -> Optional[dict]:
    query = urllib.parse.urlencode({"query": entry.title, "limit": 3, "fields": "title,authors,year,externalIds"})
    data = fetch_json(f"https://api.semanticscholar.org/graph/v1/paper/search?{query}", timeout=15, retry_429=True)
    for paper in [] if data.get("total") == 0 else data["data"]:
        title = paper.get("title", "")
        similarity = title_similarity(entry.title, title)
        if similarity > 0.6:
            ids = paper.get("externalIds") or {}
            return {
                "title": title,
                "authors": ", ".join(a.get("name", "") for a in paper.get("authors", [])),
                "doi": ids.get("DOI", ""),
                "arxiv": ids.get("ArXiv", ""),
                "year": str(paper.get("year", "")),
                "similarity": similarity,
            }
    return None


def check_openalex(entry: BibEntry) -> Optional[dict]:
    for title in title_candidates(entry.title):
        query = urllib.parse.urlencode({"filter": f"title.search:{title}", "per_page": 5})
        data = fetch_json(f"https://api.openalex.org/works?{query}", timeout=15)
        for work in data["results"]:
            found_title = work.get("title", "")
            similarity = title_similarity(entry.title, found_title)
            if similarity > 0.6:
                return {
                    "title": found_title,
                    "authors": ", ".join(a.get("author", {}).get("display_name", "") for a in work.get("authorships", [])),
                    "doi": (work.get("doi") or "").replace("https://doi.org/", ""),
                    "year": str(work.get("publication_year", "")),
                    "similarity": similarity,
                }
    return None


# ---------------------------------------------------------------------------
# Red Flag Detection
# ---------------------------------------------------------------------------

def detect_red_flags(entry: BibEntry) -> list[str]:
    """Detect markers that suggest a citation may be AI-hallucinated."""
    flags = []

    # 1. DOI format check
    if entry.doi:
        if not re.match(r"10\.\d{4,}/", entry.doi):
            flags.append(f"Invalid DOI format: '{entry.doi}'")

    # 2. Suspiciously generic title
    generic_patterns = [
        r"^a (?:comprehensive |novel |survey)",
        r"^towards ",
        r"(?:comprehensive|systematic) (?:survey|review|study|analysis)",
    ]
    for pattern in generic_patterns:
        if re.search(pattern, entry.title.lower()):
            flags.append(
                "Title matches common AI-hallucination pattern (overly generic)"
            )
            break

    # 3. Missing key fields
    if not entry.authors:
        flags.append("Missing author field")
    if not entry.year:
        flags.append("Missing year field")

    # 4. Future year
    if entry.year and entry.year.isdigit():
        if int(entry.year) > 2026:
            flags.append(f"Future year: {entry.year}")

    # 5. Author name patterns — split by "and" (BibTeX convention), not comma
    if entry.authors:
        author_parts = re.split(r"\band\b", entry.authors)
        for part in author_parts:
            stripped = part.strip().strip(",").strip()
            if stripped and len(stripped.split()) == 1 and len(stripped) > 2:
                flags.append(
                    f"Single-word author name: '{stripped}' (may be incomplete)"
                )

    return flags


# ---------------------------------------------------------------------------
# Verification Engine
# ---------------------------------------------------------------------------

def verify_entry(entry: BibEntry, verbose: bool = False) -> VerificationResult:
    """Verify a single BibTeX entry using cascading multi-source lookup."""
    result = VerificationResult(entry=entry, status="not_found", confidence=0.0)
    result.red_flags = detect_red_flags(entry)

    # Cascade: CrossRef → Semantic Scholar → OpenAlex
    checkers = [
        ("CrossRef", check_crossref),
        ("Semantic Scholar", check_semantic_scholar),
        ("OpenAlex", check_openalex),
    ]

    matches = []

    for source_name, checker in checkers:
        result.sources_checked.append(source_name)
        if verbose:
            print(f"  Checking {source_name} for '{entry.key}'...", file=sys.stderr)

        try:
            match = checker(entry)
        except (OSError, HTTPException, ValueError, KeyError, TypeError, AttributeError, IndexError) as exc:
            reason = f"HTTP {exc.code}" if isinstance(exc, HTTPError) else type(exc).__name__
            result.source_errors[source_name] = reason
            if verbose:
                print(f"  {source_name} lookup failed: {reason}", file=sys.stderr)
            match = None

        if match:
            result.sources_found.append(source_name)
            matches.append(match)

            # Store best match
            sim = match.get("similarity", 1.0)
            if sim > result.best_match_similarity:
                result.best_match_similarity = sim
                result.best_match_title = match.get("title", "")

        # Rate limiting between APIs (Semantic Scholar needs ~1s between requests)
        time.sleep(1.0)

    # Compute confidence
    if len(result.sources_found) >= 2:
        result.status = "verified"
        result.confidence = min(0.95, 0.5 + 0.2 * len(result.sources_found))

        # Boost confidence if title similarity is high
        if result.best_match_similarity > 0.85:
            result.confidence = min(1.0, result.confidence + 0.1)

        # Check author overlap for best match
        if matches:
            best = max(matches, key=lambda m: m.get("similarity", 0))
            ao = author_overlap(entry.authors, best.get("authors", ""))
            if ao > 0.3:
                result.confidence = min(1.0, result.confidence + 0.1)
                result.notes.append(f"Author overlap: {ao:.0%}")
            elif ao == 0 and entry.authors:
                # Zero author overlap = likely chimeric (real title, wrong authors)
                result.notes.append("WARNING: No author overlap with best match")
                result.confidence -= 0.3
                result.red_flags.append(
                    "Title matches but authors don't — possible chimeric hallucination"
                )
                result.status = "suspicious"

    elif len(result.sources_found) == 1:
        result.status = "suspicious"
        result.confidence = 0.4 + (result.best_match_similarity * 0.2)
        result.notes.append("Found in only 1 source — verify manually")

    elif result.source_errors:
        result.status = "unverified"
        result.notes.append("Lookup incomplete — retry unavailable sources or verify manually")
    else:
        result.notes.append("No match in the queried databases — verify manually")

    # Red flags reduce confidence
    if result.red_flags:
        result.confidence = max(0.0, result.confidence - 0.1 * len(result.red_flags))

    return result


def verify_all(
    entries: list[BibEntry], verbose: bool = False, *, progress: bool = True
) -> list[VerificationResult]:
    """Verify all entries with progress reporting."""
    results = []
    total = len(entries)

    for i, entry in enumerate(entries, 1):
        if progress and not verbose:
            print(f"  [{i}/{total}] Checking: {entry.key}", end="", flush=True)

        result = verify_entry(entry, verbose=verbose)

        if progress and not verbose:
            status_icon = {
                "verified": " ✓",
                "suspicious": " ?",
                "not_found": " ✗",
                "unverified": " !",
            }
            print(status_icon.get(result.status, " ?"))

        results.append(result)

        # Rate limiting between entries
        time.sleep(1.0)

    return results


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_report(results: list[VerificationResult]) -> None:
    """Print formatted verification report."""
    verified = [r for r in results if r.status == "verified"]
    suspicious = [r for r in results if r.status == "suspicious"]
    not_found = [r for r in results if r.status == "not_found"]
    unverified = [r for r in results if r.status == "unverified"]
    with_flags = [r for r in results if r.red_flags]

    print("\n" + "=" * 65)
    print("  CITATION VERIFICATION REPORT")
    print("=" * 65)

    print(f"\n  Total citations: {len(results)}")
    print(f"  Verified (2+ sources): {len(verified)}")
    print(f"  Suspicious:            {len(suspicious)}")
    print(f"  NOT FOUND (0 sources):  {len(not_found)}")
    print(f"  UNVERIFIED:            {len(unverified)}")

    for r in results:
        if r.source_errors:
            errors = ", ".join(f"{name}: {reason}" for name, reason in r.source_errors.items())
            print(f"    [{r.entry.key}] Source failures: {errors}")
    print(f"  With red flags:         {len(with_flags)}")

    if not_found:
        print(f"\n  {'='*60}")
        print("  CITATIONS NOT FOUND — VERIFY MANUALLY")
        print(f"  {'='*60}")
        for r in not_found:
            print(f"\n  [{r.entry.key}] {r.entry.file_path}:{r.entry.line_number}")
            print(f"    Title:   {r.entry.title}")
            print(f"    Authors: {r.entry.authors}")
            print(f"    Year:    {r.entry.year}")
            if r.red_flags:
                for flag in r.red_flags:
                    print(f"    FLAG: {flag}")

    if suspicious:
        print(f"\n  {'-'*60}")
        print("  SUSPICIOUS — VERIFY MATCHES MANUALLY")
        print(f"  {'-'*60}")
        for r in suspicious:
            print(f"\n  [{r.entry.key}] confidence={r.confidence:.0%}")
            print(f"    Title:      {r.entry.title}")
            print(f"    Best match: {r.best_match_title}")
            print(f"    Similarity: {r.best_match_similarity:.0%}")
            print(f"    Found in:   {', '.join(r.sources_found)}")
            for note in r.notes:
                print(f"    Note: {note}")
            if r.red_flags:
                for flag in r.red_flags:
                    print(f"    FLAG: {flag}")

    if with_flags and not not_found and not suspicious:
        print(f"\n  {'-'*60}")
        print("  RED FLAGS ON VERIFIED CITATIONS")
        print(f"  {'-'*60}")
        for r in with_flags:
            if r.status == "verified":
                print(f"\n  [{r.entry.key}]")
                for flag in r.red_flags:
                    print(f"    FLAG: {flag}")

    # Summary
    print("\n" + "=" * 65)
    if not_found:
        print(
            f"  RESULT: {len(not_found)} UNFOUND CITATION(S) — "
            "verify manually before submission"
        )
    if unverified:
        print(f"  RESULT: {len(unverified)} UNVERIFIED — retry unavailable sources or check manually")
    if suspicious:
        print(
            f"  RESULT: {len(suspicious)} SUSPICIOUS — "
            "manually verify these citations"
        )
    if not (not_found or suspicious or unverified):
        print("  RESULT: All citations verified in 2+ sources")
    print("=" * 65 + "\n")


def json_report(results: list[VerificationResult]) -> str:
    """Generate JSON report."""
    output = {
        "summary": {
            "total": len(results),
            "verified": sum(1 for r in results if r.status == "verified"),
            "suspicious": sum(1 for r in results if r.status == "suspicious"),
            "not_found": sum(1 for r in results if r.status == "not_found"),
            "unverified": sum(1 for r in results if r.status == "unverified"),
        },
        "citations": [],
    }
    for r in results:
        output["citations"].append(
            {
                "key": r.entry.key,
                "title": r.entry.title,
                "status": r.status,
                "confidence": round(r.confidence, 2),
                "sources_found": r.sources_found,
                "source_errors": r.source_errors,
                "best_match_title": r.best_match_title,
                "best_match_similarity": round(r.best_match_similarity, 2),
                "red_flags": r.red_flags,
                "notes": r.notes,
            }
        )
    return json.dumps(output, indent=2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Verify academic citations against CrossRef, Semantic Scholar, and OpenAlex"
    )
    parser.add_argument(
        "path", help="Path to .bib file or directory containing .bib files"
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    target = Path(args.path)
    bib_files = []
    if target.is_file() and target.suffix == ".bib":
        bib_files = [target]
    elif target.is_dir():
        bib_files = sorted(target.rglob("*.bib"))
    else:
        print(f"Error: {target} is not a .bib file or directory", file=sys.stderr)
        sys.exit(1)

    if not bib_files:
        print(f"No .bib files found in {target}", file=sys.stderr)
        sys.exit(1)

    # Parse all entries
    all_entries = []
    for bib_file in bib_files:
        entries = parse_bib_file(bib_file)
        all_entries.extend(entries)
        if not args.json:
            print(f"Parsed {len(entries)} entries from {bib_file}")

    if not all_entries:
        print(json_report([]) if args.json else "No BibTeX entries found")
        sys.exit(0)

    if not args.json:
        print(f"\nVerifying {len(all_entries)} citations across 3 databases...\n")

    # Verify
    results = verify_all(all_entries, verbose=args.verbose, progress=not args.json)

    # Report
    if args.json:
        print(json_report(results))
    else:
        print_report(results)

    statuses = {r.status for r in results}
    for status, code in (("not_found", 1), ("unverified", 3), ("suspicious", 2)):
        if status in statuses:
            sys.exit(code)
    sys.exit(0)


if __name__ == "__main__":
    main()
