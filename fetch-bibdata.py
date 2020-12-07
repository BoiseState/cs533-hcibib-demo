"""
Fetch bibliographic data from the HCI Bibliography.

Usage:
    fetch-bibdata.py [-d <dir>] (-m <pattern> | --all)

Options:
    -d <dir>
        Store downloaded paper data in <dir> [default: bibdata]
    -m <pattern>
        Download data from papers matching regular expression <pattern>
    --all
        Download data from all papers.
"""

from pathlib import Path
import re
import pandas as pd
from requests.models import stream_decode_response_unicode
import html5lib as html
import requests
from tqdm import tqdm
from docopt import docopt

hcibib_root = 'http://hcibib.org'

def fetch_index():
    file_index = requests.get(f'{hcibib_root}/listdir.cgi')
    idx_html = html.parse(file_index.text)
    files = {}
    bib_re = re.compile(r'^/bibdata/(.*\.bib)')
    for link in idx_html.findall('*//{http://www.w3.org/1999/xhtml}a'):
        href = link.get('href')
        m = bib_re.match(href)
        if m:
            files[m.group(1)] = href
    return files


def save_file(files, name, dir):
    path = files[name]
    data = requests.get(f'{hcibib_root}{path}')
    outf = dir / name
    outf.write_text(data.text, encoding='utf8')


def main(opts):
    dir = Path(opts['-d'])
    pattern = opts.get('-m', None)
    dir.mkdir(exist_ok=True, parents=True)
    
    files = fetch_index()
    print('located', len(files), 'known files')

    if pattern is None:
        assert opts.get('--all')  # docopt will check this in advance
        to_fetch = list(files.keys())
    else:
        pre = re.compile(pattern)
        to_fetch = [n for n in files.keys() if pre.match(n)]

    print('will fetch', len(to_fetch), 'files')
    for name in tqdm(to_fetch):
        save_file(files, name, dir)


if __name__ == '__main__':
    opts = docopt(__doc__)
    main(opts)