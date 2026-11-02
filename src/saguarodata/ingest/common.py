import json
from . import excel
from ..normalize.identifiers import stable_id, normalize_identifier
from ..normalize.missing import number
from ..normalize.annotations import observation_annotations,verification_status,ANNOTATION_METHOD

def stringify(value):
    return '' if value is None else str(value)

def lineage(entry, sheet, row):
    return dict(source_dataset=entry['dataset'], source_file=entry['local_filename'], source_sheet=sheet,
        source_row=int(row), source_reference_id=entry['source_reference_id'], source_sha256=entry['sha256'],
        source_row_id=stable_id(entry['sha256'], sheet, int(row)))

def observation(entry, sheet, rownum, row, program, year, plot, height_column=None, arms_column=None,
                unit=None, unit_source='unknown', individual=None, notes_column=None, status=None, status_source=None):
    source = lineage(entry, sheet, rownum)
    source_plot = normalize_identifier(plot)
    plot_id = f'{program}:{source_plot}' if source_plot else None
    height_raw = row.get(height_column, '') if height_column else ''
    height, height_reason = number(height_raw, bool(height_column))
    arms_raw = row.get(arms_column, '') if arms_column else ''
    arms, arms_reason = number(arms_raw, bool(arms_column))
    from ..normalize.units import height_to_m
    notes = stringify(row.get(notes_column, '')) if notes_column else ''
    verify_raw=stringify(row.get('Verify',''))
    return dict(**source, **observation_annotations(notes), annotation_method=ANNOTATION_METHOD,notes_source_column=notes_column,
        verification_status=verification_status(verify_raw),verification_raw=verify_raw,
        verification_source_column='Verify' if 'Verify' in row else None,
        verification_time_basis=('shared_source_row' if program=='historic_plots' else 'source_record') if 'Verify' in row else None,
        observation_id=stable_id(source['source_row_id'], program, year), program_id=program,
        organism_id=individual, survey_event_id=f'{program}:{year}', plot_id=plot_id, survey_year=int(year),
        nominal_round=int(year), status=status or 'unknown', status_raw=notes,
        status_source=status_source or 'unknown', height_raw=stringify(height_raw), height_unit_raw=unit if unit_source=='documented' else None,
        height_normalization_unit=unit,
        height_m=height_to_m(height, unit) if unit else None, height_missing_reason=height_reason if unit else (height_reason or 'unit_unknown'),
        unit_source=unit_source, arm_count_raw=stringify(arms_raw), arm_count=arms,
        arm_count_missing_reason=arms_reason, x=None, y=None, latitude=None, longitude=None, coordinate_crs=None,
        coordinate_time_basis=None, notes=notes,
        raw_values_json=json.dumps({str(k): stringify(v) for k,v in row.items()}, ensure_ascii=False))

def note_status(value, year=None):
    token = str(value).strip().lower()
    # Exact phrases only. 'not dead', 'dead arm', etc. must not become death.
    if token in {'dead', 'd'} or (year is not None and token == f'dead {year}'):
        return 'dead', 'explicit_note'
    if token in {'alive', 'live', 'living'}:
        return 'alive', 'explicit_note'
    if token in {'not found', 'missing', 'tag only'}:
        return 'not_found', 'explicit_note'
    return 'unknown', 'unknown'
