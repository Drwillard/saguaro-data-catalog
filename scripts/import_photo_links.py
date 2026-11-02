"""Import portable original-source photo links without copying image files."""
import argparse
import csv
from hashlib import sha256
import json
from pathlib import Path
from urllib.parse import urlparse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', type=Path, required=True, help='iNaturalist observation_photos.csv')
    args = parser.parse_args()
    photos = []
    seen = set()
    with args.csv.open(encoding='utf-8-sig', newline='') as stream:
        for row in csv.DictReader(stream):
            observation_id, photo_id = int(row['observation_id']), int(row['photo_id'])
            if photo_id in seen:
                raise ValueError(f'Duplicate photo ID: {photo_id}')
            seen.add(photo_id)
            url = row['photo_url']
            parsed = urlparse(url)
            if parsed.scheme != 'https' or parsed.hostname not in {
                'inaturalist-open-data.s3.amazonaws.com', 'static.inaturalist.org'}:
                raise ValueError(f'Unsupported original image URL: {url}')
            photos.append(dict(observation_id=observation_id, photo_id=photo_id,
                observation_url=f'https://www.inaturalist.org/observations/{observation_id}',
                photo_page_url=f'https://www.inaturalist.org/photos/{photo_id}',
                image_url=url, license=row['photo_license'], attribution=row['attribution']))
    payload = dict(source='Separate iNaturalist saguaro morphology pilot',
        source_csv_name=args.csv.name, source_csv_sha256=sha256(args.csv.read_bytes()).hexdigest(),
        note='These photos have no verified identity crosswalk to the NPS monitoring cacti.',
        photos=sorted(photos, key=lambda row:(row['observation_id'], row['photo_id'])))
    target = Path(__file__).resolve().parents[1] / 'src/saguarodata/reports/assets/photo_links.json'
    target.write_text(json.dumps(payload, separators=(',', ':')), encoding='utf8')
    print(f'Exported {len(photos)} photo links from {len({p["observation_id"] for p in photos})} observations; no images copied.')


if __name__ == '__main__':
    main()
