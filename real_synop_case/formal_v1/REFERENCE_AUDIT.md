# Independent reference audit, pre-inference

The user supplied the raw report. Its upstream provenance and redistribution rights have not been independently verified. It is treated as an input string, not a claim about observation accuracy. Station identifier is retained as encoded; station identity and station-specific pressure are not assumed. The prompt explicitly constrains both pressures to 950–1050 hPa and explicitly identifies group 4 as MSL pressure because the string alone is insufficient to establish all pressure context. This is a conditional reference, not independent validation of the station's pressure. Section 3 conventions are checked against WMO 306 Volume I.1, 2010 edition, FM 12. Regional observing periods for minimum temperature are not inferred.

The reference below was separately derived by splitting code groups and applying published tables; it does not use `decode.py` to calculate expected values. `reference.json` contains these exact numeric values. WMO [Manual on Codes 2010](https://www.vedur.is/gogn/athuganir/wmo/files/306_Vol_I.1_2010_en.pdf), FM12 §§12.2 and 12.4, is the edition baseline. Supporting primary sources: [HKO SYNOP/SHIP shared group definitions, Appendix X](https://www.weather.gov.hk/en/wservice/tsheet/pms/files/weather_services_for_shipping_16th.pdf), [WMO table 1600](https://www.nodc.noaa.gov/archive/arc0021/0002199/1.2/data/0-data/HTML/WMO-CODE/WMO1600.HTM), [WMO table 4377](https://www.nodc.noaa.gov/archive/arc0021/0000907/1.1/data/0-data/HTML/WMO-CODE/WMO4377.HTM) and [WMO table 1819 as reproduced by Environment Canada](https://www.canada.ca/en/environment-climate-change/services/weather-manuals-documentation/manobs-surface-observations.html).

| Group | Fields checked independently | Derivation |
|---|---|---|
| `31031 41850` | observation_day, observation_hour_utc, station_number | 31, 3, 41850; iw=1 indicates m/s. |
| `01450` | precipitation_indicator, weather_station_indicator, cloud_base_min_m, cloud_base_max_exclusive_m, visibility_km | iR=0, iX=1; h=4 is 300 to less than 600 m; VV=50 is 5 km. |
| `8//00` | total_cloud_oktas, wind_direction_deg, wind_speed_mps | 8, unavailable, 0 m/s. |
| `10222 20210` | air_temperature_c, dewpoint_c | positive 22.2 and 21.0 C. |
| `30087 40188` | station_pressure_hpa, msl_pressure_hpa | 1008.7 and 1018.8 hPa within explicitly stated bounds. |
| `70522` | present_weather_code, past_weather_1_code, past_weather_2_code | code figures 05, 2 and 2; task requests numbers, not interpretation. |
| `8852/` | low_cloud_amount_oktas, low_cloud_type_code, medium_cloud_type_code, high_cloud_type_code | 8, 5, 2 and unavailable. |
| Section 3 `20213` | minimum_temperature_c | +21.3 C; interval unspecified. |
| Section 3 `59008` | pressure_change_24h_hpa | group 59 indicates negative change; 008 in tenths gives -0.8 hPa. WMO 2010 §12.4.7.1.2(k–l) and symbolic p24. |
| Section 3 `70020` | precipitation_24h_mm | 0020 in tenths = 2.0 mm; WMO 2010 §12.4.9. This is distinct from the missing 6RRRtR group. |
| Group presence | six_group_section1_present, six_group_section3_present | neither section contains a group beginning 6: 0 and 0. iR=0 expects group 6 in both, but this presence field reflects actual transmitted content; no missing amount is invented. |

The user-provided source report and reference were not independently certified by a human meteorologist. The formal prompt was designed after the earlier qualitative model responses: this task is an exploratory follow-up and its scores do not represent a pre-registered, unbiased evaluation sample.
