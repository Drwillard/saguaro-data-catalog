import numpy as np
import pandas as pd
from .rules import finding

def temporal_findings(observations, config):
    findings, pairs = [], []
    linked = observations[observations.organism_id.notna()]
    for organism, group in linked.groupby('organism_id'):
        group = group.sort_values(['survey_year','observation_id'])
        # Ambiguous duplicate observations are not legitimate successive events.
        group = group[~group.duplicated('survey_event_id', keep=False)]
        rows = group.to_dict('records')
        dead = None
        for row in rows:
            if row['status'] == 'dead' and row['status_source'] in ('explicit_note','explicit_field'):
                dead = row
            elif dead and row['status'] == 'alive' and row['status_source'] in ('explicit_note','explicit_field'):
                findings.append(finding('TEMPORAL_RESURRECTION', row, 'status',
                    dict(previous=dead['observation_id'], previous_status='dead', current_status='alive'),
                    'Explicit death must not precede explicit life for a linked organism',
                    'Investigate source status, tagging and linkage; no correction applied.', 'error'))
            elif dead and row['survey_year'] > dead['survey_year'] and pd.notna(row.get('height_m')) and row['height_m'] > 0:
                findings.append(finding('TEMPORAL_MEASUREMENT_AFTER_DEATH', row, 'height_m',
                    dict(previous=dead['observation_id'], height=row['height_m']),
                    'Review measurements recorded after explicit death',
                    'A standing dead cactus can be measured; positive height does not establish resurrection.'))
        for previous, row in zip(rows, rows[1:]):
            years = row['survey_year'] - previous['survey_year']
            if years <= 0:
                continue
            if previous['status']=='not_found' and (row['status']=='alive' or (pd.notna(row.get('height_m')) and row['height_m']>0)):
                findings.append(finding('TEMPORAL_REOBSERVED',row,'status',dict(previous=previous['observation_id'],previous_status='not_found',current_status=row['status']),
                    'Review reobservation after not_found without interpreting prior absence as death',
                    'Interesting relocation sequence; not a resurrection or proof of source error.','info'))
            elif previous['status']=='unknown' and row['status']=='alive' and row['status_source'] in ('explicit_note','explicit_field'):
                findings.append(finding('TEMPORAL_STATUS_RESOLVED',row,'status',dict(previous=previous['observation_id'],previous_status='unknown',current_status='alive'),
                    'Unknown status may become explicitly known', 'A status-resolution event, not an inconsistency.','info'))
            h1, h2 = previous.get('height_m'), row.get('height_m')
            if pd.notna(h1) and pd.notna(h2) and h1 > 0 and h2 > 0:
                drop = h1 - h2
                if drop >= config['shrinkage_absolute_m'] and drop / h1 >= config['shrinkage_fraction']:
                    findings.append(finding('TEMPORAL_SHRINKAGE', row, 'height_m',
                        dict(previous=previous['observation_id'], height_before=h1, height_after=h2, elapsed_years=years),
                        'Decrease below configured absolute and proportional thresholds',
                        'Possible broken top, measurement change, unit issue, transcription error or mislinkage.'))
                pairs.append(dict(row=row, previous=previous['observation_id'], rate=(h2-h1)/years,
                    interval=(row['program_id'],previous['survey_year'],row['survey_year'])))
            a1, a2 = previous.get('arm_count'), row.get('arm_count')
            if pd.notna(a1) and pd.notna(a2) and a2 < a1:
                findings.append(finding('TEMPORAL_ARM_DECREASE', row, 'arm_count',
                    dict(previous=previous['observation_id'], arms_before=a1, arms_after=a2),
                    'Review arm-count decreases', 'Arms can break; a decrease is a warning, not proof of source error.'))
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
                    dict(previous=pair['previous'], annual_growth_m=pair['rate'], empirical_upper=upper,
                         median=center, robust_spread=spread, n=len(members)),
                    'Annualized growth within interval-specific robust empirical threshold',
                    'Statistical screening only; no biological maximum asserted.'))
    return findings
