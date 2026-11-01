from pathlib import Path
import pandas as pd
import yaml
from .rules import Finding
from .structural import structural_findings
from .temporal import temporal_findings
from .spatial import spatial_findings, coordinate_displacements
from ..pipeline import write_table

def validate(root='.'):
    root = Path(root)
    folder = root / 'data/processed'
    config = yaml.safe_load((root / 'configs/validation_rules.yaml').read_text())
    read = lambda name: pd.read_parquet(folder / f'{name}.parquet')
    observations, plots, events, features = [read(n) for n in ('organism_observations','plots','survey_events','spatial_features')]
    findings = structural_findings(observations,plots,events)
    findings += temporal_findings(observations,config)
    findings += spatial_findings(observations,plots,features,config)
    distances=coordinate_displacements(observations)
    write_table(root,'coordinate_displacements',distances)
    summaries=[]
    for (program,before,after),group in distances.groupby(['program_id','before_year','after_year']):
        values=group.displacement_m
        summaries.append(dict(program_id=program,before_year=before,after_year=after,n=len(values),
            median_m=float(values.median()),q95_m=float(values.quantile(.95)),max_m=float(values.max())))
    write_table(root,'displacement_summaries',summaries,['program_id','before_year','after_year','n','median_m','q95_m','max_m'])
    result = write_table(root,'validation_findings',findings,list(Finding.__dataclass_fields__))
    return result
