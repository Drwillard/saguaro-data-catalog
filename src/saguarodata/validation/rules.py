from dataclasses import dataclass, asdict
import json
from ..jsonutil import dumps
import hashlib
from ..model.canonical import FINDING_CATEGORIES

RULE_ALIASES={'TEMPORAL_RESURRECTION':'TEMPORAL_STATUS_CONTRADICTION'}

def finding_category(rule,severity='warning'):
    rule=RULE_ALIASES.get(rule,rule)
    if rule.startswith(('PROVENANCE_','SCHEMA_','ROW_')):return 'integrity_violation'
    if rule=='TEMPORAL_STATUS_CONTRADICTION':return 'semantic_contradiction'
    if rule in ('TEMPORAL_SHRINKAGE','TEMPORAL_ARM_DECREASE'):return 'biological_transition'
    if rule in ('TEMPORAL_REOBSERVED','TEMPORAL_STATUS_RESOLVED'):return 'informational'
    if rule in {'NEGATIVE_MEASUREMENT','INVALID_NUMERIC','NONINTEGER_ARM_COUNT','REQUIRED_PLOT_ID','FK_PLOT','FK_SURVEY_EVENT',
        'DUPLICATE_OBSERVATION_ID','DUPLICATE_SOURCE_ROW','DUPLICATE_ORGANISM_EVENT','INVALID_GEOGRAPHIC_COORDINATE',
        'INVALID_OR_NULL_GEOMETRY','INVALID_SOURCE_GEOMETRY','IDENTITY_CONTEXT_MISMATCH','EVENT_YEAR_MISMATCH','NORMALIZED_UNIT_MISSING',
        'COORDINATE_CRS_MISMATCH','INVALID_COORDINATE_CRS'}:return 'integrity_violation'
    return 'informational' if severity=='info' else 'data_quality_warning'

def finding_id(row):
    """Content identity independent of report ordering, timestamps and review status."""
    keys=('rule_id','table','entity_identifier','survey_event','field','observed_value','source_lineage')
    return hashlib.sha256(dumps({k:row.get(k) for k in keys},sort_keys=True,default=str).encode()).hexdigest()[:24]

@dataclass
class Finding:
    rule_id: str
    severity: str
    table: str
    entity_identifier: str
    survey_event: str | None
    field: str
    observed_value: str
    expected_condition: str
    message: str
    source_lineage: str
    status: str = 'open'
    finding_category: str = 'data_quality_warning'

def finding(rule, row, field, value, expected, message, severity='warning', table='organism_observations',category=None):
    rule=RULE_ALIASES.get(rule,rule)
    keys = ['source_dataset','source_file','source_sheet','source_row','source_reference_id','source_sha256','source_row_id']
    result = asdict(Finding(rule, severity, table,
        str(row.get('observation_id', row.get('feature_id', row.get('entity_identifier', '')))),
        row.get('survey_event_id'), field, dumps(value, default=str), expected, message,
        dumps({k:row.get(k) for k in keys}, default=str)))
    result['finding_id']=finding_id(result)
    result['finding_category']=category or finding_category(rule,severity)
    if result['finding_category'] not in FINDING_CATEGORIES:raise ValueError(result['finding_category'])
    return result
