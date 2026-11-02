"""Build evidence-flow tables from authoritative canonical/provenance data."""
from collections import Counter
from pathlib import Path
import json
import sqlite3
import pandas as pd
from ..acquisition.checksums import sha256
from ..jsonutil import dumps
from ..validation.rules import finding_id
from ..validation.provenance import EXPECTED,equivalent
from ..normalize.identifiers import stable_id
from .trace import node_id,edge_id,evidence_trace,observation_node,field_node,evidence_entities,finding_node
from .graph import LineageGraph

def build_graph(root='.',export_tables=True):
    root=Path(root).resolve();folder=root/'data/lineage';folder.mkdir(parents=True,exist_ok=True)
    paths=sorted((root/'data/processed').glob('*.parquet'))
    inputs={p.name:sha256(p) for p in paths}
    tables={p.stem:pd.read_parquet(p) for p in paths}
    target=folder/'lineage.sqlite';temporary=folder/'lineage.build.sqlite'
    if temporary.exists():temporary.unlink()
    conn=sqlite3.connect(temporary)
    conn.executescript('PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF; PRAGMA cache_size=-131072; CREATE TABLE nodes(id TEXT PRIMARY KEY,type TEXT,label TEXT,attributes TEXT); CREATE TABLE edges(id TEXT PRIMARY KEY,source TEXT,target TEXT,type TEXT);')
    node_buffer={};edge_buffer={};counts=Counter();coverage=Counter();depth={};max_depth=0
    def flush():
        conn.executemany('INSERT OR IGNORE INTO nodes VALUES (?,?,?,?)',node_buffer.values())
        conn.executemany('INSERT OR IGNORE INTO edges VALUES (?,?,?,?)',edge_buffer.values())
        conn.commit();node_buffer.clear();edge_buffer.clear()
    def node(ident,kind,label,attrs):
        node_buffer[ident]=(ident,kind,str(label),dumps(attrs,default=str,sort_keys=True))
    def edge(a,b,kind):edge_buffer[edge_id(a,b,kind)]=(edge_id(a,b,kind),a,b,kind)
    manifest_path=root/'data/raw/manifest.json'
    manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else tables['source_files'].to_dict('records')
    files={r['local_filename']:r for r in manifest}
    inventory={(r['file'],r['sheet']) for r in tables['source_inventory'].to_dict('records')}
    source_columns={(r['file'],r['sheet']):json.loads(r['original_columns']) for r in tables['source_inventory'].to_dict('records')}
    traces={}
    for row in tables['provenance'].to_dict('records'):traces.setdefault((row['table'],row['observation_id']),[]).append(row)
    complete={};field_complete={};entity_lookup={};examples=[]
    # Explicit context entities contain their observations; they do not connect
    # unrelated observations to one another or imply longitudinal identity.
    for table,kind,key in [('organisms','organism','organism_id'),('plots','plot','plot_id'),('survey_events','survey_event','survey_event_id')]:
        for row in tables[table].to_dict('records'):
            ident=node_id(kind,str(row[key]));node(ident,kind,row[key],{k:v for k,v in row.items() if k!='geometry'})
    for table,key in [('organism_observations','observation_id'),('vegetation_observations','observation_id'),('plot_observations','observation_id'),('spatial_features','feature_id')]:
        frame=tables[table]
        for row in frame.to_dict('records'):
            entity=str(row[key]);file=files.get(row.get('source_file'))
            records=traces.get((table,entity),[])
            valid=bool(file and file['sha256']==row.get('source_sha256') and (row.get('source_file'),row.get('source_sheet')) in inventory and pd.notna(row.get('source_row')) and row.get('source_row_id')==stable_id(row.get('source_sha256'),row.get('source_sheet'),int(row['source_row'])))
            # A missing manifest artifact is not synthesized from the row's claim.
            trace=evidence_trace(table,row,records,file if valid else None,source_columns=source_columns.get((row.get('source_file'),row.get('source_sheet'))))
            field_complete[(table,entity)]={n['attributes']['field'] for n in trace['nodes'] if n['type']=='canonical_field' and n['attributes'].get('transformation_recorded') and n['attributes'].get('value_matches_record') and (n['attributes'].get('source_mapping_verified') or n['attributes'].get('input_uncollected_or_unmapped'))}
            for item in trace['nodes']:node(item['id'],item['type'],item['label'],item['attributes'])
            for item in trace['edges']:edge(item['source'],item['target'],item['type'])
            oid=observation_node(table,entity);entity_lookup[(table,entity)]=oid;complete[(table,entity)]=valid
            for field,kind in [('organism_id','organism'),('plot_id','plot'),('survey_event_id','survey_event')]:
                value=row.get(field)
                if value is not None and not pd.isna(value):edge(node_id(kind,str(value)),oid,'has_observation')
            counts[table]+=1
            if table!='spatial_features':
                coverage['observations']+=1;coverage['observations_row_lineage_complete']+=int(valid)
                expected=list(EXPECTED[table])
                if table=='organism_observations' and pd.notna(row.get('longitude')):expected+=['longitude,latitude']
                coverage['expected_normalized_fields']+=len(expected)
                known={r['field'] for r in records if r.get('transformation')}
                coverage['normalized_fields_with_transformation']+=sum(f in known for f in expected)
                verified_fields=field_complete[(table,entity)]
                coverage['normalized_fields_with_verified_source_mapping']+=sum(set(f.split(','))<=verified_fields for f in expected)
                coverage['observations_complete_field_lineage']+=int(valid and all(set(f.split(','))<=verified_fields for f in expected))
                coverage['observations_all_expected_transforms']+=int(all(f in known for f in expected))
                coverage['canonical_fields_without_explicit_mapping']+=sum(item['type']=='canonical_field' and not item['attributes']['mapping_recorded'] for item in trace['nodes'])
            if len(examples)<3 and table=='organism_observations' and valid:examples.append(entity)
            if len(node_buffer)>10000:flush()
        print(f'Lineage: {table}, {len(frame):,} records',flush=True)
    # Add only real references/artifacts/sheets, including zero-row inventories.
    for file in files.values():
        ref=node_id('source_reference',str(file['source_reference_id']));artifact=node_id('source_artifact',file['sha256'])
        node(ref,'source_reference','NPS '+str(file['source_reference_id']),dict(reference_id=file['source_reference_id'],url=file.get('source_url')))
        node(artifact,'source_artifact',file.get('filename'),dict(sha256=file['sha256'],filename=file.get('filename'),url=file.get('direct_download_url'),source_url=file.get('source_url')))
        edge(ref,artifact,'references')
    for row in tables['source_inventory'].to_dict('records'):
        sid=node_id('source_sheet',row['sha256'],row['sheet']);node(sid,'source_sheet',row['sheet'],dict(source_sheet=row['sheet'],source_sha256=row['sha256']))
        if row['file'] in files:edge(node_id('source_artifact',row['sha256']),sid,'contains')
    flush()
    for row in tables['plots'].to_dict('records'):
        source=entity_lookup.get(('spatial_features',str(row.get('geometry_source'))))
        if source:edge(source,node_id('plot',str(row['plot_id'])),'geometry_for')
    for row in tables['validation_findings'].to_dict('records'):
        fid=row.get('finding_id') or finding_id(row);ident=node_id('validation_finding',fid)
        node(ident,'validation_finding',row['rule_id'],dict(row,finding_id=fid))
        table=row['table'];current=str(row['entity_identifier']);involved=[(table,current)]
        for previous in evidence_entities(row):involved.append(('spatial_features' if 'previous_feature' in str(row.get('observed_value')) else 'organism_observations',previous))
        ok=True;fields_ok=True
        for entity_table,entity in involved:
            oid=entity_lookup.get((entity_table,entity))
            if oid:
                edge(oid,ident,'triggered' if entity==current else 'contributes')
                ok &= complete.get((entity_table,entity),False)
                fields_ok &= set(row['field'].split(','))<=field_complete.get((entity_table,entity),set())
                for field in row['field'].split(','):
                    cfid=field_node(entity_table,entity,field)
                    if conn.execute('SELECT 1 FROM nodes WHERE id=?',(cfid,)).fetchone():edge(cfid,ident,'validated_by')
            else:
                context_kind='plot' if entity_table=='plots' else None
                if context_kind:edge(node_id(context_kind,entity),ident,'triggered')
                else:ok=False;fields_ok=False
        coverage['findings']+=1
        coverage['findings_complete_source_row_lineage']+=int(ok)
        coverage['findings_complete_evidence_lineage']+=int(ok and fields_ok)
        if len(node_buffer)>10000:flush()
    flush()
    conn.executescript('CREATE INDEX edge_source ON edges(source); CREATE INDEX edge_target ON edges(target); CREATE INDEX node_type ON nodes(type);')
    orphans=conn.execute('SELECT count(*) FROM edges e LEFT JOIN nodes s ON e.source=s.id LEFT JOIN nodes t ON e.target=t.id WHERE s.id IS NULL OR t.id IS NULL').fetchone()[0]
    max_depth,unreached=calculate_depths(conn)
    conn.commit();conn.close()
    temporary.replace(target)
    graph=LineageGraph(target)
    if export_tables:graph.export(folder,'parquet')
    summary=dict(graph.summary(),coverage=dict(coverage),orphan_edges=orphans,unresolved_depth_nodes=unreached,largest_trace_depth=max_depth,
        canonical_sha256=inputs,manifest_sha256=sha256(manifest_path) if manifest_path.exists() else None,example_observation_ids=examples,
        implementation_sha256={str(p.relative_to(Path(__file__).parents[1])):sha256(p) for directory in ('lineage','validation') for p in (Path(__file__).parents[1]/directory).glob('*.py')})
    (folder/'summary.json').write_text(dumps(summary,indent=2),encoding='utf8')
    write_summary(root,summary,graph)
    return graph

