"""Indexed typed node/edge tables backed by local SQLite, exportable to Parquet."""
from collections import deque
from contextlib import contextmanager
import json
from pathlib import Path
import sqlite3
from .trace import observation_node,field_node,node_id

class LineageGraph:
    def __init__(self,path):
        self.path=Path(path)
        if not self.path.exists():raise FileNotFoundError('Build lineage first: saguarodata lineage build')
    @contextmanager
    def _connect(self):
        conn=sqlite3.connect(f'file:{self.path.resolve().as_posix()}?mode=ro',uri=True)
        try:yield conn
        finally:conn.close()
    def _walk(self,start,upstream=True,max_nodes=10000):
        with self._connect() as conn:
            if not conn.execute('SELECT 1 FROM nodes WHERE id=?',(start,)).fetchone():raise KeyError(start)
            seen={start};queue=deque([start]);truncated=False
            column,other=('target','source') if upstream else ('source','target')
            while queue:
                current=queue.popleft()
                for (neighbor,) in conn.execute(f'SELECT {other} FROM edges WHERE {column}=? ORDER BY id',(current,)):
                    if neighbor in seen:continue
                    if len(seen)>=max_nodes:truncated=True;continue
                    seen.add(neighbor);queue.append(neighbor)
            nodes=[];edges=[]
            for ident in sorted(seen):
                record=conn.execute('SELECT id,type,label,attributes FROM nodes WHERE id=?',(ident,)).fetchone()
                if record:nodes.append(dict(id=record[0],type=record[1],label=record[2],attributes=json.loads(record[3])))
                for eid,source,target,kind in conn.execute('SELECT id,source,target,type FROM edges WHERE source=? ORDER BY id',(ident,)):
                    if target in seen:edges.append(dict(id=eid,source=source,target=target,type=kind))
            return dict(root=start,nodes=nodes,edges=sorted(edges,key=lambda row:row['id']),truncated=truncated)
    def upstream(self,node_id,max_nodes=10000):return self._walk(node_id,True,max_nodes)
    def downstream(self,node_id,max_nodes=10000):return self._walk(node_id,False,max_nodes)
    def trace_observation(self,observation_id,table='organism_observations'):
        return self.upstream(observation_node(table,observation_id))
    def trace_field(self,observation_id,field,table='organism_observations'):
        try:trace=self.upstream(field_node(table,observation_id,field))
        except KeyError:
            # Source metadata and serialized raw blobs are already represented
            # by origin nodes rather than duplicated as millions of extra nodes.
            # Resolve their value from the authoritative canonical table.
            import pandas as pd
            if table not in ('organism_observations','vegetation_observations','plot_observations','spatial_features'):raise
            key='feature_id' if table=='spatial_features' else 'observation_id'
            path=self.path.parent.parent/'processed'/f'{table}.parquet'
            try:frame=pd.read_parquet(path,columns=[key,field],filters=[(key,'=',observation_id)])
            except Exception as exc:raise KeyError(field) from exc
            if frame.empty:raise KeyError(observation_id)
            trace=self.trace_observation(observation_id,table)
            from .trace import plain
            trace.update(requested_field=field,normalized_value=plain(frame.iloc[0][field]),mapping='source_row_only_no_field_transformation')
            return trace
        trace['requested_field']=field
        trace['normalized_value']=next(n['attributes']['value'] for n in trace['nodes'] if n['id']==trace['root'])
        return trace
    def trace_finding(self,finding_id):
        return self.upstream(node_id('validation_finding',finding_id))
    def export(self,path,format='json'):
        from .export import export_graph
        return export_graph(self,path,format)
    def summary(self):
        with self._connect() as conn:
            return dict(node_counts=dict(conn.execute('SELECT type,count(*) FROM nodes GROUP BY type')),
                        edge_counts=dict(conn.execute('SELECT type,count(*) FROM edges GROUP BY type')))
