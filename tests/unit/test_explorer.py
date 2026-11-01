import json
from saguarodata.inventory import inventory
from saguarodata.pipeline import build
from saguarodata.schema_history import evolution
from saguarodata.validation.engine import validate
from saguarodata.reports.quality_report import report

def test_explorer_exports_complete_auditable_records(fixture_root):
    root=fixture_root
    inventory(root);build(root);evolution(root);validate(root);report(root)
    folder=root/'reports/explorer'
    payload=json.loads((folder/'data.json').read_text())
    columns=payload['observation_columns']
    rows=[dict(zip(columns,row)) for row in payload['observations']]
    assert len(rows)==10
    linked=[row for row in rows if row['organism_id']]
    for row in rows:
        entity=row['observation_id']
        detail=json.loads((folder/'details'/f'{entity[:2]}.json').read_text())[entity]
        assert detail['raw'] and detail['canonical']['source_sha256']
        assert detail['canonical']['source_row']>=1
        if row['height_m'] is None:
            assert detail['canonical']['height_missing_reason']
    pairs=payload['pairs']
    assert len(pairs)==3
    assert all(pair['after_id'] in {row['observation_id'] for row in linked} for pair in pairs)
    assert not any(row['organism_id'] for row in rows if row['plot_id']=='historic_plots:71G')
    html=(root/'reports/data_quality_report.html').read_text()
    assert 'explorer/app.js' in html and 'explorer/app.css' in html
    assert 'https://cdn' not in html
    assert (root/'reports/data_quality_report_static.html').exists()
    assert (folder/'sources.json').exists()
    manifest=json.loads((folder/'manifest.json').read_text())
    assert manifest['observations']==10
    assert manifest['linked_measurement_pairs']==3
    assert manifest['presentation_assets']['app.js']
    assert len(payload['summaries']['plot'])==2
