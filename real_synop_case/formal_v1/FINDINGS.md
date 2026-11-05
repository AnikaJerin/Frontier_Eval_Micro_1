# Formal real-report SYNOP exploration, version 1

Nine new trials were run only after the task, reference, source report, grader and runner were frozen. Raw responses, prompts, parsed JSON, per-field grades, usage, timestamps and costs are in `results/synop_real_formal_v1/`. Existing original benchmark, prior exploratory results and earlier prose comparison remain separate. The supplied report's upstream data provenance and sharing terms were not independently established; it is retained because the user supplied it for this project. The task was created after examining one earlier response per model, so it is a post-hoc exploratory follow-up, not independent evidence for general performance.

| Model | Exact task success | Field accuracy | Observed pass³ |
|---|---:|---:|---:|
| gpt-5.4 | 0/3 | 71/81 (87.65%) | 0 |
| gpt-6-astra | 3/3 | 81/81 (100.00%) | 1 |
| muse-wonder-1.0 | 2/3 | 80/81 (98.77%) | 0 |

Pass³ is 1 only when all three complete attempts passed; it is not a probability estimate. Field accuracy is correct fields divided by 81 across three attempts. Missing or malformed schema would score zero field credit under the frozen grader; all nine responses here were valid JSON with exact keys. Returned-token cost estimate: $0.198404. A GPT-6 Astra request timed out with no saved response and unknown billing state before the explicit resume; possible charges for that request are not included. OpenAI used provider-default reasoning and temperature, Meta Muse Wonder used minimal reasoning; 2048 maximum output tokens. Settings differ, and three attempts on one report do not estimate population accuracy.

## Failure-by-failure review

- [gpt-5.4 trial 1](../../results/synop_real_formal_v1/gpt-5.4_1.json): cloud_base_min_m: returned 50, reference 300, cloud_base_max_exclusive_m: returned 100, reference 600, visibility_km: returned 0, reference 5.
- [gpt-5.4 trial 2](../../results/synop_real_formal_v1/gpt-5.4_2.json): cloud_base_min_m: returned None, reference 300, cloud_base_max_exclusive_m: returned None, reference 600, visibility_km: returned 0, reference 5, dewpoint_c: returned -21, reference 21.0.
- [gpt-5.4 trial 3](../../results/synop_real_formal_v1/gpt-5.4_3.json): cloud_base_min_m: returned 1500, reference 300, cloud_base_max_exclusive_m: returned 2000, reference 600, visibility_km: returned 50, reference 5.
- [muse-wonder-1.0 trial 1](../../results/synop_real_formal_v1/muse-wonder-1.0_1.json): precipitation_24h_mm: returned 20, reference 2.0.

The incorrect cloud-base categories and visibility values conflict with WMO tables 1600 and 4377. The reversed dewpoint sign in GPT-5.4 trial 2 conflicts with the sign digit in `20210`. In Muse Wonder trial 1, `70020` was returned as 20 mm rather than 2.0 mm; WMO 306 2010 FM12 §12.4.9 specifies tenths of a millimetre. These are field-level decoding errors, not JSON formatting failures. Models' internal reasoning is unavailable, so root causes are not established. See [reference audit](REFERENCE_AUDIT.md).

The two pressure fields are conditional on the explicitly stated range and group-4 interpretation; values are not an independent station-pressure measurement. Section 3 minimum-temperature observation period is not inferred. Independent human meteorological review remains pending. See `results/user_synop_20261031/` for the earlier open-ended, unscored comparison; those outputs were not reused as formal trials.
