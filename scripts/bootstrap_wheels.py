"""Download compatible wheels with stdlib when pip's index connection stalls."""
import json
from pathlib import Path
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor

out = Path('.wheels')
out.mkdir(exist_ok=True)
packages = 'pyarrow openpyxl et-xmlfile xlrd requests charset-normalizer idna urllib3 certifi pyyaml geopandas shapely pyproj pyogrio duckdb pypdf setuptools'.split()
def download(package):
    meta = json.load(urlopen(f'https://pypi.org/pypi/{package}/json', timeout=30))
    files = [f for f in meta['urls'] if f['filename'].endswith('.whl')]
    files = [f for f in files if f['filename'].endswith('py3-none-any.whl') or f['filename'].endswith('py2.py3-none-any.whl') or ('win_amd64' in f['filename'] and ('cp312-cp312' in f['filename'] or 'cp311-abi3' in f['filename'] or 'cp310-abi3' in f['filename'] or 'cp312-none' in f['filename']))]
    if not files:
        print('NO COMPATIBLE WHEEL', package, flush=True)
        return
    f = files[0]
    path = out / f['filename']
    if not path.exists():
        path.write_bytes(urlopen(f['url'], timeout=120).read())
    print(path.name, flush=True)
with ThreadPoolExecutor(max_workers=6) as pool:
    list(pool.map(download, packages))
