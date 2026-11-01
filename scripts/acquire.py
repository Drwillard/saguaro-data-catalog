from saguarodata.acquisition.catalog import discover
from saguarodata.acquisition.downloader import download
catalog = discover()
print('Holdings:', len(catalog['records']), 'failures:', catalog['failures'], flush=True)
print('Download errors:', download('.', catalog), flush=True)
