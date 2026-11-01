import json
import math
import pandas as pd
from shapely import from_wkb
from shapely.geometry import Point
from pyproj import Transformer, Geod
from .rules import finding

def coordinate_displacements(observations):
    """Independent linked fixes only; shared source coordinates are not repeats."""
    columns=['organism_id','program_id','previous_observation_id','observation_id','before_year','after_year','displacement_m']
    independent=observations[observations.organism_id.notna() & observations.longitude.notna() & observations.latitude.notna() & observations.coordinate_time_basis.eq('survey_event')]
    geod=Geod(ellps='WGS84'); rows=[]
    for organism,group in independent.groupby('organism_id'):
        group=group[~group.duplicated('survey_event_id',keep=False)].sort_values('survey_year')
        records=group.to_dict('records')
        for before,after in zip(records,records[1:]):
            if after['survey_year']<=before['survey_year']:continue
            distance=geod.inv(before['longitude'],before['latitude'],after['longitude'],after['latitude'])[2]
            rows.append(dict(organism_id=organism,program_id=after['program_id'],previous_observation_id=before['observation_id'],
                observation_id=after['observation_id'],before_year=before['survey_year'],after_year=after['survey_year'],displacement_m=distance))
    return pd.DataFrame(rows,columns=columns)

def contains(polygon_wkb, x, y):
    return from_wkb(polygon_wkb).covers(Point(x,y))

def spatial_findings(observations, plots, features, config):
    findings = []
    boxes = config['vicinity_bbox']
    polygons = {r['plot_id']:r for r in plots.to_dict('records') if r.get('geometry') is not None}
    transformers = {}
    coords = observations[observations.longitude.notna() & observations.latitude.notna()]
    for row in coords.to_dict('records'):
        lon, lat = row['longitude'], row['latitude']
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            findings.append(finding('INVALID_GEOGRAPHIC_COORDINATE', row, 'longitude,latitude', [lon,lat], 'Valid geographic ranges', 'Coordinate out of range.', 'error'))
        elif not (boxes[0]<=lon<=boxes[2] and boxes[1]<=lat<=boxes[3]):
            findings.append(finding('OUTSIDE_PARK_VICINITY', row, 'longitude,latitude', [lon,lat], f'Within screening bbox {boxes}', 'Vicinity screen, not a legal park-boundary test.'))
        plot = polygons.get(row['plot_id'])
        if plot and plot.get('crs'):
            key = ('EPSG:4326', plot['crs'])
            if key not in transformers:
                transformers[key] = Transformer.from_crs(*key, always_xy=True)
            transformer = transformers[key]
            x,y = transformer.transform(lon,lat)
            if not contains(plot['geometry'], x,y):
                findings.append(finding('OUTSIDE_ASSIGNED_PLOT', row, 'longitude,latitude', [lon,lat],
                    'Point covered by exact-matched source plot polygon', 'Boundary/GPS differences or plot assignment require review.'))
    for row in coords[coords.duplicated(['program_id','survey_event_id','longitude','latitude'],keep=False)].to_dict('records'):
        findings.append(finding('DUPLICATE_COORDINATES', row, 'longitude,latitude', [row['longitude'],row['latitude']],
            'Review shared coordinates within event', 'Shared positions may reflect source copies, precision or mapping methods.'))
    # Shared Historic source coordinates are explicitly excluded from displacement.
    displacements=coordinate_displacements(observations)
    lookup=observations.drop_duplicates('observation_id',keep=False).set_index('observation_id').to_dict('index')
    for pair in displacements.to_dict('records'):
        if pair['displacement_m'] > config['coordinate_displacement_warning_m'] and pair['observation_id'] in lookup:
            row=dict(lookup[pair['observation_id']],observation_id=pair['observation_id'])
            findings.append(finding('COORDINATE_DISPLACEMENT', row, 'longitude,latitude', dict(previous=pair['previous_observation_id'], displacement_m=pair['displacement_m']),
                'Displacement within configured screening tolerance', 'Measurement systems change; examine the exported displacement distribution before concluding object movement.'))
    for row in features.to_dict('records'):
        if not row.get('geometry_valid'):
            findings.append(finding('INVALID_OR_NULL_GEOMETRY', row, 'geometry', row.get('geometry_type'), 'Valid source geometry', 'Malformed source geometry retained as null or invalid; no repair.', table='spatial_features'))
    if not features.empty:
        unknown = features[features.crs.isna() | features.crs.fillna('').eq('')]
        for _, group in unknown.groupby(['source_sha256','source_sheet']):
            row=group.iloc[0].to_dict()
            findings.append(finding('UNKNOWN_SPATIAL_CRS', row, 'crs', dict(layer=row['source_sheet'], affected_features=len(group)), 'CRS required before geographic comparison', 'Local or undocumented source coordinates; excluded from geographic validation. One finding per affected layer.', 'info', table='spatial_features'))
    # Parent containment requires an explicit relationship and compatible CRS.
    if 'parent_plot_id' in plots:
        lookup=plots.set_index('plot_id').to_dict('index')
        for row in plots[plots.parent_plot_id.notna()].to_dict('records'):
            parent=lookup.get(row['parent_plot_id'])
            if parent and row.get('geometry') is not None and parent.get('geometry') is not None and row.get('crs') == parent.get('crs') and row.get('crs'):
                if not from_wkb(parent['geometry']).covers(from_wkb(row['geometry'])):
                    row['entity_identifier']=row['plot_id']
                    findings.append(finding('SUBPLOT_OUTSIDE_PARENT',row,'geometry',row['parent_plot_id'],
                        'Subplot geometry covered by documented parent', 'Explicit parent relation fails containment.',table='plots'))
    # Independently supplied Section17 grids have exact plot labels in two layers.
    if not features.empty:
        representations={}
        for row in features[features.layer.isin(['Grids','Section17_Plots_percentchange'])].to_dict('records'):
            attrs=json.loads(row['attributes_json'])
            name=attrs.get('GRID_ID',attrs.get('Plot'))
            if name and row.get('geometry') is not None and row.get('crs'):
                previous=representations.get(name)
                if previous and previous['crs']==row['crs']:
                    a,b=from_wkb(previous['geometry']),from_wkb(row['geometry'])
                    if a.is_valid and b.is_valid and a.area>0:
                        fraction=a.symmetric_difference(b).area/a.area
                        if fraction>config.get('plot_geometry_difference_fraction',.01):
                            findings.append(finding('PLOT_GEOMETRY_DISAGREEMENT',row,'geometry',dict(plot=name,previous_feature=previous['feature_id'],symmetric_difference_fraction=fraction),
                                'Source representations agree within configured area fraction','Independent grid representations differ; no geometry replaced or repaired.',table='spatial_features'))
                representations[name]=row
    return findings
