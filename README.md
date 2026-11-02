# saguarodata

Historical scientific datasets rarely retain one schema, sampling protocol, unit system or identifier scheme for decades. `saguarodata` is a Python research-software case study in making those changes explicit and reproducible, using Saguaro National Park monitoring records.

The package discovers official public holdings, preserves original bytes with SHA-256 provenance, inventories every spreadsheet sheet and shapefile layer, builds relational Parquet tables, and applies structural, temporal and spatial validation. Findings retain source lineage and remain review candidates. No anomalies are automatically corrected and no cross-survey cactus identities are invented.

## Rebuild

Python 3.11+; the recorded environment uses Python 3.12. From this repository:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-lock.txt
python -m pip install -e ".[dev]" --no-deps
saguarodata all
python -m pytest -q
```

This installs the recorded dependency versions; the lock was tested with Python 3.12 on Windows. For an unpinned development environment, use `python -m pip install -e ".[dev]"` instead. Network access is needed for discovery and first acquisition. Subsequent downloads verify cached raw bytes. To build entirely offline after acquisition:

```powershell
saguarodata inventory
saguarodata build
saguarodata validate
saguarodata report
```

`saguarodata sources list` prints the cached discovery catalog, discovering sources if none is present. `sources discover` refreshes metadata. `download --refresh` checks upstream bytes again and preserves changed versions. Every command accepts a project directory through the **global** option, e.g. `saguarodata --root C:\code\saguaro_new validate`.

`saguarodata all` and `saguarodata download` always run live discovery, even when the artifact bytes are cached. The four explicit offline commands above do not. A manifest-only checkout downloads missing files from the current upstream holdings; it cannot recover an older version that NPS no longer serves. For exact historical reconstruction, retain the matching raw artifacts along with the manifest, source revision, configuration and dependency lock. The default build selects the latest acquired version per download URL. Acquisition times and build metadata can differ between equivalent runs; byte-identical Parquet output across environments is not promised.

To audit a fresh acquisition against this checkout's existing build:

```powershell
python scripts/check_reproducibility.py
```

This verifies cached hashes, discovers and downloads sources into a separate directory under `data/interim/`, compares upstream artifact hashes with the baseline manifest, rebuilds there, and compares canonical observation, organism, aggregate, vegetation and spatial tables plus validation findings. It leaves the primary data and served reports unchanged. It uses live NPS services and retains its audit files in ignored interim storage.

Verified November 1, 2026: all 25 freshly downloaded artifact hashes matched. The isolated rebuild matched 63,432 organism observations, 3,169 linked organisms, 340 plot summaries, 1,554 vegetation summaries, 86,901 spatial features and 8,412 validation findings. All 32 offline tests passed. See [provenance and reproducibility](docs/provenance.md) for the scope and limitations of this comparison.

## Use the data

```python
import saguarodata as sd

ds = sd.load("data/processed")
print(ds.programs())
print(ds.surveys())
observations = ds.observations(program="historic_plots", year=2010)
linked = observations[observations.organism_id.notna()].iloc[0]
print(ds.history(organism_id=linked.organism_id))
print(ds.provenance(observation_id=linked.observation_id))
print(ds.validation_findings(severity="warning"))
print(ds.validation_findings(severity="warning", finding_category="biological_transition"))
# Every table is also an ordinary pandas DataFrame:
print(ds.table("vegetation_observations"))
```

DuckDB is optional:

```powershell
python -m pip install -e ".[duckdb]"
saguarodata duckdb
```

```python
with ds.duckdb() as conn:
    print(conn.sql("select program_id, count(*) from organism_observations group by 1").df())
