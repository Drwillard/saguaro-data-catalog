import hashlib
import re

def normalize_identifier(value):
    if value is None or str(value).strip() == '':
        return None
    value = str(value).strip()
    return re.sub(r'^(\d+)\.0$', r'\1', value).upper()

def stable_id(*parts):
    import json
    return hashlib.sha256(json.dumps(parts, ensure_ascii=False, default=str).encode()).hexdigest()[:24]
