# Validation rules

Findings are review candidates. Severity is error, warning or info; status is initially open, never automatically source_error. The supported adjudication vocabulary is open, explainable, source_error, normalization_error, unresolved. Source lineage and any previous observation identifier travel with each finding. No rule mutates normalized or raw data.

Structural checks cover required plot IDs, plot/event foreign keys, negative measurements, unparseable numeric tokens, noninteger arm counts, duplicate observation/source/organism-event keys, duplicate local Census IDs, categorical drift, inferred units, and explicitly unsupported 71G linkage. Categorical drift preserves exact source phrases. No maximum cactus height is hard-coded.

Temporal rules require a supported non-null organism_id and distinct survey events. Ambiguous duplicate organism/event records are excluded from temporal comparisons. TEMPORAL_STATUS_CONTRADICTION requires explicitly dead then explicitly alive; not_found and positive height do not count as life/death evidence. A measurement after explicit death has its own warning: standing dead cacti can still be measured. Notes saying 'dead 2014' in a 2010 column do not establish death in 2010.

Category describes the kind of issue; severity describes review priority. Both are stored on every finding and independently filterable in the API and explorer.

| finding_category | Meaning |
|---|---|
| integrity_violation | Declared schema, key, reference or evidence-chain constraint is breached |
| semantic_contradiction | Explicit statuses conflict for the same supported identity |
| biological_transition | A potentially real height/arm loss needs scientific context |
| data_quality_warning | Measurement, interpretation or coverage needs review |
| informational | Collection context or a status-resolution/reobservation event |

Height shrinkage and arm decreases remain warnings with unchanged thresholds, categorized biological_transition. Field breakage, measurement differences, unit problems, transcription and linkage remain possible explanations, not adjudicated causes. After-death measurements are data_quality_warning; robust growth outliers are statistical screens in that category. Reobservation after not_found and unknown-to-alive resolution are informational with info severity. Prior absence is not death.

Every temporal finding carries both observation IDs, years, heights, arms, normalized/raw status and status basis, original notes, operational tags, and normalized/raw Verify with its time basis. Historic Verify is shared physical-row context, not an independent verification for each year. Exact operational phrases are parsed separately from formal status; descriptive prose such as fairtop thin, damaged, poor or leaning remains unknown status. See the canonical model for the literal phrase vocabulary.

Migration: TEMPORAL_RESURRECTION is retained only as an input alias for TEMPORAL_STATUS_CONTRADICTION in finding creation, API rule filters and explorer deep links. Newly generated findings use the new rule ID, warning severity and semantic_contradiction category; no literal biological reversal is claimed. Old Parquet findings without a category receive one when read through Dataset.validation_findings(). Rebuild and validate to persist the new schema and paired evidence.

Shrinkage requires both the absolute decrease and proportional decrease in `configs/validation_rules.yaml`. It is a warning: broken tops are possible. Arm decreases are warnings because breakage is possible. Historic zero heights remain zero but are excluded from height-pair comparisons because their sentinel semantics are unresolved. Growth outliers use the median plus six robust standard deviations (1.4826 MAD, IQR/1.349 fallback), within program/year intervals; groups smaller than the configured minimum and groups with zero spread are not tested. These are screening thresholds, not biological limits.

Spatial rules cover geographic ranges, a configurable vicinity rectangle (not official park boundaries), exact-matched plot containment including boundaries, duplicate event coordinates, independently dated linked-organism displacement, invalid/null geometries, CRS coverage, and differing Section17 grid geometries. Subplot containment requires an explicit parent_plot_id and compatible known CRS. No parent relation or georeferencing is inferred. Missing CRS is reported once per layer with affected feature count. Invalid WKB is retained as a null geometry with attributes and an explicit finding; no automatic geometry repair occurs.

The displacement threshold is configurable. Eligible geodesic distances and interval-specific median, 95th percentile and maximum are exported to `coordinate_displacements` and `displacement_summaries`. The current real data have no independent event-specific coordinate pairs for linked organisms, so only fixture-based displacement behavior is demonstrated. No empirical movement distribution is claimed. Shared Historic coordinates are excluded. The report displays coverage to distinguish untested data from passing data.

Plot geometry disagreement uses the configurable symmetric-difference area fraction. It is only applied where two source layers have the same documented Section17 grid label and CRS. The canonical plot table uses the Grids representation; the alternative remains in spatial_features.

Not implemented as automatic scientific conclusions: broad taxonomic synonym reconciliation, inferred individual matching, automatic cover-unit correction, full reconciliation of every plot geometry representation, and local-coordinate subplot georeferencing. These require additional evidence.
