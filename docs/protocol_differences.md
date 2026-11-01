# Protocol evidence and incompatibilities

Evidence: the acquired workbook sheets, the [NPS monitoring page](https://www.nps.gov/sagu/learn/nature/long-term-monitoring.htm), and *Relocation and Restudy of Historic Saguaro Plots*, Funicelli & Turner (2002), especially Methods p. 5. Raw documents are listed with hashes in `data/raw/manifest.json`. Text extracts are derived files in `data/interim/reports/`.

These concrete incompatibilities were inspected before implementing the relational model:

1. Census 1990 contains height-class **densities**, not individual measurements. The read-me explicitly multiplies density by 4 ha to produce plot totals. Fractional totals are not transcription errors or individual organisms.
2. Census includes a combined 2000/2010 sheet and separate year sheets: appending them doubles representations of observations. Use the combined sheet as the primary individual representation; retain separate sheets for inventory and reconciliation.
3. Census combined-sheet headers start on row 2; Historic Plots has six institutional/banner rows before its header on row 7.
4. Historic Plots is **wide**, with Height/Arms/Notes suffixes 1975, 2001, 2010, 2014. Census is mostly long, with a Year field. Historic columns must be unpivoted.
5. Historic's `Height_2001` represents the 2001–2002 round: the report gives February 2001–May 2002. The canonical nominal year remains the source label, with an event date interval.
6. Census nominal 2010 contains actual Year values outside 2010. Preserve actual year and nominal round separately; no rewriting of source years.
7. Census plot identifiers are numeric; Historic uses 41A, 71G, 75M, etc. They require program namespaces, not fuzzy matching.
8. Census `Saguaro_id` and `COUNTER` have no demonstrated inter-round identity. Historic `SaguaroID` is presented on a shared longitudinal source row. Census identities remain null.
9. **71G is an explicit exception**: the 2002 report says vandalism/tag removal made individual tracking impossible and excludes it from recruitment/mortality analyses. Do not assign cross-round identities to 71G even though the workbook contains IDs.
10. Historic contains zero heights alongside `dead`, `tag only`, or blank notes. Zero is preserved and flagged, not silently interpreted as death or genuine shrinkage. Primary temporal height comparisons exclude ambiguous zero endpoints.
11. Historic status is embedded in free-text Notes, whereas Section 17 1941 has an explicit Dead y/n field. Measured height is not evidence of *explicitly* alive status; inferred and explicit states must differ.
12. Census 2000 has four stem browning/scarring fields; 2010's standalone sheet lacks them. The NPS page confirms browning was discontinued. A source union column existing in a workbook does not prove collection in every round.
13. Historic plots are 2 ha (100 × 200 m); Census core plots are about 4 ha; vegetation subplots are 100 m². Counts cannot be compared without a sampling-area denominator.
14. Historic relocation used a clinometer and GPS plot corners accurate to about 3 m. Its detection was unreliable below 10 cm. These methods do not support millimeter-level temporal interpretations.
15. Section 17 1941 has Height_Class, not continuous height. No conversion to meters is justified. Its Cactus_Number does not establish an identity crosswalk to the 2011 Sub/FID fields.
16. Section 17 workbook labels 2011 but spatial layer is named saguaros_2012. Preserve the discrepancy as metadata; do not create a second independent census from the spatial copy.
17. Vegetation 1990 workbook's numbered sheets have headers but no body observations. This does **not** mean no plants were present; spatial source layers supply separate source evidence.
18. Vegetation 2000 uses Code/Cover/Count; 2010 uses Species/Name/Stems/Area (m2)/% Cover and includes worksheet totals and side calculations. Taxon code is not an individual identifier. Cover units cannot be assumed equivalent.
19. Vegetation `% Cover` values in 2010 appear numerically consistent with area/100, i.e. a fraction despite the label. Preserve raw cover and flag the ambiguity; do not silently multiply by 100.
20. Spatial archives include multiple representations, annotation layers, local-coordinate vegetation maps without CRS, and projected NAD83/UTM coordinates. Never label local x/y as longitude/latitude.
21. The Census aggregate sheet includes 1941/1975 historic summaries, GPS variants, subsamples, and `75G` labels whereas the individual Historic workbook uses `71G`. Non-core aggregate labels remain in `census_summary_auxiliary`; no undocumented 75G-to-71G or GPS/subsample crosswalk is applied. The mere filename Census does not determine a row's sampling frame.

The NPS page, DataStore descriptive text, and the 2002 report disagree on some district/plot descriptions and dates. Canonical memberships follow explicit program/source identifiers; unresolved descriptive conflicts remain documented rather than repaired.

2020 reports were acquired from Census holdings. No 2020 raw individual workbook was exposed by those holdings at discovery time. This is an availability result for the inspected public records, not a claim that such data do not exist.
