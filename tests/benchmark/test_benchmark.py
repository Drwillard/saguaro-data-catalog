import copy
import pandas as pd
import pytest
import yaml
from saguarodata.inventory import inventory
from saguarodata.pipeline import build
from saguarodata.schema_history import evolution
from saguarodata.validation.engine import validate
from saguarodata.benchmark.corruption import inject
from saguarodata.benchmark.runner import validate_layers,run_benchmark
from saguarodata.benchmark.metrics import score,summarize,LAYERS

@pytest.fixture
def canonical(fixture_root):
    inventory(fixture_root);build(fixture_root);evolution(fixture_root);validate(fixture_root)
    return {p.stem:pd.read_parquet(p) for p in (fixture_root/'data/processed').glob('*.parquet')}

def test_injection_deterministic_isolated_ground_truth(canonical):
    original=canonical['organism_observations'].copy(deep=True)
    a,truth=inject(canonical,'row_negative_height',42)
    b,repeated=inject(canonical,'row_negative_height',42)
    pd.testing.assert_frame_equal(a['organism_observations'],b['organism_observations'])
    pd.testing.assert_frame_equal(canonical['organism_observations'],original)
    assert truth==repeated and truth['row_ids'] and truth['fields']==['height_m']
    assert (a['organism_observations'].height_m<0).sum()==1

def test_all_thirty_scenarios_reproducible(canonical):
    from saguarodata.benchmark.scenarios import load_scenarios
    from shapely.affinity import translate
    from shapely import from_wkb
    tables={k:v.copy(deep=True) for k,v in canonical.items()}
    obs=tables['organism_observations'];other=obs.loc[obs.longitude.notna()&obs.organism_id.notna()].iloc[0].copy()
    other['observation_id']='second-plot-observation';other['organism_id']='second-organism';other['plot_id']='historic_plots:41B';other['longitude']+=.02
    tables['organism_observations']=pd.concat([obs,other.to_frame().T],ignore_index=True)
    plot=tables['plots'].loc[tables['plots'].geometry.notna()].iloc[0].copy();plot['plot_id']=other.plot_id
    plot['geometry']=translate(from_wkb(plot.geometry),xoff=2000).wkb
    tables['plots']=pd.concat([tables['plots'],plot.to_frame().T],ignore_index=True)
    scenarios=load_scenarios('.')
    assert len(scenarios)==30
    for ordinal,scenario in enumerate(scenarios):
        first,truth=inject(tables,scenario,17,ordinal)
        second,repeated=inject(tables,scenario,17,ordinal)
        assert truth==repeated and truth['changes_json'] and truth['row_ids']
        for table in first:pd.testing.assert_frame_equal(first[table],second[table])

def test_baseline_subtraction_uses_source_anchor():
    from saguarodata.benchmark.metrics import signature,matches
    alert=dict(rule_id='EXISTING_WARNING',table='organism_observations',entity_identifier='old',survey_event='e',field='height_m',observed_value='{"value": 1.0}',source_lineage='{"source_row_id":"r","source_row":1}')
    changed=dict(alert,entity_identifier=None,source_lineage='{"source_row_id":"r","source_row":999}',observed_value='{"value": 1}')
    assert signature(alert)==signature(changed)
    with_reference=dict(alert,observed_value='{"value":1,"previous":"old-id"}')
    without_reference=dict(alert,observed_value='{"value":1,"previous":null}')
    assert signature(with_reference)==signature(without_reference)
    assert matches(changed,dict(row_ids=['r'],fields=['observation_id'],entity_id='old'))

@pytest.mark.parametrize('scenario,layer,rule',[
    ('row_negative_height','row','ROW_RANGE'),
    ('schema_numeric_string','schema','SCHEMA_NUMERIC_TYPE'),
    ('temporal_dead_to_alive','temporal','TEMPORAL_RESURRECTION'),
    ('spatial_crs_mislabeled','spatial','COORDINATE_CRS_MISMATCH'),
    ('provenance_source_row_changed','provenance','PROVENANCE_SOURCE_ROW_MISMATCH'),
    ('provenance_transformation_removed','provenance','PROVENANCE_MISSING_TRANSFORMATION')])
def test_actual_validators(canonical,scenario,layer,rule):
    config=yaml.safe_load(open('configs/validation_rules.yaml'))
    mutated,truth=inject(canonical,scenario,1)
    results=validate_layers(mutated,config)
    assert results[layer]['error'] is None
    assert rule in {r['rule_id'] for r in results[layer]['findings']}

def test_metrics_units_and_overlap():
    rows=[]
    for layer in LAYERS:
        rows.extend([dict(layer=layer,seed=1,injected=1,detected=1,matched_alerts=3,false_positive_alerts=1,validator_error=None),
                     dict(layer=layer,seed=2,injected=1,detected=0,matched_alerts=0,false_positive_alerts=0,validator_error=None)])
    summary=summarize(pd.DataFrame(rows))
    assert summary.iloc[0].precision==.5 and summary.iloc[0].recall==.5 and summary.iloc[0].f1==.5
    assert summary.iloc[0].alert_precision==.75

def test_numeric_intensity_preserves_targets(canonical):
    low,a=inject(canonical,'temporal_positive_growth',42,intensity=.25)
    high,b=inject(canonical,'temporal_positive_growth',42,intensity=1.)
    assert a['row_ids']==b['row_ids'] and a['corruption_id']!=b['corruption_id']
    assert a['intensity']==.25 and b['intensity']==1.
    changed=(high['organism_observations'].height_m-low['organism_observations'].height_m).dropna()
    assert changed.max()==75.

def test_end_to_end_repeat_seeds(fixture_root,canonical):
    import shutil
    shutil.copy('configs/corruption_scenarios.yaml',fixture_root/'configs/corruption_scenarios.yaml')
    path=fixture_root/'data/processed/organism_observations.parquet';before=path.read_bytes()
    run_benchmark(fixture_root,[1,2],count=3,sample_size=0)
    first=pd.read_parquet(fixture_root/'data/benchmark/ground_truth.parquet')
    run_benchmark(fixture_root,[1,2],count=3,sample_size=0)
    pd.testing.assert_frame_equal(first,pd.read_parquet(fixture_root/'data/benchmark/ground_truth.parquet'))
    assert path.read_bytes()==before
    assert len(first)==6 and (fixture_root/'reports/corruption_benchmark.md').exists()
    run_benchmark(fixture_root,[3],count=1,sample_size=0,intensity=.25,append=True)
    assert len(pd.read_parquet(fixture_root/'data/benchmark/ground_truth.parquet'))==7
