import json
from saguarodata.jsonutil import dumps

def test_machine_readable_json_has_no_nonfinite_constants():
    value=dumps({'x':float('nan'),'y':[float('inf'),1]})
    assert json.loads(value,parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))=={'x':None,'y':[None,1]}
