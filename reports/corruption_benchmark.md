# Synthetic intervention benchmark

Executed runs: [{"seeds": [1, 2, 3], "count": 100, "intensity": 1.0}, {"seeds": [42], "count": 30, "intensity": 0.25}]. Canonical cohort: 1200 observations; 179 spatial features. Complete selected organism histories and all plot context are retained. This is a deterministic cohort experiment on real canonical records, not a whole-corpus prevalence estimate.

Each trial starts from the same unchanged cohort and applies one synthetic intervention. All six layers run independently. Strict schema types/nullability/enums and conventional scalar ranges (height 0–30 m, arms 0–200, geographic ranges), integer counts, primary/composite keys and exact row duplicates form the baselines. The structural/spatial layers include the existing checks plus explicit identity/event/unit and CRS/geometry cross-checks added in this extension. Provenance checks are a separate integrity layer.

Completed synthetic interventions: 330; ineligible trials: 0. Skips are not detections or misses. Validator failures are misses and are counted separately.

| layer | injected | detections | misses | false_positives | matched_alerts | precision | alert_precision | recall | f1 | seed_recall_std | validator_errors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| provenance | 330 | 230 | 100 | 0 | 99596 | 1.000 | 1.000 | 0.697 | 0.821 | 0.016 | 0 |
| row | 330 | 118 | 212 | 0 | 200 | 1.000 | 1.000 | 0.358 | 0.527 | 0.014 | 0 |
| schema | 330 | 75 | 255 | 0 | 75 | 1.000 | 1.000 | 0.227 | 0.370 | 0.013 | 0 |
| spatial | 330 | 96 | 234 | 8 | 171 | 0.923 | 0.955 | 0.291 | 0.442 | 0.019 | 0 |
| structural | 330 | 115 | 215 | 0 | 15782 | 1.000 | 1.000 | 0.348 | 0.517 | 0.007 | 0 |
| temporal | 330 | 51 | 279 | 10 | 67 | 0.836 | 0.870 | 0.155 | 0.261 | 0.012 | 0 |

Precision counts one matched detection per intervention, collapses redundant matching alerts, and treats newly emitted alerts outside the recorded affected rows/histories as operational false positives. Alert precision additionally reports matched alerts / all new alerts. Recall is detected interventions / completed interventions. F1 uses the event precision and injection recall. Baseline signatures are subtracted; pre-existing scientific findings are neither scored as successes nor declared source errors. Unmatched new alerts can be secondary real effects of the injection rather than scientifically false claims.

## Executed detection rates by intervention semantics

| scenario_semantics | schema | row | structural | temporal | spatial | provenance |
| --- | --- | --- | --- | --- | --- | --- |
| integrity_violation | 0.259 | 0.376 | 0.397 | 0.045 | 0.331 | 0.655 |
| plausible_biological_transition | 0.000 | 0.000 | 0.000 | 0.900 | 0.000 | 1.000 |
| semantic_contradiction | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 1.000 |
| statistical_anomaly | 0.000 | 0.900 | 0.000 | 1.000 | 0.000 | 1.000 |

## Executed detection rates by intervention family

| corruption_class | schema | row | structural | temporal | spatial | provenance |
| --- | --- | --- | --- | --- | --- | --- |
| provenance | 0.000 | 0.200 | 0.200 | 0.000 | 0.180 | 0.800 |
| row | 0.139 | 1.000 | 0.681 | 0.056 | 0.375 | 0.806 |
| schema | 0.833 | 0.000 | 0.333 | 0.000 | 0.000 | 0.667 |
| spatial | 0.000 | 0.167 | 0.000 | 0.000 | 0.833 | 0.500 |
| temporal | 0.000 | 0.371 | 0.429 | 0.671 | 0.143 | 0.714 |

## Executed detection rates by scenario