def calculate_depths(conn):
    """One pass per explicit DAG stratum, followed by an edge-order check.

    Unlike repeated whole-graph recursive joins, work follows the typed evidence
    model and each target is assigned once. Spatial feature records precede the
    plots whose boundary they supply; those plots precede organism observations.
    """
    conn.executescript('PRAGMA cache_size=-131072; PRAGMA temp_store=MEMORY; DROP TABLE IF EXISTS depths; CREATE TABLE depths(id TEXT PRIMARY KEY,depth INTEGER);')
    phases=[("type IN ('source_reference','organism','survey_event')",'roots'),
        ("type='source_artifact'",'artifacts'),("type='source_sheet'",'sheets'),
        ("type='source_row'",'rows'),("type='source_field'",'source fields'),
        ("type='transformation'",'transformations'),("type='canonical_field'",'canonical fields'),
        ("type='canonical_observation' AND json_extract(attributes,'$.table')='spatial_features'",'spatial features'),
        ("type='plot'",'plots'),
        ("type='canonical_observation' AND json_extract(attributes,'$.table')!='spatial_features'",'observations'),
        ("type='validation_finding'",'findings')]
    for condition,label in phases:
        conn.execute(f'INSERT INTO depths SELECT n.id,coalesce(max(d.depth)+1,0) FROM nodes n LEFT JOIN edges e ON e.target=n.id LEFT JOIN depths d ON d.id=e.source WHERE n.{condition} GROUP BY n.id')
        conn.commit();print('Lineage depth: '+label,flush=True)
    unresolved=conn.execute('SELECT count(*) FROM nodes n LEFT JOIN depths d ON d.id=n.id WHERE d.id IS NULL').fetchone()[0]
    violations=conn.execute('SELECT count(*) FROM edges e JOIN depths s ON s.id=e.source JOIN depths t ON t.id=e.target WHERE s.depth>=t.depth').fetchone()[0]
    if violations:raise ValueError(f'Graph violates its documented DAG strata: {violations} edges')
    return conn.execute('SELECT max(depth) FROM depths').fetchone()[0] or 0,unresolved

