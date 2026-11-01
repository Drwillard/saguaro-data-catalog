"""Discover holdings from the same public JSON endpoint used by NPS's UI."""
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
import requests
import yaml

BASE = 'https://irma.nps.gov'

def discover(root='.', session=None):
    root = Path(root)
    config = yaml.safe_load((root / 'configs/sources.yaml').read_text())
    session = session or requests.Session()
    target = root / 'data/interim/discovery'
    target.mkdir(parents=True, exist_ok=True)
    def get(url, name):
        response = session.get(url, timeout=90)
        response.raise_for_status()
        (target / name).write_bytes(response.content)
        return response
    page = get(config['monitoring_url'], 'monitoring.html').text
    refs = set(map(int, re.findall(r'/DataStore/Reference/Profile/(\d+)', page)))
    configured = {int(ref): key for key, values in config['references'].items() for ref in values}
    records, failures = [], []
    for ref in sorted(refs | set(configured)):
        url = f'{BASE}/DataStore/Reference/Profile/{ref}'
        try:
            profile = get(url, f'{ref}.html').text
            match = re.search(r'<title>(.*?)</title>', profile, re.S)
            title = html.unescape(match[1].strip()) if match else str(ref)
            holdings_url = f'{BASE}/DataStore/Reference/GetHoldings?referenceId={ref}'
            holdings = get(holdings_url, f'{ref}_holdings.json').json()
            for item in holdings:
                records.append(dict(dataset=configured.get(ref, 'additional'), source_title=title,
                    source_reference_id=str(ref), source_url=url, discovery_url=config['monitoring_url'],
                    metadata_url=holdings_url, direct_download_url=item.get('Url'),
                    filename=item.get('FileDescription'), content_type=item.get('MimeType'),
                    downloadable=item.get('CanDownload', False), holding=item))
        except (requests.RequestException, ValueError) as exc:
            failures.append(dict(source_reference_id=str(ref), source_url=url, error=str(exc)))
    catalog = dict(discovered_at=datetime.now(timezone.utc).isoformat(), records=records, failures=failures)
    (target / 'catalog.json').write_text(json.dumps(catalog, indent=2), encoding='utf8')
    return catalog
