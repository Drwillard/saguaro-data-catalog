import pytest
from saguarodata.normalize.missing import missing_reason, number
from saguarodata.normalize.units import height_to_m
from saguarodata.normalize.identifiers import normalize_identifier, stable_id
from saguarodata.ingest.common import note_status

@pytest.mark.parametrize('value,reason', [('', 'source_missing'),('NA','unknown'),('not measured','not_measured'),('not applicable','not_applicable'),('not found','not_found'),('dead',None),(0,None)])
def test_missing_semantics(value,reason): assert missing_reason(value)==reason

def test_missing_arms_never_become_zero():
    assert number('')[0] is None
    assert number('dead')==(None,'invalid_numeric')
    assert number(0)==(0,None)
    assert missing_reason('',collected=False)=='not_collected'

def test_units():
    assert height_to_m(10,'ft')==pytest.approx(3.048)
    assert height_to_m(100,'cm')==1
    with pytest.raises(ValueError):height_to_m(2,'unknown')

def test_identifiers():
    assert normalize_identifier(' 41a ')=='41A'
    assert normalize_identifier('1.0')=='1'
    assert stable_id('a:b','c')!=stable_id('a','b:c')

def test_status_is_not_a_substring_or_an_undated_comment():
    assert note_status('not dead')[0]=='unknown'
    assert note_status('dead arm')[0]=='unknown'
    assert note_status('dead 2014',2010)[0]=='unknown'
    assert note_status('dead 2014',2014)[0]=='dead'