def resume_built_tables(root='.'):
    """Finalize complete typed tables after an interrupted expensive export step."""
    root=Path(root).resolve();folder=root/'data/lineage';temporary=folder/'lineage.build.sqlite'
    conn=sqlite3.connect(temporary)
    if conn.execute('PRAGMA quick_check').fetchone()[0]!='ok':raise ValueError('Interrupted graph failed SQLite integrity check; rebuild it')
    tables={p.stem:pd.read_parquet(p) for p in (root/'data/processed').glob('*.parquet')}
    for table,key in [('organism_observations','observation_id'),('vegetation_observations','observation_id'),('plot_observations','observation_id'),('spatial_features','feature_id')]:
        count=conn.execute("SELECT count(*) FROM nodes WHERE type='canonical_observation' AND json_extract(attributes,'$.table')=?",(table,)).fetchone()[0]
        if count!=tables[table][key].nunique():raise ValueError('Incomplete graph table: '+table)
    if conn.execute("SELECT count(*) FROM nodes WHERE type='validation_finding'").fetchone()[0]!=len(tables['validation_findings']):raise ValueError('Incomplete findings')
    for row in tables['plots'].to_dict('records'):
        if isinstance(row.get('geometry_source'),str):
            source=observation_node('spatial_features',row['geometry_source']);target=node_id('plot',row['plot_id'])
            conn.execute('INSERT OR IGNORE INTO edges VALUES(?,?,?,?)',(edge_id(source,target,'geometry_for'),source,target,'geometry_for'))
    conn.commit()
    maximum,unresolved=calculate_depths(conn)
    orphans=conn.execute('SELECT count(*) FROM edges e LEFT JOIN nodes s ON e.source=s.id LEFT JOIN nodes t ON e.target=t.id WHERE s.id IS NULL OR t.id IS NULL').fetchone()[0]
    # Coverage is computed from the existing authoritative tables, never from
    # assumed success of a previously interrupted loop.
    files={r['local_filename']:r for r in tables['source_files'].to_dict('records')}
    inventory={(r['file'],r['sheet']):set(json.loads(r['original_columns'])) for r in tables['source_inventory'].to_dict('records')}
    traces={}
    for r in tables['provenance'].to_dict('records'):traces.setdefault((r['table'],r['observation_id']),[]).append(r)
    complete={};verified={};coverage=Counter();examples=[]
    for table,key in [('organism_observations','observation_id'),('vegetation_observations','observation_id'),('plot_observations','observation_id'),('spatial_features','feature_id')]:
        for row in tables[table].to_dict('records'):
            entity=str(row[key]);file=files.get(row.get('source_file'));columns=inventory.get((row.get('source_file'),row.get('source_sheet')))
            valid=bool(file and row.get('source_sha256')==file['sha256'] and columns is not None and pd.notna(row.get('source_row')) and row.get('source_row_id')==stable_id(row.get('source_sha256'),row.get('source_sheet'),int(row['source_row'])))
            complete[(table,entity)]=valid;fields=set();known=set()
            for trace in traces.get((table,entity),[]):
                if trace.get('transformation'):known.add(trace['field'])
                column=trace.get('source_column');has_column=isinstance(column,str) and bool(column)
                mapping_ok=not has_column or (columns is not None and set(column.split(','))<=columns)
                names=trace['field'].split(',');value=trace.get('normalized_value')
                if len(names)>1:
                    try:values=json.loads(value)
                    except (TypeError,ValueError):values=[None]*len(names)
                else:values=[value]
                if trace.get('transformation') and mapping_ok and len(values)==len(names) and all(equivalent(row.get(f),v) for f,v in zip(names,values)):fields.update(names)
            verified[(table,entity)]=fields
            if table=='spatial_features':continue
            expected=list(EXPECTED[table])
            if table=='organism_observations' and pd.notna(row.get('longitude')):expected+=['longitude,latitude']
            coverage['observations']+=1;coverage['observations_row_lineage_complete']+=int(valid)
            coverage['expected_normalized_fields']+=len(expected)
            coverage['normalized_fields_with_transformation']+=sum(f in known for f in expected)
            coverage['normalized_fields_with_verified_source_mapping']+=sum(set(f.split(','))<=fields for f in expected)
            coverage['observations_all_expected_transforms']+=int(all(f in known for f in expected))
            coverage['observations_complete_field_lineage']+=int(valid and all(set(f.split(','))<=fields for f in expected))
            if len(examples)<3 and table=='organism_observations' and valid:examples.append(entity)
    coverage['canonical_fields_without_explicit_mapping']=conn.execute("SELECT count(*) FROM nodes WHERE type='canonical_field' AND json_extract(attributes,'$.mapping_recorded')=0 AND json_extract(attributes,'$.table')!='spatial_features'").fetchone()[0]
    for finding in tables['validation_findings'].to_dict('records'):
        involved=[(finding['table'],str(finding['entity_identifier']))]+[('spatial_features' if 'previous_feature' in str(finding.get('observed_value')) else 'organism_observations',p) for p in evidence_entities(finding)]
        ok=all(complete.get(pair,False) for pair in involved);mapped=all(set(finding['field'].split(','))<=verified.get(pair,set()) for pair in involved)
        coverage['findings']+=1;coverage['findings_complete_source_row_lineage']+=int(ok);coverage['findings_complete_evidence_lineage']+=int(ok and mapped)
    conn.commit();conn.close();temporary.replace(folder/'lineage.sqlite')
    graph=LineageGraph(folder/'lineage.sqlite');graph.export(folder,'parquet')
    manifest=root/'data/raw/manifest.json'
    summary=dict(graph.summary(),coverage=dict(coverage),orphan_edges=orphans,unresolved_depth_nodes=unresolved,largest_trace_depth=maximum,
        canonical_sha256={p.name:sha256(p) for p in (root/'data/processed').glob('*.parquet')},manifest_sha256=sha256(manifest),example_observation_ids=examples,
        implementation_sha256={str(p.relative_to(Path(__file__).parents[1])):sha256(p) for directory in ('lineage','validation') for p in (Path(__file__).parents[1]/directory).glob('*.py')})
    (folder/'summary.json').write_text(dumps(summary,indent=2),encoding='utf8');write_summary(root,summary,graph)
    return graph

