"""Audit cached bytes, independently reacquire NPS sources and rebuild in isolation.

Uses live NPS services and keeps the audit under ignored interim storage. It
never changes the primary raw manifest, processed tables or served reports.
"""
import json
from pathlib import Path
import shutil
import tempfile

import pandas as pd

from saguarodata.acquisition.catalog import discover
from saguarodata.acquisition.checksums import sha256
from saguarodata.acquisition.downloader import download, read_manifest
from saguarodata.inventory import inventory
from saguarodata.pipeline import build
from saguarodata.schema_history import evolution
from saguarodata.validation.engine import validate


def main():
    root = Path(__file__).resolve().parents[1]
    expected = read_manifest(root)
    if not expected:
        raise ValueError('A baseline raw manifest is required')
    for entry in expected:
        if sha256(root / entry['local_filename']) != entry['sha256']:
            raise ValueError(f"Cached integrity failure: {entry['filename']}")
    parent = root / 'data/interim'
    parent.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix='reproducibility-', dir=parent))
    shutil.copytree(root / 'configs', scratch / 'configs')
    catalog = discover(scratch)
    if catalog['failures']:
        raise ValueError(catalog['failures'])
    errors = download(scratch, catalog)
    if errors:
        raise ValueError(errors)
    actual = read_manifest(scratch)
    identity = lambda entry: (entry['direct_download_url'], entry['sha256'])
    expected_set = {identity(entry) for entry in expected}
    actual_set = {identity(entry) for entry in actual}
    if expected_set != actual_set:
        raise ValueError(f'Upstream selection/bytes changed: missing={expected_set-actual_set}; added={actual_set-expected_set}')
    print(f'Fresh pull matches all {len(actual)} baseline artifact hashes.', flush=True)
    inventory(scratch)
    build(scratch)
    evolution(scratch)
    validate(scratch)
    comparisons = {}
    for table, key in [
        ('organism_observations', 'observation_id'),
        ('organisms', 'organism_id'),
        ('plot_observations', 'observation_id'),
        ('vegetation_observations', 'observation_id'),
        ('spatial_features', 'feature_id'),
    ]:
        before = pd.read_parquet(root / f'data/processed/{table}.parquet').sort_values(key).reset_index(drop=True)
        after = pd.read_parquet(scratch / f'data/processed/{table}.parquet').sort_values(key).reset_index(drop=True)
        pd.testing.assert_frame_equal(before, after)
        comparisons[table] = len(after)
    # Acquisition timestamps and build metadata intentionally differ. Findings
    # are compared by semantic fields rather than their presentation ordering.
    before = pd.read_parquet(root / 'data/processed/validation_findings.parquet')
    after = pd.read_parquet(scratch / 'data/processed/validation_findings.parquet')
    fields = ['rule_id', 'severity', 'table', 'entity_identifier', 'message']
    pd.testing.assert_frame_equal(before[fields].sort_values(fields).reset_index(drop=True),
                                  after[fields].sort_values(fields).reset_index(drop=True))
    result = dict(artifact_hashes_matched=len(actual), canonical_rows_matched=comparisons,
                  validation_findings_matched=len(after), audit_directory=str(scratch.relative_to(root)))
    (parent / 'reproducibility_check.json').write_text(json.dumps(result, indent=2), encoding='utf8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
