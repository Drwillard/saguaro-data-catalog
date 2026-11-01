# Interactive research explorer

Run `saguarodata report` after building and validating the canonical data. This writes the interactive entry point `reports/data_quality_report.html`, a self-contained static fallback `reports/data_quality_report_static.html`, and local assets and data shards in `reports/explorer/`. It does not change canonical or raw data.

Serve the **reports directory**, preserving its `explorer/` subdirectory:

```powershell
python -m http.server 8000 --bind 127.0.0.1 --directory reports
```

Open http://127.0.0.1:8000/data_quality_report.html. Interactive data files are loaded with HTTP requests; use the static fallback when opening files directly from disk. The explorer uses no external JavaScript libraries, analytics or CDN scripts. The Spatial view uses bundled geographic layers and regional terrain snapshots. With a terrain background selected, it requests map images from USGS (topographic) or Esri (shaded relief) for the visible extent; plain coordinates uses local assets only. Source links open the cited providers.

## Paths through the evidence

- **Overview:** sampling-frame bars filter the corpus; coverage cells open the corresponding frame/year records. Numeric, missing/unknown and not-collected values have separate encodings. No observed records is not rendered as a zero measurement.
- **Linked changes:** before/after scatterplots compare the same source-supported individual. The diagonal means unchanged measurement, not expected biological growth. Choose an interval and compare heights, arm counts or annualized growth; click a pair for the later source record and its full history. Colors correspond to the validation finding for that exact prior/later pair.
- **Records & histories:** inspect all observations, search plot/tag/record IDs, filter availability, sort columns, export matching rows, hover/select scatter points, or drag a rectangle to zoom. Only supported identities have a connected history; 71G and unlinked censuses do not.
- **Plot & vegetation:** inspect plot aggregate representations and taxon/plot/round summaries separately. Original fractional count estimates remain fractional. Do not add overlapping aggregate representations as independent samples. Vegetation count/stem and cover labels retain their source meaning; normalized cover is withheld pending unit evidence.
- **Validation findings:** filter rule and severity, then drill into any finding rather than a curated sample. Rule/severity filters apply to this register only; frame/year filters apply across record and finding views. Source profiles always cover whole source tables and use the frame/source-search filters, not the year filter. Spatial-layer findings with no event year are excluded when a year is selected.
- **Spatial view:** pan/zoom source-derived geographic coordinates, overlay known-CRS plot polygons, color by frame or most severe finding, and select co-located records. The map is an equirectangular coordinate view (longitude scaled at 32.2°N) with optional geographic context. Display polygons are simplified to 0.000005°; canonical/source geometry remains unchanged. Unknown-CRS maps are not guessed into place. Historic source positions are not independent event-specific GPS fixes.
- **Sources & schemas:** search all workbook sheets/layers, inspect original headers and column profiles, expand literal categories and explicit schema changes, and inspect immutable artifact hashes and NPS references.

Every observation drawer provides source file/hash/sheet/physical row, raw source cells, normalized values, transformation kind, applicable findings, and any source-supported history. Clickable history points select the corresponding observation. Raw and normalized values are separate evidence views. Full evidence can be downloaded as JSON. Observation, finding, linked-pair and summary registers export filtered CSV. Row IDs in CSV link back to the full evidence; CSV is a view export, not a replacement for canonical Parquet.

`Copy view link` and record links retain filters and the selected entity in the URL fragment. Links are local to the same served build; content-addressed observation IDs can change when source bytes change. Chart viewport pan/zoom is exploratory and is not encoded in the link.

## Interpretation and performance

Spatial markers are saguaro silhouettes. With **Survey observation count** selected, green shading encodes the number of distinct observed survey rounds: one round is light green, two and three use intermediate shades, and four use the darkest green. The legend reports each count separately. Hollow gray cacti indicate unsupported individual continuity, including 71G and Section 17; these are not treated as one-round histories. Sampling-frame and finding-severity colors remain selectable and replace the count colors. Hover lists exact counts and present/absent years. Distinct rounds count once, including explicit death/status records; field completeness is not the criterion. Missing rounds do not imply death. A thin outline and pale halo keep the cactus silhouette legible on terrain backgrounds.

