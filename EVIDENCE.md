# Evidence, reference derivations and analysis

Each result below is one of 45 preserved API responses. Three independent, single-turn trials per task and model used the exact model-visible prompts in `data/`; all retained trials are completed. Test code regrades each raw answer and verifies the saved prompt and field-level grade. A task passes only when every reference field is correct. The incomplete Meta attempt from the earlier experiment is not among these 45 completed trials.

The selection is retrospective: all five cases have at least one GPT-5.4 failure and three passes by the other two models, and cases passed by all three models were left out. Therefore the selected-only 1/15 GPT-5.4 pass rate should not be generalized to weather reports or the original benchmark. Cases share conventions and a TAF forecast, so they are not independent evidence of five unrelated weaknesses. No meteorologist has reviewed the references. Reasoning settings differ between providers. The exact weather meanings and synthetic inputs were source-checked with Codex assistance; the user must review these materials before submitting.

## synop_cold — sign in a section-1 temperature

Reference: `11025` is -2.5°C, `21048` is -4.8°C and `49987` is 998.7 hPa within the given range. GPT-5.4 returned +2.5°C in trials [1](results/gpt-5.4_synop_cold_1.json) and [3](results/gpt-5.4_synop_cold_3.json), while trial [2](results/gpt-5.4_synop_cold_2.json) passed. GPT-6 Astra and Muse Wonder each passed 3/3. The two failures contain valid JSON; the sign of one field is incorrect. HKO Appendix X defines the sign and tenths conventions.

## synop_trend — signs, scope and pressure arithmetic

Reference: current air -2.5°C, dew point -4.8°C, pressure 998.7 hPa; a specified 1.8 hPa rise means previous pressure 996.9 hPa; the temperature–dewpoint difference is 2.3°C. Section 3 values are not current observations. GPT-5.4 failed 3/3, including sign and pressure errors; [trial 1](results/gpt-5.4_synop_trend_1.json) has all five fields wrong. GPT-6 Astra and Muse Wonder passed 3/3.

## taf_four_times — overlays, expiration and replacement

Reference ceilings at the four query times: prevailing 6000, null, null, 1200 feet; temporary 800, null, 1200, null feet. Prevailing winds are 10, 15, 15, 8 kt. The prompt explicitly defines interval boundaries and FM/TEMPO handling. GPT-5.4 failed 3/3: in [trial 1](results/gpt-5.4_taf_four_times_1.json), it assigned the temporary 800-ft ceiling as prevailing at 15:59 and treated scattered cloud SCT030 as a prevailing 3000-ft ceiling at two times; nine other fields were correct. The other models passed 3/3. NWS sources describe prevailing ceiling and forecast change groups.

## cross_code — signs, rounding and unknown ceiling

Under the prompt's explicit assumption linking the two synthetic excerpts, 998.7 hPa rounds down to Q0998; the pressures are consistent and VV/// does not specify a numeric ceiling. Temperatures are -0.8°C and -1.2°C. GPT-5.4 failed 3/3 by reversing the air-temperature sign, and reversed the dewpoint sign in two trials; [trial 2](results/gpt-5.4_cross_code_2.json) shows a near miss with the pressure and missing-ceiling fields correct. The other models passed 3/3.

## T13 — multiple reports with missing values

Report A temperature/dewpoint/pressure are -2.5°C, -4.8°C and 998.7 hPa; report B values are +0.8°C, -1.2°C and 1003.2 hPa; their spreads are 2.3°C and 2.0°C, and their pressure difference is 4.5 hPa. Report C contains an air temperature of -1.0°C but no dewpoint or MSL-pressure group; its dewpoint, pressure and derived spread remain null. In all three attempts GPT-5.4 gave positive temperatures for reports A and C and a dependent wrong spread; [trial 1](results/gpt-5.4_T13_1.json) shows that it did correctly preserve the missing fields. The other models passed 3/3.

## Source and grading limits

The input strings are original synthetic fixtures prepared during this project; they are not archived weather observations. Some omit operational bulletin context; treat them as decoding excerpts. Group-4 sea-level pressure is read under each task's stated range/context, not as a measured station fact. References are independently traced to [HKO Appendix X](https://www.weather.gov.hk/en/wservice/tsheet/pms/files/weather_services_for_shipping_16th.pdf), [WMO Manual on Codes Vol I.1, 2010 edition](https://www.vedur.is/gogn/athuganir/wmo/files/306_Vol_I.1_2010_en.pdf), [NWS TAF guide](https://aviationweather.gov/help/data/), and [NWS ceiling explanation](https://www.weather.gov/asos/METAR.html). These linked publications retain their publishers' terms and are not republished here. Numeric arithmetic and explicit TAF intervals are cross-checked by local tests.

The responses do not expose model reasoning, so the internal cause of an error is unknown. The analysis describes returned fields, not model thought processes. The JSON format is part of each prompt: malformed JSON or the wrong key set scores zero, and exact-key valid JSON gets equal per-field partial credit. Human inspection of the linked failures shows domain-field errors rather than schema errors; the reference and mutation tests exercise the grader but do not prove absence of all false positives or false negatives.
