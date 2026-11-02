"""Shared node identities and evidence-flow semantics for full and compact graphs."""
import hashlib
import json
import math
from ..normalize.identifiers import stable_id
from ..jsonutil import sanitize,dumps
from ..validation.rules import finding_id
from ..validation.provenance import equivalent

def node_id(kind,*parts):return kind+':'+stable_id(kind,*sanitize(list(parts)))
def edge_id(source,target,kind):return stable_id('edge',source,target,kind)
def plain(value):
    if isinstance(value,bytes):return dict(encoding='wkb-sha256',sha256=hashlib.sha256(value).hexdigest(),bytes=len(value))
    return sanitize(value)

def observation_node(table,entity):return node_id('canonical_observation',table,str(entity))
def field_node(table,entity,field):return node_id('canonical_field',table,str(entity),field)
def finding_node(row):return node_id('validation_finding',row.get('finding_id') or finding_id(row))

def evidence_trace(table,row,traces,file=None,fields=None,source_columns=None):
    """Exact local evidence slice using the same model as the full graph builder.

    Forward edges always run from evidence to derived result. Null source columns
    mean absent/uncollected source fields, not invented cells or mappings.
    """
    nodes={};edges={}
    def node(kind,parts,label,attributes):
        ident=node_id(kind,*parts);nodes[ident]=dict(id=ident,type=kind,label=str(label),attributes=plain(attributes));return ident
    def edge(a,b,kind):
        ident=edge_id(a,b,kind);edges[ident]=dict(id=ident,source=a,target=b,type=kind)
    entity=str(row.get('observation_id',row.get('feature_id')))
    sha=row.get('source_sha256');sheet=row.get('source_sheet');physical=row.get('source_row')
    source_row=node('source_row',(sha,sheet,str(physical)),f'{sheet} · row {physical}',
        dict(source_row=physical,source_row_id=row.get('source_row_id'),source_sheet=sheet,source_sha256=sha,source_file=row.get('source_file')))
    source_sheet=node('source_sheet',(sha,sheet),sheet,dict(source_sheet=sheet,source_sha256=sha))
    edge(source_sheet,source_row,'contains')
    if file:
        reference=node('source_reference',(str(file.get('source_reference_id')),),'NPS '+str(file.get('source_reference_id')),
            dict(reference_id=file.get('source_reference_id'),url=file.get('source_url')))
        artifact=node('source_artifact',(sha,),file.get('filename') or row.get('source_file'),
            dict(sha256=sha,filename=file.get('filename'),url=file.get('direct_download_url'),source_url=file.get('source_url')))
        edge(reference,artifact,'references');edge(artifact,source_sheet,'contains')
    observation=node('canonical_observation',(table,entity),entity,
        dict(table=table,entity_id=entity,program_id=row.get('program_id',row.get('source_dataset')),survey_year=row.get('survey_year'),plot_id=row.get('plot_id')))
    edge(source_row,observation,'represents')
    mapped=set()
    for trace in traces:
        names=trace['field'].split(',')
        if fields is not None and not set(names)&set(fields):continue
        column=trace.get('source_column')
        has_column=isinstance(column,str) and bool(column)
        verified=bool(has_column and source_columns is not None and set(column.split(','))<=set(source_columns))
        transform=node('transformation',(table,entity,trace['field'],trace.get('source_column'),trace.get('source_value'),trace.get('normalized_value'),trace.get('transformation')),
            trace.get('transformation') or 'Missing transformation',
            dict({k:trace.get(k) for k in ('field','source_column','source_value','normalized_value','transformation','value_kind')},source_mapping_verified=verified,input_uncollected_or_unmapped=not has_column))
        if has_column:
            source_field=node('source_field',(sha,sheet,str(physical),column,str(sanitize(trace.get('source_value')))),
                column if verified or source_columns is None else column+' (not in source sheet)',dict(source_column=column,value=trace.get('source_value'),exists_in_source=verified if source_columns is not None else None))
            edge(source_row,source_field,'contains');edge(source_field,transform,'transformed_by')
        else:edge(source_row,transform,'uncollected_or_unmapped_input')
        for field in names:
            recorded=trace.get('normalized_value')
            if len(names)>1:
                try:recorded=json.loads(recorded)[names.index(field)]
                except (ValueError,TypeError,IndexError):recorded=None
            canonical=node('canonical_field',(table,entity,field),field,dict(table=table,entity_id=entity,field=field,value=plain(row.get(field)),mapping_recorded=True,transformation_recorded=bool(trace.get('transformation')),value_matches_record=equivalent(row.get(field),recorded),source_mapping_verified=verified,input_uncollected_or_unmapped=not has_column))
            edge(transform,canonical,'derives');edge(canonical,observation,'belongs_to');mapped.add(field)
    if fields is None:
        selected=[field for field in row if not field.startswith('source_') and field not in ('raw_values_json','attributes_json','observation_id','feature_id')]
    else:selected=fields
    for field in selected:
        if field in mapped:continue
        canonical=node('canonical_field',(table,entity,field),field,dict(table=table,entity_id=entity,field=field,value=plain(row.get(field)),mapping_recorded=False))
        edge(source_row,canonical,'row_lineage_only');edge(canonical,observation,'belongs_to')
    return dict(root=observation,nodes=list(nodes.values()),edges=list(edges.values()),truncated=False)

def evidence_entities(finding):
    """Only recorded explicit references; never infer identity from nearby rows."""
    value=finding.get('observed_value')
    try:value=json.loads(value) if isinstance(value,str) else value
    except ValueError:value={}
    result=[]
    if isinstance(value,dict):
        for key in ('previous','previous_observation_id','previous_feature'):
            if isinstance(value.get(key),str):result.append(value[key])
    return result