Each linked cactus is drawn once at its latest visible source location. Its coverage is calculated from the full linked history, unaffected by the year filter; filtering to 2014 does not turn a four-round history into a one-round history. Historic Plots has four available individually represented rounds: 1975, 2001–2002 (source label 2001), 2010 and 2014. Unlinked observations retain separate markers; co-location never creates a history or an individual identity. Asset URLs include content hashes to avoid stale cached marker code after report regeneration.

Overview counts refer to organism observation records, not park population estimates or independent samples. A record can trigger multiple findings. The finding total also includes spatial-layer checks and information-level findings. The count of distinct flagged organism observations has its own denominator.

Linked height pairs exclude null/nonpositive endpoints, duplicate organism/event records, and unsupported identities. History lines also break at unresolved zero endpoints and duplicate years. Individual histories ignore the page's year filter so context is not accidentally hidden. Source year 2001 in Historic Plots labels the 2001–2002 field round; growth denominators use that nominal source year and retain this timing uncertainty.

The initial index contains the complete organism corpus and finding register, not a sample. Full raw rows and field provenance are split into content-addressed-prefix JSON shards and fetched on demand. Detailed source column profiles load only in the source view. Canvas charts avoid tens of thousands of DOM elements; accessible tables provide the same selectable records. Files are generated locally and excluded from Git.

`reports/explorer/manifest.json` records canonical-input and presentation-asset hashes, entity counts and linked-pair counts. This distinguishes a presentation rebuild from the earlier canonical build recorded in `data/processed/build_metadata.json`.

## Verification

Offline pytest fixtures exercise source acquisition through interactive export, including raw lineage, supported pairs, null/zero semantics and static fallback generation. Optional real-browser checks use an installed Edge browser:

```powershell
python -m pip install playwright
python scripts/check_explorer.py
```

The check script assumes the supplied real-data build and running local server, then tests filtering, paired-point selection, source and history drill-downs, deep-link reloads, CSV/JSON exports, co-location/zoom, missingness semantics, separate aggregates/vegetation, and mobile overflow. Its screenshots and check results are generated under `reports/explorer/qa/`. Browser tooling is a development aid and is not a runtime dependency.

## Geographic context and terrain

Spatial view defaults to **Topographic · USGS**. Use **Shaded relief · mountains** for terrain shape, or **Plain coordinates** for the local coordinate view. **Tucson region** shows both Saguaro districts and the city; **Fit selected records** returns to the filtered cactus locations. Toggle park boundaries, Tucson city limits, roads, study plots and labels independently. Local roads and road names appear as you zoom in. A local distance scale is approximate at the map latitude.

The bundled geographic snapshot uses the NPS `SAGU_Boundary` layer from [Saguaro tract and boundary data](https://irma.nps.gov/DataStore/DownloadFile/754039), [Census incorporated places](https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/4) filtered to Arizona / Tucson city, and [Census primary, secondary and local roads](https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Transportation/MapServer) intersecting longitude -111.30 to -110.45 and latitude 32.00 to 32.43. Roads are clipped to that extent and grouped by source name and road class. Display geometry is simplified by 0.00002 degrees for boundaries and 0.000015 degrees for roads; coordinates are rounded to six decimal places. These are current contextual features, separate from canonical research tables, and do not establish historical park boundaries or individual cactus identities.

Terrain backgrounds come from [USGS The National Map](https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer) and [Esri World Shaded Relief](https://services.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer). Bundled regional JPEG snapshots remain available if live services fail; at close zoom their detail is limited. Live geographic exports use each service's **returned extent**, accounting for its adjustment of the requested aspect ratio, to align with observation coordinates. Image requests follow pan/zoom after a short debounce. Browser memory retains a small cache. No research observation attributes are sent; requests include only the map extent and image size.

Topographic contours describe ground elevation in the units printed on the map. Shaded relief describes terrain shape. Neither supplies a measured ground elevation for an individual cactus; cactus height remains a separate research measurement. Boundary layers and the longitudinal history markers stay above the terrain background.

Run `python scripts/fetch_map_context.py` explicitly to build or refresh the geographic assets (delete the relevant files in `data/external/map_context/` first to refresh cached inputs). The script caches complete source responses, checks road pagination counts, and records query parameters, retrieval timestamps and raw response SHA-256 values in `geographic_context.json`. Report builds copy the bundled snapshot and never download geographic data. These assets are included in package data and presentation hashes.

View links retain the terrain background and regional/selected-record view. Free pan/zoom remains exploratory and is not encoded.
