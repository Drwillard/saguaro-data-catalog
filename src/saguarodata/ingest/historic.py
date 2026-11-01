from .common import observation, note_status
from ..normalize.identifiers import normalize_identifier, stable_id

def ingest(entry, sheet, frame):
    if sheet != 'Sheet1':
        return []
    result = []
    for index, row in frame.iterrows():
        plot = normalize_identifier(row.get('PLOT'))
        source_id = normalize_identifier(row.get('SaguaroID'))
        individual = stable_id('historic_plots', plot, source_id) if source_id and plot and plot != '71G' else None
        for year in (1975, 2001, 2010, 2014):
            # A fully empty round is not an observation of absence.
            columns = [f'Height_{year}', f'Arms_{year}', f'Notes_{year}']
            if all(str(row.get(c, '')).strip() == '' for c in columns):
                continue
            status, basis = note_status(row.get(f'Notes_{year}', ''), year)
            obs = observation(entry, sheet, index, row, 'historic_plots', year, plot,
                f'Height_{year}', f'Arms_{year}', 'm', 'inferred', individual,
                f'Notes_{year}', status, basis)
            obs.update(x=_number(row.get('UTM_X_83')), y=_number(row.get('UTM_Y_83')),
                coordinate_crs='EPSG:26912', coordinate_time_basis='shared_source_location',
                source_individual_id=source_id, source_plot_id=plot,
                height_source_column=f'Height_{year}', arms_source_column=f'Arms_{year}')
            result.append(obs)
    return result

def _number(value):
    from ..normalize.missing import number
    return number(value)[0]
