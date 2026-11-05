# Real-world decoding tasks v1

24 prospective tasks (RS01–RS08 SYNOP, RM01–RM08 METAR, RT01–RT08 TAF) use 24 distinct records, with 108 manually transcribed reference fields. These are separate from three E tasks, earlier experiments, and the frozen submission. `tasks.json` retains each report, prompt, fields, expected values and derivation; `grader.py` supplies exact-field deterministic grading. The source file is byte-preserved at `../raw/attributed_reports.jsonl`. See [REFERENCE_AUDIT.md](REFERENCE_AUDIT.md) before interpreting any grade.

From the project root run:

```sh
.venv/bin/python -m unittest discover -s real_world_collection/decoding_v1/tests -v
.venv/bin/python -m unittest discover -s real_world_collection/tests -v
```

No paid model inference has been performed or authorized yet. This is a pre-inference freeze; do not modify task content, grader, or scoring after inference. Versions that change them must be stored separately. Any future run must save the exact prompt, model response, settings, timestamps, token usage, cost and field-level grade, and include all successes and failures.

Source-record independence means no identical source report is reused in this 24-task set or the E01–E03 set. It does not mean reports from nearby times or the same station are independent statistical draws. These exercises do not establish physical truth of the original observations.
