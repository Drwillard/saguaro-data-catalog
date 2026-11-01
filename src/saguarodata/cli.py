import argparse
import json
from pathlib import Path
from .acquisition.catalog import discover
from .acquisition.downloader import download
from .inventory import inventory
from .pipeline import build
from .schema_history import evolution
from .validation.engine import validate
from .reports.quality_report import report
from .api.dataset import Dataset

def main(argv=None):
    parser=argparse.ArgumentParser(description='Auditable longitudinal scientific data pipeline')
    parser.add_argument('--root',default='.',help='Project root containing configs and data')
    sub=parser.add_subparsers(dest='command',required=True)
    source=sub.add_parser('sources'); source.add_argument('action',choices=['list','discover'])
    for name in ['download','inventory','build','validate','report','all','duckdb']:
        command=sub.add_parser(name)
        if name in ('download','all'): command.add_argument('--refresh',action='store_true',help='Acquire upstream bytes again, preserving changed versions')
    provenance=sub.add_parser('provenance'); provenance.add_argument('--observation-id',required=True)
    args=parser.parse_args(argv); root=Path(args.root).resolve()
    if args.command=='sources':
        catalog=discover(root) if args.action=='discover' else _catalog(root)
        print(json.dumps(catalog,indent=2)); return
    if args.command in ('download','all'):
        catalog=discover(root)
        errors=download(root,catalog,args.refresh)
        if catalog['failures'] or errors:
            raise SystemExit('Acquisition incomplete; see discovery catalog and acquisition_errors.json. Cached bytes remain available.')
    if args.command in ('inventory','all'): inventory(root)
    if args.command in ('build','all'): build(root); evolution(root)
    if args.command in ('validate','all'): print(f'Findings: {len(validate(root))}')
    if args.command in ('report','all'): print(json.dumps(report(root),indent=2,default=str))
    if args.command=='provenance': print(Dataset(root/'data/processed').provenance(args.observation_id).to_json(orient='records',indent=2))
    if args.command=='duckdb':
        conn=Dataset(root/'data/processed').duckdb(); conn.close()
        print(root/'data/processed/saguaro.duckdb')

def _catalog(root):
    path=root/'data/interim/discovery/catalog.json'
    return json.loads(path.read_text()) if path.exists() else discover(root)

if __name__=='__main__': main()
