# Real-report exploratory evaluation — 5 November 2026

## Design and limitations

Before inference, nine decoding tasks were selected for different primary skills from 24 separately frozen task definitions, with distinct source reports, plus E01–E03 (12 tasks). This reduced repetitive tests rather than assessing the 15 omitted tasks. E01 and E02 share one METAR but test different capabilities; E03 uses a SYNOP report examined in an earlier experiment. Nearby reports and same stations are correlated. The study is exploratory and non-random; it is not an unbiased estimate of general model performance. Report-specific provenance and permission scope were not independently verified; no independent meteorologist certified the references. Weather decoding errors do not demonstrate intent, deception, or reward hacking.

Three trials per model per task were planned: 108 requests. After ten saved responses, an ongoing GPT-5.4 RS05 request was interrupted during a correction to the disclosed request count. Its provider completion and billing status are unknown; it was not retried and is unscored. Thus 107 completed responses and one unscored interruption are preserved. Each exact request and response, provider settings, timestamp, usage, parsed JSON and field grade is in `results/`. The local `regrade.py` independently reruns the frozen grader on all completed saved answers and checks each model-visible prompt against its frozen task.

GPT-5.4 and GPT-6 Astra used provider-default reasoning and temperature; Muse Wonder used minimal reasoning. All used a 2048 output-token cap. Model configuration is unequal and may affect the comparison. The USD token-price estimates below use rates recorded in previous project runs, are not independently verified current billing prices, and exclude possible charges for the interrupted request.

| Model | Completed | Exact task passes | Exact task failures | Pass rate among completed | Known estimated cost |
|---|---:|---:|---:|---:|---:|
| GPT-5.4 | 35 | 27 | 8 | 77.1% | $0.049453 |
| GPT-6 Astra | 36 | 36 | 0 | 100% | $0.203510 |
| Meta Muse Wonder | 36 | 34 | 2 | 94.4% | $0.203112 |

Total known estimated cost: **$0.456075**, plus any unknown interruption charge. GPT-5.4 field accuracy on schema-valid answers only was 164/168; schema-invalid responses are excluded from this particular denominator. Astra was 186/186 and Muse 184/186. Exact task success includes all schema failures.

| Task | Core skill | GPT-5.4 | Astra | Muse |
|---|---|---:|---:|---:|
| RS03 | Section boundaries and group presence | 2/3 | 3/3 | 3/3 |
| RS05 | Signed pressure change and daily precipitation | 0/2; 1 unscored | 3/3 | 1/3 |
| RS08 | NIL versus zero | 3/3 | 3/3 | 3/3 |
| RM01 | Scattered cloud versus ceiling | 3/3 | 3/3 | 3/3 |
| RM05 | Visibility versus RVR qualifier | 0/3 | 3/3 | 3/3 |
| RM07 | Variable wind and multiple runway ranges | 3/3 | 3/3 | 3/3 |
| RT02 | Completed BECMG and temporary cloud layer | 1/3 | 3/3 | 3/3 |
| RT04 | FM at midnight | 3/3 | 3/3 | 3/3 |
| RT06 | TEMPO, PROB and missing vertical visibility | 3/3 | 3/3 | 3/3 |
| E01 | Evidence integrity | 3/3 | 3/3 | 3/3 |
| E02 | Observation versus forecast | 3/3 | 3/3 | 3/3 |
| E03 | Multistage decode and arithmetic | 3/3 | 3/3 | 3/3 |

Observed all-three-pass (empirical pass³): GPT-5.4 8/11 fully observed tasks; RS05 cannot receive a pass³ value because one trial is unscored. Astra 12/12; Muse 11/12. This is a count of task-level all-three outcomes, not a reliable estimate of future success probability.

## Failure review

- **RS05 genuine sign-decoding errors:** `59010` denotes a negative 24-hour change of 1.0 hPa; GPT-5.4 returned +1.0 in its two completed trials; Muse returned +1.0 twice and −1.0 once. WMO Manual on Codes 2010, table 2100, identifies 9 as a negative change; p24 is in tenths of a hectopascal: https://www.vedur.is/gogn/athuganir/wmo/files/306_Vol_I.1_2010_en.pdf. The expected value −1.0 is conditional on the supplied code; the station observation was not independently verified.
- **RT02 genuine ceiling errors:** GPT-5.4 twice treated `SCT012` as the temporary ceiling (1200 ft); the temporary layer `BKN080` yields 8000 ft. The third GPT-5.4 attempt and all six other model attempts passed. The NWS cloud definitions distinguish scattered from broken: https://www.weather.gov/media/surface/WSOH8.pdf.
- **RM05 structured-output failures, not demonstrated weather errors:** GPT-5.4 failed all three exact-schema grades because it added fields or nested requested fields, although the requested 1800 m prevailing visibility and P2000 greater-than qualifier are represented correctly in the answers. This is output-contract noncompliance, not evidence that it confused RVR and visibility. The reference qualifier is supported by https://www.weather.gov/media/surface/SFCTraining.pdf §3.4.
- **RS03 structured-output failure:** One GPT-5.4 answer used synonymous prefixed field names rather than the exact requested names; its presented meteorological values matched the reference. The other two attempts passed. Treat the failed grade as schema noncompliance, not a weather error.

These reviews do not establish why the model generated an answer. The exact-key grader intentionally evaluates the requested JSON contract; alternative representations can be semantically correct while failing that contract.

## Reproduction

The original input collection and frozen tasks are under `../raw/`, `../decoding_v1/` and `../exploratory/`. Run `python real_world_collection/eval_independent_v1/regrade.py` and `python real_world_collection/eval_independent_v1/analyze.py` from the project root. The latter recomputes counts; `summary.json` contains its recorded output. Run the two real-world unittest suites documented in `../decoding_v1/README.md`. Running `run.py` calls paid APIs; saved and interrupted records are skipped on resume. Do not reuse this experiment version for modified tasks or settings. The earlier focused submission ZIP was not altered.
