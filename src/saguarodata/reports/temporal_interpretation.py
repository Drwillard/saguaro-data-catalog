"""Executed commentary/context summaries, without adjudicating biological causes."""
import json
from pathlib import Path
import pandas as pd
from ..ingest.common import note_status
from ..normalize.annotations import observation_annotations
from ..jsonutil import dumps
from ..validation.rules import finding_category
from ..model.canonical import FINDING_CATEGORIES

RULES=('TEMPORAL_SHRINKAGE','TEMPORAL_ARM_DECREASE','TEMPORAL_STATUS_CONTRADICTION',
       'TEMPORAL_MEASUREMENT_AFTER_DEATH','TEMPORAL_REOBSERVED','TEMPORAL_GROWTH_OUTLIER','TEMPORAL_STATUS_RESOLVED')

def context_flags(evidence):
    notes=[evidence.get(prefix+'_notes') or '' for prefix in ('previous','current')]
    explicit=[note_status(note,evidence.get(prefix+'_year'))[0] for prefix,note in zip(('previous','current'),notes)]
    tags=[observation_annotations(note) for note in notes]
    verify=[evidence.get(prefix+'_verification_status') or 'not_recorded' for prefix in ('previous','current')]
    return dict(has_any_note=any(str(note).strip() for note in notes),
        has_explicit_alive_dead_note=any(value in ('alive','dead') for value in explicit),
        has_explicit_status_note=any(value in ('alive','dead','not_found') for value in explicit),
        has_review_annotation=any(t['needs_review'] for t in tags),
        has_tag_only_or_off_plot=any(t['tag_only'] or t['off_plot'] for t in tags),
        has_not_measured_annotation=any(t['not_measured'] for t in tags),
        has_verify_status=any(v not in ('not_recorded','') for v in verify),
        verify_yes='yes' in verify,verify_no='no' in verify,verify_not_found='not_found' in verify)

def table(frame):
    if frame.empty:return '(No represented observations.)'
    def cell(v):
        if v is None or (isinstance(v,float) and pd.isna(v)):return '—'
        return str(v).replace('|','\\|').replace('\n',' ')
    lines=['| '+' | '.join(frame.columns)+' |','| '+' | '.join(['---']*len(frame.columns))+' |']
    lines+=['| '+' | '.join(cell(v) for v in row)+' |' for row in frame.itertuples(index=False,name=None)]
    return '\n'.join(lines)

