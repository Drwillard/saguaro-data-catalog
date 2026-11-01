from .common import observation
from ..normalize.missing import number

def ingest(entry, sheet, frame):
    if sheet != 'RawData_2000_2010':
        return []
    result = []
    for index, row in frame.iterrows():
        year = number(row.get('Year'))[0]
        if year is None:
            continue
        program = 'census' if row.get('Plot_type') == 'Saguaro Census' else 'census_auxiliary'
        # Type must be part of the auxiliary plot namespace to avoid collisions.
        plot = str(row.get('Plot', '')) if program == 'census' else f"{row.get('Plot_type')}:{row.get('Plot', '')}"
        obs = observation(entry, sheet, index, row, program, int(year), plot,
            'Height (m)', 'Arms', 'm', 'documented', notes_column='Comments')
        obs.update(nominal_round=2000 if int(year) <= 2000 else 2010,
            source_individual_id=str(row.get('Saguaro_id', '')), source_plot_id=str(row.get('Plot', '')),
            height_source_column='Height (m)', arms_source_column='Arms',
            browning_missing_reason='not_collected' if int(year) > 2000 else 'see_source_fields')
        result.append(obs)
    return result