```

Geometry is WKB plus an explicit CRS in Parquet/DuckDB; no DuckDB Spatial extension installation is required. Convert known-CRS geometries with GeoPandas/Shapely for spatial queries. Local-coordinate maps with no documented CRS are not treated as geographic data.

## Results and scope

Serve the interactive explorer locally:

```powershell
python -m http.server 8000 --bind 127.0.0.1 --directory reports
```

Open http://127.0.0.1:8000/data_quality_report.html. Click through sampling-frame and missingness summaries, linked before/after measurements, individual histories, findings, map positions and source profiles. Filtered CSV and full evidence JSON exports are available. The explorer uses local assets and bundled Tucson boundaries, roads and regional terrain snapshots. Optional live USGS topography and Esri shaded relief add terrain detail as you zoom; plain coordinates uses local assets only. It is regenerated by `saguarodata report` or `saguarodata all`; a [static fallback](reports/data_quality_report_static.html) remains available. See [interaction and interpretation details](docs/interactive_report.md).

On **Spatial view**, saguaro icons use progressively darker greens for one through four distinct survey rounds. Hollow gray cacti mean individual history is unknown. Hover shows exact counts and years; page year filters do not change the full-history count. Use **Tucson region** for the park/city overview, **Fit selected records** for the filtered cacti, and the layer checkboxes for roads, boundaries and labels. Topographic contours describe ground elevation; cactus height is a separate measurement.

**Photos & original sources** links to NPS/USGS historical landscape photography and 548 iNaturalist photos from 300 observations in the separate morphology pilot. Search photo IDs, observation IDs or photographer attribution, filter licenses, and export original-source links as CSV. The app does not download or embed these photographs. Nine physical NPS source rows mention photos without supplying verified image URLs; these references open their observation evidence and original workbook. No photo-to-NPS-individual crosswalk is inferred. See [photo sources and link metadata](docs/photo_sources.md).

The bundled map context is part of the source assets. `saguarodata all` does not refresh it. To refresh it separately, follow the cache and acquisition instructions in [Geographic context and terrain](docs/interactive_report.md#geographic-context-and-terrain), then run `saguarodata report`. Live terrain images are contextual and are not reproducible historical research inputs.

Optional browser checks require Playwright and an installed Microsoft Edge browser, plus the running HTTP server:

```powershell
python -m pip install playwright
python scripts/check_explorer.py
```

[Build results](reports/results.md) contain counts, rule frequencies, ten source-linked examples, limitations and supported conference claims. [Source inventory](reports/source_inventory.md) enumerates all parsed sheets/layers; its Parquet counterpart includes per-column missingness, inferred types, categories, candidate IDs and units.

The acquired public records cover Census, Historic Plots, Section17, vegetation subplots, plot boundaries/corners, and Ecotone. The Census workbook includes core and auxiliary sampling frames; they remain distinct. `plot_observations` preserves aggregate representations, normalized source count estimates and densities. The 1990 Census contains density-derived fractional estimates, not individual cactus records. Historic's shared rows support individual histories **except plot 71G**, where the original report explicitly documents failed tracking. Source duplicate identifiers further restrict temporal checks. Section17 has no verified cross-round individual crosswalk.

Vegetation 1990 workbook sheets are header-only. Its historical mapped attributes are preserved in `spatial_features`; the 2000/2010 tabular summaries are in `vegetation_observations`. These representations are not appended as independent duplicate measurements. Two 2020 Census reports were downloaded, but no raw individual workbook was exposed by the inspected holdings. Historic's coordinate columns are a shared source location, not independent GPS measurements in every year: this dataset cannot support a real temporal-displacement result.

Finding category distinguishes integrity violations, semantic contradictions, biological transitions, data-quality warnings and information; severity remains a separate review priority. Observation drawers show temporal pairs side by side with original notes, status basis, measurements and Verify context. The Historic Verify cell is shared by several survey rounds, not evidence of independent per-year verification. Descriptive notes do not become formal life/death status.

The executed [temporal interpretation](reports/temporal_interpretation.md) includes per-rule context counts and source-checked L130/L167 histories, with CSV/JSON companions. The current build has 502 temporal findings, including 94 height decreases, 226 arm decreases and zero explicit dead-to-alive contradictions. Decreases can reflect real breakage; positive height after death can describe a standing dead cactus. No finding automatically proves a source error or ecological conclusion. Unresolved cover units, inferred Historic height units, ambiguous zero heights, missing spatial references, inconsistent plot descriptions and dated notes remain visible limitations. See [protocol evidence](docs/protocol_differences.md), [canonical schema](docs/canonical_model.md), [validation rules](docs/validation_rules.md), [provenance](docs/provenance.md), and [research notes](docs/research_notes.md).

## Synthetic intervention benchmark and evidence graph

The project compares conventional validation with identity, temporal, spatial and
provenance context using 30 deterministic synthetic intervention scenarios. Trials
run on isolated canonical copies, subtract unchanged-cohort findings, and preserve
ground truth and detector outcomes. Results are benchmark evidence, not ecological
conclusions or estimates of natural source-error prevalence.

`scenario_semantics` separates integrity interventions, plausible biological transitions, semantic contradictions and statistical anomalies in configuration, truth and results. Height/arm loss is screened without calling it intrinsically invalid. The legacy corruption CLI and ID fields remain supported; TEMPORAL_RESURRECTION input aliases resolve to TEMPORAL_STATUS_CONTRADICTION, the warning emitted for conflicting explicit dead/alive records.

```powershell
saguarodata validate
saguarodata benchmark corruption --seeds 1,2,3 --count 100 --sample-size 1200
saguarodata benchmark corruption --seed 42 --count 30 --sample-size 1200 --intensity 0.25 --append
saguarodata benchmark report
saguarodata lineage build
saguarodata lineage export --format graphml
saguarodata lineage trace --observation-id fbc090fb9c5184f1043c1027 --field height_m
saguarodata report
```

Run validation **before** the benchmark and graph build; do not change the normal
processed tables while either is running. `--sample-size 0` benchmarks the entire
corpus. Count controls independent injected trials, not simultaneous damage density.
The real-data provenance audit found 9,296 status traces naming an absent source
column; these are mapping review findings, with no source or canonical value
silently repaired. Total findings after the added checks: 17,708.

```python
graph = ds.lineage_graph()
trace = graph.trace_field(observation_id, "height_m")
finding = ds.validation_findings().query("rule_id == 'TEMPORAL_SHRINKAGE'").iloc[0]
evidence = graph.trace_finding(finding.finding_id)
```

Observation drawers offer **Explore executable evidence lineage**; finding cards
offer **Trace finding evidence**, including explicitly referenced prior records.
The graph uses typed local tables and streaming exports, with no graph server or
new runtime dependency. Canonical/provenance tables remain authoritative.

Read [benchmark methods](docs/corruption_benchmark.md), [graph semantics and gaps](docs/lineage_graph.md),
[executed benchmark results](reports/corruption_benchmark.md), and
[executed lineage coverage](reports/lineage_summary.md). Large benchmark/graph files
live under ignored `data/benchmark/` and `data/lineage/`; small reports can be tracked.

## Repository contents

Track `src/` (including bundled map JSON/JPEG assets), `configs/`, `tests/`, `scripts/`, `docs/`, `notebooks/`, `.gitignore`, `pyproject.toml`, `requirements-lock.txt`, `README.md`, `LICENSE`, `CITATION.cff`, and `data/raw/manifest.json`. The small generated `data/processed/build_metadata.json`, static report, results, inventory and repository-tree snapshots can also be retained as review evidence; regenerate them when source inputs or relevant code change.

`.gitignore` excludes environments, wheel/build caches, original raw artifact directories, interim/external downloads, processed Parquet/DuckDB, server logs and generated interactive assets. It also excludes `reports/data_quality_report.html`, whose `reports/explorer/` data is generated locally. A fresh checkout must run the rebuild before serving the interactive app. The tracked static fallback can be read without that generated data. Original downloaded data should be backed up outside Git if historical byte recovery matters.

```text
configs/                 source discovery, collection semantics, validation thresholds
data/raw/manifest.json   checksummed artifact/version manifest; original files untracked
data/interim/            discovery pages, report text, extracted spatial layers
data/processed/          canonical Parquet, schema history, build metadata, optional DuckDB
docs/                    evidence, model, validation and provenance documentation
notebooks/               four reproducible API/report examples
reports/                 inventory, quality report, results, source catalog and tree
scripts/                 development reconnaissance/bootstrap utilities
src/saguarodata/
  acquisition/           public holding discovery and immutable downloads
  ingest/                explicit Excel, spatial and program-specific adapters
  model/                 canonical contracts
  normalize/             units, missing reasons and identifiers
  validation/            structural, temporal and spatial finding engine
  api/                   pandas access and optional DuckDB
  reports/               standalone HTML and machine-readable results
  pipeline.py            relational build and transformation lineage
  schema_history.py      source snapshots and explicit schema-evolution changes
  cli.py                 complete command-line pipeline
tests/                   offline unit/integration tests with synthetic acquisition
```

Full file listing: [repository tree](reports/repository_tree.txt). Software is MIT licensed; upstream data/reports retain their own rights. Cite both the software and the NPS sources used in your build.
