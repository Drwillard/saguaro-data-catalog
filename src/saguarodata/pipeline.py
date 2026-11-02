"""Small, explicit source adapters feeding relational Parquet tables."""
import importlib.metadata
import json
from pathlib import Path
import re
import pandas as pd
import yaml
from pyproj import Transformer
from .acquisition.downloader import read_manifest
from .acquisition.checksums import sha256
from .ingest.excel import read_sheets
from .ingest.spatial import extract_archive, read_spatial
from .ingest.common import observation, lineage, stringify
from .ingest import census, historic, section17, vegetation
from .normalize.identifiers import normalize_identifier, stable_id
from .normalize.missing import number
from .model.canonical import OBSERVATION_COLUMNS

def write_table(root, name, rows, columns=None):
    frame = rows if isinstance(rows, pd.DataFrame) else pd.DataFrame(rows)
    if columns is not None:
        for column in columns:
            if column not in frame:
                frame[column] = None
    path = Path(root) / 'data/processed' / f'{name}.parquet'
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(path, index=False)
    return frame

def active_sources(root):
    """Use latest acquired version per URL, retaining every prior version raw."""
    latest = {}
    for entry in read_manifest(root):
        latest[entry['direct_download_url']] = entry
    return sorted(latest.values(), key=lambda e: (e['dataset'], e['local_filename']))

