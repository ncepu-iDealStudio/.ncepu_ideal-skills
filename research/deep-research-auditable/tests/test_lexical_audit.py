import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import lexical_audit as la  # noqa: E402

SCRIPT = ROOT / "scripts" / "lexical_audit.py"


def make_corpus(tmp_path):
    c = tmp_path / "corpus"
    c.mkdir()
    (c / "a.txt").write_text(
        "1.1\tThe River floods the plain in spring\n"
        "1.2\tNothing relevant here\n"
        "\n", encoding="utf-8")
    (c / "b.txt").write_text(
        "Café owners trade grain by the river\nA flooded valley, a tradesman\n",
        encoding="utf-8")
    (c / "c.txt").write_text("empty of themes\n", encoding="utf-8")
    cfg = tmp_path / "stems.json"
    cfg.write_text(json.dumps({"fields": {"water": ["river", "flood"], "commerce": ["trad", "grain"]},
                               "min_fields": 1}), encoding="utf-8")
    return c, cfg


def test_normalize_folds_accents_case_and_final_sigma():
    assert la.normalize("Café") == "cafe"
    assert la.normalize("λόγος") == "λογοσ"


def test_audit_finds_expected_lines(tmp_path):
    corpus, cfg = make_corpus(tmp_path)
    fields, mn = la.load_config(cfg)
    rows, n = la.audit(corpus, fields, mn)
    assert n == 3
    refs = [(r["file"], r["ref"]) for r in rows]
    assert ("a.txt", "1.1") in refs
    assert ("a.txt", "1.2") not in refs
    assert ("b.txt", "b.txt:1") in refs and ("b.txt", "b.txt:2") in refs
    assert not any(r["file"] == "c.txt" for r in rows)


def test_min_fields_two(tmp_path):
    corpus, cfg = make_corpus(tmp_path)
    fields, _ = la.load_config(cfg)
    rows, _ = la.audit(corpus, fields, 2)
    assert [(r["file"], r["ref"]) for r in rows] == [("b.txt", "b.txt:1"), ("b.txt", "b.txt:2")]
    assert rows[0]["fields_matched"] == "commerce;water"


def test_cli_writes_csv(tmp_path):
    corpus, cfg = make_corpus(tmp_path)
    out = tmp_path / "hits.csv"
    res = subprocess.run([sys.executable, "-I", str(SCRIPT), str(corpus), "--config", str(cfg),
                          "--out", str(out)], capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
    assert "not validated counts" in res.stdout
    with open(out, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 3
    assert list(rows[0]) == la.FIELDS


def test_cli_bad_inputs_exit_2(tmp_path):
    corpus, cfg = make_corpus(tmp_path)
    r1 = subprocess.run([sys.executable, "-I", str(SCRIPT), str(tmp_path / "nope"), "--config",
                         str(cfg), "--out", str(tmp_path / "o.csv")], capture_output=True, text=True)
    assert r1.returncode == 2
    bad = tmp_path / "bad.json"
    bad.write_text("{}", encoding="utf-8")
    r2 = subprocess.run([sys.executable, "-I", str(SCRIPT), str(corpus), "--config", str(bad),
                         "--out", str(tmp_path / "o.csv")], capture_output=True, text=True)
    assert r2.returncode == 2
