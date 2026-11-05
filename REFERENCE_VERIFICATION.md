# Reference verification: all 39 fields

Each reference was checked by the participant against the cited source rules and an explicit arithmetic/timeline derivation; the separate local test suite independently checks selected calculations and regrades stored responses. This is **not** independent meteorological certification.

Source A: [Hong Kong Observatory, Weather Services for Shipping, 16th edition (2007), Appendix X](https://www.weather.gov.hk/en/wservice/tsheet/pms/files/weather_services_for_shipping_16th.pdf), shared SYNOP/SHIP section-1 group sign, tenths and pressure definitions; [WMO No. 306, Volume I.1, 2010, FM12](https://www.vedur.is/gogn/athuganir/wmo/files/306_Vol_I.1_2010_en.pdf), section scope. For synop_trend the trend direction and amount are explicitly supplied by the task.

Source B: [NWS Aviation Weather Center product help](https://aviationweather.gov/help/data/), TAF FM and TEMPO conventions; [FAA Aeronautical Information Manual, chapter 7](https://www.faa.gov/Air_traffic/publications/atpubs/aim_html/chap7_section_1.html), ceiling definition. The interval boundary convention is explicitly supplied in the prompt. The NWS/FAA web pages are living documents, not a pinned print edition; consulted 5 November 2026.

Source C: [WMO No. 306, Volume I.1, 2010, FM15 §§15.9.2 and 15.12](https://www.vedur.is/gogn/athuganir/wmo/files/306_Vol_I.1_2010_en.pdf): unknown VV and QNH rounding. The task explicitly assumes the SYNOP and METAR values share an underlying pressure; operational observations need not.

| Task | Reference field | Expected | Verification trace | Source |
|---|---|---:|---|---|
| synop_cold | `air_temperature_c` | -2.5 | 11025 sign/tenths; -25/10 | A |
| synop_cold | `dewpoint_c` | -4.8 | 21048 sign/tenths; -48/10 | A |
| synop_cold | `msl_pressure_hpa` | 998.7 | 49987, 9987/10 within prompt range | A |
| synop_trend | `current_temperature_c` | -2.5 | 11025 → -25/10 | A |
| synop_trend | `current_dewpoint_c` | -4.8 | 21048 → -48/10 | A |
| synop_trend | `current_msl_pressure_hpa` | 998.7 | 49987 → 9987/10 within range | A |
| synop_trend | `msl_pressure_three_hours_ago_hpa` | 996.9 | 998.7 - stated rise 1.8 = 996.9 | A |
| synop_trend | `temperature_dewpoint_spread_c` | 2.3 | -2.5 - (-4.8) = 2.3 | A |
| taf_four_times | `p1559` | 6000 | BKN060 prevailing at 05/15:59 | B |
| taf_four_times | `temp1559` | 800 | TEMPO BKN008 at 05/15:59 | B |
| taf_four_times | `wind1559` | 10 | prevailing 18010KT | B |
| taf_four_times | `p1600` | null | FM SCT030: no BKN/OVC/VV ceiling | B |
| taf_four_times | `temp1600` | null | TEMPO ends at explicit exclusive boundary | B |
| taf_four_times | `wind1600` | 15 | FM 24015G25KT | B |
| taf_four_times | `p1900` | null | prevailing SCT030: no ceiling | B |
| taf_four_times | `temp1900` | 1200 | TEMPO BKN012 at 05/19 | B |
| taf_four_times | `wind1900` | 15 | prevailing FM wind 15 kt | B |
| taf_four_times | `p0000` | 1200 | FM060000 OVC012 = 1200 ft | B |
| taf_four_times | `temp0000` | null | no TEMPO at day 06 00:00 | B |
| taf_four_times | `wind0000` | 8 | FM060000 30008KT | B |
| cross_code | `synop_temperature_c` | -0.8 | 11008 → -8/10 | A |
| cross_code | `synop_dewpoint_c` | -1.2 | 21012 → -12/10 | A |
| cross_code | `synop_msl_pressure_hpa` | 998.7 | 49987 → 9987/10 | A |
| cross_code | `metar_qnh_hpa` | 998 | Q0998 = 998 hPa | C |
| cross_code | `pressure_consistent` | 1 | floor(998.7) = 998, under task assumption | C |
| cross_code | `metar_ceiling_ft_agl` | null | VV/// has no numerical value | C |
| T13 | `a_temp_c` | -2.5 | 11025 → -25/10 | A |
| T13 | `a_dew_c` | -4.8 | 21048 → -48/10 | A |
| T13 | `a_msl_hpa` | 998.7 | 49987 → 9987/10 | A |
| T13 | `a_spread_c` | 2.3 | -2.5 - (-4.8) = 2.3 | A |
| T13 | `b_temp_c` | 0.8 | 10008 → +8/10 | A |
| T13 | `b_dew_c` | -1.2 | 21012 → -12/10 | A |
| T13 | `b_msl_hpa` | 1003.2 | 40032 → 1003.2 within range | A |
| T13 | `b_spread_c` | 2 | 0.8 - (-1.2) = 2.0 | A |
| T13 | `c_temp_c` | -1 | 11010 → -10/10 | A |
| T13 | `c_dew_c` | null | group absent; task requires null | A |
| T13 | `c_msl_hpa` | null | group absent; task requires null | A |
| T13 | `c_spread_c` | null | dewpoint absent; task requires null | A |
| T13 | `b_minus_a_msl_hpa` | 4.5 | 1003.2 - 998.7 = 4.5 | A |
