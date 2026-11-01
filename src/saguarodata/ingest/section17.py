from .common import observation
from ..normalize.missing import number

def ingest(entry, sheet, frame):
    if sheet not in ('1941', '2011'):
        return []
    result = []
    for index, row in frame.iterrows():
        if not str(row.get('Plot', '')).strip():
            continue
        dead = str(row.get('Dead', '')).strip().lower()
        status = {'y':'dead', 'n':'alive'}.get(dead, 'unknown')
        obs = observation(entry, sheet, index, row, 'section17', int(sheet), row['Plot'],
            'Height_m_' if sheet == '2011' else None, 'arms' if sheet == '2011' else None,
            'm' if sheet == '2011' else None, 'documented' if sheet == '2011' else 'unknown',
            notes_column='Notes' if sheet == '2011' else 'Comments', status=status,
            status_source='explicit_field' if dead in ('y','n') else 'unknown')
        obs.update(source_plot_id=str(row['Plot']), height_class_raw=str(row.get('Height_Class', '')),
            height_source_column='Height_m_' if sheet == '2011' else 'Height_Class',
            arms_source_column='arms' if sheet == '2011' else None,
            x=number(row.get('x_coord'))[0], y=number(row.get('y_coord'))[0],
            coordinate_crs='EPSG:26912' if sheet == '2011' else None,
            coordinate_time_basis='survey_event' if sheet == '2011' else None)
        if sheet == '1941':
            obs['height_missing_reason'] = 'not_collected_continuous_height'
            obs['status_raw'] = str(row.get('Dead', ''))
        result.append(obs)
    return result
