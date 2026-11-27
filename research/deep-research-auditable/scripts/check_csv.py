#!/usr/bin/env python3
"""Check that every CSV row has as many fields as its header.

Usage: check_csv.py FILE_OR_DIR [...]
Exit codes: 0 all rows fit, 1 a row does not, 2 usage error.
"""
import csv
import sys
from pathlib import Path


def check(path):
    problems = []
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    if not rows:
        return ["%s: empty file" % path]
    width = len(rows[0])
    for i, row in enumerate(rows[1:], 2):
        if len(row) != width:
            problems.append("%s:%d: %d fields, header has %d" % (path, i, len(row), width))
    return problems


def main(argv):
    if not argv:
        print(__doc__, file=sys.stderr)
        return 2
    files = []
    for a in argv:
        p = Path(a)
        files += sorted(p.rglob("*.csv")) if p.is_dir() else [p]
    problems = [m for f in files for m in check(f)]
    for m in problems:
        print(m)
    print("%d file(s) checked, %d problem(s)" % (len(files), len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
