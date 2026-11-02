"""Integrity of the evidence chain, separate from scientific-data plausibility."""
import json
import math
import pandas as pd
from .rules import finding
from ..normalize.identifiers import stable_id

OBS_TABLES=('organism_observations','vegetation_observations','plot_observations')
EXPECTED={'organism_observations':('height_m','arm_count','status'),
          'vegetation_observations':('count','cover_normalized'),
          'plot_observations':('count_estimate','density_per_ha')}

def missing(value):
    return value is None or (isinstance(value,float) and math.isnan(value)) or value==''

def equivalent(a,b):
    null=lambda v:missing(v) or str(v).lower() in ('none','nan','null')
    if null(a) or null(b):return null(a) and null(b)
    try:return math.isclose(float(a),float(b),rel_tol=1e-9,abs_tol=1e-9)
    except (ValueError,TypeError):return str(a)==str(b)

def provenance_findings(tables, manifest=None):
    files=manifest if manifest is not None else tables.get('source_files',pd.DataFrame()).to_dict('records')
    file_hashes={row.get('local_filename'):row.get('sha256') for row in files}
    hashes={row.get('sha256') for row in files}
    inventory=tables.get('source_inventory',pd.DataFrame())
    sheets={(row['file'],row['sheet']) for row in inventory.to_dict('records')}
    source_columns={}
    for entry in inventory.to_dict('records'):
        try:source_columns[(entry['file'],entry['sheet'])]=set(json.loads(entry['original_columns']))
        except (ValueError,TypeError):pass
    traces=tables.get('provenance',pd.DataFrame()).to_dict('records')
    index={};canonical={};out=[]
    def emit(rule,row,field,value,message,table):
        out.append(finding(rule,row,field,value,'Consistent source evidence chain',message,'error',table))
    for trace in traces:index.setdefault((trace['table'],trace['observation_id'],trace['field']),[]).append(trace)
    for table in (*OBS_TABLES,'spatial_features'):
        for row in tables.get(table,pd.DataFrame()).to_dict('records'):
            entity=row.get('observation_id',row.get('feature_id'))
            canonical[(table,entity)]=row
            if missing(row.get('source_row_id')) or missing(row.get('source_row')):
                emit('PROVENANCE_MISSING_SOURCE',row,'source_row_id',row.get('source_row_id'),'Canonical entity lacks a source row/feature.',table)
            sha=row.get('source_sha256');filename=row.get('source_file')
            if sha not in hashes or file_hashes.get(filename)!=sha:
                emit('PROVENANCE_HASH_MISMATCH',row,'source_sha256',sha,'Source SHA is absent from the manifest or disagrees with its artifact path.',table)
            if sheets and (filename,row.get('source_sheet')) not in sheets:
                emit('PROVENANCE_MISSING_SOURCE_SHEET',row,'source_sheet',row.get('source_sheet'),'Source sheet/layer is absent from the source inventory.',table)
            if not missing(row.get('source_row')) and not missing(sha):
                try:expected=stable_id(sha,row.get('source_sheet'),int(row['source_row']))
                except (ValueError,TypeError):expected=None
                if expected!=row.get('source_row_id'):
                    emit('PROVENANCE_SOURCE_ROW_MISMATCH',row,'source_row',row.get('source_row'),'Source row ID does not match artifact, sheet and physical row.',table)
            if table not in EXPECTED:continue
            fields=list(EXPECTED[table])
            if table=='organism_observations' and not missing(row.get('longitude')):fields.append('longitude,latitude')
            for field in fields:
                records=index.get((table,entity,field),[])
                if not records:
                    emit('PROVENANCE_MISSING_TRANSFORMATION',row,field,row.get(field),'Expected normalized field has no provenance record.',table)
                for trace in records:
                    column=trace.get('source_column')
                    columns=source_columns.get((filename,row.get('source_sheet')))
                    if isinstance(column,str) and column and columns is not None and not set(column.split(','))<=columns:
                        emit('PROVENANCE_SOURCE_FIELD_MISSING',row,field,column,'Recorded source column is absent from the inventoried sheet/layer.',table)
                    if missing(trace.get('transformation')):
                        emit('PROVENANCE_MISSING_TRANSFORMATION',row,field,trace.get('transformation'),'Transformation metadata is blank.',table)
                    if any(not equivalent(row.get(k),trace.get(k)) for k in ('source_row_id','source_row','source_sha256','source_sheet')):
                        emit('PROVENANCE_LINEAGE_MISMATCH',row,field,trace.get('source_row_id'),'Transformation lineage disagrees with its canonical row.',table)
                    value=[row.get(f) for f in field.split(',')] if ',' in field else row.get(field)
                    recorded=trace.get('normalized_value')
                    if ',' in field:
                        try:recorded=json.loads(recorded);same=len(value)==len(recorded) and all(equivalent(a,b) for a,b in zip(value,recorded))
                        except (ValueError,TypeError):same=False
                    else:same=equivalent(value,recorded)
                    if not same:emit('PROVENANCE_VALUE_MISMATCH',row,field,dict(canonical=value,provenance=recorded),'Canonical value differs from its recorded normalized value.',table)
                variants={(str(t.get('source_column')),str(t.get('source_value')),str(t.get('normalized_value')),str(t.get('transformation'))) for t in records}
                if len(variants)>1:emit('PROVENANCE_CONFLICTING_TRANSFORMATION',row,field,len(variants),'Multiple conflicting provenance records exist for one canonical field.',table)
    for trace in traces:
        if (trace['table'],trace['observation_id']) not in canonical:
            emit('PROVENANCE_ORPHAN_TRANSFORMATION',trace,'observation_id',trace['observation_id'],'Transformation points to a nonexistent canonical entity.','provenance')
    all_entities={name:set(frame[key]) for name,frame in tables.items() for key in ['observation_id' if name in OBS_TABLES else 'feature_id' if name=='spatial_features' else 'plot_id' if name=='plots' else ''] if key and key in frame}
    findings=tables.get('validation_findings',pd.DataFrame())
    for row in findings.to_dict('records'):
        entity=row.get('entity_identifier');table=row.get('table')
        if table in all_entities and entity not in all_entities[table]:
            context=dict(row,observation_id=row.get('finding_id') or entity)
            emit('PROVENANCE_ORPHAN_FINDING',context,'entity_identifier',entity,'Validation finding points to a nonexistent entity.','validation_findings')
    return out
