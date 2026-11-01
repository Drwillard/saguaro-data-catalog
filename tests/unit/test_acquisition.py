import hashlib
import zipfile
import pytest
from saguarodata.acquisition.checksums import sha256
from saguarodata.acquisition.downloader import acquire,read_manifest
from saguarodata.ingest.spatial import extract_archive
from conftest import Session

def test_manifest_preserves_changed_upstream_versions(tmp_path):
    record=dict(dataset='census',filename='file.xlsx',source_title='fixture',source_reference_id='1',source_url='https://example.test',direct_download_url='https://example.test/file')
    one=acquire(tmp_path,record,Session(b'original'))
    two=acquire(tmp_path,record,Session(b'changed'))
    acquire(tmp_path,record,Session(b'changed'))
    assert len(read_manifest(tmp_path))==2
    assert (tmp_path/one['local_filename']).read_bytes()==b'original'
    assert sha256(tmp_path/two['local_filename'])==hashlib.sha256(b'changed').hexdigest()

def test_raw_integrity_failure_is_not_overwritten(tmp_path):
    record=dict(dataset='census',filename='f.xlsx',source_reference_id='1',direct_download_url='https://example.test')
    entry=acquire(tmp_path,record,Session(b'original'))
    (tmp_path/entry['local_filename']).write_bytes(b'corrupt')
    with pytest.raises(ValueError,match='integrity'):acquire(tmp_path,record,Session(b'original'))

def test_html_error_is_not_saved_as_workbook(tmp_path):
    with pytest.raises(ValueError,match='HTML'):
        acquire(tmp_path,dict(dataset='census',filename='f.xlsx',direct_download_url='https://example.test'),Session(b'<html>error</html>','text/html'))

def test_zip_traversal(tmp_path):
    path=tmp_path/'unsafe.zip'
    with zipfile.ZipFile(path,'w') as archive: archive.writestr('../escape.txt','bad')
    with pytest.raises(ValueError,match='Unsafe'):extract_archive(path,tmp_path/'interim')

def test_manifest_only_checkout_redownloads_missing_artifact(tmp_path,monkeypatch):
    from saguarodata.acquisition.downloader import download
    record=dict(dataset='census',filename='f.xlsx',source_reference_id='1',direct_download_url='https://example.test',downloadable=True)
    entry=acquire(tmp_path,record,Session(b'original'))
    (tmp_path/entry['local_filename']).unlink()
    monkeypatch.setattr('saguarodata.acquisition.downloader.requests.Session',lambda:Session(b'original'))
    assert download(tmp_path,dict(records=[record]))==[]
    assert (tmp_path/entry['local_filename']).read_bytes()==b'original'
