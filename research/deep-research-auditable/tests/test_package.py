import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    assert m, "no frontmatter"
    return dict(l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)


def test_skill_frontmatter_and_length():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    fm = frontmatter(text)
    assert fm["name"].strip() == "deep-research-auditable"
    assert len(fm["description"].strip()) <= 300
    assert len(text.splitlines()) <= 300


def test_prompt_sizes():
    assert len((ROOT / "PROMPT.md").read_text(encoding="utf-8")) <= 6000
    assert len((ROOT / "PROMPT.short.md").read_text(encoding="utf-8")) <= 1400


def test_agents_md_limits_and_pointers():
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert len(agents.splitlines()) <= 150
    for name in ("CLAUDE.md", "GEMINI.md"):
        assert (ROOT / name).read_text(encoding="utf-8").startswith("@AGENTS.md")
    assert "AGENTS.md" in (ROOT / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")


def test_required_files_exist():
    need = ["README.md", "LICENSE", "install.sh", "test_install.sh", "templates/AUDIT.md",
            "templates/SOURCE_STATUS.md", "templates/RUN_MANIFEST.md", "scripts/lexical_audit.py",
            "examples/toy-run/00_RUN_MANIFEST.md", ".github/workflows/ci.yml"] + [
        "references/" + n for n in ("waves.md", "schemas.md", "verification-levels.md", "profiles.md",
                                    "untrusted-web-content.md", "informal-to-academic-tracing.md",
                                    "negative-findings.md")]
    for n in need:
        assert (ROOT / n).exists(), n


def test_toy_csv_rows_fit_headers_and_are_labelled():
    res = subprocess.run([sys.executable, "-I", str(ROOT / "scripts" / "check_csv.py"),
                          str(ROOT / "examples" / "toy-run")], capture_output=True, text=True)
    assert res.returncode == 0, res.stdout
    import csv
    with open(ROOT / "examples" / "toy-run" / "04_LEADS.csv", newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 5
    assert all(r["title"].startswith("EXAMPLE") for r in rows)
    levels = {"DISCOVERED", "OPENED", "METADATA-VERIFIED", "ABSTRACT-VERIFIED", "FULL-TEXT-VERIFIED"}
    assert all(r["verification_level"] in levels for r in rows)
    assert not any(r["verification_level"] == "FULL-TEXT-VERIFIED" for r in rows)


def test_schema_headers_match_toy_csv():
    schema = (ROOT / "references" / "schemas.md").read_text(encoding="utf-8")
    header = (ROOT / "examples" / "toy-run" / "04_LEADS.csv").read_text(encoding="utf-8").splitlines()[0]
    assert header in schema


def test_check_csv_detects_bad_row(tmp_path):
    bad = tmp_path / "x.csv"
    bad.write_text("a,b,c\n1,2\n", encoding="utf-8")
    res = subprocess.run([sys.executable, "-I", str(ROOT / "scripts" / "check_csv.py"), str(bad)],
                         capture_output=True, text=True)
    assert res.returncode == 1
