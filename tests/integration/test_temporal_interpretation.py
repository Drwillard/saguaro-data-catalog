import json
from saguarodata.inventory import inventory
from saguarodata.pipeline import build
from saguarodata.schema_history import evolution
from saguarodata.validation.engine import validate
from saguarodata.api.dataset import Dataset
from saguarodata.reports.temporal_interpretation import temporal_report

def test_context_categories_api_and_interpretation(fixture_root):
    inventory(fixture_root);build(fixture_root);evolution(fixture_root);validate(fixture_root)
    ds=Dataset(fixture_root/'data/processed')
    selected=ds.validation_findings(finding_category='biological_transition',severity='warning')
    assert len(selected)>0 and selected.finding_category.eq('biological_transition').all()
    legacy=ds.validation_findings(rule_id='TEMPORAL_RESURRECTION')
    assert legacy.rule_id.eq('TEMPORAL_STATUS_CONTRADICTION').all() and len(legacy)>0
    historic=ds.observations(program='historic_plots')
    assert historic[historic.source_individual_id.eq('A1')].verification_status.eq('yes').all()
    assert historic[historic.source_individual_id.eq('A1')].verification_time_basis.eq('shared_source_row').all()
    result=temporal_report(fixture_root,ds)
    assert result['real_status_contradictions']>0 and result['context_totals']['verify_yes']>0
    assert (fixture_root/'reports/temporal_interpretation_by_rule.csv').exists()
