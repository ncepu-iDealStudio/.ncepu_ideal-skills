#!/usr/bin/env python3
"""Keyword-stem audit over a local text corpus.

A reproducible finding aid. Stem matches are string-prefix matches on
accent-folded, lower-cased words. They are not lemmatisation, not a validated
count and not evidence that one text depends on another.

Config (JSON):
  {"fields": {"theme_a": ["stem1", "stem2"], "theme_b": ["stem3"]},
   "min_fields": 1}

Corpus: a directory of .txt files. A line may be "ref<TAB>text"; otherwise the
reference is "<file>:<line number>".

Usage:
  lexical_audit.py CORPUS_DIR --config stems.json --out hits.csv [--pattern '*.txt']
Exit codes: 0 success, 2 usage or input error.
"""
import argparse
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

WORD = re.compile(r"\w+", re.UNICODE)
FIELDS = ["file", "ref", "fields_matched", "stems_matched", "text"]


def normalize(text):
    """Lower-case, strip combining marks, fold final sigma."""
    folded = unicodedata.normalize("NFD", text.lower())
    folded = "".join(c for c in folded if not unicodedata.combining(c))
    return folded.replace("ς", "σ")


def load_config(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    fields = data.get("fields")
    if not isinstance(fields, dict) or not fields:
        raise ValueError("config needs a non-empty 'fields' object")
    clean = {}
    for name, stems in fields.items():
        if not isinstance(stems, list) or not stems:
            raise ValueError("field %r needs a non-empty list of stems" % name)
        clean[name] = sorted({normalize(str(s)) for s in stems if str(s).strip()})
    return clean, int(data.get("min_fields", 1))


def split_line(file_name, number, line):
    if "\t" in line:
        ref, text = line.split("\t", 1)
        return ref.strip(), text
    return "%s:%d" % (file_name, number), line


def match_line(text, fields):
    words = WORD.findall(normalize(text))
    hits = {}
    for name, stems in fields.items():
        found = sorted({s for s in stems if any(w.startswith(s) for w in words)})
        if found:
            hits[name] = found
    return hits


def audit(corpus, fields, min_fields=1, pattern="*.txt"):
    rows = []
    files = sorted(Path(corpus).rglob(pattern))
    for path in files:
        rel = path.relative_to(corpus).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for number, line in enumerate(text.splitlines(), 1):
            if not line.strip():
                continue
            ref, body = split_line(rel, number, line)
            hits = match_line(body, fields)
            if len(hits) >= min_fields:
                rows.append({
                    "file": rel,
                    "ref": ref,
                    "fields_matched": ";".join(sorted(hits)),
                    "stems_matched": ";".join(s for k in sorted(hits) for s in hits[k]),
                    "text": body.strip(),
                })
    return rows, len(files)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("corpus", help="directory of text files")
    ap.add_argument("--config", required=True, help="JSON file with fields and stems")
    ap.add_argument("--out", required=True, help="CSV output path")
    ap.add_argument("--pattern", default="*.txt", help="file glob (default *.txt)")
    ap.add_argument("--min-fields", type=int, help="override config min_fields")
    args = ap.parse_args(argv)
    corpus = Path(args.corpus)
    if not corpus.is_dir():
        print("error: corpus is not a directory: %s" % corpus, file=sys.stderr)
        return 2
    try:
        fields, min_fields = load_config(args.config)
    except (OSError, ValueError) as exc:
        print("error: bad config: %s" % exc, file=sys.stderr)
        return 2
    if args.min_fields is not None:
        min_fields = args.min_fields
    rows, n_files = audit(corpus, fields, min_fields, args.pattern)
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print("files searched: %d; matching lines: %d (stem matches, not validated counts)"
          % (n_files, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
