FACTORS = {'m': 1.0, 'cm': 0.01, 'ft': 0.3048, 'in': 0.0254}

def height_to_m(value, unit):
    if unit not in FACTORS:
        raise ValueError(f'Unknown unit: {unit}')
    return None if value is None else value * FACTORS[unit]
