import json
import pandas as pd
from saguarodata.inventory import inventory
from saguarodata.pipeline import build
from saguarodata.schema_history import evolution
from saguarodata.validation.engine import validate
from saguarodata.reports.quality_report import report
from saguarodata import load

def test_mock_download_to_parquet_query_and_report(fixture_root):
    root=fixture_root
    inv=inventory(root)
    assert len(inv)>0
    build(root);evolution(root);findings=validate(root)
    ds=load(root/'data/processed')
    assert len(ds.observations(program='census'))==2
    assert ds.observations(program='census').organism_id.isna().all()
    aggregates=ds.table('plot_observations')
    assert aggregates.loc[aggregates.survey_year.eq(1990),'count_estimate'].iloc[0]==3.2
    assert aggregates.loc[aggregates.source_plot_id.eq('75G'),'program_id'].iloc[0]=='census_summary_auxiliary'
    assert 'census:1990' in set(ds.surveys().survey_event_id)
    assert 'census_summary_auxiliary:75G' in set(ds.plots().plot_id)
    historic=ds.observations(program='historic_plots')
    assert historic.loc[historic.source_plot_id.eq('71G'),'organism_id'].isna().all()
    linked=historic.organism_id.dropna().iloc[0]
    assert len(ds.history(linked))==4
    obs=ds.history(linked).iloc[0]
    trace=ds.provenance(obs.observation_id)
    assert set(trace.field)>={'height_m','arm_count','status','longitude,latitude'}
    assert trace.source_row.eq(8).all()
    assert 'TEMPORAL_RESURRECTION' in set(findings.rule_id)
    summary=report(root)
    assert summary['validation_findings']>0
    assert (root/'reports/data_quality_report.html').exists()
    # Derived rebuild retains deterministic observation identities.
    before=ds.observations().observation_id.tolist()
    build(root)
    assert ds.observations().observation_id.tolist()==before

def test_inventory_preserves_literal_missing_tokens(fixture_root):
    inv=inventory(fixture_root)
    row=inv[inv.sheet.eq('RawData_2000_2010')].iloc[0]
    fields={f['name']:f for f in json.loads(row.fields)}
    assert 'not measured' in fields['Arms']['categories']
    assert fields['Arms']['missing_count']==0
