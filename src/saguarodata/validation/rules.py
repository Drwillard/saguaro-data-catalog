from dataclasses import dataclass, asdict
import json
from ..jsonutil import dumps
import hashlib

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

def finding(rule, row, field, value, expected, message, severity='warning', table='organism_observations'):
    keys = ['source_dataset','source_file','source_sheet','source_row','source_reference_id','source_sha256','source_row_id']
    result = asdict(Finding(rule, severity, table,
        str(row.get('observation_id', row.get('feature_id', row.get('entity_identifier', '')))),
        row.get('survey_event_id'), field, dumps(value, default=str), expected, message,
        dumps({k:row.get(k) for k in keys}, default=str)))
    result['finding_id']=finding_id(result)
    return result
