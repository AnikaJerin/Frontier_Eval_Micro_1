# Real-world collection audit — 5 November 2026

## Inventory and provenance

The original `raw/attributed_reports.jsonl` is copied byte for byte, SHA-256 `0d7219c2750ce1694fe9d59dbc1a0f799dd10eb95f91b0dd9462e6026e25863f`. It contains 156 JSON objects: 40 SYNOP, 101 METAR, 15 TAF. There are 156 distinct raw strings and record IDs; every supplied raw SHA-256 matches. All nine metadata keys exist on every record, but `original_source_url` is null on all 156. The participant identifies Ogimet for SYNOP and Aviation Weather Center (https://aviationweather.gov/data/metar) for METAR/TAF. These are collection-level assertions, not verified report-specific permalinks; none were invented or inserted into original data. Source authenticity, aviation report year/month, completeness, and precise reuse rights are not independently established. The participant previously stated they have redistribution permission for a real SYNOP report; the scope for all 40 is not documented. Resolve permission for every included record before public distribution.

Timestamps for all 40 SYNOP records include year/month/day/time; all 116 METAR and TAF timestamps contain only day/hour/minute. Day/time and station metadata match the parsed code headers where checked. One SYNOP is a valid-looking `NIL` message with no observation groups; it is not a malformed temperature observation and is unsuitable for a temperature task. The limited structural checks found no flagged report headers, but do not validate every group, chronology, bulletin, national convention, or weather value. NIL and any slashes must not become zero measurements. Manual provenance, meteorological and chronological review is still required for **all 156**.

## Suitability, references, and coverage

The constrained first-pass extractor produced 301 **provisional** field values from 155 records: 39 SYNOP air temperatures, 202 METAR air/dewpoint values, and 60 TAF validity components. These are generated candidate labels, not independently verified gold; none of the 155 should be described as fully validated for scoring on this basis. One NIL record may support an explicitly scoped absence task, after review. `candidate_references.jsonl` records the narrow fields and their provisional status; the extractor deliberately leaves all other values unknown. These results are not 155 distinct, independent meteorological capabilities.

Three tasks E01–E03 are source-rule checked and independently calculated for the fields stated in `exploratory/EVIDENCE.md`. They use three distinct underlying report records and cover **three task-level primary capabilities**; the first two share one observation and therefore are not independent examples. Reference review is a desk check with cited code manuals, not independent human certification. These task definitions were frozen before inference. Their later model results are in `eval_independent_v1/FINDINGS.md`.

| Capability | Data evidence | Status |
|---|---|---|
| Observation provenance and unsupported verification claims | METAR excerpt and missing source link | E01 scoped and frozen |
| Observation versus forecast, temporary window, missing correction | METAR and TAF at matching day/time | E02 scoped and frozen; no authentic correction pair found, so correction precedence is not tested |
| SYNOP signed/decimal fields, derived spread, 24-hour pressure and precipitation | SYNOP with sections 1 and 3 | E03 scoped and frozen |
| METAR coded air/dewpoint | 101 candidate records | Automated candidates only; source and reference review pending |
| TAF validity / date boundary | 15 candidate records | Automated candidates only; year/month and reference review pending |
| SYNOP missing/NIL and other missing fields | 1 NIL plus slashed groups | Review needed before scoring; count of slash occurrences is not missing-value validation |
| TAF FM/BECMG/TEMPO/PROB, METAR gust/visibility/cloud and SYNOP pressure, cloud, precipitation | Present in some reports | Candidate coverage only; no blanket ground truth or record counts asserted |
| Authentic corrections and correction precedence | No `COR` token found in this dataset; two TAFs contain `AMD` | Review amendments and find a documented original/amended pair before a precedence task |

The 155 candidate rows are not the 20–30 fully validated real tasks the participant ultimately wants. Creating those requires specific task definitions, careful independent code-table checks, report-specific provenance, licensing, and tests. We do not fabricate an archive URL or substitute decoder agreement for independent verification. This is a work-in-progress collection, separate from the earlier five synthetic tasks, existing experiments, and focused submission ZIP.

## Reproduce and interpret

From the project root: `.venv/bin/python real_world_collection/inventory.py` and `.venv/bin/python -m unittest discover -s real_world_collection/tests -v`. These use CPU and standard library only. `inventory.json` includes line-level flags; `candidate_references.jsonl` includes unreviewed candidates. Freeze and hash records are in `exploratory/freeze.json`. Task definitions are frozen; create a new version before changing them.

## Subsequent real decoding task set

`decoding_v1/` adds 24 report-distinct, manually specified real-data tasks (eight per format) and 108 reference fields, separate from E01–E03. None of its source report IDs overlaps the three E tasks. Each field is a conditional interpretation of the supplied text, and the individual task derivations are in `decoding_v1/REFERENCE_AUDIT.md`. This increases coverage to **27 distinct task definitions across the decoding and evidence sets**, not 27 independent statistical samples: nearby reports and stations create correlations, and E01/E02 share a report. The earlier 301 automatically extracted values remain provisional and are not represented as 301 independently validated answers. Source authenticity, source permissions and independent expert review remain unresolved.

The header-only structural check did not identify every internal coding anomaly. For example, one excluded METAR contains `SCT1800`, which does not match the usual three-digit cloud-height group form and requires human source inspection. Its existence shows why the 155 candidate count is not a validity count; no blanket assertion that all 155 reports are well formed is justified.
