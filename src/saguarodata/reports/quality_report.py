"""Self-contained HTML, plus an evidence-backed JSON/Markdown result summary."""
import html
import json
from pathlib import Path
import pandas as pd
from ..api.dataset import Dataset
from ..jsonutil import dumps, sanitize

def report(root='.'):
    root=Path(root)
    ds=Dataset(root/'data/processed')
    obs=ds.observations()
    findings=ds.validation_findings()
    counts=obs.groupby('program_id').size().rename('observations').reset_index()
    kinds=findings.groupby(['rule_id','severity']).size().rename('findings').reset_index()
    missing=obs.groupby(['program_id','survey_year']).agg(records=('observation_id','size'),height_null=('height_m',lambda s:int(s.isna().sum())),arms_null=('arm_count',lambda s:int(s.isna().sum()))).reset_index()
    reasons=obs.groupby(['program_id','survey_year','height_missing_reason'],dropna=False).size().rename('records').reset_index()
    priority=['TEMPORAL_RESURRECTION','TEMPORAL_MEASUREMENT_AFTER_DEATH','TEMPORAL_SHRINKAGE','TEMPORAL_GROWTH_OUTLIER','TEMPORAL_ARM_DECREASE','OUTSIDE_ASSIGNED_PLOT','DUPLICATE_LOCAL_SOURCE_ID','DUPLICATE_COORDINATES','NONINTEGER_ARM_COUNT','INVALID_NUMERIC','AMBIGUOUS_ZERO_HEIGHT','INVALID_OR_NULL_GEOMETRY','UNKNOWN_SPATIAL_CRS']
    examples=[]
    for rule in priority:
        subset=findings[findings.rule_id.eq(rule)]
        if not subset.empty:
            examples.append(subset.iloc[0].to_dict())
        if len(examples)==10: break
    # Add distinct entities if fewer than ten rule types actually occur.
    if len(examples)<10:
        used={r['entity_identifier'] for r in examples}
        for row in findings[findings.rule_id.isin(priority)].to_dict('records'):
            if row['entity_identifier'] not in used:
                examples.append(row); used.add(row['entity_identifier'])
            if len(examples)==10: break
    blocks=[]
    for index,item in enumerate(examples,1):
        entity=item['entity_identifier']
        match=obs[obs.observation_id.eq(entity)]
        detail={k:v for k,v in item.items()}
        if not match.empty:
            row=match.iloc[0]
            detail['raw_source_row']=json.loads(row.raw_values_json)
            detail['canonical_observation']=row.to_dict()
            detail['provenance']=ds.provenance(entity).to_dict('records')
            observed=json.loads(item['observed_value'])
            previous_id=observed.get('previous') if isinstance(observed,dict) else None
            if previous_id:
                detail['prior_observation']=obs[obs.observation_id.eq(previous_id)].to_dict('records')
        else:
            match=ds.table('spatial_features').loc[lambda f:f.feature_id.eq(entity)]
            if not match.empty:
                detail['raw_spatial_attributes']=json.loads(match.iloc[0].attributes_json)
        blocks.append(f'<article><h3>{index}. {html.escape(item["rule_id"])}</h3><p>{html.escape(item["message"])}</p><pre>{html.escape(dumps(detail,indent=2,default=str))}</pre></article>')
    inventory=ds.table('source_inventory')
    evolution=ds.table('schema_evolution')
    plants=ds.table('vegetation_observations')
    spatial=ds.table('spatial_features')
    aggregates=ds.table('plot_observations')
    coverage=dict(linked_organisms=len(ds.table('organisms')),unlinked_observations=int(obs.organism_id.isna().sum()),
        points_with_geographic_coordinates=int(obs.longitude.notna().sum()),plots_with_polygons=int(ds.plots().geometry.notna().sum()),
        independent_linked_coordinate_observations=int((obs.organism_id.notna()&obs.coordinate_time_basis.eq('survey_event')).sum()),
        spatial_features=len(spatial),spatial_features_without_crs=int(spatial.crs.isna().sum()),
        vegetation_observations=len(plants))
    limitations=[
        'No downloaded 2020 individual raw workbook was exposed by inspected NPS holdings; the two 2020 reports are preserved.',
        'Census and Section17 observations have no established cross-round individual linkage; no histories are invented.',
        'Historic 71G is excluded from individual linkage because the 2002 report explicitly describes tag loss.',
        'Historic coordinates repeat a shared source location, so they cannot establish temporal displacement. Displacement rule is tested on fixtures; no real-data movement result is claimed.',
        'Zero Historic heights and uncertain units are retained and flagged; no automatic source correction.',
        'Vegetation 1990 workbook sheets are header-only. Historical mapped attributes remain available separately in spatial_features.',
        'Subplot containment is not established for undated local-coordinate maps without CRS or explicit parent geometry; no inferred georeferencing.',
        'Spatial layers are separate source representations, not appended as additional organism observations. Geometry differences across layers require further source reconciliation.',
        'Cover labels differ; canonical vegetation cover is null until units and denominator are resolved.',
        'Report flags screen data for review; they are not confirmed source errors or ecological findings.'
    ]
    bars=''.join(f'<div class="barrow"><span>{html.escape(str(r.program_id))}</span><div style="width:{max(1,60*r.observations/counts.observations.max())}%;background:#467b52;height:18px"></div><b>{r.observations:,}</b></div>' for r in counts.itertuples())
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><title>saguarodata — data archaeology</title>
<style>body{font:16px system-ui;max-width:1200px;margin:40px auto;padding:0 24px;color:#22332a}h1,h2{color:#315a38}table{border-collapse:collapse;font-size:13px;display:block;overflow:auto}td,th{padding:7px;border:1px solid #d9e1d9;text-align:left}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f1f4ed;padding:16px;font-size:12px}article{border-top:1px solid #ccd5c5;margin:24px 0}.barrow{display:flex;align-items:center;gap:12px;margin:12px 0}.barrow span{width:170px}.barrow b{font-size:13px}</style>
<h1>Data archaeology in longitudinal scientific monitoring</h1><p>Changing schemas, sampling frames and identifiers require explicit scientific context. All findings remain open for review; source bytes and values are preserved.</p>'''
    page+='<h2>Canonical records by sampling frame</h2>'+bars+counts.to_html(index=False)
    page+='<h2>Plot aggregate representations</h2><p>These source summaries overlap other representations; do not sum their rows as independent observations. Fractional density-derived estimates remain fractional. Auxiliary historic/GPS/sample labels are kept in their own source summary namespace.</p>'+aggregates.groupby(['program_id','representation']).size().rename('records').reset_index().to_html(index=False)
    page+='<h2>Validation coverage and limits</h2><pre>'+html.escape(dumps(coverage,indent=2))+'</pre><ul>'+''.join('<li>'+html.escape(t)+'</li>' for t in limitations)+'</ul>'
    page+='<h2>Validation findings</h2>'+kinds.to_html(index=False)
    page+='<h2>Independent coordinate displacement</h2><p>All eligible distances and interval distributions are exported as coordinate_displacements and displacement_summaries. An empty table means no eligible independent linked fixes, rather than zero movement.</p>'+ds.table('displacement_summaries').to_html(index=False)
    page+='<h2>Missingness through time</h2><p>Source blanks, invalid numeric tokens, and variables not collected remain distinguishable. See per-field reasons in Parquet.</p>'+missing.to_html(index=False)+reasons.to_html(index=False)
    page+='<h2>Schema evolution</h2>'+evolution.to_html(index=False)
    page+='<h2>Illustrative unresolved cases and provenance</h2>'+''.join(blocks)
    page+='<h2>Source inventory</h2><p>Full machine-readable field profiles are in source_inventory.parquet.</p>'+inventory[['dataset','sheet','rows','columns','crs']].to_html(index=False)+'</html>'
    out=root/'reports'; out.mkdir(exist_ok=True)
    (out/'data_quality_report_static.html').write_text(page,encoding='utf8')
    summary=dict(records_by_program=counts.set_index('program_id').observations.to_dict(),
        aggregate_records_by_representation=aggregates.groupby('representation').size().to_dict(),
        vegetation_records_by_year=plants.groupby('survey_year').size().to_dict(), validation_findings=len(findings),
        findings_by_rule=findings.rule_id.value_counts().to_dict(),coverage=coverage,limitations=limitations,examples=examples)
    (out/'results.json').write_text(dumps(summary,indent=2,default=str),encoding='utf8')
    markdown='# Build results\n\n```json\n'+dumps({k:v for k,v in summary.items() if k!='examples'},indent=2,default=str)+'\n```\n\n## Ten illustrative examples\n\n'
    for i,item in enumerate(examples,1):
        markdown+=f"{i}. **{item['rule_id']}**, `{item['entity_identifier']}`: {item['observed_value']}. {item['message']} Source: `{item['source_lineage']}`\n\n"
    markdown+='## Supported conference-paper claims\n\n- Source-aware adapters must separate aggregate densities from individual measurements; the Census workbook contains both.\n- Shared source identifiers can support histories while documented tag loss makes the same strategy unsafe on 71G.\n- Temporal height and arm rules reveal review candidates that pass nonnegative scalar validation; see actual counts above.\n- Provenance preserves the path from a flagged SI value to a hashed file, sheet, physical row and source column.\n- Spatial validity and CRS coverage constrain which geographic checks are defensible; missing CRS must remain visible.\n'
    (out/'results.md').write_text(markdown,encoding='utf8')
    from .explorer import export_explorer
    export_explorer(root,ds,sanitize(summary))
    return sanitize(summary)
