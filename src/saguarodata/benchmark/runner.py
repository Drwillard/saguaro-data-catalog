"""Independent synthetic intervention trials on an immutable canonical cohort."""
from pathlib import Path
import json
import math
import numbers
import numpy as np
import pandas as pd
import yaml
from ..model.canonical import OBSERVATION_COLUMNS
from ..validation.structural import structural_findings
from ..validation.temporal import temporal_findings
from ..validation.spatial import spatial_findings
from ..validation.context import context_findings
from ..validation.provenance import provenance_findings
from ..validation.rules import finding
from ..acquisition.checksums import sha256
from .corruption import inject,IneligibleScenario
from .scenarios import load_scenarios
from .metrics import LAYERS,score,summarize,overlap

def cohort(tables,limit=1200,seed=17):
    """Fixed across experiment seeds; retain whole supported individual histories."""
    if not limit:return {k:v.copy(deep=True) for k,v in tables.items()}
    rng=np.random.default_rng(seed);obs=tables['organism_observations']
    ids=sorted(obs.organism_id.dropna().unique());rng.shuffle(ids)
    chosen=[];count=0
    for organism in ids:
        chosen.append(organism);count+=int(obs.organism_id.eq(organism).sum())
        if count>=limit*.7:break
    linked=obs[obs.organism_id.isin(chosen)]
    remaining=obs[~obs.organism_id.isin(chosen)]
    unlinked=remaining[remaining.organism_id.isna()]
    count=min(max(0,limit-len(linked)),len(unlinked))
    extra=unlinked.sample(n=count,random_state=seed)
    result={k:v.copy(deep=True) for k,v in tables.items()}
    result['organism_observations']=pd.concat([linked,extra]).sort_values('observation_id').reset_index(drop=True)
    for table in ('vegetation_observations','plot_observations'):
        result[table]=tables[table].head(25).copy().reset_index(drop=True)
    all_ids=set().union(*(set(result[t].observation_id) for t in ('organism_observations','vegetation_observations','plot_observations')))
    result['provenance']=tables['provenance'][tables['provenance'].observation_id.isin(all_ids)].copy().reset_index(drop=True)
    # Keep all plot entities/polygons, and representative source features including
    # every feature supplying a plot geometry. Research bytes remain untouched.
    features=tables['spatial_features'];geometry_ids=set(tables['plots'].geometry_source.dropna()) if 'geometry_source' in tables['plots'] else set()
    feature_sample=features.head(40)
    result['spatial_features']=pd.concat([features[features.feature_id.isin(geometry_ids)],feature_sample]).drop_duplicates('feature_id').reset_index(drop=True)
    result['validation_findings']=pd.DataFrame()  # Baseline findings are recomputed on this exact cohort.
    return result

def schema_checks(tables):
    frame=tables['organism_observations'];out=[]
    def emit(rule,row,field,value):out.append(finding(rule,row,field,value,'Declared canonical schema','Schema/type contract violation.','error'))
    for column in OBSERVATION_COLUMNS:
        if column not in frame:emit('SCHEMA_MISSING_COLUMN',{'observation_id':'__table__'},column,None)
    required=('observation_id','program_id','survey_event_id','survey_year','source_row_id','source_sha256','source_row','source_sheet')
    numerics=('survey_year','nominal_round','source_row','height_m','arm_count','x','y','latitude','longitude')
    booleans=('tag_only','off_plot','not_measured','needs_review')
    for row in frame.to_dict('records'):
        context=dict(row)
        if pd.isna(context.get('observation_id')):context['observation_id']=row.get('source_row_id')
        for field in required:
            if field in frame and (pd.isna(row.get(field)) or row.get(field)==''):emit('SCHEMA_NULL_REQUIRED',context,field,row.get(field))
        for field in numerics:
            value=row.get(field)
            if pd.notna(value) and (not isinstance(value,numbers.Real) or isinstance(value,(bool,np.bool_))):emit('SCHEMA_NUMERIC_TYPE',context,field,value)
        for field in frame:
            value=row.get(field)
            if field in booleans:
                if pd.notna(value) and not isinstance(value,(bool,np.bool_)):emit('SCHEMA_BOOLEAN_TYPE',context,field,value)
                continue
            if field in numerics or pd.isna(value):continue
            if field in OBSERVATION_COLUMNS and not isinstance(value,str):emit('SCHEMA_TEXT_TYPE',context,field,value)
        if row.get('status') not in ('unknown','alive','dead','not_found'):emit('SCHEMA_STATUS_ENUM',context,'status',row.get('status'))
    return out

