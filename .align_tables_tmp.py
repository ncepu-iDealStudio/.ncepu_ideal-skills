"""把 Markdown 文档中的表格统一为 aligned 风格（所有管道符列对齐）。"""
import re
import sys

PATH = r"e:/Open_source_project/ncepu_ideal-skills/docs/CodeBuddy中使用skill配置.md"

SEP_RE = re.compile(r"^:?-{3,}:?$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def split_row(line):
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return None
    inner = s[1:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", inner)]


def main():
    with open(PATH, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    out = []
    in_fence = False
    i = 0
    touched = 0
    while i < len(lines):
        line = lines[i]
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue

        is_table = False
        if not in_fence and i + 1 < len(lines):
            cur, nxt = lines[i].strip(), lines[i + 1].strip()
            if cur.startswith("|") and cur.endswith("|") and nxt.startswith("|") and nxt.endswith("|"):
                cells = re.split(r"(?<!\\)\|", nxt[1:-1])
                if cells and all(SEP_RE.match(c.strip()) for c in cells):
                    is_table = True

        if not is_table:
            out.append(line)
            i += 1
            continue

        # 收集整个表格
        block = []
        j = i
        while j < len(lines) and lines[j].strip().startswith("|"):
            block.append(lines[j])
            j += 1

        rows = [split_row(b) for b in block]
        ncol = len(rows[0])
        for idx, r in enumerate(rows):
            if len(r) != ncol:
                sys.exit("列数不一致：块起始行 %d，第 %d 行有 %d 列" % (i + 1, idx + 1, len(r)))

        widths = [0] * ncol
        for ridx, r in enumerate(rows):
            for c in range(ncol):
                if ridx == 1 and SEP_RE.match(r[c]):
                    continue
                widths[c] = max(widths[c], len(r[c]))

        for ridx, r in enumerate(rows):
            if ridx == 1:
                out.append("| " + " | ".join("-" * widths[c] for c in range(ncol)) + " |")
            else:
                out.append("| " + " | ".join(r[c].ljust(widths[c]) for c in range(ncol)) + " |")

        touched += 1
        i = j

    with open(PATH, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))

    print("已对齐表格块数：%d" % touched)


if __name__ == "__main__":
    main()
