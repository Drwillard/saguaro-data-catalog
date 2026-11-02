import pandas as pd
import pytest
from shapely.geometry import box
from saguarodata.validation.temporal import temporal_findings
from saguarodata.validation.structural import structural_findings,schema_drift
from saguarodata.validation.spatial import contains,spatial_findings

CONFIG=dict(shrinkage_absolute_m=.5,shrinkage_fraction=.2,robust_mad_multiplier=6,minimum_growth_pairs=3,coordinate_displacement_warning_m=15,vicinity_bbox=[-111.4,31.9,-110.3,32.6])
def records(**changes):
    rows=[]
    for i in range(2):
        row=dict(observation_id=str(i),organism_id='linked',program_id='historic_plots',survey_year=2000+10*i,survey_event_id=str(i),plot_id='historic_plots:41A',status='dead' if i==0 else 'alive',status_source='explicit_note',height_m=5-i*2,arm_count=3-i,source_row_id=str(i),source_individual_id='A1',status_raw='dead' if i==0 else 'alive',height_missing_reason=None,arm_count_missing_reason=None,source_plot_id='41A',height_raw='5',notes='')
        row['unit_source']='documented'
        row.update(changes);rows.append(row)
    return pd.DataFrame(rows)

def test_temporal_resurrection_shrinkage_and_arms():
    rules={r['rule_id'] for r in temporal_findings(records(),CONFIG)}
    assert {'TEMPORAL_STATUS_CONTRADICTION','TEMPORAL_SHRINKAGE','TEMPORAL_ARM_DECREASE'}<=rules

def test_unlinked_individuals_are_excluded():
    assert temporal_findings(records(organism_id=None),CONFIG)==[]

def test_not_found_is_not_death():
    frame=records();frame.loc[0,'status']='not_found'
    assert 'TEMPORAL_STATUS_CONTRADICTION' not in {r['rule_id'] for r in temporal_findings(frame,CONFIG)}

def test_inferred_alive_is_not_explicit_resurrection():
    frame=records();frame.loc[1,'status_source']='inferred_measurement'
    assert 'TEMPORAL_STATUS_CONTRADICTION' not in {r['rule_id'] for r in temporal_findings(frame,CONFIG)}

def test_zero_sentinel_is_not_extreme_shrinkage():
    frame=records();frame.loc[1,'height_m']=0
    assert 'TEMPORAL_SHRINKAGE' not in {r['rule_id'] for r in temporal_findings(frame,CONFIG)}

def test_duplicate_organism_event():
    frame=records();frame.loc[1,'survey_event_id']='0'
    rules=structural_findings(frame,pd.DataFrame({'plot_id':['historic_plots:41A']}),pd.DataFrame({'survey_event_id':['0']}))
    assert 'DUPLICATE_ORGANISM_EVENT' in {r['rule_id'] for r in rules}

def test_containment_includes_boundary():
    polygon=box(0,0,10,10).wkb
    assert contains(polygon,0,5)
    assert not contains(polygon,11,5)

def test_schema_drift():
    drift=schema_drift({'height':'float','browning':'float'},{'height':'str','arms':'int'})
    assert drift['removed']==['browning']
    assert drift['introduced']==['arms']
    assert drift['type_changes']['height']==['float','str']

def test_spatial_displacement_requires_independent_coordinates():
    frame=records();frame['longitude']=[-111.0,-110.99];frame['latitude']=[32.2,32.2];frame['coordinate_time_basis']='survey_event'
    rules=spatial_findings(frame,pd.DataFrame(columns=['plot_id','geometry']),pd.DataFrame(),CONFIG)
    assert 'COORDINATE_DISPLACEMENT' in {r['rule_id'] for r in rules}
    frame['coordinate_time_basis']='shared_source_location'
    rules=spatial_findings(frame,pd.DataFrame(columns=['plot_id','geometry']),pd.DataFrame(),CONFIG)
    assert 'COORDINATE_DISPLACEMENT' not in {r['rule_id'] for r in rules}

def test_unknown_crs_is_reported_once_per_layer():
    frame=records();frame['longitude']=None;frame['latitude']=None;frame['coordinate_time_basis']=None
    features=pd.DataFrame([dict(feature_id=str(i),geometry_valid=True,crs=None,source_sha256='hash',source_sheet='local',layer='local') for i in range(3)])
    findings=spatial_findings(frame,pd.DataFrame(columns=['plot_id','geometry']),features,CONFIG)
    assert len(findings)==1
    assert findings[0]['rule_id']=='UNKNOWN_SPATIAL_CRS'

def test_explicit_subplot_parent_containment():
    frame=records();frame['longitude']=None;frame['latitude']=None;frame['coordinate_time_basis']=None
    plots=pd.DataFrame([dict(plot_id='p',parent_plot_id=None,geometry=box(0,0,10,10).wkb,crs='EPSG:26912'),dict(plot_id='s',parent_plot_id='p',geometry=box(9,9,11,11).wkb,crs='EPSG:26912')])
    findings=spatial_findings(frame,plots,pd.DataFrame(),CONFIG)
    assert 'SUBPLOT_OUTSIDE_PARENT' in {r['rule_id'] for r in findings}

def test_empirical_growth_outlier():
    frames=[]
    for i in range(20):
        frame=records(organism_id=f'plant{i}',status='unknown')
        frame['height_m']=frame.height_m.astype(float)
        frame.loc[0,'height_m']=1
        frame.loc[1,'height_m']=2+i*.01 if i<19 else 20
        frame['observation_id']=[f'{i}:a',f'{i}:b']
        frames.append(frame)
    findings=temporal_findings(pd.concat(frames),CONFIG)
    outliers=[r for r in findings if r['rule_id']=='TEMPORAL_GROWTH_OUTLIER']
    assert len(outliers)==1
    assert outliers[0]['entity_identifier']=='19:b'
