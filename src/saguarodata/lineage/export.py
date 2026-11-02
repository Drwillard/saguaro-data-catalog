"""Streaming exports: JSON, GraphML, and typed node/edge Parquet or CSV."""
import csv
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import pyarrow as pa
import pyarrow.parquet as pq

def export_graph(graph,path,format='json'):
    path=Path(path)
    if format in ('parquet','csv'):
        path.mkdir(parents=True,exist_ok=True)
        with graph._connect() as conn:
            for table,columns in [('nodes',['id','type','label','attributes']),('edges',['id','source','target','type'])]:
                cursor=conn.execute('SELECT '+','.join(columns)+' FROM '+table+' ORDER BY id')
                target=path/(table+'.'+format)
                if format=='csv':
                    with target.open('w',encoding='utf8',newline='') as stream:
                        writer=csv.writer(stream);writer.writerow(columns)
                        while rows:=cursor.fetchmany(10000):writer.writerows(rows)
                else:
                    schema=pa.schema([(column,pa.string()) for column in columns])
                    with pq.ParquetWriter(target,schema) as writer:
                        while rows:=cursor.fetchmany(10000):writer.write_table(pa.Table.from_pylist([dict(zip(columns,row)) for row in rows],schema=schema))
        return str(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    with graph._connect() as conn,path.open('w',encoding='utf8') as stream:
        if format=='json':
            stream.write('{"nodes":[')
            for i,row in enumerate(conn.execute('SELECT id,type,label,attributes FROM nodes ORDER BY id')):
                if i:stream.write(',')
                stream.write(json.dumps(dict(id=row[0],type=row[1],label=row[2],attributes=json.loads(row[3])),ensure_ascii=False))
            stream.write('],"edges":[')
            for i,row in enumerate(conn.execute('SELECT id,source,target,type FROM edges ORDER BY id')):
                if i:stream.write(',')
                stream.write(json.dumps(dict(zip(['id','source','target','type'],row))))
            stream.write(']}')
        elif format=='graphml':
            stream.write('<?xml version="1.0" encoding="UTF-8"?><graphml xmlns="http://graphml.graphdrawing.org/xmlns">')
            for key in ('type','label','attributes'):
                stream.write(f'<key id="{key}" for="all" attr.name="{key}" attr.type="string"/>')
            stream.write('<graph id="lineage" edgedefault="directed">')
            for row in conn.execute('SELECT id,type,label,attributes FROM nodes ORDER BY id'):
                node=ET.Element('node',id=row[0])
                for key,value in zip(('type','label','attributes'),row[1:]):ET.SubElement(node,'data',key=key).text=value
                stream.write(ET.tostring(node,encoding='unicode'))
            for eid,source,target,kind in conn.execute('SELECT id,source,target,type FROM edges ORDER BY id'):
                edge=ET.Element('edge',id=eid,source=source,target=target);ET.SubElement(edge,'data',key='type').text=kind
                stream.write(ET.tostring(edge,encoding='unicode'))
            stream.write('</graph></graphml>')
        else:raise ValueError('Supported formats: json, graphml, parquet, csv')
    return str(path)
