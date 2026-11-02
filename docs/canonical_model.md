# Canonical model after source inspection

See `reports/source_inventory.md` and `data/processed/source_inventory.parquet` for actual source fields and missingness. The source-informed decisions and at least ten incompatibilities are in `protocol_differences.md`.

The model separates populations, organisms, observations, spatial representations, and lineage. IDs are deterministic namespaced hashes or explicit program/plot labels. All canonical observations carry file hash, file path, source sheet, original one-based Excel row, and NPS reference ID. A source row serialized as JSON preserves source fields before normalization.

| Table | Grain and fields |
|---|---|
| survey_programs | program_id, name, description, source_reference_id |
| survey_events | survey_event_id, program_id, survey_year, nominal_round, start_date, end_date, protocol_version, notes |
| plots | plot_id, program_id, canonical_plot_name, source_plot_id, district, area_m2, geometry (WKB), crs, geometry_source, spatial_precision |
| organisms | organism_id, program_id, plot_id, source_individual_id, linkage_evidence |
| organism_observations | observation_id, organism_id (nullable), survey_event_id, plot_id, survey_year, status, status_source, height_raw, height_unit_raw, height_m, height_missing_reason, unit_source, arm_count_raw, arm_count, arm_count_missing_reason, x, y, coordinate_crs, coordinate_time_basis, latitude, longitude, notes; source lineage |
| plot_observations | source plot/year aggregate representation, observation_id, survey_event_id, count_raw, count_estimate, density_raw, density_per_ha, missing reasons and original class boundaries; auxiliary summaries kept separate; no invented individuals |
| vegetation_observations | taxon/plot/year rows, count_raw, count, cover_raw, cover_unit_raw, area_m2, species_raw, species_name_raw; source lineage |
| spatial_features | source layer/feature, attributes_json, WKB geometry, original CRS and source lineage; separate from primary tabular observations |
| plot_identifier_map | source_dataset, source_value, canonical_value, mapping_method, confidence, evidence |
| organism_identifier_map | shared-row IDs only, with evidence and 71G exclusion |
| source_files | acquisition manifest records |
| provenance | observation_id, table, field, source_column, source_value, normalized_value, transformation, value_kind, source lineage |
| validation_findings | rule_id, finding_category, severity, table, entity_identifier, survey_event, field, observed_value, expected_condition, message, source_lineage, status |
| schema_history | source file/sheet/round fields and documented collection changes; no inferred rename without explicit mapping |
| protocol_fields | program/nominal round/field collection semantics, source evidence and identity policy |
| coordinate_displacements | independently dated linked fixes only; source observation pair and geodesic distance |
| displacement_summaries | program/year interval counts, median, 95th percentile and maximum displacement |

`source_row_id` hashes the artifact checksum, sheet and physical row. Observation IDs add the source year/measurement context. Historic coordinates are stored as a shared source location, **not** repeated independent GPS measurements at each event. Temporal displacement is only calculated for independently dated coordinates. Geographic transformations require known CRS; unknown CRS remains unknown.

Historic heights are treated as meters based on the companion spatial representation's numeric agreement and the report's meter height classes. This unit assignment is recorded as **inferred**, with evidence; it is not a unit in the spreadsheet header. Census Height (m) and Section17 Height_m_ are documented in source columns. Exact raw values remain available. Zero Historic heights are retained as ambiguous measurements and excluded from growth estimates, not changed to null.

Missing reasons include source_missing (blank), unknown, not_measured, not_applicable, not_found, invalid_numeric, and not_collected. `NA` is retained as an ambiguous source token and is not automatically declared not_applicable. No correction is applied. Proposed inference is explicitly marked. Null organism IDs mean there is no defensible longitudinal identity, not that a plant was absent.

Organism observations also retain `notes_source_column`, Boolean `tag_only`, `off_plot`, `not_measured`, `needs_review`, and `annotation_method=exact_operational_phrases_v1`. Parsing only trims/case-folds/collapses whitespace and normalizes dash variants, then matches whole phrases: tag only; off plot; not measured; off plot - not measured; need check. No broad damage classifier is used and original notes are unchanged. These flags never override formal status or measurement values. Formal status parsing is unchanged, including its survey-year guard on dated death notes.

`verification_raw` preserves the source Verify cell. `verification_status` is yes, no, not_found, not_recorded (blank), or unrecognized; `verification_source_column` names Verify when present. `verification_time_basis=shared_source_row` on Historic observations explicitly records that several survey rounds share one workbook cell; other represented Verify cells use source_record. Verify is review context, never a correctness label. The normalization is traced in provenance and the evidence graph.

Finding categories are integrity_violation, semantic_contradiction, biological_transition, data_quality_warning and informational. They are distinct from error/warning/info severity and from adjudication status. Temporal `observed_value` JSON includes paired IDs, years, measurements, statuses and their basis, original notes, operational flags and Verify values/scope. Categories and this evidence survive Parquet/API/report export.