def row_checks(tables):
    frame=tables['organism_observations'];out=[]
    def emit(rule,row,field,value):out.append(finding(rule,row,field,value,'Conventional scalar/key constraints','Row-wise baseline violation.','error'))
    for row in frame.to_dict('records'):
        for field in ('height_m','arm_count','longitude','latitude'):
            value=row.get(field)
            if pd.isna(value):continue
            try:number=float(value)
            except (ValueError,TypeError):emit('ROW_INVALID_NUMERIC',row,field,value);continue
            low,high={'height_m':(0,30),'arm_count':(0,200),'longitude':(-180,180),'latitude':(-90,90)}[field]
            if not math.isfinite(number) or not low<=number<=high:emit('ROW_RANGE',row,field,value)
            elif field=='arm_count' and number%1:emit('ROW_INTEGER_COUNT',row,field,value)
    for keys in (['observation_id'],['source_row_id','survey_event_id'],['organism_id','survey_event_id']):
        if not set(keys)<=set(frame):continue
        subset=frame.dropna(subset=keys)
        for row in subset[subset.duplicated(keys,keep=False)].to_dict('records'):emit('ROW_DUPLICATE_KEY',row,','.join(keys),{key:row[key] for key in keys})
    for row in frame[frame.astype(str).duplicated(keep=False)].to_dict('records'):emit('ROW_DUPLICATE_ROW',row,'observation_id',row.get('observation_id'))
    return out

def validate_layers(tables,config):
    # Legacy scientific validators require numeric columns. Preserve schema failures
    # separately and supply nulls, never restored original values, to those checks.
    safe={k:v for k,v in tables.items()};obs=tables['organism_observations'].copy()
    for column in OBSERVATION_COLUMNS:
        if column not in obs:obs[column]=None
    for column in ('height_m','arm_count','survey_year','latitude','longitude','x','y','source_row'):
        obs[column]=pd.to_numeric(obs[column],errors='coerce')
    safe['organism_observations']=obs
    context=None
    def extra(kind):
        nonlocal context
        if context is None:context=context_findings(safe)
        is_spatial=lambda row:row['rule_id'].startswith(('COORDINATE_','INVALID_COORDINATE_','INVALID_SOURCE_GEOMETRY'))
        return [row for row in context if is_spatial(row)==(kind=='spatial')]
    functions={
        'schema':lambda:schema_checks(tables),'row':lambda:row_checks(tables),
        'structural':lambda:structural_findings(obs,tables['plots'],tables['survey_events'])+extra('structural'),
        'temporal':lambda:temporal_findings(obs,config),
        'spatial':lambda:spatial_findings(obs,tables['plots'],tables['spatial_features'],config)+extra('spatial'),
        'provenance':lambda:provenance_findings(tables)}
    result={}
    for layer,fn in functions.items():
        try:result[layer]=dict(findings=fn(),error=None)
        except Exception as exc:result[layer]=dict(findings=[],error=f'{type(exc).__name__}: {exc}')
    return result

