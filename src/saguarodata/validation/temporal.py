import numpy as np
import pandas as pd
from .rules import finding

def transition_evidence(previous,current,**specific):
    evidence=dict(previous=previous['observation_id'],previous_observation_id=previous['observation_id'],
        current_observation_id=current['observation_id'],previous_year=previous['survey_year'],current_year=current['survey_year'])
    for prefix,row in [('previous',previous),('current',current)]:
        for field in ('height_m','arm_count','unit_source','height_normalization_unit','status','status_raw','status_source','notes','verification_status','verification_raw','verification_time_basis',
                      'tag_only','off_plot','not_measured','needs_review'):
            evidence[prefix+'_'+field]=row.get(field)
    evidence.update(specific)
    return evidence

def temporal_findings(observations, config):
    findings, pairs = [], []
    linked = observations[observations.organism_id.notna()].sort_values(['organism_id','survey_year','observation_id'])
    linked=linked[~linked.duplicated(['organism_id','survey_event_id'],keep=False)]
    for organism, group in linked.groupby('organism_id'):
        # Ambiguous duplicate organism/events were excluded before grouping.
        rows = group.to_dict('records')
        dead = None
        for row in rows:
            if row['status'] == 'dead' and row['status_source'] in ('explicit_note','explicit_field'):
                dead = row
            elif dead and row['status'] == 'alive' and row['status_source'] in ('explicit_note','explicit_field'):
                findings.append(finding('TEMPORAL_STATUS_CONTRADICTION', row, 'status',
                    transition_evidence(dead,row,transition='dead_to_alive'),
                    'Review conflicting explicit statuses for the same linked organism',
                    'Explicit dead and later alive statuses conflict for the same linked organism. Review field classification, identity linkage, source notes, and transcription.', 'warning'))
            elif dead and row['survey_year'] > dead['survey_year'] and pd.notna(row.get('height_m')) and row['height_m'] > 0:
                findings.append(finding('TEMPORAL_MEASUREMENT_AFTER_DEATH', row, 'height_m',
                    transition_evidence(dead,row,height=row['height_m']),
                    'Review measurements recorded after explicit death',
                    'A standing dead cactus can still be measured. A later positive height does not establish survival; review status and measurement semantics.'))
        for previous, row in zip(rows, rows[1:]):
            years = row['survey_year'] - previous['survey_year']
            if years <= 0:
                continue
            if previous['status']=='not_found' and (row['status']=='alive' or (pd.notna(row.get('height_m')) and row['height_m']>0)):
                findings.append(finding('TEMPORAL_REOBSERVED',row,'status',transition_evidence(previous,row,transition='not_found_to_observed'),
                    'Review reobservation after not_found without interpreting prior absence as death',
                    'Re-observation after not_found. Prior absence is not equivalent to death.','info'))
            elif previous['status']=='unknown' and row['status']=='alive' and row['status_source'] in ('explicit_note','explicit_field'):
                findings.append(finding('TEMPORAL_STATUS_RESOLVED',row,'status',transition_evidence(previous,row,transition='unknown_to_alive'),
                    'Unknown status may become explicitly known', 'A status-resolution event, not an inconsistency.','info'))
            h1, h2 = previous.get('height_m'), row.get('height_m')
            if pd.notna(h1) and pd.notna(h2) and h1 > 0 and h2 > 0:
                drop = h1 - h2
                if drop >= config['shrinkage_absolute_m'] and drop / h1 >= config['shrinkage_fraction']:
                    findings.append(finding('TEMPORAL_SHRINKAGE', row, 'height_m',
                        transition_evidence(previous,row,height_before=h1,height_after=h2,elapsed_years=years),
                        'Decrease below configured absolute and proportional thresholds',
                        'Large height decrease detected. Possible explanations include top/stem breakage, measurement differences, source-unit problems, transcription error, or identity mismatch.'))
                pairs.append(dict(row=row, previous_row=previous, previous=previous['observation_id'], rate=(h2-h1)/years,
                    interval=(row['program_id'],previous['survey_year'],row['survey_year'])))
            a1, a2 = previous.get('arm_count'), row.get('arm_count')
            if pd.notna(a1) and pd.notna(a2) and a2 < a1:
                findings.append(finding('TEMPORAL_ARM_DECREASE', row, 'arm_count',
                    transition_evidence(previous,row,arms_before=a1,arms_after=a2),
                    'Review arm-count decreases', 'Arm count decreased between surveys. Saguaros can lose arms through breakage or damage; review source notes and measurements before interpreting this as an error.'))
    intervals = sorted({p['interval'] for p in pairs})
    for interval in intervals:
        members = [p for p in pairs if p['interval'] == interval]
        if len(members) < config.get('minimum_growth_pairs', 10):
            continue
        rates = np.array([p['rate'] for p in members])
        center = float(np.median(rates))
        mad = float(np.median(np.abs(rates-center)))
        spread = 1.4826*mad
        if spread == 0:
            spread = float(np.subtract(*np.percentile(rates,[75,25])) / 1.349)
        if spread == 0:
            continue
        upper = center + config['robust_mad_multiplier'] * spread
        for pair in members:
            if pair['rate'] > upper:
                findings.append(finding('TEMPORAL_GROWTH_OUTLIER', pair['row'], 'height_m',
                    transition_evidence(pair['previous_row'],pair['row'],annual_growth_m=pair['rate'],empirical_upper=upper,median=center,robust_spread=spread,n=len(members)),
                    'Annualized growth within interval-specific robust empirical threshold',
                    'Statistical screening only; no biological maximum asserted.'))
    return findings
