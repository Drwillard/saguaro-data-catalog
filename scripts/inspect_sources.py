"""Development source reconnaissance; production discovery lives in the package."""
from pathlib import Path
from urllib.request import urlopen
import re
import json

out = Path('data/interim/discovery')
out.mkdir(parents=True, exist_ok=True)
urls = ['https://www.nps.gov/sagu/learn/nature/long-term-monitoring.htm']
page = urlopen(urls[0], timeout=60).read().decode()
(out / 'monitoring.html').write_text(page, encoding='utf8')
refs = sorted(set(re.findall(r'https?://irma.nps.gov/DataStore/Reference/Profile/\d+', page)))
for url in refs:
    ref = url.rsplit('/', 1)[-1]
    try:
        text = urlopen(url, timeout=60).read().decode()
        (out / f'{ref}.html').write_text(text, encoding='utf8')
        links = sorted(set(re.findall(r'[^\s"<>]*DownloadFile[^\s"<>]*', text)))
        title = re.search(r'<title>(.*?)</title>', text, re.S)
        print(json.dumps({'reference': ref, 'title': title[1].strip() if title else '', 'downloads': links}), flush=True)
    except Exception as exc:
        print(ref, repr(exc), flush=True)
