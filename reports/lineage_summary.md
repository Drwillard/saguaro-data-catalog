# Lineage graph summary

Derived evidence-flow node/edge tables; canonical tables and the raw manifest remain authoritative. SQLite is a local index over typed tables, not an external graph service. Parquet exports are the portable graph representation.

| Node type | Count |
|---|---:|
| canonical_field | 3,023,324 |
| canonical_observation | 152,227 |
| organism | 3,169 |
| plot | 610 |
| source_artifact | 25 |
| source_field | 196,882 |
| source_reference | 15 |
| source_row | 145,325 |
| source_sheet | 763 |
| survey_event | 26 |
| transformation | 223,852 |
| validation_finding | 17,708 |

| Edge type | Count |
|---|---:|
| belongs_to | 3,023,324 |
| contains | 342,970 |
| contributes | 502 |
| derives | 243,094 |
| geometry_for | 165 |
| has_observation | 140,041 |
| references | 25 |
| represents | 152,227 |
| row_lineage_only | 2,780,230 |
| transformed_by | 210,458 |
| triggered | 17,708 |
| uncollected_or_unmapped_input | 13,394 |
| validated_by | 20,777 |

## Provenance coverage

- observations: 65,326
- observations_row_lineage_complete: 65,326
- expected_normalized_fields: 223,852
- normalized_fields_with_transformation: 223,852
- normalized_fields_with_verified_source_mapping: 214,556
- observations_complete_field_lineage: 56,030
- observations_all_expected_transforms: 65,326
- canonical_fields_without_explicit_mapping: 2,258,824
- findings: 17,708
- findings_complete_source_row_lineage: 17,708
- findings_complete_evidence_lineage: 6,300

Orphan edges: 0; longest recorded evidence-flow path: 8 edges; nodes without a resolved acyclic depth: 0.

Row-lineage completeness means an existing manifest artifact, inventoried sheet/layer and physical source row are recorded. Transformation coverage is measured separately for explicitly normalized fields. Other canonical fields retain source-row lineage only; no cell-level transformation is invented. Coverage is not proof that the recorded source values are correct.

## Example observation traces

- `ef61b89ddc3093bbfadf36df`
- `1182fbd52e7e57b5e7c5cbae`
- `b45230de82354ce6b5881656`

## Executed temporal finding trace

Finding `da7a103cd6d8ed6e4c574ef4` (`TEMPORAL_SHRINKAGE`) has 118 nodes and 206 edges in its upstream evidence slice.

Canonical records (including boundary context): `spatial_features/e25ddc69682f4e9c19d738fa`, `organism_observations/b2948765148316bd69993086`, `organism_observations/8d23997dd017594d7091a10c`

The trace includes each explicit contributing observation, its canonical fields, recorded transformations, source cells/rows, sheets, artifact SHA and NPS reference. Shared-row observations can legitimately converge on the same source row; this is not independent repeated GPS evidence.

Provenance-integrity findings are separately identifiable by `PROVENANCE_` rule IDs. Scientific findings remain review candidates, not verified errors. See `docs/lineage_graph.md` for semantics, expected transformation fields and remaining gaps.