def temporal_report(root,ds):
    root=Path(root);out=root/'reports';out.mkdir(exist_ok=True)
    findings=ds.validation_findings();obs=ds.observations();lookup=obs.set_index('observation_id').to_dict('index')
    rows=[]
    for row in findings[findings.rule_id.str.startswith('TEMPORAL_')].to_dict('records'):
        value=json.loads(row['observed_value']) if isinstance(row['observed_value'],str) else row['observed_value']
        record=dict(finding_id=row['finding_id'],rule_id=row['rule_id'],finding_category=row['finding_category'],severity=row['severity'],
            current_observation_id=row['entity_identifier'],previous_observation_id=value.get('previous_observation_id',value.get('previous')),
            **context_flags(value))
        rows.append(record)
    columns=['finding_id','rule_id','finding_category','severity','current_observation_id','previous_observation_id',*context_flags({})]
    records=pd.DataFrame(rows,columns=columns);records.to_csv(out/'temporal_interpretation.csv',index=False)
    summary=[]
    for rule in RULES:
        group=records[records.rule_id.eq(rule)]
        summary.append(dict(rule_id=rule,finding_category=finding_category(rule,'info' if rule in ('TEMPORAL_REOBSERVED','TEMPORAL_STATUS_RESOLVED') else 'warning'),
            severity='info' if rule in ('TEMPORAL_REOBSERVED','TEMPORAL_STATUS_RESOLVED') else 'warning',count=len(group),
            **{key:int(group[key].sum()) for key in context_flags({})}))
    summary_frame=pd.DataFrame(summary);summary_frame.to_csv(out/'temporal_interpretation_by_rule.csv',index=False)
    totals={key:int(records[key].sum()) for key in context_flags({})}
    categories=findings.finding_category.value_counts().reindex(FINDING_CATEGORIES,fill_value=0).to_dict()
    lines=['# Real-data temporal interpretation','',
        'Temporal findings identify transitions requiring review. They do not classify biological change as data corruption. A value can be structurally valid while its meaning depends on organism identity, time, field protocol and observation notes.','',
        f'Total temporal findings: {len(records)}. Counts below are findings/pairs, not unique cacti or independent note texts. A note is counted if either member has nonempty commentary. Explicit alive/dead status uses the same conservative note parser and survey-year guard as ingestion. Operational tags use exact documented phrases only. These counts show potential context, not proof that a note explains a transition.','',
        '## Categories in all real validation findings','',table(pd.DataFrame([dict(finding_category=k,count=categories.get(k,0)) for k in ('integrity_violation','semantic_contradiction','biological_transition','data_quality_warning','informational')])),'',
        'Integrity-violation labels identify declared constraint/evidence-chain breaches; they are not adjudications of which biological source value is wrong.','',
        '## Temporal counts and commentary coverage','',table(summary_frame),'',
        '## Pair-level totals','',table(pd.DataFrame([dict(context=k,findings=v) for k,v in totals.items()])),'',
        'Verify values are source-row flags. In the Historic workbook a single Verify cell is shared by multiple year columns; it does not establish independent verification of each survey. Yes and No are context, not correctness labels. Yes/No counts can overlap in a pair and must not be summed as mutually exclusive classes. Unknown/unrecognized values remain visible; blank is not_recorded.','',
        '## Representative examples','',
        'Selection prioritizes L130/L167 where applicable, then deterministic finding-ID order, up to five examples per rule. No example is used to infer which record is wrong.']
    for rule in RULES:
        subset=findings[findings.rule_id.eq(rule)].copy()
        lines+=['',f'### {rule}','']
        if subset.empty:lines+=['No real findings of this type were emitted.'];continue
        subset['case_priority']=subset.entity_identifier.map(lambda entity:0 if lookup.get(entity,{}).get('source_individual_id') in ('L130','L167') else 1)
        for row in subset.sort_values(['case_priority','finding_id']).head(5).to_dict('records'):
            value=json.loads(row['observed_value']);current=lookup.get(row['entity_identifier'],{})
            lines += [f"- Finding `{row['finding_id']}` · {current.get('plot_id')} / {current.get('source_individual_id')} · {row['finding_category']} / {row['severity']}",
                '  - '+row['message'],
                f"  - {value.get('previous_year')}: height={value.get('previous_height_m')}, arms={value.get('previous_arm_count')}, status={value.get('previous_status')}, notes={value.get('previous_notes')!r}, Verify={value.get('previous_verification_status')}; {value.get('current_year')}: height={value.get('current_height_m')}, arms={value.get('current_arm_count')}, status={value.get('current_status')}, notes={value.get('current_notes')!r}, Verify={value.get('current_verification_status')}",
                f"  - Evidence: previous `{value.get('previous_observation_id',value.get('previous'))}`, current `{row['entity_identifier']}`; [NPS source](https://irma.nps.gov/DataStore/Reference/Profile/{current.get('source_reference_id')}) · {current.get('source_sheet')} row {current.get('source_row')} · SHA-256 `{current.get('source_sha256')}`"]
    lines+=['','## Source-checked case studies','']
    cases={}
    for tag in ('L130','L167'):
        case=obs[obs.program_id.eq('historic_plots')&obs.source_individual_id.eq(tag)].sort_values('survey_year')
        lines += [f'### {tag}','']
        if case.empty:lines+=['This identifier is not represented in the current build; no historical pattern is assumed.'];continue
        cases[tag]=case.observation_id.to_list()
        selected=case[['survey_year','height_m','arm_count','status','notes','verification_raw','verification_status','source_row']]
        lines += [table(selected),'']
        years=case.set_index('survey_year').to_dict('index')
        l130=(all(year in years for year in (1975,2001,2010)) and years[1975]['height_m']>years[2001]['height_m'] and years[1975]['arm_count']>years[2001]['arm_count'] and years[2001]['notes']=='live' and years[2010]['notes']=='dead' and years[1975]['notes']=='fairtop thin' and case.verification_status.eq('no').all())
        l167=(2001 in years and years[2001]['status']=='dead' and any(row['survey_year']>2001 and pd.notna(row['height_m']) and row['height_m']>0 and row['status']=='unknown' and not row['notes'] for row in case.to_dict('records')) and case.verification_status.eq('yes').all())
        if tag=='L130' and l130:lines+=['The height and arm counts fall between 1975 and the nominal 2001 round while the later note explicitly says live. The 1975 phrase fairtop thin is retained as descriptive prose, not a damage/status classification. The 2010 note explicitly says dead. This is consistent with several possible biological or recording explanations; the source does not establish that the earlier decrease is an error. Verify=No is a shared-row context flag, not proof of invalid measurements.']
        elif tag=='L167' and l167:lines+=['The 2001 note explicitly says dead; later positive heights have unknown formal status and blank notes. Those measurements do not establish later life or a literal reversal of death. A standing dead cactus can still be measured; classification, linkage and transcription also remain review possibilities. Verify=Yes does not adjudicate the conflicting interpretations.']
        else:lines+=['The current source rows differ from the documented example pattern. Interpret the measurements, explicit statuses and original notes above directly; no prior narrative or causal explanation is assumed.']
        row=case.iloc[0];lines += ['',f"Source: {row.source_file.split('/')[-1]} · {row.source_sheet} row {row.source_row} · NPS {row.source_reference_id}. A shared workbook row contains multiple survey-year columns; Verify has no independently documented survey date."]
    (out/'temporal_interpretation.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    result=dict(temporal_findings=len(records),findings_by_category=categories,context_totals=totals,
        real_status_contradictions=int(findings.rule_id.eq('TEMPORAL_STATUS_CONTRADICTION').sum()),cases=cases)
    (out/'temporal_interpretation.json').write_text(dumps(result,indent=2),encoding='utf8')
    return result