| scenario | schema | row | structural | temporal | spatial | provenance |
| --- | --- | --- | --- | --- | --- | --- |
| provenance_duplicate_lineage | 0.000 | 1.000 | 1.000 | 0.000 | 0.900 | 0.000 |
| provenance_sha_mismatch | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| provenance_source_row_changed | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| provenance_transformation_removed | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| provenance_unrecorded_value | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| row_duplicate_observation | 0.000 | 1.000 | 1.000 | 0.000 | 0.700 | 0.000 |
| row_duplicate_source | 0.000 | 1.000 | 1.000 | 0.000 | 0.846 | 1.000 |
| row_impossible_coordinate | 0.000 | 1.000 | 0.000 | 0.000 | 0.692 | 0.692 |
| row_malformed_numeric | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| row_negative_arms | 0.000 | 1.000 | 1.000 | 0.308 | 0.000 | 1.000 |
| row_negative_height | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| schema_category_changed | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| schema_column_renamed | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| schema_null_identifier | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| schema_numeric_string | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| schema_required_removed | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 |
| schema_unit_removed | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 |
| spatial_coordinates_swapped | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 |
| spatial_crs_mislabeled | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| spatial_crs_removed | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| spatial_invalid_geometry | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| spatial_other_plot_coordinates | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 |
| spatial_outside_plot | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 |
| temporal_arm_collapse | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 1.000 |
| temporal_dead_to_alive | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 1.000 |
| temporal_duplicate_event | 0.000 | 1.000 | 1.000 | 0.100 | 1.000 | 1.000 |
| temporal_height_decrease | 0.000 | 0.000 | 0.000 | 0.800 | 0.000 | 1.000 |
| temporal_identity_reassignment | 0.000 | 0.700 | 1.000 | 0.000 | 0.000 | 0.000 |
| temporal_positive_growth | 0.000 | 0.900 | 0.000 | 1.000 | 0.000 | 1.000 |
| temporal_year_swap | 0.000 | 0.000 | 1.000 | 0.800 | 0.000 | 0.000 |

An intervention may be detected by several layers. Pairwise overlaps are in `corruption_benchmark_overlap.csv`; seed recall standard deviation is population standard deviation across the executed seeds. `data/benchmark/alerts.parquet` preserves each new alert and matching decision. Ground truth includes every changed cell/row, original values, affected history IDs, seed and scenario.

## Interpretation

Context-only detections (both conventional baselines missed, at least one contextual layer detected):


| validation_group | injected | detections | misses | recall |
| --- | --- | --- | --- | --- |
| conventional | 330 | 183 | 147 | 0.555 |
| contextual | 330 | 303 | 27 | 0.918 |
| all | 330 | 320 | 10 | 0.970 |

- `schema_unit_removed`
- `temporal_dead_to_alive`
- `temporal_height_decrease`
- `temporal_arm_collapse`
- `temporal_year_swap`
- `spatial_outside_plot`
- `spatial_crs_mislabeled`
- `spatial_invalid_geometry`
- `spatial_other_plot_coordinates`
- `provenance_source_row_changed`
- `provenance_sha_mismatch`
- `provenance_transformation_removed`
- `provenance_unrecorded_value`
- `temporal_identity_reassignment`
- `temporal_positive_growth`

Synthetic scenarios show capabilities and blind spots under specified interventions; they do not estimate natural source-error frequency, identify true biological anomalies, or prove that one validator universally dominates. Statistical growth screening depends on eligible comparison pairs. Missing empirical spread or ineligible pairs may produce legitimate misses.

A detection is not automatically a source error. Height and arm decreases can be biologically real. Explicit dead/alive contradictions may reflect field classification, linkage or transcription. Synthetic interventions test detector capabilities, not ecological plausibility; temporal validators are screening tools. Context-aware validation detects not only malformed data, but also transitions whose interpretation depends on scientific context. Legacy corruption_id/corruption_class column names and benchmark corruption CLI syntax remain for compatibility; scenario_semantics identifies integrity interventions, semantic contradictions, plausible biological transitions and statistical anomalies.

Canonical values are changed while their stored provenance snapshots usually remain unchanged. Snapshot mismatch therefore measures cross-table consistency recovery, not whether the original source was scientifically correct. For a simulated biological transition, a snapshot mismatch does not imply that the changed measurement is biologically invalid. Coherent alteration of source, canonical and provenance values is outside this experiment.

The benchmark never alters `data/processed` or raw artifacts. `run.json` records source/configuration/implementation hashes. Hash equality of primary processed inputs was verified after execution.

## Informational CRS screen

10 injected CRS removals were recognized by the existing UNKNOWN_SPATIAL_CRS informational finding. These are reported separately rather than relabeled as warnings/errors. Primary recall above excludes informational collection diagnostics. The apparent CRS-removal misses in that primary table therefore describe severity-filtered recovery, not absence of a detector.
