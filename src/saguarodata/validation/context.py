"""Explicit identity, event, unit and CRS cross-checks on canonical context."""
import pandas as pd
from shapely import from_wkb
from pyproj import Transformer
from .rules import finding
from .provenance import missing

def context_findings(tables):
    out=[]
    organisms={r['organism_id']:r for r in tables.get('organisms',pd.DataFrame()).to_dict('records')}
    events={r['survey_event_id']:r for r in tables.get('survey_events',pd.DataFrame()).to_dict('records')}
    transforms={}
    for row in tables['organism_observations'].to_dict('records'):
        def emit(rule,field,value,message):out.append(finding(rule,row,field,value,'Consistent canonical context',message,'error'))
        organism=organisms.get(row.get('organism_id'))
        if organism and any(str(row.get(k))!=str(organism.get(k)) for k in ('program_id','plot_id','source_individual_id')):
            emit('IDENTITY_CONTEXT_MISMATCH','organism_id',row['organism_id'],'Linked identity conflicts with its organism program, plot or source tag.')
        event=events.get(row.get('survey_event_id'))
        if event and row.get('survey_year')!=event.get('survey_year'):
            emit('EVENT_YEAR_MISMATCH','survey_year',row.get('survey_year'),'Observation year disagrees with the referenced event.')
        if not missing(row.get('height_m')) and row.get('height_normalization_unit')!='m':
            emit('NORMALIZED_UNIT_MISSING','height_normalization_unit',row.get('height_normalization_unit'),'Normalized meter height has missing or incompatible unit metadata.')
        if all(not missing(row.get(k)) for k in ('x','y','longitude','latitude')):
            crs=row.get('coordinate_crs')
            if missing(crs):emit('COORDINATE_CRS_MISSING','coordinate_crs',crs,'Source coordinates have no declared CRS.')
            else:
                try:
                    if crs not in transforms:transforms[crs]=Transformer.from_crs(crs,'EPSG:4326',always_xy=True)
                    lon,lat=transforms[crs].transform(row['x'],row['y'])
                    if abs(lon-row['longitude'])>1e-5 or abs(lat-row['latitude'])>1e-5:
                        emit('COORDINATE_CRS_MISMATCH','longitude,latitude',dict(crs=crs,x=row['x'],y=row['y']),'Coordinates disagree with the declared source CRS transformation.')
                except Exception as exc:emit('INVALID_COORDINATE_CRS','coordinate_crs',str(crs),'CRS cannot be interpreted: '+str(exc))
    for row in tables.get('spatial_features',pd.DataFrame()).to_dict('records'):
        if row.get('geometry') is None:continue
        geom=from_wkb(row['geometry'],on_invalid='ignore')
        if geom is None or not geom.is_valid:
            out.append(finding('INVALID_SOURCE_GEOMETRY',row,'geometry',row.get('geometry_type'),'Geometry bytes form a valid shape','Geometry bytes are invalid, irrespective of the stored validity flag.','error','spatial_features'))
    return out
