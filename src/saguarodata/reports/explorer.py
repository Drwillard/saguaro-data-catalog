"""Export a local, interactive research report without a server-side dependency."""
import json
import re
from pathlib import Path
import shutil
import numpy as np
from shapely import from_wkb, transform
from shapely.geometry import mapping
from pyproj import Transformer
from ..jsonutil import dumps, sanitize
from ..acquisition.checksums import sha256

OBS_COLUMNS = ['observation_id', 'program_id', 'survey_year', 'plot_id', 'organism_id',
    'source_individual_id', 'status', 'height_m', 'arm_count', 'height_missing_reason',
    'arm_count_missing_reason', 'unit_source', 'latitude', 'longitude', 'nominal_round',
    'coordinate_time_basis']
FINDING_COLUMNS = ['entity_identifier', 'rule_id', 'severity', 'status', 'table', 'program_id',
    'survey_year', 'plot_id', 'field', 'observed_value']
VEGETATION_COLUMNS=['observation_id','program_id','survey_year','plot_id','species_raw','species_name_raw','count','count_raw','cover_raw','cover_unit_raw','area_m2']
AGGREGATE_COLUMNS=['observation_id','program_id','survey_year','plot_id','representation','count_estimate','density_per_ha','count_basis']

def _records(frame):
    return sanitize(frame.to_dict('records'))

def _decode(value):
    if isinstance(value, str):
        try: return json.loads(value)
        except (ValueError, TypeError): pass
    return value

