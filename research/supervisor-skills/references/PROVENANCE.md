# Provenance

This skill collection is adapted from **HKUSTDial/Supervisor-Skills** (Supervisor-Skills: 将博导十年科研经验，炼化为你的 AI 技能).

- Source: <https://github.com/HKUSTDial/Supervisor-Skills>
- Branch read: `main` (files as of 2026-11-20; repository last push `2026-11-05`)
- License of the source: **CC BY-NC-SA 4.0** (Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International), Copyright (c) 2026 Yuyu Luo (methodology) and contributors — <https://creativecommons.org/licenses/by-nc-sa/4.0/>
- Individual `SKILL.md` files carry their own `license` frontmatter field: 7 are `CC-BY-4.0`, 3 are `CC-BY-NC-SA-4.0`, and 2 (`drawio-reconstruction`, `rebuttal-guidance`) have no license field. `drawio-reconstruction/LICENSE` is MIT (Copyright (c) 2026 VCG-Bench Authors), inherited from the separate upstream project <https://github.com/sxy1499894281/drawio-reconstruction-skill>.

> **⚠️ License compatibility notice:** The upstream collection is **CC BY-NC-SA 4.0**, which is **NonCommercial** and **ShareAlike**. It is *not* MIT and is *not* relicensed to MIT by this repository. Only the original repository's own files are covered by its MIT license; the material under `research/supervisor-skills/` remains under its original CC BY-NC-SA 4.0 / CC-BY-4.0 / MIT terms as indicated in each file. Do not treat these skills as MIT-licensed. Any adaptation or redistribution must keep the attribution and comply with the corresponding license (in particular NonCommercial and ShareAlike where applicable).

## Files adapted

| Source in Supervisor-Skills | Local path | Notes |
|---|---|---|
| `skills/<skill>/SKILL.md` (×12) | `research/supervisor-skills/<skill>/SKILL.md` | Verbatim copies; not modified |
| `skills/<skill>/references/*` | `research/supervisor-skills/<skill>/references/*` | Verbatim copies |
| `skills/drawio-reconstruction/scripts/*`, `assets/*`, `examples/*`, `LICENSE`, `agents/openai.yaml` | same relative paths under `research/supervisor-skills/drawio-reconstruction/` | Verbatim copies, including the MIT-licensed helper scripts and case images |
| `skills/README.md`, `skills/README.en.md` | `README.md`, `README.en.md` | Verbatim upstream reader guides; **see local-additions note below** |
| — | `references/PROVENANCE.md` (this file) | Added locally |
| — | `README.zh-CN.md` | Added locally: Chinese quick-start guide adapted to this repository's layout |

All 107 files under upstream `skills/` were copied byte-for-byte; no upstream SKILL.md content was edited.

## Changes

- Added this provenance/license notice and a repository-specific Chinese guide (`README.zh-CN.md`).
- The upstream reader guides reference sibling directories (`../handbook/`, top-level `README.md`, `CONTRIBUTING.md`) that were **not** copied into this repository (only the executable `skills/` tree was collected). Their links to those directories will not resolve locally; the upstream source is linked here for readers who need the handbook.
- No skill logic, trigger conditions, generator options or reference content was changed.
