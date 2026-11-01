"""Cache official geographic context separately from research observations.

Run explicitly to refresh the bundled display-only snapshot. Report builds never
access these services. Raw response hashes and query parameters travel with it.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

import geopandas as gpd
import requests
from shapely.geometry import box, mapping, shape
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'data/external/map_context'
TARGET = ROOT / 'src/saguarodata/reports/assets/geographic_context.json'
BBOX = [-111.3, 32.0, -110.45, 32.43]
TIGER = 'https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb'
SOURCES = []


def acquire(name, url, params=None):
    path = CACHE / name
    if not path.exists():
        response = requests.get(url, params=params, timeout=120)
        response.raise_for_status()
        if name.endswith('.json') and response.json().get('error'):
            raise ValueError(response.json()['error'])
        path.write_bytes(response.content)
    raw = path.read_bytes()
    SOURCES.append(dict(url=url, query=params, sha256=sha256(raw).hexdigest(),
                        cached_file=name, retrieved_utc=datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()))
    return path


def query_roads(layer):
    url = f'{TIGER}/Transportation/MapServer/{layer}/query'
    common = dict(where='1=1', geometry=','.join(map(str, BBOX)),
                  geometryType='esriGeometryEnvelope', inSR=4326,
                  spatialRel='esriSpatialRelIntersects', f='json')
    count = json.loads(acquire(f'roads_{layer}_count.json', url,
                              dict(common, returnCountOnly='true')).read_text())['count']
    features = []
    for offset in range(0, count, 2000):
        params = dict(common, f='geojson', outFields='NAME,MTFCC,OBJECTID', outSR=4326,
                      orderByFields='OBJECTID', resultOffset=offset, resultRecordCount=2000)
        data = json.loads(acquire(f'roads_{layer}_{offset}.json', url, params).read_text())
        features.extend(data['features'])
    if len(features) != count:
        raise ValueError(f'Road layer {layer}: expected {count}, received {len(features)}')
    return features


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    park_zip = acquire('SAGU_Tract_Boundary.gdb.zip', 'https://irma.nps.gov/DataStore/DownloadFile/754039')
    park_frame = gpd.read_file(f'/vsizip/{park_zip.as_posix()}/SAGU_Tract_Boundary.gdb', layer='SAGU_Boundary').to_crs(4326)
    park_geometry = unary_union(park_frame.geometry)
    # Preserve both park districts, including all disconnected boundary parts.
    parts = list(park_geometry.geoms) if park_geometry.geom_type == 'MultiPolygon' else [park_geometry]
    parks = []
    for district, west in [('Tucson Mountain District', True), ('Rincon Mountain District', False)]:
        geom = unary_union([part for part in parts if (part.representative_point().x < -111) == west]).simplify(.00002, preserve_topology=True)
        parks.append(dict(type='Feature', properties=dict(name=district, kind='park'), geometry=mapping(geom)))
    city_url = f'{TIGER}/Places_CouSub_ConCity_SubMCD/MapServer/4/query'
    params = dict(where="STATE='04' AND NAME='Tucson city'", outFields='NAME,GEOID', outSR=4326, f='geojson')
    city_data = json.loads(acquire('tucson.json', city_url, params).read_text())
    if len(city_data['features']) != 1:
        raise ValueError('Expected exactly one Tucson city feature')
    city = city_data['features'][0]
    city['geometry'] = mapping(shape(city['geometry']).simplify(.00002, preserve_topology=True))
    city['properties'] = dict(name='City of Tucson', kind='city')
    with ThreadPoolExecutor(max_workers=3) as pool:
        road_layers = list(pool.map(query_roads, [2, 6, 8]))
    roads = []
    clip = box(*BBOX)
    for road_class, features in zip(['primary', 'secondary', 'local'], road_layers):
        groups = {}
        for feature in features:
            geom = shape(feature['geometry']).intersection(clip)
            if not geom.is_empty:
                groups.setdefault(feature['properties'].get('NAME') or 'Unnamed road', []).append(geom)
        for name, geometries in sorted(groups.items()):
            geom = unary_union(geometries).simplify(.000015, preserve_topology=True)
            roads.append(dict(type='Feature', properties=dict(name=name, kind=road_class), geometry=mapping(geom)))
    payload = dict(type='GeographicContext', bbox=BBOX, crs='EPSG:4326',
        note='Current geographic context; not historical survey boundaries or research observations. Roads clipped to the regional extent.',
        sources=sorted(SOURCES, key=lambda row:row['cached_file']),
        layers=dict(parks=parks, city=[city], roads=roads))
    backgrounds = {}
    for kind, url, credit in [
        ('topo','https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer','USGS The National Map'),
        ('relief','https://services.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer','Esri, USGS, NOAA')]:
        info = json.loads(acquire(f'{kind}_wide_export.json', url+'/export', dict(
            bbox='-111.8,31.7,-109.95,32.73',bboxSR=4326,imageSR=4326,
            size='1800,1100',format='jpg',f='json')).read_text())
        image_path = acquire(f'{kind}_wide.jpg', info['href'])
        destination = TARGET.parent / f'map_{kind}.jpg'
        destination.write_bytes(image_path.read_bytes())
        backgrounds[kind] = dict(file=destination.name,extent=info['extent'],service=url,attribution=credit)
    payload['backgrounds'] = backgrounds
    payload['sources'] = sorted(SOURCES, key=lambda row:row['cached_file'])
    def compact(value):
        if isinstance(value, float): return round(value, 6)
        if isinstance(value, (list, tuple)): return [compact(item) for item in value]
        if isinstance(value, dict): return {key:compact(item) for key,item in value.items()}
        return value
    TARGET.write_text(json.dumps(compact(payload), separators=(',', ':')), encoding='utf8')
    print(f'{TARGET}: {len(parks)} park districts, 1 city, {len(roads)} named road groups; {TARGET.stat().st_size:,} bytes')


if __name__ == '__main__':
    main()