def build(root='.'):
    root = Path(root).resolve()
    if not (root / 'data/processed/source_inventory.parquet').exists():
        raise ValueError('Run inventory and inspect sources before building the canonical model')
    manifest = active_sources(root)
    observations, plants, aggregates, spatial = [], [], [], []
    adapters = {'census': census, 'historic_plots': historic, 'section17': section17, 'vegetation': vegetation}
    schema_history = []
    for entry in manifest:
        path = root / entry['local_filename']
        if sha256(path) != entry['sha256']:
            raise ValueError(f'Raw integrity failure: {path}')
        if path.suffix.lower() in ('.xls', '.xlsx'):
            for sheet, header, frame in read_sheets(path):
                schema_history.append(dict(program_id=entry['dataset'], source_file=entry['local_filename'],
                    source_sheet=sheet, header_row=header, fields_json=json.dumps(list(map(str, frame.columns))),
                    types_json=json.dumps({str(c): pd.api.types.infer_dtype(frame[c]) for c in frame}),
                    survey_year=int(sheet) if sheet.isdigit() and len(sheet) == 4 else None,
                    protocol_notes='Source schema snapshot; year semantics require adapter; see protocol_differences.md'))
                if entry['dataset'] in adapters:
                    rows = adapters[entry['dataset']].ingest(entry, sheet, frame)
                    (plants if entry['dataset'] == 'vegetation' else observations).extend(rows)
                if entry['dataset'] == 'census' and sheet in ('raw_data_by_plot_all_years', 'RawData_1990_Total_Saguaros', 'raw_data_1990_saguaroperha '):
                    for index, row in frame.iterrows():
                        plot=normalize_identifier(row.get('plot_id',row.get('Plot','')))
                        year=number(row.get('survey_year',1990))[0]
                        program='census' if plot and plot.isdigit() and 1<=int(plot)<=45 else 'census_summary_auxiliary'
                        source=lineage(entry,sheet,index)
                        count_column=next((c for c in ['total_saguaros','Total saguaros'] if c in row),None)
                        density_column=next((c for c in ['saguaros_per_ha','Total Saguaros/ha on plot'] if c in row),None)
                        aggregates.append(dict(**source,observation_id=stable_id(source['source_row_id'],'plot_summary'),
                            program_id=program, plot_id=f'{program}:{plot}' if plot else None,source_plot_id=plot,
                            survey_year=int(year) if year is not None else None,
                            survey_event_id=f'{program}:{int(year)}' if year is not None else None,
                            count_raw=stringify(row.get(count_column,'')),count_estimate=number(row.get(count_column))[0],count_source_column=count_column,
                            density_raw=stringify(row.get(density_column,'')),density_per_ha=number(row.get(density_column))[0],density_source_column=density_column,
                            count_missing_reason=number(row.get(count_column),bool(count_column))[1],
                            density_missing_reason=number(row.get(density_column),bool(density_column))[1],
                            representation=sheet,
                            count_basis='density_scaled_4ha' if sheet == 'RawData_1990_Total_Saguaros' else ('per_hectare' if 'perha' in sheet else 'mixed_source_summary'),
                            raw_values_json=json.dumps({str(k): stringify(v) for k,v in row.items()})))
                if entry['dataset'] == 'ecotone' and sheet == 'all_plots_combined':
                    for index, row in frame.iterrows():
                        date=row.get('Date')
                        actual_year=date.year if hasattr(date,'year') else 2011
                        obs = observation(entry, sheet, index, row, 'ecotone', actual_year, row.get('Plot'),
                            'Height (m)', 'Arms', 'm', 'documented', notes_column='Comments')
                        obs.update(source_plot_id=str(row.get('Plot', '')), height_source_column='Height (m)', arms_source_column='Arms',
                            coordinate_time_basis=None, nominal_round=2011)
                        observations.append(obs)
        elif path.suffix.lower() == '.zip':
            base = root / 'data/interim/spatial' / entry['sha256']
            for shp in extract_archive(path, base):
                frame = read_spatial(shp)
                crs = frame.crs.to_string() if frame.crs else None
                for index, row in frame.iterrows():
                    attrs = {str(k): stringify(v) for k,v in row.items() if k != 'geometry'}
                    geometry = row.geometry
                    spatial.append(dict(**lineage(entry, shp.relative_to(base).as_posix(), index + 1),
                        feature_id=stable_id(entry['sha256'], shp.relative_to(base).as_posix(), index),
                        layer=shp.stem, feature_index=int(index), attributes_json=json.dumps(attrs),
                        geometry=geometry.wkb if geometry is not None else None, crs=crs,
                        geometry_valid=bool(geometry.is_valid) if geometry is not None else False,
                        geometry_type=geometry.geom_type if geometry is not None else None))
    obs = pd.DataFrame(observations)
    # Transform only explicitly supported projected coordinates. Preserve original.
    transform = Transformer.from_crs('EPSG:26912', 'EPSG:4326', always_xy=True)
    mask = obs['coordinate_crs'].eq('EPSG:26912') & obs['x'].notna() & obs['y'].notna()
    if mask.any():
        lon, lat = transform.transform(obs.loc[mask, 'x'].to_numpy(), obs.loc[mask, 'y'].to_numpy())
        obs.loc[mask, 'longitude'] = lon
        obs.loc[mask, 'latitude'] = lat
    obs = write_table(root, 'organism_observations', obs, OBSERVATION_COLUMNS)
    write_table(root, 'vegetation_observations', plants, ['observation_id', 'plot_id', 'survey_event_id', 'survey_year'])
    write_table(root, 'plot_observations', aggregates,['observation_id','program_id','representation','survey_year','survey_event_id','plot_id','count_estimate','density_per_ha'])
    features = write_table(root, 'spatial_features', spatial)
    plots = {}
    maps = []
    for row in observations + plants + aggregates:
        plot_id = row['plot_id']
        if not plot_id:
            continue
        program = row['program_id']
        name = plot_id.split(':', 1)[1]
        plots.setdefault(plot_id, dict(plot_id=plot_id, program_id=program, canonical_plot_name=name,
            source_plot_id=name, district=None, area_m2=100.0 if program == 'vegetation' else (20000.0 if program == 'historic_plots' else None),
            geometry=None, crs=None, geometry_source=None, spatial_precision=None))
        maps.append(dict(source_dataset=row['source_dataset'], source_file=row['source_file'], source_sheet=row['source_sheet'],
            source_value=str(row.get('source_plot_id', name)), canonical_value=plot_id,
            mapping_method='normalized-string', confidence='high', evidence='Program namespace; trim whitespace and numeric .0; no fuzzy matching'))
    # Geometry joins use explicit source TYPE and exact normalized plot labels.
    for feature in spatial:
        if feature['layer'] not in ('saguaro_plot_boundaries', 'Grids'):
            continue
        attrs = json.loads(feature['attributes_json'])
        name = normalize_identifier(attrs.get('PLOT_ID', attrs.get('PLOTID', attrs.get('PLOT', attrs.get('Plot', attrs.get('GRID_ID'))))))
        kind = attrs.get('TYPE', '').lower()
        program = 'section17' if feature['layer'] == 'Grids' else ('historic_plots' if kind == 'steenbergh-lowe plot' else ('census' if kind == 'duriscoe plot' else ('ecotone' if kind == '50m plot' else None)))
        plot_id = f'{program}:{name}'
        if plot_id in plots and feature['geometry'] is not None:
            plots[plot_id].update(geometry=feature['geometry'], crs=feature['crs'], geometry_source=feature['feature_id'])
    write_table(root, 'plots', list(plots.values()))
    write_table(root, 'plot_identifier_map', pd.DataFrame(maps).drop_duplicates())
    organisms = obs[obs.organism_id.notna()][['organism_id','program_id','plot_id','source_individual_id']].drop_duplicates()
    organisms['linkage_evidence'] = 'Shared longitudinal workbook row; 71G excluded per 2002 report'
    write_table(root, 'organisms', organisms)
    mapping = organisms.rename(columns={'source_individual_id':'source_value', 'organism_id':'canonical_value'}).copy()
    mapping['mapping_method'] = 'documented shared-row identifier'
    mapping['confidence'] = 'source-supported; anomalies unresolved'
    write_table(root, 'organism_identifier_map', mapping)
    programs = sorted({r['program_id'] for r in observations + plants + aggregates} | {'boundaries'})
    write_table(root, 'survey_programs', [dict(program_id=p, name=p.replace('_',' ').title(),
        description='Distinct source sampling frame; see protocol_differences.md',
        source_reference_id=','.join(sorted({e['source_reference_id'] for e in manifest if e['dataset'] == ('census' if p.startswith('census_') else p)}))) for p in programs])
    events = []
    for key, group in obs.groupby('survey_event_id'):
        row = group.iloc[0]
        historic_2001 = row.program_id == 'historic_plots' and row.survey_year == 2001
        events.append(dict(survey_event_id=key, program_id=row.program_id, survey_year=int(row.survey_year),
            nominal_round=int(row.nominal_round), start_date='2001-02-01' if historic_2001 else None,
            end_date='2002-05-31' if historic_2001 else None, protocol_version=f'{row.program_id}:{row.nominal_round}',
            notes='Month-bounded reported field interval' if historic_2001 else 'Actual year label retained; exact date not inferred'))
    for year in sorted({r['survey_year'] for r in plants}):
        events.append(dict(survey_event_id=f'vegetation:{year}', program_id='vegetation', survey_year=year,
            nominal_round=year, start_date=None, end_date=None, protocol_version=f'vegetation:{year}', notes='Source workbook round'))
    event_ids={r['survey_event_id'] for r in events}
    for row in aggregates:
        event_id=row['survey_event_id']
        if event_id and event_id not in event_ids:
            events.append(dict(survey_event_id=event_id,program_id=row['program_id'],survey_year=row['survey_year'],
                nominal_round=row['survey_year'],start_date=None,end_date=None,protocol_version=f"{row['program_id']}:aggregate",
                notes='Plot aggregate representation only; no individual history implied'))
            event_ids.add(event_id)
    write_table(root, 'survey_events', events)
    write_table(root, 'source_files', [{k:v for k,v in e.items() if k != 'holding'} for e in manifest])
    write_table(root, 'schema_history', schema_history)
    protocol_fields=[]
    for path in sorted((root/'configs/schemas').glob('*.yaml')):
        spec=yaml.safe_load(path.read_text())
        for year,fields in spec['rounds'].items():
            for field,collection in fields.items():
                protocol_fields.append(dict(program_id=spec['program'],nominal_round=int(year),field=field,
                    collection_semantics=collection,evidence=spec['evidence'],identity_policy=spec['identity']))
    write_table(root,'protocol_fields',protocol_fields,['program_id','nominal_round','field','collection_semantics','evidence','identity_policy'])
    provenance = []
    for row in obs.to_dict('records'):
        source = {k:v for k,v in row.items() if k.startswith('source_')}
        for field, column, value, transform_name, kind in (
            ('height_m', row.get('height_source_column'), row['height_raw'], f"height_to_m:{row['height_normalization_unit']}" if row['height_normalization_unit'] else 'continuous_height_not_collected', 'inferred' if row['unit_source']=='inferred' else 'normalized'),
            ('arm_count', row.get('arms_source_column'), row['arm_count_raw'], 'parse_numeric_without_zero_fill', 'normalized'),
            ('status', 'Dead' if row['status_source']=='explicit_field' else ('Notes_'+str(row['survey_year']) if row['program_id']=='historic_plots' else 'Comments'), row['status_raw'], 'exact_status_phrase', 'normalized')):
            provenance.append(dict(**source, observation_id=row['observation_id'], table='organism_observations',
                field=field, source_column=column, source_value=value, normalized_value=None if pd.isna(row.get(field)) else str(row.get(field)),
                transformation=transform_name, value_kind=kind))
        if pd.notna(row['longitude']):
            provenance.append(dict(**source, observation_id=row['observation_id'], table='organism_observations', field='longitude,latitude',
                source_column='UTM_X_83,UTM_Y_83' if row['program_id']=='historic_plots' else 'x_coord,y_coord',
                source_value=json.dumps([row['x'],row['y']]), normalized_value=json.dumps([row['longitude'],row['latitude']]),
                transformation='pyproj EPSG:26912 -> EPSG:4326 always_xy', value_kind='normalized'))
        if isinstance(row.get('verification_source_column'),str) and row['verification_source_column']:
            provenance.append(dict(**source,observation_id=row['observation_id'],table='organism_observations',field='verification_status',
                source_column=row['verification_source_column'],source_value=row['verification_raw'],normalized_value=row['verification_status'],
                transformation='normalize_verify_literal_v1',value_kind='normalized'))
    for row in plants:
        source={k:v for k,v in row.items() if k.startswith('source_')}
        for field,column,raw,value,transform in [('count','Stems' if row['survey_year']==2010 else 'Count',row['count_raw'],row['count'],'parse_numeric_without_zero_fill'),('cover_normalized','% Cover' if row['survey_year']==2010 else 'Cover',row['cover_raw'],None,'withheld_pending_unit_evidence')]:
            provenance.append(dict(**source,observation_id=row['observation_id'],table='vegetation_observations',field=field,source_column=column,
                source_value=raw,normalized_value=str(value),transformation=transform,value_kind='normalized'))
    for row in aggregates:
        source={k:v for k,v in row.items() if k.startswith('source_')}
        for field,raw,column in [('count_estimate','count_raw','count_source_column'),('density_per_ha','density_raw','density_source_column')]:
            provenance.append(dict(**source,observation_id=row['observation_id'],table='plot_observations',field=field,
                source_column=row[column],source_value=row[raw],normalized_value=str(row[field]) if row[field] is not None else None,
                transformation='parse_source_estimate_without_rounding',value_kind='normalized'))
    write_table(root, 'provenance', provenance)
    versions = {name: importlib.metadata.version(name) for name in ['saguarodata','pandas','pyarrow','openpyxl','xlrd','geopandas','pyproj','shapely'] if _installed(name)}
    (root / 'data/processed/build_metadata.json').write_text(json.dumps(dict(package_versions=versions,
        selected_sources=[dict(file=e['local_filename'],sha256=e['sha256']) for e in manifest],
        configuration_sha256={str(p.relative_to(root)):sha256(p) for p in sorted((root/'configs').rglob('*.yaml'))},
        implementation_sha256={str(p.relative_to(Path(__file__).parent)):sha256(p) for p in sorted(Path(__file__).parent.rglob('*.py'))},
        identity_policy='Historic shared-row IDs except 71G; no Census/Section17 linkage'), indent=2))
    return obs

def _installed(name):
    try:
        importlib.metadata.version(name)
        return True
    except importlib.metadata.PackageNotFoundError:
        return False
