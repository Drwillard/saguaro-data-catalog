"""Traceable longitudinal scientific datasets."""
__version__ = "0.1.0"

def load(path="data/processed"):
    from .api.dataset import Dataset
    return Dataset(path)
