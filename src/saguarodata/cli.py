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
    benchmark=sub.add_parser('benchmark');bench=benchmark.add_subparsers(dest='benchmark_action',required=True)
    corrupt=bench.add_parser('corruption');corrupt.add_argument('--seed',type=int,default=42);corrupt.add_argument('--seeds');corrupt.add_argument('--count',type=int,default=100)
    corrupt.add_argument('--sample-size',type=int,default=1200,help='Target cohort size; retains full supported histories. 0 uses the full corpus.')
    corrupt.add_argument('--intensity',type=float,default=1.,help='Positive numeric corruption magnitude multiplier; categorical scenarios stay unchanged')
    corrupt.add_argument('--append',action='store_true',help='Append distinct seeds/intensities to an identical-input experiment')
    bench.add_parser('report')
    lineage=sub.add_parser('lineage');line=lineage.add_subparsers(dest='lineage_action',required=True)
    line.add_parser('build')
    trace=line.add_parser('trace');choose=trace.add_mutually_exclusive_group(required=True)
    choose.add_argument('--observation-id');choose.add_argument('--finding-id');choose.add_argument('--node-id')
    trace.add_argument('--field');trace.add_argument('--table',default='organism_observations');trace.add_argument('--downstream',action='store_true');trace.add_argument('--output',type=Path)
    export=line.add_parser('export');export.add_argument('--format',choices=['json','graphml','parquet','csv'],default='json');export.add_argument('--output',type=Path)
    args=parser.parse_args(argv); root=Path(args.root).resolve()
    if args.command=='benchmark':
        from .benchmark.runner import run_benchmark,write_report
        if args.benchmark_action=='report':result=write_report(root)
        else:
            seeds=[int(seed) for seed in args.seeds.split(',')] if args.seeds else [args.seed]
            if args.count<1 or args.sample_size<0 or not seeds:parser.error('Positive count and nonnegative sample size required')
            result=run_benchmark(root,seeds,args.count,args.sample_size,args.intensity,args.append)
        print(json.dumps(result,indent=2));return
    if args.command=='lineage':
        from .lineage import build_graph
        from .jsonutil import dumps
        if args.lineage_action=='build':
            graph=build_graph(root);print(dumps(graph.summary(),indent=2));return
        graph=Dataset(root/'data/processed').lineage_graph()
        if args.lineage_action=='export':
            destination=args.output or root/'data/lineage'/('export' if args.format in ('parquet','csv') else 'lineage.'+args.format)
            print(graph.export(destination,args.format));return
        if args.finding_id:result=graph.trace_finding(args.finding_id)
        elif args.node_id:result=(graph.downstream if args.downstream else graph.upstream)(args.node_id)
        elif args.field:result=graph.trace_field(args.observation_id,args.field,args.table)
        else:result=graph.trace_observation(args.observation_id,args.table)
        text=dumps(result,indent=2)
        if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text,encoding='utf8')
        else:print(text)
        return
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
