import math

def missing_reason(value, collected=True):
    if not collected:
        return 'not_collected'
    if value is None or (isinstance(value, float) and math.isnan(value)) or str(value).strip() == '':
        return 'source_missing'
    token = str(value).strip().lower()
    return {'na': 'unknown', 'n/a': 'unknown', 'unknown': 'unknown', 'no data': 'not_recorded',
            'not measured': 'not_measured', 'not applicable': 'not_applicable', 'not found': 'not_found'}.get(token)

def number(value, collected=True):
    reason = missing_reason(value, collected)
    if reason:
        return None, reason
    try:
        result = float(value)
        if not math.isfinite(result):
            return None, 'invalid_numeric'
        return result, None
    except (TypeError, ValueError):
        return None, 'invalid_numeric'
