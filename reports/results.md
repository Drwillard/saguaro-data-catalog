# Build results

```json
{
  "records_by_program": {
    "census": 24222,
    "census_auxiliary": 4617,
    "ecotone": 1467,
    "historic_plots": 10526,
    "section17": 22600
  },
  "aggregate_records_by_representation": {
    "RawData_1990_Total_Saguaros": 45,
    "raw_data_1990_saguaroperha ": 45,
    "raw_data_by_plot_all_years": 250
  },
  "vegetation_records_by_year": {
    "2000": 724,
    "2010": 830
  },
  "validation_findings": 8412,
  "findings_by_rule": {
    "AMBIGUOUS_ZERO_HEIGHT": 3041,
    "DUPLICATE_COORDINATES": 1797,
    "IDENTITY_TRACKING_UNSUPPORTED": 1137,
    "OUTSIDE_ASSIGNED_PLOT": 960,
    "UNKNOWN_SPATIAL_CRS": 437,
    "DUPLICATE_LOCAL_SOURCE_ID": 360,
    "TEMPORAL_ARM_DECREASE": 226,
    "DUPLICATE_ORGANISM_EVENT": 170,
    "TEMPORAL_STATUS_RESOLVED": 109,
    "TEMPORAL_SHRINKAGE": 94,
    "TEMPORAL_MEASUREMENT_AFTER_DEATH": 49,
    "TEMPORAL_GROWTH_OUTLIER": 21,
    "INFERRED_HEIGHT_UNIT": 4,
    "CATEGORICAL_DRIFT": 3,
    "TEMPORAL_REOBSERVED": 3,
    "INVALID_OR_NULL_GEOMETRY": 1
  },
  "coverage": {
    "linked_organisms": 3169,
    "unlinked_observations": 54043,
    "points_with_geographic_coordinates": 19242,
    "plots_with_polygons": 165,
    "independent_linked_coordinate_observations": 0,
    "spatial_features": 86901,
    "spatial_features_without_crs": 68238,
    "vegetation_observations": 1554
  },
  "limitations": [
    "No downloaded 2020 individual raw workbook was exposed by inspected NPS holdings; the two 2020 reports are preserved.",
    "Census and Section17 observations have no established cross-round individual linkage; no histories are invented.",
    "Historic 71G is excluded from individual linkage because the 2002 report explicitly describes tag loss.",
    "Historic coordinates repeat a shared source location, so they cannot establish temporal displacement. Displacement rule is tested on fixtures; no real-data movement result is claimed.",
    "Zero Historic heights and uncertain units are retained and flagged; no automatic source correction.",
    "Vegetation 1990 workbook sheets are header-only. Historical mapped attributes remain available separately in spatial_features.",
    "Subplot containment is not established for undated local-coordinate maps without CRS or explicit parent geometry; no inferred georeferencing.",
    "Spatial layers are separate source representations, not appended as additional organism observations. Geometry differences across layers require further source reconciliation.",
    "Cover labels differ; canonical vegetation cover is null until units and denominator are resolved.",
    "Report flags screen data for review; they are not confirmed source errors or ecological findings."
  ]
}
```

## Ten illustrative examples

1. **TEMPORAL_MEASUREMENT_AFTER_DEATH**, `8b997c50962a63933437451a`: {"previous": "2b5ded29b7b4e5aec8a28645", "height": 3.4}. A standing dead cactus can be measured; positive height does not establish resurrection. Source: `{"source_dataset": "historic_plots", "source_file": "data/raw/historic_plots/6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a/Steenbergh&Lowe_HistoricSaguaroPlotSurvey.xls", "source_sheet": "Sheet1", "source_row": 2969, "source_reference_id": "2225187", "source_sha256": "6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a", "source_row_id": "25bcf04bcfcaf22c058739f5"}`

2. **TEMPORAL_SHRINKAGE**, `58f020371babd818c05cb635`: {"previous": "e3770fc78729a3b8520c5cb2", "height_before": 7.455, "height_after": 1.55, "elapsed_years": 26}. Possible broken top, measurement change, unit issue, transcription error or mislinkage. Source: `{"source_dataset": "historic_plots", "source_file": "data/raw/historic_plots/6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a/Steenbergh&Lowe_HistoricSaguaroPlotSurvey.xls", "source_sheet": "Sheet1", "source_row": 2928, "source_reference_id": "2225187", "source_sha256": "6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a", "source_row_id": "227cf80f0dc047b11610d301"}`

3. **TEMPORAL_GROWTH_OUTLIER**, `19b48e28e80bc68afa3c25ad`: {"previous": "b1ad67f68ca13719afe199de", "annual_growth_m": 0.5, "empirical_upper": 0.46202666666666686, "median": 0.06666666666666672, "robust_spread": 0.06589333333333336, "n": 612}. Statistical screening only; no biological maximum asserted. Source: `{"source_dataset": "historic_plots", "source_file": "data/raw/historic_plots/6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a/Steenbergh&Lowe_HistoricSaguaroPlotSurvey.xls", "source_sheet": "Sheet1", "source_row": 3091, "source_reference_id": "2225187", "source_sha256": "6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a", "source_row_id": "afbbd0cd3f80ad308f101bac"}`

