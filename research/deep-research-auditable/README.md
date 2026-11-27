# deep-research-auditable

An agent skill for research you can audit: a saturation stop rule, explicit verification levels and bounded negative findings, run by many agents in parallel or by one chat in sequence.

> **本地说明（本仓库）**：本技能源自上游 [hyderhusainarastu/deep-research-skill](https://github.com/hyderhusainarastu/deep-research-skill)（MIT），因技能名 `deep-research` 与本仓库已收录的 `supervisor-skills/deep-research` 冲突，本地改名为 `deep-research-auditable`，目录同步改名，上游文件内容保持原样。完整改造记录见 [references/PROVENANCE.md](references/PROVENANCE.md)。中文导读见 [README.zh-CN.md](README.zh-CN.md)。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

For researchers, analysts and developers who ask an AI assistant for a literature or evidence review and want to know what was searched, what was actually opened, and when it stopped.

What sets it apart:

- **Saturation stop rule.** A theme is done only when eight stated conditions hold, including two independently designed query batches that find nothing new of high priority. Then the run stops.
- **Verification levels.** Every source is `DISCOVERED`, `OPENED`, `METADATA-VERIFIED`, `ABSTRACT-VERIFIED` or `FULL-TEXT-VERIFIED`, with a list of things that do not raise a level.
- **Bounded negatives.** "None found in the material searched", plus which sources, at what access level, with which strings.

## Works with

| Surface | How (prompt / native skill / CLI / hook / MCP) | Status |
|---|---|---|
| WorkBuddy | native skill: import the skill folder through the Skills UI, or place under `.workbuddy/skills/`; use `PROMPT.md` in chat | vendored here, scripts tested offline |
| Claude Code | native skill (`SKILL.md`, `install.sh --claude`) | not tested |
| Codex | native skill via `.agents/skills` (`install.sh --agents`) | not tested |
| Gemini CLI | native skill via `.agents/skills`, or pointer block | not tested |
| Cursor | native skill via `.agents/skills`; reads `AGENTS.md` | not tested |
| Copilot | pointer block to `AGENTS.md` | not tested |
| ChatGPT / Claude.ai / Gemini (chat) | prompt (`PROMPT.md`, SCOPED profile) | not tested |
| `scripts/lexical_audit.py`, `scripts/check_csv.py` | CLI, Python 3.10+ | unit tests pass (see Example) |

## Quick start

```sh
./install.sh --claude              # ~/.claude/skills/deep-research-auditable
./install.sh --agents --project .  # .agents/skills (Codex, Cursor, Gemini CLI)
./install.sh --help                # all targets, --copy, --dry-run, --uninstall
```

> 本仓库已收录，无需再次 clone；安装脚本从 `SKILL.md` 自动读取技能名 `deep-research-auditable`。

Chat tools: paste `PROMPT.md` into the conversation (or `PROMPT.short.md` into a custom-instructions field) and add your questions.

Then ask your agent: "Use the deep-research-auditable skill, SCOPED profile, output to `research/run-1/`, on: *why did the QWERTY layout become standard?*"

## Profiles

- **FULL**: parallel workers, one stream each, a controller that delegates and merges, independent verifiers and reviewers. For agent runtimes.
- **SCOPED**: one agent or one chat, sequential streams, role separation by re-opening sources in a verifier posture. For chat tools and bounded checks.

## Example

The toy run in `examples/toy-run/` is invented; every row is labelled as an example. Check its CSV and run the corpus tool on a small text folder:

```
$ python3 scripts/check_csv.py examples/toy-run
1 file(s) checked, 0 problem(s)

$ python3 scripts/lexical_audit.py corpus/ --config stems.json --out hits.csv
files searched: 3; matching lines: 3 (stem matches, not validated counts)
```

The second output is from the synthetic three-file corpus built in `tests/test_lexical_audit.py`.

## What it writes

A numbered folder: run manifest, baseline, search protocol, query log, leads, candidates, claim-evidence trace, synthesis, nearest neighbours, objections, acquisition queue, source status, coverage and an executive summary, plus `reviews/`. Layout in `references/waves.md`, CSV headers in `references/schemas.md`, blank templates in `templates/`.

## How it differs

- Deep-research features in chat products and agent frameworks (for example LangChain's open deep research, GPT-Researcher) focus on producing a report. This skill focuses on the audit trail: levels, query logs, role separation, a stop rule and bounded negatives. It does not search by itself; it is instructions for an agent that can.
- Citation checkers verify references after the fact. This skill covers the whole pass and expects a checker to be used on the output.
- The corpus script is a plain keyword-stem finder, not an NLP pipeline.

## Limits

- It cannot make an assistant browse. Without search or file access it can only structure what you paste in, and says so.
- The levels and the stop rule are discipline, not guarantees; a model can still misjudge them. The adversarial wave exists to catch that.
- Saturation means two query batches found nothing new in the sources reachable, not that nothing exists.
- No benchmark is claimed. Nothing here was measured against other tools.
- `lexical_audit.py` stems are prefix matches on accent-folded words; no lemmatisation, no validated counts.
- Platform rows above are "not tested" until someone records a dated run.

## Related

- multi-agent-orchestration-playbook (running the FULL profile with many workers)
- gated-research-pipeline (stage gates around a research flow)
- source-intake-pipeline (bringing acquired sources into a library)
- hallucinated-citation-checker (verify references in the output)

## Keywords

deep research, research agent, literature review, fact checking, verification levels, saturation, negative findings, agent skill, SKILL.md, AGENTS.md, multi-agent.

---
Part of palimnote-skills - more at https://github.com/hyderhusainarastu
