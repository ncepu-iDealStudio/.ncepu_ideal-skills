# Output Language Protocol

## Language Detection

Use the user's explicit language request first, including different languages for different deliverables. Otherwise follow the current task request rather than the language of attached or quoted sources. If the task has no clear language, use an existing project language preference if specified, otherwise English. No host-specific file is required. Deliver both languages only when requested.

## What to Localize

- Section headings and labels
- Descriptions, analysis, commentary, recommendations
- Template boilerplate text
- Status messages and warnings

## What NOT to Localize

- Code, shell commands, file paths, directory names
- Paper titles, author names, venue names, BibTeX entries
- Technical terms with no standard Chinese translation (keep English, optionally annotate: "attention mechanism (注意力机制)")
- LaTeX commands, labels, and keys; natural-language manuscript prose follows the requested language or venue requirements
- JSON state files — keys and structure remain English
- **Machine-parsed markers** — never localize the following, regardless of language setting:
  - Markdown frontmatter keys (e.g., `outcome:`, `node_id:`, `title:`, `type:`)
  - Research Wiki schema fields parsed by `tools/research_wiki.py` (e.g., `outcome: negative`, `outcome: positive`, `node_id:`)
  - `MANIFEST.md` column headers and table structure
  - Any field that downstream tools or scripts read programmatically

## Skill-Specific Rules

| Skill | Language Support | Notes |
|-------|-----------------|-------|
| /idea-creator | Full | IDEA_REPORT.md follows language setting |
| /idea-discovery | Full | Inherits from sub-skills |
| /analyze-results | Full | Result analysis follows language setting |
| /auto-review-loop | Partial | AUTO_REVIEW.md follows setting; reviewer prompts stay English |
| /experiment-plan | Full | EXPERIMENT_PLAN.md follows setting |
| /experiment-bridge | Full | EXPERIMENT_RESULTS.md follows setting |
| /research-refine | Full | FINAL_PROPOSAL.md follows setting |
| /research-refine-pipeline | Full | PIPELINE_SUMMARY.md follows setting |
| /research-pipeline | Full | Inherits from sub-skills |
| /result-to-claim | Full | Claim descriptions follow setting |
| Manuscript drafting | Full | Explicit language → venue requirements → existing draft language → English for a new draft |
