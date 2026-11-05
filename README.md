# MeteoCode-Eval — real-report exploratory evaluation

**Submission description:** MeteoCode-Eval examines whether language models preserve the meaning of SYNOP, METAR and TAF codes. It includes 156 user-supplied reports, deterministic weather-decoding tasks, and saved responses from three models. In a 12-task real-report exploratory selection, GPT-5.4 passed 27 of 35 completed trials, GPT-6 Astra 36 of 36, and Meta Muse Wonder 34 of 36. Four GPT-5.4 failures were output-schema errors; observed decoding errors include a reversed SYNOP pressure-change sign and a scattered cloud layer treated as a ceiling. These small, correlated samples do not estimate general model reliability; individual source URLs, redistribution scope and independent meteorological review remain unresolved.

**Video walkthrough:** .....

## Quick start: offline, no API keys

From the extracted ZIP root on macOS ARM64 with Python 3.11 or later:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m unittest discover -s real_world_collection/tests -v
python -m unittest discover -s real_world_collection/decoding_v1/tests -v
python validate_submission.py
python real_synop_case/formal_v1/verify.py
python analyze_results.py
python real_world_collection/eval_independent_v1/regrade.py
python real_world_collection/eval_independent_v1/analyze.py
```

The two analysis scripts reproduce the saved group summaries; `regrade.py` recomputes 107 completed real-report grades from raw saved responses. The 108th planned trial is unscored because its response and billing status are unknown after interruption. All offline checks use only the Python standard library and local CPU.

For fresh paid inference on the 12-task real-report selection, export `OPENAI_API_KEY` and `META_API_KEY` securely in the shell, then run `python real_world_collection/eval_independent_v1/run.py --output fresh_results`. This writes separate results without altering historical transcripts. The runner uses a conservative estimated $1.50 ceiling based on historical assumed prices, not a provider-enforced spending cap; check current provider pricing and billing controls before running. Three trials per task and model are configured. Historic completed requests used a total of about 307 seconds of API request time and an estimated $0.456075, excluding any charge for the interrupted request and retry delays. Provider-default reasoning and temperature were used for OpenAI; Meta used minimal reasoning. Each response stores exact request settings, timestamp, returned model metadata and usage.

**Domain and experience:** I've previously worked on a meteorological project for the Bangladesh Meteorological Department involving coded reports and supplied an earlier dataset; those reports predate this evaluation. I've created the evaluation and analysis for the hackathon. Codex assisted with task design,source checks and draft analysis. The decoding references were prepared using relevant WMO and aviation-weather guidance.(https://mdass.bmd.gov.bd/file/2022/01/23/pdf/124607.pdf);Independent meteorological review of every reference remains pending. The real-world data was collected from OGIMET(https://www.ogimet.com) and (https://aviationweather.gov/)

Five synthetic meteorological decoding tasks test SYNOP signed temperatures and pressure, missing-data propagation and TAF prevailing versus temporary conditions. Each task retained here has at least one GPT-5.4 failure and three passes from both GPT-6 Astra and Meta Muse Wonder. A structured answer can look plausible while reversing a temperature sign or assigning a temporary or scattered cloud layer as a prevailing ceiling.

**Selection was made after observing model results.** Other tasks where all three models passed were removed. Consequently these scores are conditional on this selection and must not be reported as an unbiased benchmark-wide model failure rate. The tasks overlap in signed-temperature and TAF concepts. Three trials per task are insufficient to estimate population performance. Independent human meteorological review remains pending. These are synthetic excerpts, not operational reports or flight guidance.

| Selected task | GPT-5.4 passes / 3 | GPT-6 Astra | Muse Wonder |
|---|---:|---:|---:|
| synop_cold | 1 | 3 | 3 |
| synop_trend | 0 | 3 | 3 |
| taf_four_times | 0 | 3 | 3 |
| cross_code | 0 | 3 | 3 |
| T13 | 0 | 3 | 3 |
| Total (selected only) | 1/15 | 15/15 | 15/15 |

All-success empirical pass³ by task: GPT-5.4 **0/5**; GPT-6 Astra **5/5**; Muse Wonder **5/5**. Pass³ is an observed all-three outcome per task, not a general probability. Each task’s failure evidence is in [EVIDENCE.md](EVIDENCE.md), all 39 field derivations are in [REFERENCE_VERIFICATION.md](REFERENCE_VERIFICATION.md), and [CONTEXT.md](CONTEXT.md) explains the broader results and case selection. Domain background and untested hypotheses are in [BACKGROUND.md](BACKGROUND.md).

Each trial starts with the exact prompt in `data/`. All 45 recorded requests and raw responses are in `results/`. GPT-5.4 snapshot was `gpt-5.4-2026-03-05`; GPT-6 Astra and Muse Wonder returned `gpt-6-astra` and `muse-wonder-1.0`. OpenAI trials used provider-default reasoning and temperature, and Meta used minimal reasoning; all used a 2048 output-token ceiling. Reasoning differences limit direct comparisons. On these selected records, estimated returned-token costs were $0.02304, $0.12401 and $0.150472 respectively, excluding unsuccessful or interrupted calls. Costs and runtimes are stored in the trial records. Total elapsed API-call times for the five-task runs were approximately 38 seconds (GPT-5.4), 57 seconds (GPT-6 Astra), and 70 seconds (Muse Wonder), excluding setup and failed requests. All selected trials were run on 5 November 2026 UTC. No new model calls were made to prepare the synthetic selection; later real-report runs are documented separately above.


## Separate real-report exploratory experiment

A sixth, separately reported task uses a public SYNOP report from Ogimet. The task was designed after an earlier qualitative comparison. Its frozen prompt, 27-field reference, code, audit, nine raw trial records and field scores are included in `real_synop_case/formal_v1/` and `results/synop_real_formal_v1/`. On three trials each, GPT-5.4 passed 0, GPT-6 Astra passed 3, and Muse Wonder passed 2; Muse once returned 20 mm instead of 2.0 mm. Observed pass³ was 0, 1 and 0 respectively. These scores are separate from the selected synthetic score, use explicit pressure assumptions, and do not establish general model accuracy. The report is a decoding input, not proof of actual observed conditions. Source derivations and review limitations are in the [audit](real_synop_case/formal_v1/REFERENCE_AUDIT.md) and [findings](real_synop_case/formal_v1/FINDINGS.md). Run `python real_synop_case/formal_v1/verify.py` for its 144 validation checks; the full test suite also regrades the nine records.

## Real-report dataset and new exploratory results

The separate `real_world_collection/decoding_v1/` contains 24 report-distinct decoding tasks and 108 manually transcribed reference fields; `real_world_collection/exploratory/` contains E01–E03. Before the new model runs, nine decoding tasks were selected for different capabilities, plus E01–E03. This tests 12 tasks, not every dataset record or every one of the 24 decoding tasks. The source reports are correlated by station and time; E01 and E02 share one METAR but test distinct skills, and E03 reuses a report seen in earlier work. Do not interpret the results as an independent, representative benchmark. The 15 unrun decoding tasks remain packaged for review; candidate labels for additional reports remain provisional.

| Model | Completed passes | Failures | Unscored |
|---|---:|---:|---:|
| GPT-5.4 | 27/35 | 8 | 1 interrupted request |
| GPT-6 Astra | 36/36 | 0 | 0 |
| Meta Muse Wonder | 34/36 | 2 | 0 |

Four GPT-5.4 failures were JSON-schema failures, not established weather errors. Weather errors include reversal of a SYNOP pressure-change sign by GPT-5.4 and Muse, and twice treating a scattered layer as a TAF ceiling by GPT-5.4. The nine decoding tasks and three evidence tasks were selected before these trials, but the collection had been explored in earlier experiments. All three models passed all E tasks; no finding establishes deception or intent. Models used different reasoning settings. [Full findings, task scores, settings and cost estimates](real_world_collection/eval_independent_v1/FINDINGS.md) link to all 107 completed raw responses and one interrupted unscored record. The known estimated cost was $0.456075, excluding an unknown interrupted-request charge; pricing assumptions were not independently verified against current billing.

Offline checks for the added collection:

```sh
python -m unittest discover -s real_world_collection/tests -v
python -m unittest discover -s real_world_collection/decoding_v1/tests -v
python real_world_collection/eval_independent_v1/regrade.py
python real_world_collection/eval_independent_v1/analyze.py
```

The source-rule references, graders, original data and new trial records are included. No one should infer physical truth of an observation solely from a decoded code. Independent meteorologist review and source-specific provenance remain outstanding.

## Reproduction on macOS ARM64

Python 3.11+ and the standard library are sufficient. Tested with Apple Silicon Python 3.11.13; no GPU or third-party runtime dependency is required.

```sh
/opt/homebrew/bin/python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python validate_submission.py
python analyze_results.py
export OPENAI_API_KEY='your-key'
python run_eval.py --model gpt-5.4 --trials 3
```

For Meta, place its key in `META_API_KEY` in the process environment and use `python run_eval.py --provider meta --model muse-wonder-1.0 --trials 3`. Never share or commit keys. Only inference uses network access; decoding checks, tests, scoring and processing use local CPU. The runner saves each raw request, response, usage, timing and field-level grade before moving on; rerunning resumes completed files. Incomplete responses are not counted as weather failures. HTTP 429 and transient 5xx responses use limited exponential backoff. Network ambiguity stops the run because billing/completion state is unknown. New runs will incur API costs; the runner accepts optional `--input-usd-per-million`, `--output-usd-per-million`, and `--cached-input-usd-per-million` to estimate costs; without all three, cost is unknown. It does not enforce a spending cap. Use provider billing controls and inspect response usage. Existing stored records retain their original cost estimates.

## Grading and references

`grader.py` accepts exactly one JSON object, exact keys and types, absolute numeric tolerance 1e-6, and null for specified unavailable values. The grader records per-field accuracy and requires all fields to pass for task success. Reference and deliberately wrong answers are tested locally. Whitespace and key order are immaterial. Exact prompts, expected answers and units appear in `data/`.

The sources supporting the code semantics include [WMO Manual on Codes, 2010 edition](https://www.vedur.is/gogn/athuganir/wmo/files/306_Vol_I.1_2010_en.pdf), [Hong Kong Observatory group definitions, Appendix X](https://www.weather.gov.hk/en/wservice/tsheet/pms/files/weather_services_for_shipping_16th.pdf), [NWS TAF change-group guidance](https://aviationweather.gov/help/data/), and [NWS METAR ceiling explanation](https://www.weather.gov/asos/METAR.html). 
