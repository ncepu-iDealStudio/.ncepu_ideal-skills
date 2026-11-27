# CSV schemas

UTF-8, RFC 4180 quoting, one header row, stable IDs that are never reused after a merge. Count the fields of every row against the header before reporting completion (`scripts/check_csv.py` does this offline).

## 03_QUERY_LOG.csv

```
query_id,stream,source_class,platform,query_language,query_text,filters,searched_at_utc,result_count_observed,result_depth_reviewed,access_status,new_lead_count,notes
```

## 04_LEADS.csv

```
lead_id,title,creator,date,platform,source_type,url,locator,found_by_query_ids,accessed_at_utc,verification_level,evidence_role,theme,relevance,idea_paraphrase,short_excerpt,excerpt_locator,trace_status,duplicate_status,baseline_match,priority,limitations,stream
```

`priority`: `P0` possible novelty threat or validity-changing evidence; `P1` likely to improve framing, evidence or method; `P2` useful context; `P3` peripheral, kept for transparency.

## 05_CANDIDATES.csv

```
candidate_id,title,authors,year,venue,source_type,identifier,canonical_url,open_access_url,version,review_status,status_evidence_url,verification_level,full_text_access,from_lead_ids,found_by_query_ids,theme,contribution_paraphrase,methods,findings_paraphrase,qualifiers,neighbor_relation,novelty_risk,duplicate_status,baseline_match,recommended_action,limitations,metadata_verifier,relevance_verifier
```

## 06_CLAIM_EVIDENCE.csv

```
trace_id,lead_id,candidate_id,relationship,direction,method,verification_level,rationale,limitations,verified_by
```

`relationship`: `ORIGINATES`, `POPULARIZES`, `APPLIES`, `CITES`, `SUPPORTS`, `QUALIFIES`, `CONTRADICTS`, `OPERATIONALIZES`, `REVIEWS`, `REPLICATES`, `RELATED-VOCABULARY`.

## 10_ACQUISITION_QUEUE.csv

```
candidate_id,priority,access_now,lawful_primary_url,lawful_fallback_url,access_basis,reason,verification_still_needed,status
```

Every row is a recommendation. `status` is `PROPOSED-NOT-AUTHORIZED` until the user approves.

## Allowed values

- `verification_level`: see `verification-levels.md`.
- `evidence_role`: `LEAD`, `PRIMARY-RECORD`, `SCHOLARLY-SUPPORT`, `SCHOLARLY-QUALIFICATION`, `SCHOLARLY-CONTRADICTION`, `NEAREST-NEIGHBOR`, `METHOD`, `CONTEXT`.
- `duplicate_status`: `NEW`, `EXACT-DUPLICATE`, `WORK-DUPLICATE`, `VERSION-SIBLING`, `POSSIBLE-MATCH`, `ALREADY-HELD`.
- `access_status`: `OPEN`, `PAYWALLED`, `LOGIN-REQUIRED`, `BLOCKED`, `ERROR`, `NOT-ATTEMPTED`.
