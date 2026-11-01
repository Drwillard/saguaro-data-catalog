"""Strict JSON for scientific values: nonfinite/missing scalars become null."""
import json
import math
from numbers import Real

def sanitize(value):
    if isinstance(value,dict): return {str(k):sanitize(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [sanitize(v) for v in value]
    if isinstance(value,Real) and not math.isfinite(value): return None
    if hasattr(value,'item'): return sanitize(value.item())
    return value

def dumps(value,**kwargs):
    kwargs.pop('allow_nan',None)
    return json.dumps(sanitize(value),allow_nan=False,**kwargs)
