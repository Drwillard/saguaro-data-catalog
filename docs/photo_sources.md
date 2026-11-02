# Photo sources and original links

The interactive **Photos & original sources** tab is available at
http://127.0.0.1:8000/data_quality_report.html#tab=photos after generating the report.
This is a link catalog: the app does not embed or download photographs. Selecting
a link opens its original provider in a new tab.

## Historical landscape photography

- [NPS long-term monitoring](https://www.nps.gov/sagu/learn/nature/long-term-monitoring.htm): 1935/1998 repeat views of the Rincon Mountain District cactus forest.
- [USGS Saguaro repeat photographs](https://www.usgs.gov/media/slideshows/repeat-photographs-saguaro-national-monument-east-now-saguaro-national-park-rincon): 1935/2010 series, camera point s0013. The source labels this series public domain.
- [USGS Southwest Repeat Photography Collection](https://www.usgs.gov/centers/southwest-biological-science-center/science/southwest-repeat-photography-collection): broader regional archive, with original-media/download links on the provider's pages.

These sources were checked November 1, 2026. The landscapes provide context;
they have no established correspondence to specific tagged NPS census cacti.

## iNaturalist photos

The portable catalog in `src/saguarodata/reports/assets/photo_links.json` contains
548 unique photo IDs from 300 observations in the separate local saguaro
morphology pilot. It preserves the recorded image URLs, photo licenses and
attribution. Each entry links to the original iNaturalist observation, the
iNaturalist photo page, and the image at its recorded source host. Image links
use the recorded medium-resolution rendition; the original photo page provides
the provider's available sizes and current metadata. Availability and licensing
can change upstream; the catalog records the imported metadata, not a perpetual
availability guarantee.

No local image paths, morphology labels, or photo-to-NPS cactus identities are
imported. The catalog is separate from canonical monitoring observations, so the
global NPS sampling-frame/year/record filters do not apply to it. Its own search
and license filters affect the displayed links and CSV export. The historical
collection links and NPS photo-reference register always cover the whole corpus.

To regenerate from an explicitly selected morphology-pilot CSV:

```powershell
python scripts/import_photo_links.py --csv C:/path/to/observation_photos.csv
saguarodata report
```

The import records the CSV basename and SHA-256, validates source hosts and unique
photo IDs, and copies metadata only. The bundled link catalog is tracked in Git
and included in package data; ordinary report generation requires neither the
separate pilot checkout nor external photo-service access.

## Photo mentions in NPS records

Nine physical source rows contain photo references. Examples include `Photo taken`,
`wrong photo`, `J51 in photo`, and `1135 in 2014 photo`. The report preserves the
literal source field/note and links to the original workbook and evidence drawer.
Repeated survey observations from the same physical row are represented once in
this register; opening the drawer shows the latest represented survey record and
the raw row, which may contain notes from other years.

These are references to photography, **not located photographs**. No verified
image URL is provided for those references in the acquired observation data.
The separate iNaturalist catalog and the historical collections do not resolve
those references. They do not establish individual identity across surveys.

Every organism-observation drawer displays **Photos for this observation** near
the top, even when its source row does not mention photography. It shows the
source cactus tag/plot/year, states when a verified individual photo link is
unavailable, and links directly to the original NPS record and historical
landscape collections. The latter are labeled as landscape context, with a
button to browse the complete photo-source catalog.

For the requested example `fbc090fb9c5184f1043c1027`, the source is cactus K30,
plot 75K, survey year 2014, workbook Sheet1 row 2544. Its raw row contains no photo
identifier or URL. A live check on November 1, 2026 of NPS holdings 2225187,
2225397 and 2225404 found the workbook, report and shapefile archive, respectively,
without a separate photo holding. No verified public image of K30 was located.
