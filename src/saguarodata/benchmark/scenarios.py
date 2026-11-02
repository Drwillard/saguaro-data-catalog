from pathlib import Path
import yaml

def expected_detection_classes(scenario,category):
    """Design hypotheses, independent of the executed detector outcomes."""
    return {
        'schema_unit_removed':['structural'],
        'temporal_duplicate_event':['row','structural'],
        'temporal_identity_reassignment':['structural'],
        'temporal_year_swap':['structural','temporal'],
        'provenance_duplicate_lineage':['row','structural'],
    }.get(scenario,[category])

def load_scenarios(root):
    config=yaml.safe_load((Path(root)/'configs/corruption_scenarios.yaml').read_text())
    scenarios=config['scenarios']
    if len({row['id'] for row in scenarios})!=len(scenarios):raise ValueError('Scenario IDs must be unique')
    return scenarios
