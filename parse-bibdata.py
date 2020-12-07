"""
Transform bibliography data into a format easily usable in Pandas.

Usage:
    parse-bibdata.py [-o <file>] <dir>

Options:
    -o <file>
        Write output to <file>.
    <dir>
        The directory of bibliographic data to process.
"""

from pathlib import Path
import re
import pandas as pd
from requests.models import stream_decode_response_unicode
import html5lib as html
import requests
from tqdm import tqdm
from docopt import docopt

_c_re = re.compile(r'^%([A-Z*]) (.*)')
_blank_re = re.compile(r'^\s*$')
_bib_codes = {
    'T': 'title',
    'X': 'abstract',
    'A': 'authors',
    'D': 'date',
    'M': 'id'
}
def parse_bib(text):
    bibrec = {}
    last_fld = None
    for line in text.splitlines():
        cm = _c_re.match(line)
        if _blank_re.match(line):
            # end of record, emit
            if bibrec:
                yield bibrec
            bibrec = {}
        elif cm:
            # new field
            code = cm.group(1)
            value = cm.group(2)
            fld = _bib_codes.get(code, None)
            if fld:
                if fld in bibrec:
                    bibrec[fld] += '; ' + value
                else:
                    bibrec[fld] = value
            last_fld = fld
        elif last_fld:
            # text, add to field
            bibrec[last_fld] += ' ' + line
            
    # if we have an in-progress record, emit it
    if bibrec:
        yield bibrec


def main(opts):
    dir = Path(opts['<dir>'])
    outfile = opts['-o']
    if outfile is None:
        outfile = dir.with_suffix('.csv')
    else:
        outfile = Path(outfile)
    
    # parse files
    records = []
    files = list(dir.glob('*.bib'))
    print('processing', len(files), 'files')
    for file in dir.glob('*.bib'):
        for rec in parse_bib(file.read_text('utf8')):
            rec['file'] = file.stem
            records.append(rec)
    print('parsed', len(records), 'records')
    frame = pd.DataFrame.from_records(records)
    frame['year'] = frame['date'].str.replace(r'^(\d{4}).*', r'\1').astype('i4')
    frame.to_csv(outfile, index=False)


if __name__ == '__main__':
    opts = docopt(__doc__)
    main(opts)