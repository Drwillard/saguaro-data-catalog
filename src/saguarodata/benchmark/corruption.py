"""Inject one corruption into a deep copy, retaining before/after cell evidence."""
import json
import numpy as np
import pandas as pd
from shapely.geometry import Polygon
from ..normalize.identifiers import stable_id
from ..jsonutil import sanitize
from .scenarios import expected_detection_classes

class IneligibleScenario(ValueError):pass

def inject(tables, scenario, seed=42, ordinal=0, intensity=1.0):
    if not np.isfinite(intensity) or intensity<=0:raise ValueError('Intensity must be positive and finite')
    rng=np.random.default_rng(seed+ordinal*1000003)
    copies={name:frame.copy(deep=True) for name,frame in tables.items()}
    obs=copies['organism_observations'];sid=scenario['id'] if isinstance(scenario,dict) else scenario
    category=scenario.get('class',sid.split('_')[0]) if isinstance(scenario,dict) else sid.split('_')[0]
    changes=[];targets=set();fields=set();table='organism_observations'
    def choose(frame):
        if frame.empty:raise IneligibleScenario(f'{sid}: no eligible source evidence')
        return frame.index[int(rng.integers(len(frame)))]
    i=choose(obs);entity=obs.at[i,'observation_id']
    def target(index):
        for key in ('observation_id','source_row_id'):
            value=obs.at[index,key]
            if pd.notna(value):targets.add(str(value))
        organism=obs.at[index,'organism_id']
        if pd.notna(organism):targets.update(obs.loc[obs.organism_id.eq(organism),'observation_id'].dropna().astype(str))
    def setcell(name,index,field,value):
        frame=copies[name];before=frame.at[index,field] if field in frame else None
        changes.append(dict(table=name,row_index=int(index),field=field,before=sanitize(before),after=sanitize(value)))
        if isinstance(value,str) and field in frame and pd.api.types.is_numeric_dtype(frame[field]):frame[field]=frame[field].astype(object)
        frame.at[index,field]=value;fields.add(field)
        if name=='organism_observations':target(index)
    positive=obs[pd.to_numeric(obs.height_m,errors='coerce').gt(0)]
    if sid in ('schema_column_renamed','schema_required_removed'):
        field='height_m' if sid=='schema_column_renamed' else 'observation_id'
        if sid=='schema_column_renamed':copies[table]=obs.rename(columns={field:'height_unexpected'})
        else:copies[table]=obs.drop(columns=field)
        changes.append(dict(table=table,row_index=None,field=field,before='column present',after='renamed' if sid=='schema_column_renamed' else 'removed'))
        fields.add(field);entity='__table__';targets.add(entity)
        targets.update(obs.observation_id.dropna().astype(str));targets.update(obs.source_row_id.dropna().astype(str))
    elif sid=='schema_numeric_string':
        i=choose(positive);setcell(table,i,'height_m',str(obs.at[i,'height_m']))
    elif sid=='schema_category_changed':setcell(table,i,'status','living??')
    elif sid=='schema_null_identifier':setcell(table,i,'observation_id',None)
    elif sid=='schema_unit_removed':
        i=choose(positive);setcell(table,i,'height_normalization_unit',None)
    elif sid in ('row_negative_height','row_negative_arms','row_impossible_coordinate','row_malformed_numeric','provenance_unrecorded_value'):
        i=choose(positive)
        field,value={'row_negative_height':('height_m',-3.*intensity),'row_negative_arms':('arm_count',-float(max(1,round(2*intensity)))),
                     'row_impossible_coordinate':('latitude',90.+30.*intensity),'row_malformed_numeric':('height_m','7..oops'),
                     'provenance_unrecorded_value':('height_m',float(obs.at[i,'height_m'])+.123*intensity)}[sid]
        setcell(table,i,field,value)
    elif sid in ('row_duplicate_source','row_duplicate_observation','temporal_duplicate_event','provenance_duplicate_lineage'):
        if sid=='temporal_duplicate_event':i=choose(obs[obs.organism_id.notna()])
        target(i);new=obs.loc[i].copy()
        if sid in ('row_duplicate_source','temporal_duplicate_event'):new['observation_id']=stable_id('benchmark',seed,ordinal,sid)
        copies[table]=pd.concat([obs,new.to_frame().T],ignore_index=True)
        targets.add(str(new.observation_id));fields.update(('observation_id','source_row_id','organism_id','survey_event_id'))
        changes.append(dict(table=table,row_index=len(obs),field='__row__',before=None,after=new.to_dict()))
    elif sid.startswith('temporal_') and sid!='temporal_identity_reassignment':
        groups=[]
        for _,group in obs[obs.organism_id.notna()].groupby('organism_id'):
            group=group[~group.duplicated('survey_event_id',keep=False)].sort_values('survey_year')
            group=group[pd.to_numeric(group.height_m,errors='coerce').gt(0)]
            if len(group)>1:groups.append(group)
        if not groups:raise IneligibleScenario(sid+': no supported positive-height pair')
        group=groups[int(rng.integers(len(groups)))];a,b=group.index[:2];i=b
        if sid=='temporal_dead_to_alive':
            for idx,status in [(a,'dead'),(b,'alive')]:
                setcell(table,idx,'status',status);setcell(table,idx,'status_source','explicit_field');setcell(table,idx,'status_raw',status)
        elif sid=='temporal_height_decrease':setcell(table,b,'height_m',float(obs.at[a,'height_m'])*(.1 if intensity==1 else max(.01,1-.9*intensity)))
        elif sid=='temporal_positive_growth':setcell(table,b,'height_m',float(obs.at[a,'height_m'])+100.*intensity)
        elif sid=='temporal_arm_collapse':setcell(table,a,'arm_count',float(max(1,round(8*intensity))));setcell(table,b,'arm_count',0.)
        elif sid=='temporal_year_swap':
            first,second=obs.at[a,'survey_year'],obs.at[b,'survey_year'];setcell(table,a,'survey_year',second);setcell(table,b,'survey_year',first)
    elif sid=='temporal_identity_reassignment':
        i=choose(obs[obs.organism_id.notna()]);other=obs[obs.organism_id.notna()&obs.organism_id.ne(obs.at[i,'organism_id'])]
        j=choose(other);target(j);setcell(table,i,'organism_id',obs.at[j,'organism_id'])
    elif sid in ('spatial_outside_plot','spatial_crs_mislabeled','spatial_coordinates_swapped','spatial_other_plot_coordinates'):
        known=set(copies['plots'].loc[copies['plots'].geometry.notna()&copies['plots'].crs.notna(),'plot_id'])
        geographic=obs[obs.longitude.notna()&obs.latitude.notna()&obs.plot_id.isin(known)]
        i=choose(geographic)
        if sid=='spatial_outside_plot':setcell(table,i,'longitude',float(obs.at[i,'longitude'])+intensity)
        elif sid=='spatial_crs_mislabeled':setcell(table,i,'coordinate_crs','EPSG:4326')
        elif sid=='spatial_coordinates_swapped':
            lon,lat=obs.at[i,'longitude'],obs.at[i,'latitude'];setcell(table,i,'longitude',lat);setcell(table,i,'latitude',lon)
        else:
            j=choose(geographic[geographic.plot_id.ne(obs.at[i,'plot_id'])])
            setcell(table,i,'longitude',obs.at[j,'longitude']);setcell(table,i,'latitude',obs.at[j,'latitude'])
    elif sid in ('spatial_crs_removed','spatial_invalid_geometry'):
        table='spatial_features';frame=copies[table];i=choose(frame[frame.geometry.notna()&frame.crs.notna()])
        entity=str(frame.at[i,'feature_id']);targets.add(entity)
        if sid=='spatial_crs_removed':setcell(table,i,'crs',None)
        else:setcell(table,i,'geometry',Polygon([(0,0),(intensity,intensity),(intensity,0),(0,intensity),(0,0)]).wkb)
    elif sid=='provenance_source_row_changed':setcell(table,i,'source_row',int(obs.at[i,'source_row'])+max(1,round(100000*intensity)))
    elif sid=='provenance_sha_mismatch':setcell(table,i,'source_sha256','f'*64)
    elif sid=='provenance_transformation_removed':
        target(i);prov=copies['provenance'];mask=prov.observation_id.eq(obs.at[i,'observation_id'])&prov.field.eq('height_m')
        if not mask.any():raise IneligibleScenario(sid+': transformation absent at baseline')
        changes.append(dict(table='provenance',row_index=None,field='height_m',before=prov[mask].to_dict('records'),after=None))
        copies['provenance']=prov[~mask].reset_index(drop=True);fields.add('height_m')
    else:raise KeyError(sid)
    if table=='organism_observations' and entity!='__table__':entity=str(obs.at[i,'observation_id'] or entity)
    corruption_id=stable_id('corruption',seed,ordinal,sid) if intensity==1 else stable_id('corruption',seed,ordinal,sid,intensity)
    truth=dict(corruption_id=corruption_id,scenario=sid,corruption_class=category,intensity=float(intensity),
        table=table,entity_id=entity,row_ids=sorted(targets),fields=sorted(fields),
        expected_detection_class=expected_detection_classes(sid,category),seed=int(seed),ordinal=int(ordinal),changes_json=json.dumps(changes,default=lambda v:v.hex() if isinstance(v,bytes) else str(v),sort_keys=True))
    return copies,truth