def export_explorer(root, ds, summary):
    root = Path(root)
    folder = root / 'reports/explorer'
    folder.mkdir(parents=True, exist_ok=True)
    details_folder = folder / 'details'
    details_folder.mkdir(exist_ok=True)
    observations = _records(ds.observations())
    photo_references = {}
    for row in sorted(observations, key=lambda row:row['survey_year']):
        raw = _decode(row.get('raw_values_json')) or {}
        mentions = {key:value for key,value in raw.items() if re.search(r'\bphoto(?:graph)?s?\b', str(value), re.I)}
        if mentions:
            key = (row['source_file'], row['source_sheet'], row['source_row'])
            photo_references[key] = dict(observation_id=row['observation_id'], program_id=row['program_id'],
                plot_id=row['plot_id'], source_individual_id=row['source_individual_id'],
                source_file=row['source_file'], source_sheet=row['source_sheet'], source_row=row['source_row'],
                mentions=mentions)
    obs_index = {r['observation_id']: r for r in observations}
    pairs=[]
    for organism, group in ds.observations().dropna(subset=['organism_id']).groupby('organism_id'):
        group=group[~group.duplicated('survey_event_id',keep=False)].sort_values(['survey_year','observation_id'])
        rows=_records(group)
        for before,after in zip(rows,rows[1:]):
            elapsed=after['survey_year']-before['survey_year']
            if elapsed<=0:continue
            height_valid=before['height_m'] is not None and after['height_m'] is not None and before['height_m']>0 and after['height_m']>0
            arms_valid=before['arm_count'] is not None and after['arm_count'] is not None and before['arm_count']>=0 and after['arm_count']>=0
            if height_valid or arms_valid:
                pairs.append(dict(before_id=before['observation_id'],after_id=after['observation_id'],
                    program_id=after['program_id'],before_year=before['survey_year'],after_year=after['survey_year'],
                    height_before=before['height_m'] if height_valid else None,height_after=after['height_m'] if height_valid else None,
                    annual_growth_m=(after['height_m']-before['height_m'])/elapsed if height_valid else None,
                    arms_before=before['arm_count'] if arms_valid else None,arms_after=after['arm_count'] if arms_valid else None))
    findings = _records(ds.validation_findings())
    details = {}
    for row in observations:
        entity = row['observation_id']
        canonical = {k: v for k, v in row.items() if k != 'raw_values_json'}
        details[entity] = dict(kind='observation', canonical=canonical,
            raw=_decode(row['raw_values_json']), transforms=[], findings=[])
    # Non-organism records can also be reached from findings or the source register.
    for name in ['vegetation_observations', 'plot_observations']:
        for row in _records(ds.table(name)):
            details[row['observation_id']] = dict(kind=name, canonical={k:v for k,v in row.items() if k!='raw_values_json'},
                raw=_decode(row.get('raw_values_json', '{}')), transforms=[], findings=[])
    transform_fields=['field','source_column','source_value','normalized_value','transformation','value_kind']
    for row in _records(ds.table('provenance')[['observation_id']+transform_fields]):
        entry = details.get(row['observation_id'])
        if entry:
            entry['transforms'].append({key: row.get(key) for key in transform_fields})
    spatial = ds.table('spatial_features')
    spatial_ids = {row['entity_identifier'] for row in findings if row['table']=='spatial_features'}
    for row in _records(spatial[spatial.feature_id.isin(spatial_ids)]):
        row.pop('geometry', None)
        attributes = _decode(row.pop('attributes_json'))
        details[row['feature_id']] = dict(kind='spatial_features', canonical=row, raw=attributes, transforms=[], findings=[])
    finding_rows = []
    for i, row in enumerate(findings):
        entity = row['entity_identifier']
        lineage = _decode(row['source_lineage'])
        row['source_lineage'] = lineage
        row['observed_value'] = _decode(row['observed_value'])
        row['finding_index'] = i
        target = details.get(entity)
        if target:
            target['findings'].append(row)
        observation = obs_index.get(entity, {})
        compact = dict(row, program_id=observation.get('program_id') or (lineage or {}).get('source_dataset'),
            survey_year=observation.get('survey_year'), plot_id=observation.get('plot_id'))
        finding_rows.append([compact.get(c) for c in FINDING_COLUMNS])
    shards = {}
    for entity, entry in details.items():
        shards.setdefault(entity[:2], {})[entity] = entry
    for prefix, contents in shards.items():
        (details_folder / f'{prefix}.json').write_text(dumps(contents, separators=(',', ':'), default=str), encoding='utf8')
    geometry = []
    for row in ds.plots().to_dict('records'):
        if not isinstance(row.get('geometry'), (bytes,bytearray)) or not isinstance(row.get('crs'),str) or not row['crs']:
            continue
        shape = from_wkb(row['geometry'])
        if shape is None or not shape.is_valid:
            continue
        transformer = Transformer.from_crs(row['crs'], 'EPSG:4326', always_xy=True)
        shape = transform(shape,lambda coordinates:np.array(transformer.transform(coordinates[:,0],coordinates[:,1])).T).simplify(.000005, preserve_topology=True)
        geometry.append(dict(type='Feature', properties=dict(plot_id=row['plot_id'], program_id=row['program_id']),geometry=mapping(shape)))
    payload = dict(photo_references=list(photo_references.values()), observation_columns=OBS_COLUMNS,
        observations=[[r.get(c) for c in OBS_COLUMNS] for r in observations],
        finding_columns=FINDING_COLUMNS, findings=finding_rows, summary=summary,
        plots=dict(type='FeatureCollection',features=geometry),pairs=pairs,
        files=_records(ds.table('source_files')), surveys=_records(ds.surveys()),
        aggregate_counts=ds.table('plot_observations').groupby(['program_id','representation']).size().rename('records').reset_index().to_dict('records'))
    payload['summary_columns']={'vegetation':VEGETATION_COLUMNS,'plot':AGGREGATE_COLUMNS}
    payload['summaries']={kind:[[row.get(column) for column in columns] for row in _records(ds.table(table))]
        for kind,columns,table in [('vegetation',VEGETATION_COLUMNS,'vegetation_observations'),('plot',AGGREGATE_COLUMNS,'plot_observations')]}
    (folder / 'data.json').write_text(dumps(payload, separators=(',', ':'), default=str), encoding='utf8')
    inventory = _records(ds.table('source_inventory'))
    for row in inventory:
        for key in ['fields','original_columns','candidate_id_fields','coordinate_columns','measurement_columns']:
            row[key] = _decode(row.get(key))
        for field in row.get('fields', []):
            field['categories'] = _decode(field.get('categories'))
    sources = dict(inventory=inventory, schemas=_records(ds.table('schema_evolution')),
        protocols=_records(ds.table('protocol_fields')))
    (folder / 'sources.json').write_text(dumps(sources, separators=(',', ':'), default=str), encoding='utf8')
    assets = Path(__file__).parent / 'assets'
    for name in ['app.js','app.css']:
        shutil.copyfile(assets / name, folder / name)
    if (assets / 'geographic_context.json').exists():
        shutil.copyfile(assets / 'geographic_context.json', folder / 'geographic_context.json')
    if (assets / 'photo_links.json').exists():
        shutil.copyfile(assets / 'photo_links.json', folder / 'photo_links.json')
    for image in assets.glob('map_*.jpg'):
        shutil.copyfile(image, folder / image.name)
    html = (assets / 'explorer.html').read_text(encoding='utf8')
    # Version asset URLs so a refreshed report cannot reuse an older marker implementation.
    for name in ['app.js','app.css']:
        html=html.replace(f'explorer/{name}',f'explorer/{name}?v={sha256(assets/name)[:12]}')
    (root / 'reports/data_quality_report.html').write_text(html, encoding='utf8')
    manifest=dict(format_version=1,canonical_inputs={path.name:sha256(path) for path in sorted((root/'data/processed').glob('*.parquet'))},
        presentation_assets={path.name:sha256(path) for path in sorted(assets.iterdir()) if path.is_file()},
        observations=len(observations),findings=len(findings),linked_measurement_pairs=len(pairs),detail_entities=len(details))
    (folder/'manifest.json').write_text(dumps(manifest,indent=2),encoding='utf8')
