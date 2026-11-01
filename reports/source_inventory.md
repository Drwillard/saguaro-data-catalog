# Source inventory

Counts describe parsed sheet rows, including any source summaries or blank formatted rows; they are not canonical observation counts. Header rows are one-based Excel rows. Full field types, literal categories, missingness and candidate IDs are in Parquet. Empty strings count as blank; NA/dead/not found remain distinct source tokens.

| Program | File | Sheet/layer | Header row | Rows | Columns |
|---|---|---|---:|---:|---:|
| ecotone | 50mPlots_RawData_2011.xlsx | all_plots_combined | 1 | 1467 | 14 |
| ecotone | 50mPlots_RawData_2011.xlsx | summary_data | 1 | 171 | 6 |
| ecotone | 50mPlots_RawData_2011.xlsx | 4 | 1 | 401 | 14 |
| ecotone | 50mPlots_RawData_2011.xlsx | 12 | 1 | 19 | 16 |
| ecotone | 50mPlots_RawData_2011.xlsx | 23 | 1 | 22 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 25 | 1 | 120 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 41 | 1 | 36 | 9 |
| ecotone | 50mPlots_RawData_2011.xlsx | 100 | 1 | 5 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 101 | 1 | 11 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 102 | 1 | 7 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 103 | 1 | 1 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 104 | 1 | 12 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 105 | 1 | 12 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 106 | 1 | 1 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 108 | 1 | 13 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 109 | 1 | 18 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 110 | 1 | 7 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 111 | 1 | 3 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 112 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 113 | 1 | 16 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 114 | 1 | 17 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 115 | 1 | 24 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 116 | 1 | 2 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 117 | 1 | 12 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 118 | 1 | 18 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 119 | 2 | 8 | 13 |
| ecotone | 50mPlots_RawData_2011.xlsx | 120 | 1 | 9 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 121 | 1 | 38 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 123 | 1 | 79 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 124 | 1 | 4 | 10 |
| ecotone | 50mPlots_RawData_2011.xlsx | 126 | 1 | 32 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 127 | 1 | 2 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 128 | 1 | 9 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 129 | 1 | 2 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 130 | 1 | 4 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 131 | 1 | 10 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 132 | 1 | 47 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 133 | 1 | 2 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 134 | 1 | 37 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 135 | 2 | 1 | 13 |
| ecotone | 50mPlots_RawData_2011.xlsx | 136 | 2 | 13 | 13 |
| ecotone | 50mPlots_RawData_2011.xlsx | 141 | 2 | 35 | 13 |
| ecotone | 50mPlots_RawData_2011.xlsx | 143 | 2 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 146 | 2 | 11 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 147 | 1 | 13 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 152 | 1 | 46 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 153  | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 154 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 157 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 158 | 2 | 10 | 13 |
| ecotone | 50mPlots_RawData_2011.xlsx | 159 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 163 | 2 | 4 | 13 |
| ecotone | 50mPlots_RawData_2011.xlsx | 164 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 165 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 167  | 2 | 1 | 13 |
| ecotone | 50mPlots_RawData_2011.xlsx | 168 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 169  | 1 | 1 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 170  | 2 | 5 | 13 |
| ecotone | 50mPlots_RawData_2011.xlsx | 171 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 172 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 173 | 2 | 6 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 174  | 2 | 6 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 175 | 1 | 2 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 176  | 2 | 48 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 177 | 1 | 1 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 178 | 2 | 6 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 179 | 1 | 1 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 180 | 1 | 22 | 13 |
| ecotone | 50mPlots_RawData_2011.xlsx | 184 | 2 | 1 | 13 |
| ecotone | 50mPlots_RawData_2011.xlsx | 185 | 3 | 2 | 13 |
| ecotone | 50mPlots_RawData_2011.xlsx | 186 | 2 | 55 | 13 |
| ecotone | 50mPlots_RawData_2011.xlsx | 187 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 188 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 193 | 2 | 5 | 13 |
| ecotone | 50mPlots_RawData_2011.xlsx | 195 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 197 | 2 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 198 | 1 | 45 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 199 | 1 | 4 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 201 | 1 | 3 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 205 | 1 | 8 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 206 | 1 | 39 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 325; | 1 | 5 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 326; | 1 | 3 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 329 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 335 | 1 | 29 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 336 | 1 | 9 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 337 | 1 | 5 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 341 | 1 | 1 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 339 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 311 | 1 | 14 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 313 | 1 | 10 | 11 |
| ecotone | 50mPlots_RawData_2011.xlsx | 331 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 196 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 323 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 142 | 1 | 5 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 148 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 144 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 145 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 137 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 140 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 315 | 1 | 4 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 314 | 1 | 51 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 338 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 327 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 348 | 1 | 4 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 355 | 1 | 5 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 156 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 162 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 309 | 1 | 11 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 321 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 322 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 340 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 342 | 1 | 18 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 344 | 1 | 4 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 349 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 350 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 351 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 352 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 353 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 354 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 356 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 357 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 358 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 359 | 1 | 16 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 360 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 316 | 1 | 19 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 312 | 1 | 27 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 310 | 1 | 32 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 319 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 320 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 151 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 343 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 160 | 1 | 30 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 324 | 1 | 2 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 191 | 1 | 13 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 183 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 304 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 210 | 1 | 2 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 306 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 305 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 307 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 182 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 318 | 1 | 5 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 211 | 1 | 5 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 302 | 1 | 4 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 303 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 301 | 1 | 6 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 300 | 1 | 5 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 204 | 1 | 12 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 207 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 328 | 1 | 3 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 194 | 1 | 6 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 213 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 214 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 122 | 1 | 5 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 138 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 166 | 1 | 1 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 208 | 1 | 3 | 12 |
| ecotone | 50mPlots_RawData_2011.xlsx | 203 | 1 | 4 | 12 |
| historic_plots | Steenbergh&Lowe_HistoricSaguaroPlotSurvey.xls | Sheet1 | 7 | 3631 | 21 |
| historic_plots | Steenbergh&Lowe_HistoricSaguaroPlotSurvey.xls | Sheet2 | None | 0 | 0 |
| historic_plots | Steenbergh&Lowe_HistoricSaguaroPlotSurvey.xls | Sheet3 | None | 0 | 0 |
| census | SaguaroCensus_RawData_1990_2000_2010.xlsx | Read-me | None | 3 | 1 |
| census | SaguaroCensus_RawData_1990_2000_2010.xlsx | RawData_1990_Total_Saguaros | 2 | 45 | 16 |
| census | SaguaroCensus_RawData_1990_2000_2010.xlsx | RawData_2000_2010 | 2 | 28839 | 38 |
| census | SaguaroCensus_RawData_1990_2000_2010.xlsx | raw_data_by_plot_all_years | 1 | 250 | 47 |
| census | SaguaroCensus_RawData_1990_2000_2010.xlsx | raw_data_1990_saguaroperha  | 2 | 45 | 16 |
| census | SaguaroCensus_RawData_1990_2000_2010.xlsx | raw_data_2000 | 1 | 6923 | 10 |
| census | SaguaroCensus_RawData_1990_2000_2010.xlsx | raw_data_2010 | 1 | 21916 | 17 |
| vegetation | VegSubplot_RawData_2010.xlsx | 1 | 1 | 16 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 2 | 1 | 23 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 3 | 1 | 13 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 4 | 1 | 30 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 5 | 1 | 14 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 6 | 1 | 22 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 7 | 1 | 23 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 8 | 1 | 8 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 9 | 1 | 16 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 10 | 1 | 20 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 11 | 1 | 23 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 12 | 1 | 109 | 13 |
| vegetation | VegSubplot_RawData_2010.xlsx | 13 | 1 | 23 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 14 | 1 | 23 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 15 | 1 | 13 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 16 | 1 | 26 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 17 | 1 | 24 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 18 | 1 | 22 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 19 | 1 | 25 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 20 | 1 | 24 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 21 | 1 | 23 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 22 | 1 | 25 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 23 | 1 | 26 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 24 | 1 | 15 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 25 | 1 | 16 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 26 | 1 | 23 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 27 | 1 | 20 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 28 | 1 | 17 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 29 | 1 | 8 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 30 | 1 | 17 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 31 | 1 | 9 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 32 | 1 | 13 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 33 | 1 | 7 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 34 | 1 | 23 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 35 | 1 | 13 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 36 | 1 | 31 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 37 | 1 | 23 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 38 | 1 | 15 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 39 | 1 | 15 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 40 | 1 | 19 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 41 | 1 | 20 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 42 | 1 | 18 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 43 | 1 | 263 | 11 |
| vegetation | VegSubplot_RawData_2010.xlsx | 44 | 1 | 13 | 8 |
| vegetation | VegSubplot_RawData_2010.xlsx | 45 | 1 | 159 | 14 |
| vegetation | VegSubplot_RawData_2000.xlsx | 1 | 1 | 13 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 2 | 1 | 22 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 3 | 1 | 10 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 4 | 1 | 21 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 5 | 1 | 12 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 6 | 1 | 19 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 7 | 22 | 19 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 8 | 1 | 8 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 9 | 1 | 14 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 10 | 1 | 17 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 11 | 1 | 24 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 12 | 1 | 20 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 13 | 1 | 14 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 14 | 1 | 18 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 15 | 10 | 12 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 16 | 1 | 18 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 17 | 1 | 24 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 18 | 1 | 19 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 19 | 1 | 21 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 20 | 1 | 22 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 21 | 1 | 19 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 22 | 1 | 21 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 23 | 1 | 23 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 24 | 1 | 14 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 25 | 1 | 18 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 26 | 1 | 17 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 27 | 1 | 18 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 28 | 1 | 15 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 29 | 1 | 7 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 30 | 1 | 16 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 31 | 1 | 5 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 32 | 1 | 11 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 33 | 1 | 6 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 34 | 1 | 19 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 35 | 1 | 11 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 36 | 1 | 27 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 37 | 1 | 20 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 38 | 1 | 16 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 39 | 1 | 18 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 40 | 1 | 17 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 41 | 1 | 20 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 42 | 1 | 20 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 43 | 1 | 23 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 44 | 1 | 14 | 7 |
| vegetation | VegSubplot_RawData_2000.xlsx | 45 | 1 | 27 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 1 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 2 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 3 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 4 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 5 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 6 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 7 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 8 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 9 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 10 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 11 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 12 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 13 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 14 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 15 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 16 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 17 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 18 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 19 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 20 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 21 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 22 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 23 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 24 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 25 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 26 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 27 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 28 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 29 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 30 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 31 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 32 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 33 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 34 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 35 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 36 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 37 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 38 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 39 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 40 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 41 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 42 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 43 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 44 | 1 | 0 | 7 |
| vegetation | VegSubplot_RawData_1990.xlsx | 45 | 1 | 0 | 7 |
| vegetation | VegetationSubplotCorners.xlsx | Sheet1 | 3 | 183 | 5 |
| vegetation | VegetationSubplotCorners.xlsx | Sheet2 | None | 0 | 0 |
| vegetation | VegetationSubplotCorners.xlsx | Sheet3 | None | 0 | 0 |
| section17 | Section17_RawData_1941_2011.xlsx | 2011 | 1 | 9297 | 13 |
| section17 | Section17_RawData_1941_2011.xlsx | 1941 | 1 | 13304 | 9 |
| section17 | Section17_RawData_1941_2011.xlsx | Sheet3 | None | 0 | 0 |
| boundaries | PlotCorners.xls | saguaro_plot_corners | 3 | 1197 | 8 |
| boundaries | PlotBoundaries.xls | saguaro_plot_boundaries | 6 | 317 | 5 |
| boundaries | PlotBoundaries.xls | Sheet1 | 1 | 318 | 7 |
| section17 | Section17_Shapefiles.zip | Section17_Shapefiles/Grids.shp | None | 64 | 4 |
| section17 | Section17_Shapefiles.zip | Section17_Shapefiles/saguaros_2012.shp | None | 9297 | 11 |
| section17 | Section17_Shapefiles.zip | Section17_Shapefiles/Section17_Plots_percentchange.shp | None | 64 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot01/plot1.shp | None | 11 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot02/plot2.shp | None | 18 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot03/plot3.shp | None | 10 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot04/plot4.shp | None | 15 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot05/plot5.shp | None | 7 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot06/real plot6.shp | None | 18 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot07/plot7.shp | None | 16 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot08/plot8.shp | None | 6 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot09/plot9.shp | None | 12 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot10/plot10.shp | None | 12 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot11/really plot11.shp | None | 17 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot12/plot12.shp | None | 12 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot13/plot13.shp | None | 12 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot14/plot14.shp | None | 16 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot15/plot15.shp | None | 10 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot16/plot16.shp | None | 14 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot17/plot17.shp | None | 20 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot18/plot18.shp | None | 14 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot19/plot19.shp | None | 19 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot20/plot20.shp | None | 22 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot21/plot21.shp | None | 13 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot22/plot22.shp | None | 15 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot23/plot23.shp | None | 16 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot24/plot24.shp | None | 12 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot25/plot25.shp | None | 18 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot26/plot26.shp | None | 16 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot27/plot27.shp | None | 16 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot28/plot28.shp | None | 12 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot29/plot29.shp | None | 4 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot30/plot30.shp | None | 9 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot31/plot31.shp | None | 5 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot32/plot32.shp | None | 12 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot33/plot33.shp | None | 6 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot34/plot34.shp | None | 15 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot35/plot35.shp | None | 8 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot36/plot36.shp | None | 19 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot37/plot37.shp | None | 18 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot38/plot38.shp | None | 15 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot39/plot39.shp | None | 18 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot40/plot40.shp | None | 12 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot41/plot41.shp | None | 14 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot42/plot42.shp | None | 17 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot43/plot43.shp | None | 19 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot44/plot44.shp | None | 13 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Data Analysis/plot45/plot45.shp | None | 11 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot01/eplot1.shp | None | 401 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot02/eplot2.shp | None | 815 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot03/eplot3.shp | None | 610 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot04/eplot4.shp | None | 1043 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot05/eplot5.shp | None | 648 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot06/eplot6.shp | None | 1227 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot07/eplot7.shp | None | 1377 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot08/eplot8.shp | None | 234 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot09/eplot9.shp | None | 920 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot10/eplot10.shp | None | 898 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot11/eplot11.shp | None | 1099 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot12/eplot12.shp | None | 531 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot13/eplot13.shp | None | 1187 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot14/eplot14.shp | None | 669 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot15/eplot15.shp | None | 812 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot16/eplot16.shp | None | 450 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot17/eplot17.shp | None | 2903 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot18/eplot18.shp | None | 313 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot19/eplot19.shp | None | 1217 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot20/eplot20.shp | None | 779 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot21/eplot21.shp | None | 727 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot22/eplot22.shp | None | 806 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot23/eplot23.shp | None | 927 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot24/eplot24.shp | None | 1333 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot25/eplot25.shp | None | 440 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot26/eplot26.shp | None | 804 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot27/eplot27.shp | None | 856 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot28/eplot28.shp | None | 850 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot29/eplot29.shp | None | 236 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot30/eplot30.shp | None | 1101 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot31/eplot31.shp | None | 1491 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot32/eplot32.shp | None | 1374 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot33/eplot33.shp | None | 370 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot34/eplot34.shp | None | 594 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot35/eplot35.shp | None | 313 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot36/eplot36.shp | None | 1378 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot37/eplot37.shp | None | 863 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot38/eplot38.shp | None | 978 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot39/eplot39.shp | None | 1075 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot40/eplot40.shp | None | 2319 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot41/eplot41.shp | None | 667 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot42/eplot42.shp | None | 903 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot43/eplot43.shp | None | 2208 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot44/eplot44.shp | None | 446 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot45/eplot45.shp | None | 912 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot01/totalcov.shp | None | 12 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot02/totalcov.shp | None | 21 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot03/totalcov.shp | None | 9 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot04/totalcov.shp | None | 20 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot05/totalcov.shp | None | 11 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot06/totalcov.shp | None | 19 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot07/totalcov.shp | None | 18 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot08/totalcov.shp | None | 7 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot09/totalcov.shp | None | 13 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot10/totalcov.shp | None | 16 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot11/totalcov.shp | None | 24 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot12/totalcov.shp | None | 21 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot13/totalcov.shp | None | 13 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot14/totalcov.shp | None | 17 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot15/totalcov.shp | None | 11 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot16/totalcov.shp | None | 17 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot17/totalcov.shp | None | 23 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot18/totalcov.shp | None | 19 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot19/totalcov.shp | None | 20 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot20/totalcov.shp | None | 21 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot21/totalcov.shp | None | 18 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot22/totalcov.shp | None | 20 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot23/totalcov.shp | None | 22 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot24/totalcov.shp | None | 13 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot25/totalcov.shp | None | 17 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot26/totalcov.shp | None | 17 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot27/totalcov.shp | None | 18 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot28/totalcov.shp | None | 14 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot29/totalcov.shp | None | 6 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot30/totalcov.shp | None | 15 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot31/totalcov.shp | None | 4 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot32/totalcov.shp | None | 10 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot33/totalcov.shp | None | 5 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot34/totalcov.shp | None | 18 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot35/totalcov.shp | None | 10 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot36/totalcov.shp | None | 27 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot37/totalcov.shp | None | 20 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot38/totalcov.shp | None | 15 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot39/totalcov.shp | None | 17 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot40/totalcov.shp | None | 16 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot41/totalcov.shp | None | 19 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot42/totalcov.shp | None | 20 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot43/totalcov.shp | None | 24 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot44/totalcov.shp | None | 13 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Data Analysis/plot45/totalcov.shp | None | 26 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot01/plot1buffer.shp | None | 225 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot01/plot1point.shp | None | 33 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot01/plot1poly.shp | None | 32 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot02/plot2buffer.shp | None | 238 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot02/plot2point.shp | None | 19 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot02/plot2poly.shp | None | 23 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot03/plot3buffer.shp | None | 52 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot03/plot3point.shp | None | 30 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot03/plot3poly.shp | None | 16 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot04/plot4buffer.shp | None | 87 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot04/plot4point.shp | None | 90 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot04/plot4poly.shp | None | 45 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot05/plot5buffer.shp | None | 79 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot05/plot5point.shp | None | 14 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot05/plot5poly.shp | None | 16 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot06/plot6buffer.shp | None | 111 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot06/plot6point.shp | None | 105 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot06/plot6poly.shp | None | 71 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot07/plot7buffer.shp | None | 135 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot07/plot7point.shp | None | 42 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot07/plot7poly.shp | None | 38 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot08/plot8buffer.shp | None | 6 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot08/plot8point.shp | None | 25 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot08/plot8poly.shp | None | 20 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot09/plot9buffer.shp | None | 24 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot09/plot9point.shp | None | 19 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot09/plot9poly.shp | None | 25 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot10/plot10buffer.shp | None | 80 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot10/plot10point.shp | None | 22 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot10/plot10poly.shp | None | 27 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot11/plot11buffer.shp | None | 49 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot11/plot11point.shp | None | 90 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot11/plot11poly.shp | None | 59 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot12/plot12buffer.shp | None | 152 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot12/plot12point.shp | None | 41 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot12/plot12poly.shp | None | 46 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot13/plot13buffer.shp | None | 24 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot13/plot13point.shp | None | 25 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot13/plot13poly.shp | None | 25 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot14/plot14buffer.shp | None | 99 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot14/plot14point.shp | None | 62 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot14/plot14poly.shp | None | 44 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot15/plot15buffer.shp | None | 85 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot15/plot15point.shp | None | 17 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot15/plot15poly.shp | None | 17 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot16/plot16buffer.shp | None | 46 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot16/plot16point.shp | None | 43 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot16/plot16poly.shp | None | 26 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot17/plot17buffer.shp | None | 117 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot17/plot17point.shp | None | 65 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot17/plot17poly.shp | None | 64 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot18/plot18buffer.shp | None | 125 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot18/plot18point.shp | None | 29 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot18/plot18poly.shp | None | 36 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot19/plot19buffer.shp | None | 273 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot19/plot19point.shp | None | 22 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot19/plot19poly.shp | None | 28 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot20/plot20buffer.shp | None | 136 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot20/plot20point.shp | None | 33 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot20/plot20poly.shp | None | 28 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot21/plot21buffer.shp | None | 358 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot21/plot21point.shp | None | 7 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot21/plot21poly.shp | None | 9 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot22/plot22buffer.shp | None | 61 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot22/plot22point.shp | None | 50 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot22/plot22poly.shp | None | 36 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot23/plot23buffer.shp | None | 210 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot23/plot23point.shp | None | 29 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot23/plot23poly.shp | None | 33 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot24/plot24buffer.shp | None | 136 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot24/plot24point.shp | None | 93 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot24/plot24poly.shp | None | 76 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot25/plot25buffer.shp | None | 90 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot25/plot25point.shp | None | 47 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot25/plot25poly.shp | None | 44 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot26/plot26buffer.shp | None | 80 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot26/plot26point.shp | None | 23 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot26/plot26poly.shp | None | 20 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot27/plot27buffer.shp | None | 146 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot27/plot27point.shp | None | 45 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot27/plot27poly.shp | None | 45 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot28/plot28buffer.shp | None | 200 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot28/plot28point.shp | None | 67 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot28/plot28poly.shp | None | 42 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot29/plot29buffer.shp | None | 63 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot29/plot29point.shp | None | 16 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot29/plot29poly.shp | None | 15 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot30/plot30buffer.shp | None | 75 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot30/plot30point.shp | None | 17 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot30/plot30poly.shp | None | 21 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot31/plot31buffer.shp | None | 152 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot31/plot31point.shp | None | 4 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot31/plot31poly.shp | None | 4 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot32/plot32buffer.shp | None | 256 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot32/plot32point.shp | None | 22 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot32/plot32poly.shp | None | 24 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot33/plot33buffer.shp | None | 79 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot33/plot33point.shp | None | 27 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot33/plot33poly.shp | None | 9 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot34/plot34buffer.shp | None | 83 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot34/plot34point.shp | None | 40 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot34/plot34poly.shp | None | 47 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot35/plot35buffer.shp | None | 71 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot35/plot35point.shp | None | 8 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot35/plot35poly.shp | None | 10 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot36/plot36buffer.shp | None | 402 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot36/plot36point.shp | None | 43 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot36/plot36poly.shp | None | 41 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot37/plot37buffer.shp | None | 139 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot37/plot37point.shp | None | 75 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot37/plot37poly.shp | None | 63 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot38/plot38buffer.shp | None | 193 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot38/plot38point.shp | None | 25 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot38/plot38poly.shp | None | 19 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot39/plot39buffer.shp | None | 98 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot39/plot39point.shp | None | 86 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot39/plot39poly.shp | None | 52 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot40/plot40buffer.shp | None | 222 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot40/plot40point.shp | None | 26 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot40/plot40poly.shp | None | 29 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot41/plot41buffer.shp | None | 117 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot41/plot41point.shp | None | 92 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot41/plot41poly.shp | None | 52 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot42/plot42buffer.shp | None | 210 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot42/plot42point.shp | None | 32 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot42/plot42poly.shp | None | 31 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot43/plot43buffer.shp | None | 191 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot43/plot43point.shp | None | 103 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot43/plot43poly.shp | None | 73 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot44/plot44buffer.shp | None | 88 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot44/plot44point.shp | None | 28 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot44/plot44poly.shp | None | 14 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot45/plot45buffer.shp | None | 186 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot45/plot45point.shp | None | 34 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Field files/plot45/plot45poly.shp | None | 38 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot01/1stems.shp | None | 253 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot01/newplot1spines.shp | None | 26 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot01/plot1bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot01/plot1cov.shp | None | 257 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot01/plot1spines.shp | None | 26 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot02/2stems.shp | None | 243 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot02/plot2bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot02/plot2cov.shp | None | 256 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot02/plot2spines.shp | None | 19 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot03/3stems.shp | None | 75 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot03/plot3bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot03/plot3cov.shp | None | 66 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot03/plot3spine.shp | None | 10 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot04/4stems.shp | None | 164 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot04/plot4bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot04/plot4cov.shp | None | 130 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot04/plot4spine.shp | None | 28 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot05/5stems.shp | None | 88 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot05/plot5bnd.shp | None | 2 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot05/plot5cov.shp | None | 95 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot05/plot5spines.shp | None | 23 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot06/6spinesmore.shp | None | 1 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot06/6stems.shp | None | 212 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot06/plot6bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot06/plot6cov.shp | None | 182 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot07/7stems.shp | None | 171 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot07/plot7bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot07/plot7cov.shp | None | 169 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot08/8stems.shp | None | 31 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot08/plot8bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot08/plot8cov.shp | None | 26 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot09/9stems.shp | None | 41 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot09/plot9bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot09/plot9cov.shp | None | 49 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot10/10stems.shp | None | 93 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot10/plot10bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot10/plt10cov.shp | None | 102 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot11/11stems.shp | None | 129 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot11/plot11bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot11/plot11cov.shp | None | 105 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot12/12stems.shp | None | 182 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot12/plot12bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot12/plot12cov.shp | None | 192 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot13/13stems.shp | None | 47 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot13/plot13bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot13/plt13cov.shp | None | 49 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot14/14stems.shp | None | 158 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot14/plot14bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot14/plt14cov.shp | None | 141 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot15/15stems.shp | None | 101 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot15/plot15bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot15/plt15cov.shp | None | 102 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot16/16stems.shp | None | 81 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot16/plot16bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot16/plt16cov.shp | None | 70 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot17/17stems.shp | None | 171 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot17/plot17bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot17/plt17cov.shp | None | 181 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot18/18stems.shp | None | 150 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot18/plot18bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot18/plt18cov.shp | None | 161 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot19/19spinesmore.shp | None | 2 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot19/19stems.shp | None | 273 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot19/plot19bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot19/plt19cov.shp | None | 296 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot20/20stems.shp | None | 164 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot20/plot20bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot20/plt20cov.shp | None | 162 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot21/21stems.shp | None | 352 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot21/plot21bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot21/plot21spines.shp | None | 13 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot21/plt21cov.shp | None | 364 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot22/22stems.shp | None | 106 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot22/plot22bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot22/plot22spines.shp | None | 13 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot22/plt22cov.shp | None | 96 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot23/23stems.shp | None | 229 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot23/plot23bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot23/plot23spines.shp | None | 28 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot23/plt23cov.shp | None | 241 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot24/24stems.shp | None | 215 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot24/plot24bnd.shp | None | 2 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot24/plot24spines.shp | None | 15 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot24/plt24cov.shp | None | 207 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot25/25stems.shp | None | 124 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot25/plot25bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot25/plot25spines.shp | None | 26 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot25/plt25cov.shp | None | 125 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot26/26spines.shp | None | 26 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot26/26stems.shp | None | 97 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot26/plot26bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot26/plt26cov.shp | None | 99 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot27/27spines.shp | None | 35 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot27/27stems.shp | None | 167 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot27/plot27bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot27/plt27cov.shp | None | 173 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot28/28spines.shp | None | 20 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot28/28stems.shp | None | 248 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot28/plot28bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot28/plt28cov.shp | None | 240 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot29/29spines.shp | None | 23 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot29/29stems.shp | None | 76 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot29/plot29bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot29/plt29cov.shp | None | 78 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot30/30spines.shp | None | 22 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot30/30stems.shp | None | 77 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot30/plot30bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot30/plt30cov.shp | None | 93 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot31/31stems.shp | None | 155 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot31/plot31bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot31/plot31spines.shp | None | 12 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot31/plt31cov.shp | None | 156 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot32/32stems.shp | None | 246 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot32/plot32bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot32/plot32spines.shp | None | 43 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot32/plt32cov.shp | None | 267 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot33/33stems.shp | None | 104 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot33/plot33bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot33/plot33spines.shp | None | 1 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot33/plt33cov.shp | None | 88 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot34/34stems.shp | None | 121 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot34/plot34bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot34/plot34spines.shp | None | 3 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot34/plt34cov.shp | None | 129 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot35/35stems.shp | None | 73 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot35/plot35bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot35/plot35spines.shp | None | 12 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot35/plt35cov.shp | None | 79 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot36/36stems.shp | None | 430 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot36/plot36bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot36/plot36spines.shp | None | 47 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot36/plt36cov.shp | None | 436 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot37/37stems.shp | None | 204 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot37/plot37bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot37/plot37spines.shp | None | 13 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot37/plt37cov.shp | None | 201 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot38/38stems.shp | None | 210 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot38/plot38bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot38/plot38spines.shp | None | 34 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot38/plt38cov.shp | None | 210 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot39/39stems.shp | None | 180 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot39/plot39bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot39/plot39spines.shp | None | 32 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot39/plt39cov.shp | None | 150 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot40/40stems.shp | None | 237 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot40/more40spines.shp | None | 8 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot40/plot40bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot40/plot40spines.shp | None | 36 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot40/plt40cov.shp | None | 247 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot41/41stems.shp | None | 192 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot41/plot41bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot41/plot41spines.shp | None | 18 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot41/plt41cov.shp | None | 158 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot42/42stems.shp | None | 237 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot42/plot42bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot42/plot42spines.shp | None | 11 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot42/plt42cov.shp | None | 239 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot43/43stems.shp | None | 283 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot43/plot43bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot43/plot43spines.shp | None | 25 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot43/plt43cov.shp | None | 262 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot44/44stems.shp | None | 110 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot44/plot44bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot44/plot44spines.shp | None | 12 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot44/plt44cov.shp | None | 102 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot45/45stems.shp | None | 207 | 7 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot45/plot45bnd.shp | None | 1 | 5 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot45/plot45spines.shp | None | 40 | 8 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/2000 Maps/plot45/plt45cov.shp | None | 217 | 6 |
| vegetation | GIS Data Veg Plots.zip | GIS Data Veg Plots/Plot Corners/new all subplot corners.shp | None | 180 | 9 |
| historic_plots | HistoricPlot_Shapefiles.zip | HistoricPlot_Shapefiles/HistoricPlot_1975.shp | None | 1546 | 9 |
| historic_plots | HistoricPlot_Shapefiles.zip | HistoricPlot_Shapefiles/HistoricPlot_2010.shp | None | 2556 | 10 |
| historic_plots | HistoricPlot_Shapefiles.zip | HistoricPlot_Shapefiles/HistoricPlot_2014.shp | None | 2525 | 10 |
| boundaries | SaguaroMonitoring_PlotCorner_Boundary.zip | SaguaroMonitoring_PlotCorner_Boundary/saguaro_plot_boundaries.shp | None | 317 | 19 |
| boundaries | SaguaroMonitoring_PlotCorner_Boundary.zip | SaguaroMonitoring_PlotCorner_Boundary/saguaro_plot_centroids.shp | None | 249 | 23 |
| boundaries | SaguaroMonitoring_PlotCorner_Boundary.zip | SaguaroMonitoring_PlotCorner_Boundary/saguaro_plot_corners.shp | None | 1194 | 19 |
| boundaries | SaguaroMonitoring_PlotCorner_Boundary.zip | SaguaroMonitoring_PlotCorner_Boundary/Saguaro_Plots___TypeAnno.shp | None | 303 | 25 |