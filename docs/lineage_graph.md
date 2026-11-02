# Executable evidence lineage

The lineage graph is a derived query/visualization layer over the raw manifest,
canonical/provenance tables, source inventory, entity tables and validation
findings. These tables remain authoritative. There is no external graph service
or new required dependency. Typed nodes and edges are stored in local SQLite for
bounded traversal and exported to Parquet; JSON, GraphML and CSV are supported.

## Reproduce and query

```powershell
saguarodata validate
saguarodata lineage build
saguarodata lineage export --format graphml
saguarodata lineage export --format json
saguarodata lineage export --format parquet
saguarodata lineage trace --observation-id fbc090fb9c5184f1043c1027 --field height_m
saguarodata lineage trace --finding-id <finding_id> --output data/lineage/trace.json
```

`finding_id` is a deterministic content ID in `validation_findings.parquet`, not
the browser's positional finding index. Look up an actual temporal example:

```python
import saguarodata as sd

ds = sd.load("data/processed")
graph = ds.lineage_graph()  # Builds once if absent; checks canonical hashes if cached.
finding = ds.validation_findings().query("rule_id == 'TEMPORAL_SHRINKAGE'").iloc[0]
trace = graph.trace_finding(finding.finding_id)
value = graph.trace_field(finding.entity_identifier, "height_m")
print(value["normalized_value"])
print(graph.upstream(value["root"]))
print(graph.downstream(value["root"], max_nodes=100))
```

Trace results are ordinary JSON-compatible dictionaries. Traversal has a bounded
node budget and explicitly returns `truncated=True` when it cannot include all
reachable nodes. Cached graphs reject changed canonical inputs until rebuilt.
Do not run concurrent builders on the same graph folder. Rebuild uses a separate
temporary database and publishes it after construction; Windows read connections
are closed after each query to permit replacement.

## Node and edge semantics

IDs use namespaced deterministic hashes of existing artifact, row, observation,
field and finding identities. Nulls and NumPy scalars are canonicalized before
hashing so report slices and full graphs share node IDs. Transformation identity
includes the recorded operation/input/output; conflicting records remain distinct.
Edges are deterministic hashes of source, target and semantic edge type.

Every edge points **from evidence toward the derived result**:

| Edge | Meaning |
|---|---|
| reference → artifact (`references`) | NPS reference lists the downloaded artifact |
| artifact → sheet → row → source field (`contains`) | Recorded physical evidence hierarchy |
| source field → transformation (`transformed_by`) | Recorded input is used by this transformation |
| row → transformation (`uncollected_or_unmapped_input`) | Provenance explicitly lacks a source column; no source cell is invented |
| transformation → canonical field (`derives`) | Recorded operation produces the normalized value |
| row → canonical field (`row_lineage_only`) | Row origin is known, but no field-level transformation is recorded |
| canonical field → observation (`belongs_to`) | Value is a field of this canonical record |
| row → observation (`represents`) | Authoritative row/feature lineage, independent of whether cell mappings exist |
| organism/plot/event → observation (`has_observation`) | Explicit foreign-key context, not inferred identity |
| source geometry feature → plot (`geometry_for`) | Recorded `geometry_source` supplying the plot boundary; spatial traces retain its source evidence |
| current observation → finding (`triggered`) | Finding's recorded target |
| explicitly named prior observation/feature → finding (`contributes`) | Additional evidence named in the finding's observed-value payload |
| relevant canonical field → finding (`validated_by`) | Existing value field involved in the rule |

The direct row-to-observation edge preserves row lineage for records and fields
without transformation records; it is not a redundant visualization shortcut.
Unsupported source columns remain visibly marked as missing/claimed mappings.
They are not certified source cells. Source metadata and serialized raw blobs
are represented by origin nodes rather than millions of extra metadata nodes;
`trace_field` can resolve these values directly from the authoritative canonical
table with an explicit source-row-only mapping label.

Supported node types are source_reference, source_artifact, source_sheet,
source_row, source_field, transformation, canonical_field,
canonical_observation, validation_finding, organism, plot and survey_event.
Spatial features use canonical_observation nodes with table=spatial_features.
Geometry values are represented by WKB byte length and SHA-256 in the graph;
the actual WKB remains in canonical Parquet and is not silently repaired.

For a temporal finding, upstream traversal includes both explicitly referenced
observations, their field values, transformations and original sources. Multiple
survey years can converge on the same historical workbook row. The graph does
not claim those years have independent source files or GPS fixes. It does not
guess predecessor observations when a finding provides no predecessor ID.

## Integrity and coverage

`saguarodata validate` adds distinguishable provenance-integrity checks:

- PROVENANCE_MISSING_SOURCE / SOURCE_ROW_MISMATCH
- PROVENANCE_HASH_MISMATCH / MISSING_SOURCE_SHEET / SOURCE_FIELD_MISSING
- PROVENANCE_MISSING_TRANSFORMATION / LINEAGE_MISMATCH / VALUE_MISMATCH
- PROVENANCE_CONFLICTING_TRANSFORMATION / ORPHAN_TRANSFORMATION / ORPHAN_FINDING

These are evidence-integrity findings, separate from scientific plausibility
findings. A normalized field is expected to have the existing adapter's declared
trace: height, arms and status plus coordinate-pair transformation where present;
vegetation count and withheld cover; aggregate count estimate and density.
The coordinate pair counts as one expected transformation group, but has two
canonical field nodes. Other fields can have row lineage only.

`reports/lineage_summary.md` records executed node/edge counts, row-origin coverage,
expected normalization groups with transformation records, verified source-column
and value-snapshot coverage, finding evidence coverage, dangling-edge counts and
the actual longest evidence-flow path. Finding source-row coverage and strict
field-level transformation coverage are reported separately. Neither measures
scientific truth or validates missing biological identity.

The real audit found 9,296 Section 17 status traces naming `Comments`, absent
from the 2011 source sheet. The canonical/provenance records are preserved; these
are emitted as PROVENANCE_SOURCE_FIELD_MISSING and reduce verified field coverage.
This is a mapping/auditability gap, not evidence that 9,296 biological statuses
are erroneous. Full-field cell mappings for other canonical attributes are not
invented to inflate coverage.

## Interactive evidence slices

Run `saguarodata report` and serve `reports/`. Observation drawers include
**Explore executable evidence lineage** with a field selector and JSON export.
Each finding has **Trace finding evidence**, which loads explicitly named prior
records and shows separate source → transformation → canonical-value branches.
Shared artifacts and their SHA/NPS reference are shown together. Missing inputs
are called out instead of omitted silently.

The report uses compact static slices from the same `evidence_trace` builder and
IDs as the full graph, embedded in the existing detail shards. No giant global
graph is sent to the browser. Ordinary report generation needs no SQLite graph
build; the slice is derived directly from the same authoritative tables.
Report slices omit unselected/unmapped scalar fields to stay compact, while the
Python graph supports larger upstream/downstream exploration. Parquet node/edge
attributes are JSON strings; GraphML attributes are likewise scalar JSON text,
so no NetworkX or graph server is required for export round-trips.
