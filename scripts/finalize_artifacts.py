"""Write source notes, executed lightweight notebooks, and a reviewable tree."""
import contextlib
import io
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'data/raw/manifest.json').read_text())
lines=['# Acquired public NPS sources','',
    'Discovery starts from https://www.nps.gov/sagu/learn/nature/long-term-monitoring.htm and the linked DataStore holding metadata. These are newly downloaded official artifacts, not relabeled copies of the earlier local workbook. Every download succeeded; full hashes, URLs, MIME types and times are in `data/raw/manifest.json`.','',
    '| Program | NPS reference | Acquired artifact | SHA-256 | Bytes |','|---|---|---|---|---:|']
for entry in manifest:
    lines.append(f"| {entry['dataset']} | [{entry['source_reference_id']}]({entry['source_url']}) | {entry['filename']} | `{entry['sha256']}` | {entry['byte_size']} |")
lines+=['','The 2020 Census reports are in reference 2225396. No 2020 raw individual workbook appeared in these holdings. Reports are evidence for protocols, not substitutes for raw observations. Other publicly available files may exist outside this discovery scope.','',
    'The pre-existing `C:/code/saguaro` Census workbook has SHA-256 `acd73e553169c2808c3e4829cba17e95bfdb08824144f1985befcfa6a9b589ff`. It was inspected read-only. Its two copies are byte-identical. The new pipeline independently acquired the official workbook; compare the manifest hash to verify equivalence.','',
    '`C:/code/saguaro2` contains an iNaturalist morphology/photo project and a Phoenix urban Census guide, not NPS monitoring data. `C:/code/saguaro-cv` contains NAIP imagery and detection code. Neither is merged into NPS monitoring observations.','',
    'Tables extracted from source archives include duplicate representations and analysis/annotation layers. They remain distinguishable by source_sheet/layer. Their row counts are inventory counts, not independent plant totals.']
(root/'docs/data_sources.md').write_text('\n'.join(lines)+'\n',encoding='utf8')

notebooks=[
    ('01_source_inventory','Source inventory',"import pandas as pd\nframe = pd.read_parquet('data/processed/source_inventory.parquet')\nprint(frame.groupby('dataset')['rows'].agg(['count','sum']).to_string())"),
    ('02_schema_comparison','Schema comparison',"print(ds.table('schema_evolution').to_string(index=False))\nprint(ds.table('protocol_fields').head(12).to_string(index=False))"),
    ('03_data_quality','Data quality',"findings = ds.validation_findings()\nprint(findings.groupby(['rule_id','severity']).size().to_string())\nprint('Review reports/data_quality_report.html for raw values and lineage.')"),
    ('04_longitudinal_examples','Longitudinal examples',"linked = ds.observations(program='historic_plots').dropna(subset=['organism_id']).iloc[0]\nprint(ds.history(linked.organism_id)[['survey_year','height_raw','height_m','arm_count','status']].to_string(index=False))\nprint(ds.provenance(linked.observation_id).to_string(index=False))\nassert ds.observations(program='census').organism_id.isna().all()")]
folder=root/'notebooks';folder.mkdir(exist_ok=True)
setup="from pathlib import Path\nimport os\nif not Path('configs').exists():\n    os.chdir('..')\nimport saguarodata as sd\nds = sd.load('data/processed')"
for name,title,code in notebooks:
    cells=[dict(cell_type='markdown',metadata={},source=[f'# {title}\n','Run `saguarodata all` from the project root first. No network is used by this notebook.'])]
    namespace={}
    for count,source in enumerate([setup,code],1):
        output=io.StringIO()
        with contextlib.redirect_stdout(output):exec(compile(source,name,'exec'),namespace)
        cells.append(dict(cell_type='code',metadata={},source=source.splitlines(keepends=True),execution_count=count,
            outputs=[dict(output_type='stream',name='stdout',text=output.getvalue().splitlines(keepends=True))] if output.getvalue() else []))
    notebook=dict(cells=cells,metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),language_info=dict(name='python',version='3.12')),nbformat=4,nbformat_minor=5)
    for index,cell in enumerate(cells):cell['id']=f'{name}-{index}'
    (folder/f'{name}.ipynb').write_text(json.dumps(notebook,indent=2),encoding='utf8')

exclude={'.venv','.wheels','__pycache__','.pytest_cache','.git','build'}
files=[]
for path in sorted(root.rglob('*')):
    rel=path.relative_to(root)
    if any(part in exclude or part.endswith('.egg-info') for part in rel.parts):continue
    if rel.parts[:2] in [('data','raw'),('data','interim'),('data','external')]:continue
    if rel.parts[:2]==('reports','explorer'):continue
    if path.is_file() and path.suffix!='.log':files.append(rel.as_posix())
files+=['data/raw/manifest.json','data/raw/<program>/<sha256>/<original files>','data/interim/<discovery pages, report text, extracted spatial layers>','reports/repository_tree.txt']
files+=['reports/explorer/<interactive assets, indexes, evidence shards and browser QA>']
(root/'reports/repository_tree.txt').write_text('\n'.join(sorted(set(files)))+'\n',encoding='utf8')
print(f'Wrote source catalog for {len(manifest)} files and executed four notebooks.')
