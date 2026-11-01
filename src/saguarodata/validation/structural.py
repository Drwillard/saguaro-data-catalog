import json
import pandas as pd
from .rules import finding

def schema_drift(before, after):
    return dict(introduced=sorted(set(after)-set(before)), removed=sorted(set(before)-set(after)),
        type_changes={k: [before[k], after[k]] for k in before.keys() & after.keys() if before[k] != after[k]})

def structural_findings(observations, plots, events):
    findings = []
    valid_plots = set(plots.plot_id)
    valid_events = set(events.survey_event_id)
    for row in observations.to_dict('records'):
        if pd.isna(row.get('plot_id')) or not row.get('plot_id'):
            findings.append(finding('REQUIRED_PLOT_ID', row, 'plot_id', row.get('plot_id'), 'Plot identifier required', 'Source plot ID is missing.', 'error'))
        elif row['plot_id'] not in valid_plots:
            findings.append(finding('FK_PLOT', row, 'plot_id', row['plot_id'], 'Reference existing plot', 'Unresolved plot foreign key.', 'error'))
        if row['survey_event_id'] not in valid_events:
            findings.append(finding('FK_SURVEY_EVENT', row, 'survey_event_id', row['survey_event_id'], 'Reference existing event', 'Unresolved event.', 'error'))
        for field in ('height_m','arm_count'):
            value = row.get(field)
            if pd.notna(value) and value < 0:
                findings.append(finding('NEGATIVE_MEASUREMENT', row, field, value, 'Value >= 0', 'Negative physical measurement retained.', 'error'))
            reason = row.get('height_missing_reason' if field=='height_m' else 'arm_count_missing_reason')
            if reason == 'invalid_numeric':
                findings.append(finding('INVALID_NUMERIC', row, field, row.get('height_raw' if field=='height_m' else 'arm_count_raw'), 'Numeric or documented missing token', 'Unparsed source token retained.'))
        if row.get('height_m') == 0 and row['program_id'] == 'historic_plots':
            findings.append(finding('AMBIGUOUS_ZERO_HEIGHT', row, 'height_m', dict(raw=row['height_raw'],notes=row['notes']),
                'Interpret zero only with documented sentinel semantics', 'Zero retained; excluded from temporal height comparisons.'))
        if pd.notna(row.get('arm_count')) and row['arm_count'] % 1:
            findings.append(finding('NONINTEGER_ARM_COUNT', row, 'arm_count', row['arm_count'], 'Integer arm count', 'Fractional count retained.'))
        if row['program_id']=='historic_plots' and row.get('source_plot_id')=='71G':
            findings.append(finding('IDENTITY_TRACKING_UNSUPPORTED', row, 'organism_id', row.get('source_individual_id'),
                'Independent evidence for individual continuity', '71G tag-loss exception: source ID retained but organism linkage withheld.', 'info'))
    for columns, rule in ((['observation_id'],'DUPLICATE_OBSERVATION_ID'),
                           (['source_row_id','survey_event_id'],'DUPLICATE_SOURCE_ROW'),
                           (['organism_id','survey_event_id'],'DUPLICATE_ORGANISM_EVENT')):
        frame = observations if 'organism_id' not in columns else observations[observations.organism_id.notna()]
        for row in frame[frame.duplicated(columns, keep=False)].to_dict('records'):
            findings.append(finding(rule, row, ','.join(columns), {c:row[c] for c in columns}, 'Unique key', 'Potential repeated source or organism record.', 'error'))
    # Census IDs are local observations, not histories; flag duplicates only within the same source event/plot.
    census = observations[observations.program_id.eq('census') & observations.source_individual_id.fillna('').ne('')]
    for row in census[census.duplicated(['survey_event_id','plot_id','source_individual_id'],keep=False)].to_dict('records'):
        findings.append(finding('DUPLICATE_LOCAL_SOURCE_ID', row, 'source_individual_id', row['source_individual_id'],
            'Unique local ID within source event and plot', 'Could be repeated rounds or source duplication; no deduplication performed.'))
    for (program, status), group in observations.groupby(['program_id','status']):
        if status == 'unknown':
            continue
        variants = sorted(set(group.status_raw.dropna().str.strip()))
        if len(variants) > 1:
            findings.append(finding('CATEGORICAL_DRIFT', group.iloc[0].to_dict(), 'status_raw', variants,
                'Inspect categories normalized to same state', 'Equivalent categories are retained in raw status; normalization uses exact phrases.', 'info'))
    for (program,year),group in observations[observations.unit_source.eq('inferred')].groupby(['program_id','survey_year']):
        findings.append(finding('INFERRED_HEIGHT_UNIT',group.iloc[0].to_dict(),'height_unit_raw',dict(unit='m',affected_observations=len(group)),
            'Unit explicitly documented in measurement field or source protocol',
            'Meter interpretation inferred from companion spatial values and report height classes; raw workbook field has no unit.', 'info'))
    return findings
