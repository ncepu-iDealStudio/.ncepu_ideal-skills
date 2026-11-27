# Verification levels

Give every lead and candidate exactly one current level. Raise it only after the step is done; lower it if a check fails.

| Level | Meaning |
|---|---|
| `DISCOVERED` | Seen in a search result or secondary reference. The source itself was not opened. |
| `OPENED` | The page, record, post, video or document was opened directly. |
| `METADATA-VERIFIED` | Identity fields were checked against an authoritative record (publisher, repository, library catalogue, platform, creator page). |
| `ABSTRACT-VERIFIED` | Metadata verified, and the source's own abstract or author summary was read. |
| `FULL-TEXT-VERIFIED` | The whole relevant source was available and the stated characterisation was checked against its text, transcript, data or official documentation. |

## Things that do not raise a level

- A search snippet is not `OPENED`.
- A publisher page without the paper text is not `FULL-TEXT-VERIFIED`.
- A video description is not a transcript.
- A README is not proof the code behaves as described.
- Text presence of a term is not semantic support.
- A citation existing beside a claim does not show it supports the claim.
- A passing script, benchmark or checksum does not show semantic validity or human benefit.

## Reporting

In the final summary give counts per level and say which findings rest on `DISCOVERED` items only. A single-level headline ("verified") is not acceptable.
