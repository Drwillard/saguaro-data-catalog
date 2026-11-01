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
| validation_findings | rule_id, severity, table, entity_identifier, survey_event, field, observed_value, expected_condition, message, source_lineage, status |
| schema_history | source file/sheet/round fields and documented collection changes; no inferred rename without explicit mapping |
| protocol_fields | program/nominal round/field collection semantics, source evidence and identity policy |
| coordinate_displacements | independently dated linked fixes only; source observation pair and geodesic distance |
| displacement_summaries | program/year interval counts, median, 95th percentile and maximum displacement |

`source_row_id` hashes the artifact checksum, sheet and physical row. Observation IDs add the source year/measurement context. Historic coordinates are stored as a shared source location, **not** repeated independent GPS measurements at each event. Temporal displacement is only calculated for independently dated coordinates. Geographic transformations require known CRS; unknown CRS remains unknown.

Historic heights are treated as meters based on the companion spatial representation's numeric agreement and the report's meter height classes. This unit assignment is recorded as **inferred**, with evidence; it is not a unit in the spreadsheet header. Census Height (m) and Section17 Height_m_ are documented in source columns. Exact raw values remain available. Zero Historic heights are retained as ambiguous measurements and excluded from growth estimates, not changed to null.

Missing reasons include source_missing (blank), unknown, not_measured, not_applicable, not_found, invalid_numeric, and not_collected. `NA` is retained as an ambiguous source token and is not automatically declared not_applicable. No correction is applied. Proposed inference is explicitly marked. Null organism IDs mean there is no defensible longitudinal identity, not that a plant was absent.
