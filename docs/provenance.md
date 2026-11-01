# Provenance and reproducibility

`data/raw/manifest.json` records each artifact's NPS reference, landing page, discovered download URL, original name, MIME type, UTC download time, byte count, SHA-256, and archive name. Files live below dataset/checksum/original-name. Downloading changed upstream bytes adds a version rather than overwriting earlier bytes. A matching existing file is verified before reuse. `download --refresh` checks upstream again; an ordinary cached build avoids unnecessary downloads. A clean checkout with the manifest but no raw files downloads missing artifacts.

Manifest updates use atomic replacement. Download one writer at a time; simultaneous manifest writers are not supported. Content hashes verify bytes, not scientific correctness. Network failures identify the affected artifact and leave acquired data available. Raw data are ignored by Git to avoid committing large artifacts; retain the manifest and independently back up raw bytes if upstream availability is a concern.

Discovery starts at the NPS monitoring page and visits the public `GetHoldings` metadata endpoint used by the DataStore interface. The catalog includes every holding, including reports, and records unavailable records. Snapshots live in interim storage. They are discovery aids, not immutable artifact versions.

Excel readers disable implicit conversion of strings such as NA to null. Canonical `raw_values_json` preserves the original cell values as string representations with source column names. It is not a replacement for the original Excel file: formula/cell formatting and exact numeric encodings remain in the immutable workbook. One-based source rows are physical Excel rows, not DataFrame offsets. Spatial source_row is a one-based feature ordinal within source_sheet/layer; geometry bytes are stored separately as WKB.

The `provenance` table records important field transformations, value kind (normalized or inferred), source column/value, normalized value, artifact hash and original row. Historic raw unit is null because its workbook header has no unit; `height_normalization_unit=m` and `unit_source=inferred` express the interpretation. No values have `corrected` kind because no corrections are applied. Future adjudications should be a separate versioned correction ledger, not changes to source files.

```python
import saguarodata as sd
ds = sd.load()
observation = ds.observations(program='historic_plots').iloc[0]
print(ds.provenance(observation_id=observation.observation_id))
print(ds.provenance(table='vegetation_observations',
                    observation_id=ds.table('vegetation_observations').iloc[0].observation_id))
```

`build_metadata.json` records selected input hashes, package versions, configuration hashes and implementation hashes. `requirements-lock.txt` records the tested environment. Observation IDs hash source content, physical row, program and year; changing an upstream artifact can change its IDs intentionally. Configured collections are exported to `protocol_fields.parquet`; source snapshots and explicit schema changes are separate tables.

The default build selects the latest acquired artifact per discovered download URL. Older bytes remain available in raw storage and the manifest. To reproduce a historical selection, restore that build's manifest and matching raw artifacts before running the offline build commands. This package does not promise to reconstruct a vanished upstream artifact from its checksum alone.

## Fresh acquisition audit

On November 1, 2026, `python scripts/check_reproducibility.py` verified the primary cached raw bytes, independently rediscovered the live NPS holdings, and downloaded all 25 artifacts to an isolated root under ignored interim storage. All URL/SHA-256 pairs matched the baseline manifest. The isolated inventory/build/schema-evolution/validation pipeline then reproduced the baseline tables below, comparing full DataFrames after sorting by stable entity ID:

| Canonical table | Matching rows |
|---|---:|
| organism_observations | 63,432 |
| organisms | 3,169 |
| plot_observations | 340 |
| vegetation_observations | 1,554 |
| spatial_features | 86,901 |

All 8,412 validation findings matched on rule, severity, table, entity identifier and message, independently of presentation ordering. This audit does not assert equality of every metadata table, acquisition timestamps, build metadata, or Parquet file bytes across dependency versions. The fresh pull and derived comparison passed without changing the primary raw manifest, processed tables or served app. Its local result is `data/interim/reproducibility_check.json`; the script can be rerun against an existing baseline build.

Geographic context is a separate bundled presentation snapshot with its own source queries and hashes; normal research-data acquisition does not refresh it. Live terrain imagery can change independently of the research data. See [geographic context and terrain](interactive_report.md#geographic-context-and-terrain).
