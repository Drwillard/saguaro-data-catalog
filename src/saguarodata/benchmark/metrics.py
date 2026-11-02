"""Injection recall and alert precision after subtracting baseline alert signatures."""
import json
from itertools import combinations
import pandas as pd
from ..validation.rules import finding_id

LAYERS=('schema','row','structural','temporal','spatial','provenance')

def signature(alert):
    # For experimental baseline subtraction, a changed/missing canonical key or
    # altered lineage metadata must not relabel an existing scientific warning
    # as a newly detected scientific error. Anchor by recorded source row/event.
    lineage=alert.get('source_lineage')
    try:lineage=json.loads(lineage) if isinstance(lineage,str) else lineage or {}
    except ValueError:lineage={}
    value=alert.get('observed_value')
    try:value=json.loads(value) if isinstance(value,str) else value
    except ValueError:pass
    def normalize(v):
        if isinstance(v,dict):return {k:normalize(x) for k,x in v.items() if k not in ('previous','previous_observation_id','previous_feature','empirical_upper','median','robust_spread','n')}
        if isinstance(v,list):return [normalize(x) for x in v]
        if isinstance(v,float) and v.is_integer():return int(v)
        return v
    return json.dumps(normalize([alert.get('rule_id'),alert.get('table'),lineage.get('source_row_id') or alert.get('entity_identifier'),alert.get('survey_event'),alert.get('field'),value]),sort_keys=True,default=str)

def matches(alert,truth):
    entity=str(alert.get('entity_identifier'))
    lineage=alert.get('source_lineage')
    try:lineage=json.loads(lineage) if isinstance(lineage,str) else lineage or {}
    except ValueError:lineage={}
    # Each independent trial has exactly one intervention. Newly emitted
    # warnings/errors attached to its affected row/history are attributable
    # effects, including downstream integrity symptoms on other fields.
    return entity in truth['row_ids'] or str(lineage.get('source_row_id')) in truth['row_ids'] or (entity=='__table__' and truth['entity_id']=='__table__')

def score(truth,baseline,observed):
    rows=[];alerts=[]
    for layer in LAYERS:
        old={signature(row) for row in baseline[layer]['findings'] if row.get('severity')!='info'}
        unique={signature(row):row for row in observed[layer]['findings'] if row.get('severity')!='info'}
        new=[row for key,row in unique.items() if key not in old]
        diagnostic_old={signature(row) for row in baseline[layer]['findings'] if row.get('rule_id')=='UNKNOWN_SPATIAL_CRS'}
        diagnostic_new=[row for row in observed[layer]['findings'] if row.get('rule_id')=='UNKNOWN_SPATIAL_CRS' and signature(row) not in diagnostic_old]
        tp=sum(matches(row,truth) for row in new);fp=len(new)-tp
        hit=tp>0
        rows.append(dict(corruption_id=truth['corruption_id'],scenario=truth['scenario'],corruption_class=truth['corruption_class'],seed=truth['seed'],layer=layer,
            intensity=float(truth.get('intensity',1.)),
            injected=1,detected=int(hit),missed=int(not hit),matched_alerts=tp,false_positive_alerts=fp,
            baseline_alerts=len(old),new_alerts=len(new),validator_error=observed[layer]['error']))
        rows[-1]['informational_crs_detection']=int(any(matches(row,truth) for row in diagnostic_new))
        for alert in new:alerts.append(dict(corruption_id=truth['corruption_id'],layer=layer,matched=matches(alert,truth),alert_json=json.dumps(alert,default=str)))
    return rows,alerts

def summarize(results):
    summaries=[]
    for layer,frame in results.groupby('layer'):
        tp=int(frame.matched_alerts.sum());fp=int(frame.false_positive_alerts.sum());n=int(frame.injected.sum());hits=int(frame.detected.sum())
        precision=tp/(tp+fp) if tp+fp else 0.;recall=hits/n if n else 0.
        # F1 uses alert-level recall: one positive opportunity per injection,
        # but multiple matched alerts are collapsed to one positive prediction.
        event_precision=hits/(hits+fp) if hits+fp else 0.
        f1=2*event_precision*recall/(event_precision+recall) if event_precision+recall else 0.
        per_seed=frame.groupby('seed').detected.mean()
        summaries.append(dict(layer=layer,injected=n,detections=hits,misses=n-hits,false_positives=fp,matched_alerts=tp,
            precision=event_precision,alert_precision=precision,recall=recall,f1=f1,
            seed_recall_std=float(per_seed.std(ddof=0)),validator_errors=int(frame.validator_error.notna().sum())))
    return pd.DataFrame(summaries)

def overlap(results):
    pivot=results.pivot(index='corruption_id',columns='layer',values='detected')
    return pd.DataFrame([dict(left=a,right=b,both=int(((pivot[a]>0)&(pivot[b]>0)).sum())) for a,b in combinations(LAYERS,2)])
