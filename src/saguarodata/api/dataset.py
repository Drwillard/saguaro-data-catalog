from pathlib import Path
import pandas as pd

class Dataset:
    def __init__(self, path):
        self.path = Path(path)
        if not (self.path / 'organism_observations.parquet').exists():
            raise FileNotFoundError(f'No canonical build at {self.path}. Run saguarodata all.')

    def table(self, name):
        if name not in {p.stem for p in self.path.glob('*.parquet')}:
            raise KeyError(name)
        return pd.read_parquet(self.path / f'{name}.parquet')

    def programs(self): return self.table('survey_programs')
    def surveys(self): return self.table('survey_events')
    def plots(self): return self.table('plots')

    def observations(self, program=None, year=None):
        result = self.table('organism_observations')
        if program is not None:
            result = result[result.program_id.eq(program)]
        if year is not None:
            result = result[result.survey_year.eq(year)]
        return result.reset_index(drop=True)

    def history(self, organism_id):
        if not organism_id:
            raise ValueError('A source-supported organism_id is required')
        return self.observations().loc[lambda x:x.organism_id.eq(organism_id)].sort_values('survey_year').reset_index(drop=True)

    def validation_findings(self, severity=None):
        frame = self.table('validation_findings')
        return frame if severity is None else frame[frame.severity.eq(severity)].reset_index(drop=True)

    def provenance(self, observation_id, table='organism_observations'):
        aliases = {'organism_observation':'organism_observations'}
        table = aliases.get(table,table)
        frame = self.table('provenance')
        return frame[frame.observation_id.eq(observation_id) & frame['table'].eq(table)].reset_index(drop=True)

    def lineage_graph(self,rebuild=False):
        from ..lineage import LineageGraph,build_graph
        from ..acquisition.checksums import sha256
        import json
        folder=self.path.resolve().parent/'lineage'
        if rebuild or not (folder/'lineage.sqlite').exists():return build_graph(self.path.resolve().parent.parent)
        metadata=json.loads((folder/'summary.json').read_text())
        current={p.name:sha256(p) for p in sorted(self.path.glob('*.parquet'))}
        if current!=metadata['canonical_sha256']:raise ValueError('Lineage graph is stale. Run saguarodata lineage build or use rebuild=True.')
        return LineageGraph(folder/'lineage.sqlite')

    def duckdb(self, filename=None):
        """Optional materialized SQL database; no spatial extension is required."""
        import duckdb
        connection = duckdb.connect(str(filename or self.path / 'saguaro.duckdb'))
        for path in sorted(self.path.glob('*.parquet')):
            name = path.stem.replace('"','""')
            connection.execute(f'CREATE OR REPLACE TABLE "{name}" AS SELECT * FROM read_parquet(?)', [str(path.resolve())])
        return connection
