import json
import xml.etree.ElementTree as ET
import pandas as pd
import pytest
from saguarodata.inventory import inventory
from saguarodata.pipeline import build
from saguarodata.schema_history import evolution
from saguarodata.validation.engine import validate
from saguarodata.validation.provenance import provenance_findings
from saguarodata.lineage import build_graph
from saguarodata.lineage.trace import node_id

@pytest.fixture
def graph(fixture_root):
    inventory(fixture_root);build(fixture_root);evolution(fixture_root);validate(fixture_root)
    return build_graph(fixture_root),fixture_root

def test_field_and_observation_trace_stable(graph):
    g,root=graph;obs=pd.read_parquet(root/'data/processed/organism_observations.parquet').iloc[0]
    trace=g.trace_field(obs.observation_id,'height_m')
    types={n['type'] for n in trace['nodes']}
    assert {'source_reference','source_artifact','source_sheet','source_row','source_field','transformation','canonical_field'}<=types
    fields=[n for n in trace['nodes'] if n['type']=='canonical_field']
    assert fields[0]['attributes']['value']==obs.height_m
    other=build_graph(root)
    assert trace==other.trace_field(obs.observation_id,'height_m')
    assert not g.trace_observation(obs.observation_id)['truncated']

def test_temporal_evidence_both_observations(graph):
    g,root=graph
    findings=pd.read_parquet(root/'data/processed/validation_findings.parquet')
    finding=findings[findings.rule_id.eq('TEMPORAL_SHRINKAGE')].iloc[0]
    trace=g.trace_finding(finding.finding_id)
    ids={n['attributes']['entity_id'] for n in trace['nodes'] if n['type']=='canonical_observation'}
    assert finding.entity_identifier in ids and json.loads(finding.observed_value)['previous'] in ids

def test_orphans_and_value_gaps(graph):
    _,root=graph;tables={p.stem:pd.read_parquet(p) for p in (root/'data/processed').glob('*.parquet')}
    obs=tables['organism_observations'];entity=obs.iloc[0].observation_id
    tables['provenance']=tables['provenance'][~(tables['provenance'].observation_id.eq(entity)&tables['provenance'].field.eq('height_m'))]
    tables['validation_findings'].loc[0,'entity_identifier']='missing-observation'
    rules={r['rule_id'] for r in provenance_findings(tables)}
    assert {'PROVENANCE_ORPHAN_FINDING','PROVENANCE_MISSING_TRANSFORMATION'}<=rules

def test_exports_and_bounded_traversal(graph,tmp_path):
    g,_=graph;counts=g.summary()
    g.export(tmp_path/'graph.json','json');payload=json.loads((tmp_path/'graph.json').read_text())
    assert len(payload['nodes'])==sum(counts['node_counts'].values())
    g.export(tmp_path/'graph.graphml','graphml')
    tree=ET.parse(tmp_path/'graph.graphml')
    assert len(tree.findall('.//{http://graphml.graphdrawing.org/xmlns}node'))==len(payload['nodes'])
    g.export(tmp_path/'tables','parquet')
    assert len(pd.read_parquet(tmp_path/'tables/nodes.parquet'))==len(payload['nodes'])
    assert g.downstream(next(n['id'] for n in payload['nodes'] if n['type']=='source_artifact'),max_nodes=2)['truncated']

def test_shared_ids_survive_json_null_conversion():
    from saguarodata.lineage.trace import evidence_trace
    from saguarodata.jsonutil import sanitize
    row=dict(observation_id='o',source_sha256='s',source_sheet='sheet',source_row=1,height_m=None)
    traces=[dict(field='height_m',source_column=float('nan'),source_value=float('nan'),normalized_value=None,transformation='not_collected')]
    a=evidence_trace('organism_observations',row,traces,fields=['height_m'])
    b=evidence_trace('organism_observations',sanitize(row),sanitize(traces),fields=['height_m'])
    assert a==b

def test_finalize_existing_typed_tables_matches_full_build(graph):
    from saguarodata.lineage.builder import resume_built_tables
    import shutil
    g,root=graph
    before=json.loads((root/'data/lineage/summary.json').read_text())
    shutil.copyfile(g.path,root/'data/lineage/lineage.build.sqlite')
    recovered=resume_built_tables(root)
    after=json.loads((root/'data/lineage/summary.json').read_text())
    assert g.summary()==recovered.summary()
    for key in ('coverage','orphan_edges','largest_trace_depth','unresolved_depth_nodes'):
        assert before[key]==after[key]
