"""Explicit storage contracts; extra source fields remain in raw_values_json."""
LINEAGE = ['source_dataset', 'source_file', 'source_sheet', 'source_row', 'source_reference_id', 'source_sha256', 'source_row_id']
OBSERVATION_COLUMNS = ['observation_id', 'program_id', 'organism_id', 'survey_event_id', 'plot_id', 'survey_year',
    'nominal_round', 'status', 'status_raw', 'status_source', 'height_raw', 'height_unit_raw', 'height_m',
    'height_missing_reason', 'unit_source', 'arm_count_raw', 'arm_count', 'arm_count_missing_reason',
    'x', 'y', 'coordinate_crs', 'coordinate_time_basis', 'latitude', 'longitude', 'notes', 'raw_values_json'] + LINEAGE
