import json
import re
from pathlib import Path
import pandas as pd
from .acquisition.downloader import read_manifest
from .acquisition.checksums import sha256
from .ingest.excel import read_sheets
from .ingest.spatial import extract_archive, read_spatial

def profile(frame):
    fields = []
    for position, column in enumerate(frame.columns):
        values = frame.iloc[:, position]
        text = values.astype(str)
        missing = values.isna() | text.str.strip().eq('')
        populated = values[~missing]
        inferred = pd.api.types.infer_dtype(populated, skipna=True)
        fields.append(dict(name=str(column), dtype=inferred, missing_count=int(missing.sum()),
            missing_fraction=float(missing.mean()) if len(frame) else None,
            unique_count=int(populated.astype(str).nunique()),
            categories=json.dumps(populated.astype(str).value_counts().to_dict()) if populated.astype(str).nunique() <= 30 else None,
            apparent_unit=next(iter(re.findall(r'\((m|ha|m2|ft|cm)\)|\b(meters|feet)\b', str(column))), None)))
    return fields

def inventory(root='.'):
    root = Path(root).resolve()
    output = root / 'data/processed'
    output.mkdir(parents=True, exist_ok=True)
    rows, summaries = [], []
    for entry in read_manifest(root):
        path = root / entry['local_filename']
        if sha256(path) != entry['sha256']:
            raise ValueError(f'Raw integrity failure: {path}')
        suffix = path.suffix.lower()
        tables = []
        if suffix in ('.xlsx', '.xls'):
            tables = list(read_sheets(path))
        elif suffix == '.zip':
            for shp in extract_archive(path, root / 'data/interim/spatial' / entry['sha256']):
                frame = read_spatial(shp)
                tables.append((shp.relative_to(root / 'data/interim/spatial' / entry['sha256']).as_posix(), None, frame))
        elif suffix == '.pdf':
            from pypdf import PdfReader
            target = root / 'data/interim/reports' / (path.stem + '.txt')
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                text = '\n'.join(page.extract_text() or '' for page in PdfReader(path).pages)
                target.write_text(text, encoding='utf8')
        for sheet, header, frame in tables:
            fields = profile(frame)
            row = dict(dataset=entry['dataset'], file=entry['local_filename'], sha256=entry['sha256'], sheet=sheet,
                header_row=header, rows=len(frame), columns=len(frame.columns),
                original_columns=json.dumps(frame.attrs.get('original_columns',[str(c) for c in frame.columns])), fields=json.dumps(fields),
                candidate_id_fields=json.dumps([str(c) for c in frame if re.search(r'id|counter|number|plot', str(c), re.I)]),
                coordinate_columns=json.dumps([str(c) for c in frame if re.search(r'utm|coord|lat|lon|^x$|^y$', str(c), re.I)]),
                measurement_columns=json.dumps([str(c) for c in frame if re.search(r'height|arms|cover|count|brow', str(c), re.I)]),
                source_reference_id=entry['source_reference_id'], crs=str(getattr(frame, 'crs', '') or ''))
            rows.append(row)
            summaries.append(f"| {entry['dataset']} | {path.name} | {sheet} | {header} | {len(frame)} | {len(frame.columns)} |")
    result = pd.DataFrame(rows)
    result.to_parquet(output / 'source_inventory.parquet', index=False)
    report = root / 'reports/source_inventory.md'
    report.parent.mkdir(exist_ok=True)
    report.write_text('# Source inventory\n\nCounts describe parsed sheet rows, including any source summaries or blank formatted rows; they are not canonical observation counts. Header rows are one-based Excel rows. Full field types, literal categories, missingness and candidate IDs are in Parquet. Empty strings count as blank; NA/dead/not found remain distinct source tokens.\n\n| Program | File | Sheet/layer | Header row | Rows | Columns |\n|---|---|---|---:|---:|---:|\n' + '\n'.join(summaries), encoding='utf8')
    return result
