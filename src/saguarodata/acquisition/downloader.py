"""Content-addressed artifacts; previously acquired bytes are never overwritten."""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
import requests
from .checksums import sha256

def read_manifest(root):
    path = Path(root) / 'data/raw/manifest.json'
    return json.loads(path.read_text()) if path.exists() else []

def acquire(root, record, session=None):
    root = Path(root)
    response = (session or requests.Session()).get(record['direct_download_url'], timeout=180)
    response.raise_for_status()
    content = response.content
    mime = response.headers.get('Content-Type', '').split(';')[0]
    if 'text/html' in mime and not str(record.get('filename', '')).endswith('.html'):
        raise ValueError(f"Expected artifact, received HTML: {record['direct_download_url']}")
    digest = hashlib.sha256(content).hexdigest()
    name = Path(record.get('filename') or 'artifact.bin').name
    name = re.sub(r'[^\w. &()+-]', '_', name)
    folder = root / 'data/raw' / record['dataset'] / digest
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / name
    if path.exists():
        if sha256(path) != digest:
            raise ValueError(f'Raw integrity failure: {path}')
    else:
        with path.open('xb') as stream:
            stream.write(content)
    entry = {k: v for k, v in record.items() if k != 'holding'}
    entry.update(downloaded_at=datetime.now(timezone.utc).isoformat(), local_filename=path.relative_to(root).as_posix(),
                 sha256=digest, byte_size=len(content), content_type=mime,
                 original_archive_filename=name if name.lower().endswith('.zip') else None,
                 notes='Public NPS holding; bytes preserved unchanged')
    manifest = read_manifest(root)
    if not any(e['sha256'] == digest and e['source_reference_id'] == entry['source_reference_id'] for e in manifest):
        manifest.append(entry)
        temp = root / 'data/raw/manifest.json.tmp'
        temp.write_text(json.dumps(manifest, indent=2), encoding='utf8')
        temp.replace(root / 'data/raw/manifest.json')
    return entry

def download(root, catalog, refresh=False):
    manifest = read_manifest(root)
    errors = []
    for record in catalog['records']:
        if not record['downloadable']:
            continue
        cached = [e for e in manifest if e['direct_download_url'] == record['direct_download_url']]
        if cached and not refresh and all((Path(root) / e['local_filename']).exists() for e in cached):
            for entry in cached:
                if sha256(Path(root) / entry['local_filename']) != entry['sha256']:
                    raise ValueError(f"Raw integrity failure: {entry['local_filename']}")
            continue
        try:
            entry = acquire(root, record)
            print(f"Acquired {entry['dataset']}: {entry['filename']}", flush=True)
        except (requests.RequestException, ValueError) as exc:
            errors.append(dict(url=record['direct_download_url'], error=str(exc)))
    path = Path(root) / 'data/interim/acquisition_errors.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(errors, indent=2))
    return errors