4. **TEMPORAL_ARM_DECREASE**, `58f020371babd818c05cb635`: {"previous": "e3770fc78729a3b8520c5cb2", "arms_before": 6.0, "arms_after": 0.0}. Arms can break; a decrease is a warning, not proof of source error. Source: `{"source_dataset": "historic_plots", "source_file": "data/raw/historic_plots/6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a/Steenbergh&Lowe_HistoricSaguaroPlotSurvey.xls", "source_sheet": "Sheet1", "source_row": 2928, "source_reference_id": "2225187", "source_sha256": "6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a", "source_row_id": "227cf80f0dc047b11610d301"}`

5. **OUTSIDE_ASSIGNED_PLOT**, `d8fe96e39935fcd0ceb28077`: [-110.72837799498066, 32.214981760455146]. Boundary/GPS differences or plot assignment require review. Source: `{"source_dataset": "historic_plots", "source_file": "data/raw/historic_plots/6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a/Steenbergh&Lowe_HistoricSaguaroPlotSurvey.xls", "source_sheet": "Sheet1", "source_row": 74, "source_reference_id": "2225187", "source_sha256": "6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a", "source_row_id": "2730b441b2dbc078bdea9a47"}`

6. **DUPLICATE_LOCAL_SOURCE_ID**, `9606b717b177416ebc11c0bf`: "3". Could be repeated rounds or source duplication; no deduplication performed. Source: `{"source_dataset": "census", "source_file": "data/raw/census/acd73e553169c2808c3e4829cba17e95bfdb08824144f1985befcfa6a9b589ff/SaguaroCensus_RawData_1990_2000_2010.xlsx", "source_sheet": "RawData_2000_2010", "source_row": 105, "source_reference_id": "2225188", "source_sha256": "acd73e553169c2808c3e4829cba17e95bfdb08824144f1985befcfa6a9b589ff", "source_row_id": "7bca6af4e8fdab8bcc9b56df"}`

7. **DUPLICATE_COORDINATES**, `85cd426fe6b06b7dcd398862`: [-111.18685189186122, 32.26524951656887]. Shared positions may reflect source copies, precision or mapping methods. Source: `{"source_dataset": "historic_plots", "source_file": "data/raw/historic_plots/6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a/Steenbergh&Lowe_HistoricSaguaroPlotSurvey.xls", "source_sheet": "Sheet1", "source_row": 1420, "source_reference_id": "2225187", "source_sha256": "6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a", "source_row_id": "6bd75f4874f9b4660d187c45"}`

8. **AMBIGUOUS_ZERO_HEIGHT**, `7122e32242a899e289679656`: {"raw": "0", "notes": "dead"}. Zero retained; excluded from temporal height comparisons. Source: `{"source_dataset": "historic_plots", "source_file": "data/raw/historic_plots/6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a/Steenbergh&Lowe_HistoricSaguaroPlotSurvey.xls", "source_sheet": "Sheet1", "source_row": 8, "source_reference_id": "2225187", "source_sha256": "6f62e764accb75e61b8b4d0b69c4d42d90fb91c197d85f5ae0f42c5bf9236a3a", "source_row_id": "f7866b0c5e85655ff3cfa0ed"}`

9. **INVALID_OR_NULL_GEOMETRY**, `21fb619e3859c8be665fb038`: null. Malformed source geometry retained as null or invalid; no repair. Source: `{"source_dataset": "vegetation", "source_file": "data/raw/vegetation/882f2ea68ecb57598dbb7d567cc1ca1a3e6193f00c81d494dfb7d5ab1441d102/GIS Data Veg Plots.zip", "source_sheet": "GIS Data Veg Plots/1990 Maps/Original CAD files in ArcView3_1 format/plot27/eplot27.shp", "source_row": 496, "source_reference_id": "2225403", "source_sha256": "882f2ea68ecb57598dbb7d567cc1ca1a3e6193f00c81d494dfb7d5ab1441d102", "source_row_id": "1ee1fef6d53514324e08c331"}`

10. **UNKNOWN_SPATIAL_CRS**, `f31be03ac94192dc88a4010c`: {"layer": "GIS Data Veg Plots/1990 Data Analysis/plot01/plot1.shp", "affected_features": 11}. Local or undocumented source coordinates; excluded from geographic validation. One finding per affected layer. Source: `{"source_dataset": "vegetation", "source_file": "data/raw/vegetation/882f2ea68ecb57598dbb7d567cc1ca1a3e6193f00c81d494dfb7d5ab1441d102/GIS Data Veg Plots.zip", "source_sheet": "GIS Data Veg Plots/1990 Data Analysis/plot01/plot1.shp", "source_row": 1, "source_reference_id": "2225403", "source_sha256": "882f2ea68ecb57598dbb7d567cc1ca1a3e6193f00c81d494dfb7d5ab1441d102", "source_row_id": "fd02ceb6b6235b5531f222be"}`

## Supported conference-paper claims

- Source-aware adapters must separate aggregate densities from individual measurements; the Census workbook contains both.
- Shared source identifiers can support histories while documented tag loss makes the same strategy unsafe on 71G.
- Temporal height and arm rules reveal review candidates that pass nonnegative scalar validation; see actual counts above.
- Provenance preserves the path from a flagged SI value to a hashed file, sheet, physical row and source column.
- Spatial validity and CRS coverage constrain which geographic checks are defensible; missing CRS must remain visible.