def write_report(root):
    root=Path(root);folder=root/'data/benchmark'
    result=pd.read_parquet(folder/'results.parquet');summary=summarize(result)
    if 'scenario_semantics' not in result:
        from .scenarios import scenario_semantics
        result['scenario_semantics']=result.scenario.map(scenario_semantics)
    matrix=result.groupby(['scenario','layer']).detected.mean().unstack().reindex(columns=LAYERS).fillna(0)
    classes=result.groupby(['corruption_class','layer']).detected.mean().unstack().reindex(columns=LAYERS).fillna(0)
    semantics=result.groupby(['scenario_semantics','layer']).detected.mean().unstack().reindex(columns=LAYERS).fillna(0)
    overview=json.loads((folder/'run.json').read_text())
    reports=root/'reports';reports.mkdir(exist_ok=True)
    summary.to_csv(reports/'corruption_benchmark.csv',index=False)
    matrix.to_csv(reports/'corruption_benchmark_by_scenario.csv')
    classes.to_csv(reports/'corruption_benchmark_by_class.csv')
    semantics.to_csv(reports/'corruption_benchmark_by_semantics.csv')
    if 'intensity' in result:
        intensity_rows=[]
        for intensity,group in result.groupby('intensity'):
            for row in summarize(group).to_dict('records'):intensity_rows.append(dict(intensity=intensity,**row))
        pd.DataFrame(intensity_rows).to_csv(reports/'corruption_benchmark_by_intensity.csv',index=False)
    overlap(result).to_csv(reports/'corruption_benchmark_overlap.csv',index=False)
    def table(frame):
        columns=list(frame.columns);lines=['| '+' | '.join(columns)+' |','| '+' | '.join(['---']*len(columns))+' |']
        for row in frame.to_dict('records'):lines.append('| '+' | '.join(f'{row[c]:.3f}' if isinstance(row[c],float) else str(row[c]) for c in columns)+' |')
        return '\n'.join(lines)
    runs=overview.get('runs',[dict(seeds=overview['seeds'],count=overview['count'],intensity=1.)])
    lines=['# Synthetic intervention benchmark','',f"Executed runs: {json.dumps(runs)}. Canonical cohort: {overview['cohort_observations']} observations; {overview['cohort_features']} spatial features. Complete selected organism histories and all plot context are retained. This is a deterministic cohort experiment on real canonical records, not a whole-corpus prevalence estimate.",'',
        'Each trial starts from the same unchanged cohort and applies one synthetic intervention. All six layers run independently. Strict schema types/nullability/enums and conventional scalar ranges (height 0–30 m, arms 0–200, geographic ranges), integer counts, primary/composite keys and exact row duplicates form the baselines. The structural/spatial layers include the existing checks plus explicit identity/event/unit and CRS/geometry cross-checks added in this extension. Provenance checks are a separate integrity layer.','',
        f"Completed synthetic interventions: {len(result)//len(LAYERS)}; ineligible trials: {len(overview['skipped'])}. Skips are not detections or misses. Validator failures are misses and are counted separately.",'',table(summary),'',
        'Precision counts one matched detection per intervention, collapses redundant matching alerts, and treats newly emitted alerts outside the recorded affected rows/histories as operational false positives. Alert precision additionally reports matched alerts / all new alerts. Recall is detected interventions / completed interventions. F1 uses the event precision and injection recall. Baseline signatures are subtracted; pre-existing scientific findings are neither scored as successes nor declared source errors. Unmatched new alerts can be secondary real effects of the injection rather than scientifically false claims.','',
        '## Executed detection rates by intervention semantics','',table(semantics.reset_index()),'',
        '## Executed detection rates by intervention family','',table(classes.reset_index()),'',
        '## Executed detection rates by scenario','',table(matrix.reset_index()),'',
        'An intervention may be detected by several layers. Pairwise overlaps are in `corruption_benchmark_overlap.csv`; seed recall standard deviation is population standard deviation across the executed seeds. `data/benchmark/alerts.parquet` preserves each new alert and matching decision. Ground truth includes every changed cell/row, original values, affected history IDs, seed and scenario.','',
        '## Interpretation','',
        'Context-only detections (both conventional baselines missed, at least one contextual layer detected):', '']
    pivot=result.pivot(index='corruption_id',columns='layer',values='detected')
    unions=[]
    for name,layers in [('conventional',['schema','row']),('contextual',['structural','temporal','spatial','provenance']),('all',list(LAYERS))]:
        detected=int(pivot[layers].any(axis=1).sum());unions.append(dict(validation_group=name,injected=len(pivot),detections=detected,misses=len(pivot)-detected,recall=detected/len(pivot)))
    lines+=['',table(pd.DataFrame(unions)),'']
    pd.DataFrame(unions).to_csv(reports/'corruption_benchmark_groups.csv',index=False)
    ids=pivot.index[(pivot.schema==0)&(pivot.row==0)&pivot[['structural','temporal','spatial','provenance']].any(axis=1)]
    examples=result[result.corruption_id.isin(ids)].scenario.value_counts().index.tolist()
    lines.extend('- `'+scenario+'`' for scenario in examples)
    lines+=['','Synthetic scenarios show capabilities and blind spots under specified interventions; they do not estimate natural source-error frequency, identify true biological anomalies, or prove that one validator universally dominates. Statistical growth screening depends on eligible comparison pairs. Missing empirical spread or ineligible pairs may produce legitimate misses.','',
        'A detection is not automatically a source error. Height and arm decreases can be biologically real. Explicit dead/alive contradictions may reflect field classification, linkage or transcription. Synthetic interventions test detector capabilities, not ecological plausibility; temporal validators are screening tools. Context-aware validation detects not only malformed data, but also transitions whose interpretation depends on scientific context. Legacy corruption_id/corruption_class column names and benchmark corruption CLI syntax remain for compatibility; scenario_semantics identifies integrity interventions, semantic contradictions, plausible biological transitions and statistical anomalies.','',
        'Canonical values are changed while their stored provenance snapshots usually remain unchanged. Snapshot mismatch therefore measures cross-table consistency recovery, not whether the original source was scientifically correct. For a simulated biological transition, a snapshot mismatch does not imply that the changed measurement is biologically invalid. Coherent alteration of source, canonical and provenance values is outside this experiment.','',
        'The benchmark never alters `data/processed` or raw artifacts. `run.json` records source/configuration/implementation hashes. Hash equality of primary processed inputs was verified after execution.']
    if 'informational_crs_detection' in result:
        informative=result[result.layer.eq('spatial')]
        count=int(informative.informational_crs_detection.sum())
        lines+=['','## Informational CRS screen','',f'{count} injected CRS removals were recognized by the existing UNKNOWN_SPATIAL_CRS informational finding. These are reported separately rather than relabeled as warnings/errors. Primary recall above excludes informational collection diagnostics. The apparent CRS-removal misses in that primary table therefore describe severity-filtered recovery, not absence of a detector.']
    (reports/'corruption_benchmark.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    return summary.to_dict('records')

def rescore_saved(root='.'):
    """Recompute stricter baseline equivalence from retained executed alerts.

    This revision only removes distinctions (numeric/reference-ID formatting),
    so baseline + retained new alerts is sufficient for primary re-scoring.
    The informational CRS scenario is replayed to retain its separate severity
    diagnostic, which was not part of the old primary-alert output.
    """
    root=Path(root).resolve();folder=root/'data/benchmark';metadata=json.loads((folder/'run.json').read_text())
    inputs={p.name:sha256(p) for p in (root/'data/processed').glob('*.parquet')}
    if inputs!=metadata['canonical_sha256']:raise ValueError('Canonical inputs changed; rerun the benchmark')
    tables=cohort({p.stem:pd.read_parquet(p) for p in (root/'data/processed').glob('*.parquet')},metadata['sample_size'])
    config=yaml.safe_load((root/'configs/validation_rules.yaml').read_text());baseline=validate_layers(tables,config)
    truth=pd.read_parquet(folder/'ground_truth.parquet');old=pd.read_parquet(folder/'alerts.parquet')
    if not (folder/'alerts_before_scoring_revision.parquet').exists():old.to_parquet(folder/'alerts_before_scoring_revision.parquet',index=False)
    grouped={key:frame.alert_json.map(json.loads).tolist() for key,frame in old.groupby(['corruption_id','layer'])}
    results=[];alerts=[]
    for record in truth.to_dict('records'):
        if record['scenario']=='spatial_crs_removed':
            mutated,replayed=inject(tables,record['scenario'],int(record['seed']),int(record['ordinal']),float(record.get('intensity',1.)))
            if replayed['changes_json']!=record['changes_json']:raise ValueError('Replayed intervention differs')
            observed=validate_layers(mutated,config)
        else:
            observed={layer:dict(findings=baseline[layer]['findings']+grouped.get((record['corruption_id'],layer),[]),error=None) for layer in LAYERS}
        rows,new=score(record,baseline,observed);results+=rows;alerts+=new
    pd.DataFrame(results).to_parquet(folder/'results.parquet',index=False)
    pd.DataFrame(alerts,columns=['corruption_id','layer','matched','alert_json']).to_parquet(folder/'alerts.parquet',index=False)
    metadata['scoring_revision']='Source-row anchored; ignore reference-ID-only changes in existing conditions; informational CRS screen separate'
    metadata['diagnostic_replayed_scenario']='spatial_crs_removed'
    metadata['implementation_sha256']={str(p.relative_to(Path(__file__).parents[1])):sha256(p) for p in Path(__file__).parents[1].rglob('*.py')}
    (folder/'run.json').write_text(json.dumps(metadata,indent=2),encoding='utf8')
    return write_report(root)

def run_benchmark(root='.',seeds=(42,),count=100,sample_size=1200,intensity=1.,append=False):
    root=Path(root).resolve();folder=root/'data/benchmark';folder.mkdir(parents=True,exist_ok=True)
    inputs={p.name:sha256(p) for p in sorted((root/'data/processed').glob('*.parquet'))}
    tables={p.stem:pd.read_parquet(p) for p in sorted((root/'data/processed').glob('*.parquet'))}
    tables=cohort(tables,sample_size)
    config=yaml.safe_load((root/'configs/validation_rules.yaml').read_text());specs=load_scenarios(root)
    baseline=validate_layers(tables,config)
    failures={k:v['error'] for k,v in baseline.items() if v['error']}
    if failures:raise RuntimeError(f'Baseline validator failed: {failures}')
    truth=[];results=[];alerts=[];skipped=[]
    for seed in seeds:
        for ordinal in range(count):
            scenario=specs[ordinal%len(specs)]
            try:mutated,record=inject(tables,scenario,int(seed),ordinal,intensity)
            except IneligibleScenario as exc:skipped.append(dict(seed=seed,scenario=scenario['id'],reason=str(exc)));continue
            detected=validate_layers(mutated,config);rows,new_alerts=score(record,baseline,detected)
            truth.append(record);results.extend(rows);alerts.extend(new_alerts)
            if (ordinal+1)%10==0:print(f'Benchmark seed {seed}: {ordinal+1}/{count}',flush=True)
    if not truth:raise ValueError('No eligible corruptions')
    old_metadata=None
    if append and (folder/'run.json').exists():
        old_metadata=json.loads((folder/'run.json').read_text())
        if old_metadata['canonical_sha256']!=inputs or old_metadata['sample_size']!=sample_size:raise ValueError('Append requires identical canonical inputs and cohort settings')
        old_truth=pd.read_parquet(folder/'ground_truth.parquet')
        if 'intensity' not in old_truth:old_truth['intensity']=1.
        if set(old_truth.corruption_id)&{r['corruption_id'] for r in truth}:raise ValueError('Duplicate trial IDs: choose new seeds or intensity')
        truth=old_truth.to_dict('records')+truth
        old_results=pd.read_parquet(folder/'results.parquet')
        if 'intensity' not in old_results:old_results['intensity']=1.
        results=old_results.to_dict('records')+results
        alerts=pd.read_parquet(folder/'alerts.parquet').to_dict('records')+alerts
    pd.DataFrame(truth).to_parquet(folder/'ground_truth.parquet',index=False)
    pd.DataFrame(results).to_parquet(folder/'results.parquet',index=False)
    pd.DataFrame(alerts,columns=['corruption_id','layer','matched','alert_json']).to_parquet(folder/'alerts.parquet',index=False)
    after={p.name:sha256(p) for p in sorted((root/'data/processed').glob('*.parquet'))}
    if after!=inputs:raise RuntimeError('Primary processed inputs changed during benchmark')
    metadata=dict(seeds=list(seeds),count=count,sample_size=sample_size,cohort_seed=17,
        cohort_observations=len(tables['organism_observations']),cohort_features=len(tables['spatial_features']),
        canonical_sha256=inputs,skipped=skipped,
        config_sha256={p.name:sha256(p) for p in (root/'configs').glob('*.yaml')},
        implementation_sha256={str(p.relative_to(Path(__file__).parents[1])):sha256(p) for p in Path(__file__).parents[1].rglob('*.py')})
    metadata['runs']=(old_metadata.get('runs',[dict(seeds=old_metadata['seeds'],count=old_metadata['count'],intensity=1.)]) if old_metadata else [])+[dict(seeds=list(seeds),count=count,intensity=float(intensity))]
    if old_metadata:metadata['skipped']=old_metadata.get('skipped',[])+skipped
    (folder/'run.json').write_text(json.dumps(metadata,indent=2),encoding='utf8')
    return write_report(root)