def refresh_plot_evidence(root='.'):
    """Idempotently enrich an existing derived graph with recorded plot origins.

    Also supports upgrading a graph built while an older implementation was
    running, without repeating millions of unchanged node insertions.
    """
    from collections import deque
    root=Path(root).resolve();folder=root/'data/lineage';path=folder/'lineage.sqlite'
    conn=sqlite3.connect(path);changed=[]
    for row in pd.read_parquet(root/'data/processed/plots.parquet').to_dict('records'):
        if not isinstance(row.get('geometry_source'),str):continue
        source=observation_node('spatial_features',row['geometry_source']);target=node_id('plot',row['plot_id'])
        if not conn.execute('SELECT 1 FROM nodes WHERE id=?',(source,)).fetchone():continue
        conn.execute('INSERT OR IGNORE INTO edges VALUES(?,?,?,?)',(edge_id(source,target,'geometry_for'),source,target,'geometry_for'));changed.append(target)
    queue=deque(changed)
    while queue:
        ident=queue.popleft()
        depth=conn.execute('SELECT max(d.depth)+1 FROM edges e JOIN depths d ON e.source=d.id WHERE e.target=?',(ident,)).fetchone()[0]
        old=conn.execute('SELECT depth FROM depths WHERE id=?',(ident,)).fetchone()
        if depth is not None and (old is None or depth>old[0]):
            conn.execute('INSERT OR REPLACE INTO depths VALUES (?,?)',(ident,depth))
            queue.extend(r[0] for r in conn.execute('SELECT target FROM edges WHERE source=?',(ident,)))
    conn.commit();maximum=conn.execute('SELECT max(depth) FROM depths').fetchone()[0];conn.close()
    graph=LineageGraph(path);graph.export(folder,'parquet')
    summary=json.loads((folder/'summary.json').read_text());summary.update(graph.summary(),largest_trace_depth=maximum)
    summary['implementation_sha256']={str(p.relative_to(Path(__file__).parents[1])):sha256(p) for directory in ('lineage','validation') for p in (Path(__file__).parents[1]/directory).glob('*.py')}
    (folder/'summary.json').write_text(dumps(summary,indent=2),encoding='utf8');write_summary(root,summary,graph)
    return graph

