from pathlib import Path
import io
import json
import shutil
import zipfile
import pandas as pd
import pytest
import geopandas as gpd
from shapely.geometry import box
from saguarodata.acquisition.downloader import acquire

class Response:
    def __init__(self, content, mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
        self.content=content; self.headers={'Content-Type':mime}
    def raise_for_status(self): pass

class Session:
    def __init__(self,content,mime=None): self.content=content; self.mime=mime
    def get(self,*args,**kwargs): return Response(self.content,self.mime) if self.mime else Response(self.content)

@pytest.fixture
def fixture_root(tmp_path):
    (tmp_path/'configs').mkdir()
    shutil.copy('configs/validation_rules.yaml',tmp_path/'configs/validation_rules.yaml')
    def workbook(name,dataset,sheets,ref):
        buffer=io.BytesIO()
        with pd.ExcelWriter(buffer,engine='openpyxl') as writer:
            for sheet,frame,startrow in sheets:
                frame.to_excel(writer,sheet_name=sheet,index=False,startrow=startrow)
        record=dict(dataset=dataset,filename=name,source_title='Synthetic offline fixture',source_reference_id=ref,
            source_url=f'https://example.test/{ref}',direct_download_url=f'https://example.test/{name}',downloadable=True)
        return acquire(tmp_path,record,Session(buffer.getvalue()))
    historic=pd.DataFrame([
        dict(SaguaroID='A1',PLOT='41A',Verify='Yes',UTM_X_83=525600,UTM_Y_83=3564200,Height_1975=7,Height_2001=5,Height_2010=6,Height_2014=6.1,Arms_1975=3,Arms_2001=2,Arms_2010=2,Arms_2014=2,Notes_1975='alive',Notes_2001='dead',Notes_2010='alive',Notes_2014=''),
        dict(SaguaroID='G1',PLOT='71G',Height_1975=3,Height_2001=4,Height_2010=5,Height_2014=6,Arms_1975='',Notes_1975='alive')])
    workbook('Steenbergh_fixture.xlsx','historic_plots',[('Sheet1',historic,6)],'1')
    census=pd.DataFrame([dict(Year=2000,Plot=1,Plot_type='Saguaro Census',Saguaro_id=1,**{'Height (m)':1.2,'Arms':'not measured'}),
                         dict(Year=2010,Plot=1,Plot_type='Saguaro Census',Saguaro_id=1,**{'Height (m)':2.0,'Arms':0})])
    aggregates=pd.DataFrame([dict(survey_year=1941,plot_id='75G',total_saguaros=7.5,saguaros_per_ha=3.75)])
    total1990=pd.DataFrame([{'Plot':1,'Total saguaros':3.2}])
    workbook('SaguaroCensus_RawData_fixture.xlsx','census',[('RawData_2000_2010',census,1),('raw_data_2000',census.head(1),0),('raw_data_2010',census.tail(1),0),('RawData_1990_Total_Saguaros',total1990,1),('raw_data_by_plot_all_years',aggregates,0)],'2')
    spatial=tmp_path/'shape';spatial.mkdir()
    gpd.GeoDataFrame({'PLOT_ID':['41A'],'TYPE':['Steenbergh-Lowe Plot']},geometry=[box(525500,3564100,525800,3564400)],crs='EPSG:26912').to_file(spatial/'saguaro_plot_boundaries.shp')
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w') as archive:
        for path in spatial.iterdir():archive.write(path,path.name)
    acquire(tmp_path,dict(dataset='boundaries',filename='boundaries.zip',source_title='Fixture',source_reference_id='3',source_url='https://example.test/3',direct_download_url='https://example.test/boundaries.zip'),Session(buffer.getvalue(),'application/zip'))
    return tmp_path
