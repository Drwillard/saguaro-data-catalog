import json
import pandas as pd
import pytest
from saguarodata.validation.temporal import temporal_findings
from saguarodata.validation.rules import finding,RULE_ALIASES
from saguarodata.normalize.annotations import observation_annotations,verification_status
from saguarodata.ingest.common import note_status

CONFIG=dict(shrinkage_absolute_m=.5,shrinkage_fraction=.2,robust_mad_multiplier=6,minimum_growth_pairs=3)

def pair(first='unknown',second='unknown'):
    return pd.DataFrame([
        dict(observation_id='a',organism_id='linked',survey_event_id='first',program_id='historic_plots',survey_year=1975,
             height_m=7.455,arm_count=6,status=first,status_source='explicit_note' if first!='unknown' else 'unknown',status_raw='fairtop thin',notes='fairtop thin',verification_status='no',verification_raw='No',verification_time_basis='shared_source_row'),
        dict(observation_id='b',organism_id='linked',survey_event_id='second',program_id='historic_plots',survey_year=2001,
             height_m=1.55,arm_count=0,status=second,status_source='explicit_note' if second!='unknown' else 'unknown',status_raw='live',notes='live',verification_status='no',verification_raw='No',verification_time_basis='shared_source_row')])

def test_explicit_status_contradiction_not_literal_claim():
    rows=temporal_findings(pair('dead','alive'),CONFIG)
    record=next(r for r in rows if r['rule_id']=='TEMPORAL_STATUS_CONTRADICTION')
    assert record['finding_category']=='semantic_contradiction' and record['severity']=='warning'
    evidence=json.loads(record['observed_value'])
    assert evidence['transition']=='dead_to_alive'
    assert evidence['previous_status']=='dead' and evidence['current_status']=='alive'
    assert not any(r['rule_id']=='TEMPORAL_RESURRECTION' for r in rows)

def test_positive_measurement_is_not_alive():
    rows=temporal_findings(pair('dead','unknown'),CONFIG)
    assert not any(r['rule_id']=='TEMPORAL_STATUS_CONTRADICTION' for r in rows)
    record=next(r for r in rows if r['rule_id']=='TEMPORAL_MEASUREMENT_AFTER_DEATH')
    assert record['finding_category']=='data_quality_warning'
    assert 'standing dead' in record['message'] and 'does not establish survival' in record['message']

def test_not_found_is_informational():
    rows=temporal_findings(pair('not_found','alive'),CONFIG)
    record=next(r for r in rows if r['rule_id']=='TEMPORAL_REOBSERVED')
    assert record['finding_category']=='informational' and record['severity']=='info'
    assert not any(r['finding_category']=='semantic_contradiction' for r in rows)

def test_biological_changes_keep_thresholds_and_source_context():
    rows=temporal_findings(pair('unknown','alive'),CONFIG)
    for rule in ('TEMPORAL_SHRINKAGE','TEMPORAL_ARM_DECREASE'):
        row=next(r for r in rows if r['rule_id']==rule)
        assert row['finding_category']=='biological_transition' and row['severity']=='warning'
        e=json.loads(row['observed_value'])
        assert e['previous_notes']=='fairtop thin' and e['current_notes']=='live'
        assert e['previous_verification_status']==e['current_verification_status']=='no'
        assert e['previous_year']==1975 and e['current_year']==2001
    assert note_status('fairtop thin')[0]=='unknown'

@pytest.mark.parametrize('phrase,expected',[
    ('tag only',{'tag_only'}),('off plot - not measured',{'off_plot','not_measured'}),
    ('NEED CHECK',{'needs_review'}),('fairtop thin',set()),('bad top',set()),('damaged',set()),('poor',set()),('leaning',set()),
    ('not dead',set()),('tag only possibly damaged',set())])
def test_literal_operational_annotations(phrase,expected):
    assert {key for key,value in observation_annotations(phrase).items() if value}==expected
    if phrase!='tag only':assert note_status(phrase)[0]=='unknown'

@pytest.mark.parametrize('raw,expected',[('Yes','yes'),('No','no'),('Not Found','not_found'),('','not_recorded'),('Maybe','unrecognized')])
def test_verify_is_context_not_correctness(raw,expected):
    assert verification_status(raw)==expected

def test_legacy_rule_alias_only_emits_new_name():
    row=finding('TEMPORAL_RESURRECTION',{},'status',{},'review','review')
    assert row['rule_id']=='TEMPORAL_STATUS_CONTRADICTION'
    assert row['finding_category']=='semantic_contradiction'
