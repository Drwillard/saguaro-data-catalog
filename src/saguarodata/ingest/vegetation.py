import json
import re
from .common import lineage, stringify
from ..normalize.identifiers import stable_id
from ..normalize.missing import number

def ingest(entry, sheet, frame):
    match = re.search(r'RawData_(\d{4})', entry['filename'])
    if not match or not sheet.isdigit():
        return []
    year = int(match[1])
    result = []
    for index, row in frame.iterrows():
        species = stringify(row.get('Species', row.get('Code', ''))).strip()
        if not species:
            continue  # totals/side calculations remain in source/inventory
        source = lineage(entry, sheet, index)
        count_raw = row.get('Stems', row.get('Count', ''))
        count, reason = number(count_raw)
        result.append(dict(**source, observation_id=stable_id(source['source_row_id'], year),
            program_id='vegetation', survey_event_id=f'vegetation:{year}', survey_year=year,
            plot_id=f'vegetation:{int(sheet)}', subplot_id=f'vegetation:{int(sheet)}',
            species_raw=species, species_name_raw=stringify(row.get('Name', '')),
            count_raw=stringify(count_raw), count=count, count_missing_reason=reason,
            cover_raw=stringify(row.get('% Cover', row.get('Cover', ''))),
            cover_unit_raw='% Cover' if '% Cover' in row else 'unknown',
            cover_normalized=None, cover_missing_reason='unit_ambiguous',
            area_m2=number(row.get('Area (m2)'))[0],
            raw_values_json=json.dumps({str(k): stringify(v) for k,v in row.items()})))
    return result