def write_summary(root,summary,graph):
    lines=['# Lineage graph summary','',
        'Derived evidence-flow node/edge tables; canonical tables and the raw manifest remain authoritative. SQLite is a local index over typed tables, not an external graph service. Parquet exports are the portable graph representation.','',
        '| Node type | Count |','|---|---:|']
    lines += [f'| {kind} | {count:,} |' for kind,count in summary['node_counts'].items()]
    lines+=['','| Edge type | Count |','|---|---:|']+[f'| {kind} | {count:,} |' for kind,count in summary['edge_counts'].items()]
    lines+=['','## Provenance coverage','']+[f'- {kind}: {count:,}' for kind,count in summary['coverage'].items()]
    lines += ['',f"Orphan edges: {summary['orphan_edges']}; longest recorded evidence-flow path: {summary['largest_trace_depth']} edges; nodes without a resolved acyclic depth: {summary['unresolved_depth_nodes']}.",'',
        'Row-lineage completeness means an existing manifest artifact, inventoried sheet/layer and physical source row are recorded. Transformation coverage is measured separately for explicitly normalized fields. Other canonical fields retain source-row lineage only; no cell-level transformation is invented. Coverage is not proof that the recorded source values are correct.','',
        '## Example observation traces','']+[f'- `{entity}`' for entity in summary['example_observation_ids']]
    with graph._connect() as conn:
        sample=conn.execute("SELECT attributes FROM nodes WHERE type='validation_finding' AND label='TEMPORAL_SHRINKAGE' ORDER BY id LIMIT 1").fetchone()
    if sample:
        finding=json.loads(sample[0]);fid=finding['finding_id'];trace=graph.trace_finding(fid)
        Path(root/'data/lineage/example_temporal_trace.json').write_text(dumps(trace,indent=2),encoding='utf8')
        lines+=['','## Executed temporal finding trace','',f"Finding `{fid}` (`{finding['rule_id']}`) has {len(trace['nodes'])} nodes and {len(trace['edges'])} edges in its upstream evidence slice.",'',
            'Canonical records (including boundary context): '+', '.join('`'+n['attributes']['table']+'/'+n['attributes']['entity_id']+'`' for n in trace['nodes'] if n['type']=='canonical_observation'),'',
            'The trace includes each explicit contributing observation, its canonical fields, recorded transformations, source cells/rows, sheets, artifact SHA and NPS reference. Shared-row observations can legitimately converge on the same source row; this is not independent repeated GPS evidence.']
    lines+=['','Provenance-integrity findings are separately identifiable by `PROVENANCE_` rule IDs. Scientific findings remain review candidates, not verified errors. See `docs/lineage_graph.md` for semantics, expected transformation fields and remaining gaps.']
    path=Path(root)/'reports/lineage_summary.md';path.parent.mkdir(exist_ok=True);path.write_text('\n'.join(lines)+'\n',encoding='utf8')
