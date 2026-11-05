# Real-data decoding tasks: reference audit

This version contains 24 tasks using 24 distinct source-report IDs: eight SYNOP, eight METAR and eight TAF. No source report is reused from E01–E03. Distinct reports are not necessarily statistically independent: some are from the same station and nearby times. The references below were explicitly written from the code groups and manually checked using the cited standards and straightforward arithmetic. They are conditional interpretations of the supplied strings, not independent confirmation that observations occurred. Independent meteorologist review and record-specific provenance remain outstanding.

## Sources and conventions

- WMO Manual on Codes, WMO-No. 306, Volume I.1, 2010 edition, FM 12 sections 12.2 and 12.4: [alphanumeric code manual](https://www.vedur.is/gogn/athuganir/wmo/files/306_Vol_I.1_2010_en.pdf). SYNOP group identifiers, sign and tenths, section 3 58/59 pressure tendency and group 7 rainfall are used only where explicitly present.
- Environment and Climate Change Canada, MANOBS 8th edition amendment 3, Chapter 15: [SYNOP code table explanations](https://www.canada.ca/en/environment-climate-change/services/weather-manuals-documentation/manobs-surface-observations.html). This supports SYNOP group definitions, wind, cloud and visibility figure 40.
- NOAA NWS, [Aviation Weather Center data help](https://aviationweather.gov/help/data/) and [METAR code definitions](https://www.weather.gov/asos/METAR.html), living documents: observation and forecast groups, prevailing/temporary conditions, time groups, wind and cloud decoding.
- NWS [surface observing training](https://www.weather.gov/media/surface/SFCTraining.pdf), §3.4, supports the P qualifier as greater than the highest reportable RVR; runways and prevailing visibility remain distinct. [NWS cloud definitions](https://www.weather.gov/media/surface/WSOH8.pdf) describe BKN/OVC ceiling and vertical visibility.

TAF tasks explicitly specify interval handling and ask after BECMG ends rather than inventing the exact transition time. Unknown numeric VV stays null. No task invents a source URL, station identity, measurement, missing value or operational authorization.

## Reference derivations

| Task | Format | Primary capability | Manually transcribed decoding |
|---|---|---|---|
| RS01 | SYNOP | section scope, missing wind direction | 10219 -> 21.9; 20210 -> 21.0; 8//00 has missing wind direction. |
| RS02 | SYNOP | signed change and precipitation | 10215 -> 21.5; 20210 -> 21.0; 58002 -> +0.2; 70030 -> 3.0. |
| RS03 | SYNOP | section maximum and group presence | Section 1 10215 -> 21.5; section 3 10240 -> 24.0; only section 3 has a 6 group. |
| RS04 | SYNOP | wind and daily change | 82702 -> direction 270 and speed 2; 10232 -> 23.2; 20180 -> 18.0; 58027 -> +2.7. |
| RS05 | SYNOP | minimum and precipitation | 10238 -> 23.8; 20220 -> 22.0; section 3 20219 -> 21.9; 59010 -> -1.0; 70015 -> 1.5. |
| RS06 | SYNOP | coded visibility and zero rain | 01440 -> VV 40 -> 4 km; 7//00 -> 7 oktas; 10250 -> 25.0; 70000 -> 0.0 mm. |
| RS07 | SYNOP | reported versus missing | 80401 -> direction 040 and speed 1; 10258 -> 25.8; 20210 -> 21.0; 69946 is present in Section 1. |
| RS08 | SYNOP | NIL missing observation | NIL supplies no observation groups; do not infer measurements or zero. |
| RM01 | METAR | scattered versus broken ceiling | 31003KT; 3200; SCT012 and FEW025CB are not BKN; BKN100 -> 10000 ft; 30/23; Q1017. |
| RM02 | METAR | low broken ceiling | 2500; BKN010 -> 1000 ft; 29/24; Q1016. |
| RM03 | METAR | no numeric coded ceiling | 11002KT; 3500; FEW015 SCT100 do not report a ceiling; 31/24. |
| RM04 | METAR | observation decoding | 29009KT; 7000; 34/25; Q1015. |
| RM05 | METAR | runway range is not visibility | 1800 is prevailing visibility; R28/P2000 is runway 28 visual range above 2000 m. |
| RM06 | METAR | multiple runway values | 1100; R28/P2000 -> greater than 2000; R29R/1900; R29L/1800. |
| RM07 | METAR | variable wind and measured ranges | VRB02KT has variable direction at 2 kt; 0800 -> 800 m; R27/1800; R29R/1700. |
| RM08 | METAR | overcast versus few cloud | 6000; SCT016 and FEW030CB are not ceilings; OVC100 -> 10000 ft; 28/26; Q1016. Local weather token is not scored. |
| RT01 | TAF | PROB and TEMPO window | PROB30 TEMPO 3106/3108 2000 applies at 07:00; it conveys a 30 percent probability of temporary 2000 m visibility. |
| RT02 | TAF | BECMG then TEMPO | BECMG 3116/3118 changes visibility to 4000; TEMPO 3118/3122 has 2500, 18015KT and BKN080. |
| RT03 | TAF | midnight and completed change | After BECMG 0101/0103 visibility 1000; previous completed BECMG 3114/3116 wind 27004KT remains. |
| RT04 | TAF | FM midnight boundary | Initial 33013KT; FM010000 begins at midnight with 32007KT and SKC. |
| RT05 | TAF | FM replacement and boundary | FM312000 25010KT ... BKN030 OVC040 -> wind 250/10 and ceiling 3000. |
| RT06 | TAF | TEMPO versus PROB and unknown vertical visibility | Initial 6000 SCT005; TEMPO 3106/3110 1500 BKN002 -> 200 ft; PROB40 3106/3109 0300 VV/// -> 40%, 300 m, unavailable VV. |
| RT07 | TAF | multiple temporary probabilities | BECMG 0103/0104 gives 4000; TEMPO 0104/0109 gives 0800; PROB40 TEMPO 0104/0107 gives 0500 VV///. |
| RT08 | TAF | completed BECMG and TEMPO scope | BECMG 3114/3117 07012KT BKN012 BKN022 -> wind 70/12 and 1200 ft; TEMPO 3122/0102 -SHRA active. |

## Verification limits

Every reference passes the deterministic grader; field-by-field changed values, wrong types, missing and extra keys, malformed JSON and duplicate keys are tested. The test suite also checks report and dataset hashes, uniqueness, frozen input hashes and a handful of independent arithmetic cases. These tests establish consistency and adversarial grader behavior, not independent validation of all 108 expected values. No model trials have been made. The prior E tasks and previous benchmark were not modified.

Original source metadata contains no per-record source URL; the participant attributes SYNOP reports to Ogimet and METAR/TAF to Aviation Weather Center. Report-specific authenticity and redistribution terms are unresolved; retain the evidence of permission and confirm its coverage before public distribution. Full year/month for the aviation records is absent; single-TAF internal day rollover tasks do not invent a calendar date.
