from pathlib import Path
import zipfile
import geopandas as gpd

def extract_archive(path, destination):
    """Extract only into interim; reject archive traversal and symlinks."""
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path) as archive:
        for member in archive.infolist():
            target = (destination / member.filename).resolve()
            if not target.is_relative_to(destination) or (member.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError(f'Unsafe archive member: {member.filename}')
        archive.extractall(destination)
    return sorted(destination.rglob('*.shp'))

def read_spatial(path):
    # Retain attribute rows when an old shapefile has malformed WKB. Null
    # geometries are surfaced as findings, never silently repaired.
    frame = gpd.read_file(path, on_invalid='warn')
    return frame
