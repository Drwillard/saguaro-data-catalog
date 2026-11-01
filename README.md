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

The bundled map context is part of the source assets. `saguarodata all` does not refresh it. To refresh it separately, follow the cache and acquisition instructions in [Geographic context and terrain](docs/interactive_report.md#geographic-context-and-terrain), then run `saguarodata report`. Live terrain images are contextual and are not reproducible historical research inputs.

Optional browser checks require Playwright and an installed Microsoft Edge browser, plus the running HTTP server:

```powershell
python -m pip install playwright
python scripts/check_explorer.py
```

[Build results](reports/results.md) contain counts, rule frequencies, ten source-linked examples, limitations and supported conference claims. [Source inventory](reports/source_inventory.md) enumerates all parsed sheets/layers; its Parquet counterpart includes per-column missingness, inferred types, categories, candidate IDs and units.

The acquired public records cover Census, Historic Plots, Section17, vegetation subplots, plot boundaries/corners, and Ecotone. The Census workbook includes core and auxiliary sampling frames; they remain distinct. `plot_observations` preserves aggregate representations, normalized source count estimates and densities. The 1990 Census contains density-derived fractional estimates, not individual cactus records. Historic's shared rows support individual histories **except plot 71G**, where the original report explicitly documents failed tracking. Source duplicate identifiers further restrict temporal checks. Section17 has no verified cross-round individual crosswalk.

Vegetation 1990 workbook sheets are header-only. Its historical mapped attributes are preserved in `spatial_features`; the 2000/2010 tabular summaries are in `vegetation_observations`. These representations are not appended as independent duplicate measurements. Two 2020 Census reports were downloaded, but no raw individual workbook was exposed by the inspected holdings. Historic's coordinate columns are a shared source location, not independent GPS measurements in every year: this dataset cannot support a real temporal-displacement result.

The report does not claim confirmed resurrection, confirmed source errors, or ecological conclusions. Unresolved cover units, inferred Historic height units, ambiguous zero heights, missing spatial references, inconsistent plot descriptions and dated free-text notes are visible limitations. See [protocol evidence](docs/protocol_differences.md), [canonical schema](docs/canonical_model.md), [validation rules](docs/validation_rules.md), [provenance](docs/provenance.md), and [research notes](docs/research_notes.md).

## Repository

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
