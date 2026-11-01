"""Inspect workbook contents without pandas' implicit NA-token conversion."""
import re
import pandas as pd

def header_index(frame, filename, sheet):
    if frame.empty:
        return None
    if filename.startswith('Steenbergh'):
        return 6
    if sheet == 'Read-me':
        return None
    if sheet in ('RawData_1990_Total_Saguaros', 'raw_data_1990_saguaroperha '):
        return 1
    # Some sheets start at Excel row 2, or contain institutional banners.
    candidates = []
    for i, row in frame.head(30).iterrows():
        values = [str(v).strip() for v in row if str(v).strip()]
        score = sum(bool(re.search(r'plot|height|species|counter|cactus|saguaro|utm|^fid$|^year$|^date$|^code$', v, re.I)) for v in values)
        candidates.append((score, -i, i))
    return max(candidates)[2]

def read_sheets(path):
    book = pd.ExcelFile(path)
    for sheet in book.sheet_names:
        raw = pd.read_excel(book, sheet_name=sheet, header=None, dtype=object, keep_default_na=False)
        header = header_index(raw, path.name, sheet)
        if header is None:
            yield sheet, None, raw
            continue
        names, counts = [], {}
        for i, cell in enumerate(raw.iloc[header]):
            name = str(cell).strip() or f'__unnamed_{i+1}'
            counts[name] = counts.get(name, 0) + 1
            names.append(name if counts[name] == 1 else f'{name}__{counts[name]}')
        data = raw.iloc[header + 1:].copy()
        data.columns = names
        data.index = data.index + 1  # original, one-based Excel row
        data.attrs['original_columns'] = [str(v) for v in raw.iloc[header]]
        yield sheet, header + 1, data
