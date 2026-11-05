# Real-world collection: findings and inference status

This collection contains 156 user-supplied reports: 40 SYNOP, 101 METAR and 15 TAF. An automated first pass generated candidate field values from 155 reports; these candidates are not independently verified gold answers. One SYNOP report is NIL. The separate `decoding_v1/` collection has 24 task definitions using 24 distinct reports, and the `exploratory/` collection has E01–E03. Reference and provenance limitations are documented in [AUDIT.md](AUDIT.md) and [decoding_v1/REFERENCE_AUDIT.md](decoding_v1/REFERENCE_AUDIT.md).

## Model trials

After the task definitions were frozen, **nine of the 24 decoding tasks and all three exploratory tasks were evaluated**, for 12 tasks total. Three trials per task and model were planned. There are 107 completed responses and one interrupted, unscored request whose billing state is unknown. The remaining 15 decoding tasks were not run in this experiment.

| Model | Exact passes / completed | Failed | Unscored |
|---|---:|---:|---:|
| GPT-5.4 | 27/35 | 8 | 1 |
| GPT-6 Astra | 36/36 | 0 | 0 |
| Meta Muse Wonder | 34/36 | 2 | 0 |

The full [experiment findings](eval_independent_v1/FINDINGS.md) include task-level outcomes, settings, estimated costs, the selection rationale and failure review. [Saved trial records](eval_independent_v1/results/) contain the actual requests, responses and grades; `eval_independent_v1/regrade.py` recomputes the completed grades offline. Four GPT-5.4 failures were JSON-schema failures, distinct from weather errors. Observed decoding errors included a reversed SYNOP pressure-change sign and a scattered cloud layer treated as a ceiling.

These are small, non-random and correlated samples. E01 and E02 share a METAR but test different capabilities; E03 uses a SYNOP report explored previously. The results do not estimate general model performance and do not establish intent, deception or reward hacking. The dataset's report-specific provenance, redistribution scope and independent meteorological review remain unresolved. No model inference was conducted on the 15 omitted decoding tasks in this experiment.
