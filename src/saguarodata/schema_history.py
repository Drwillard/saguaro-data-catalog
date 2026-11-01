"""Collection semantics and source schema evolution, separately recorded."""
import json
from pathlib import Path
import pandas as pd
from .validation.structural import schema_drift
from .pipeline import write_table

def evolution(root='.'):
    root=Path(root)
    inventory=pd.read_parquet(root/'data/processed/source_inventory.parquet')
    records=[]
    for program, filepart, sheets in [
        ('census','SaguaroCensus_RawData',['raw_data_2000','raw_data_2010']),
        ('section17','Section17_RawData',['1941','2011'])]:
        candidates=inventory[inventory.dataset.eq(program)&inventory.file.str.contains(filepart)]
        snapshots=[]
        for sheet in sheets:
            selected=candidates[candidates.sheet.eq(sheet)]
            if selected.empty: continue
            row=selected.iloc[-1]
            fields={f['name']:f['dtype'] for f in json.loads(row.fields)}
            snapshots.append((sheet,fields,row))
        for (before,fields1,row1),(after,fields2,row2) in zip(snapshots,snapshots[1:]):
            drift=schema_drift(fields1,fields2)
            records.append(dict(program_id=program,before=before,after=after,
                fields_introduced=json.dumps(drift['introduced']),fields_removed=json.dumps(drift['removed']),
                type_changes=json.dumps(drift['type_changes']),
                documented_renames=json.dumps({'height':'Height (m)','No_arms':'Arms','Plot_no':'Plot'} if program=='census' else {}),
                unit_changes='[]', unit_uncertainties='Standalone Census 2000 height lacks unit label; combined sheet explicitly labels meters' if program=='census' else '1941 classes are not continuous meters',
                protocol_differences='Browning discontinued; identifiers not cross-round tags' if program=='census' else 'Height classes replaced by continuous heights; no individual crosswalk',
                source_before=row1.file,source_after=row2.file))
    for before,after in [(1975,2001),(2001,2010),(2010,2014)]:
        records.append(dict(program_id='historic_plots',before=str(before),after=str(after),
            fields_introduced=json.dumps(['holes'] if after==2010 else []), fields_removed='[]',
            type_changes='{}', documented_renames='{}',unit_changes='[]',unit_uncertainties='Height units inferred; raw workbook suffixes retain nominal year',
            protocol_differences='2001 label spans 2001–2002; 71G linkage unsupported; shared source coordinates are not event GPS fixes',source_before='Sheet1',source_after='Sheet1'))
    return write_table(root,'schema_evolution',records)
