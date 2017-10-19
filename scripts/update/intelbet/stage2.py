#!/usr/bin/env python3


import re
import json
import datetime
import uuid
import os
import tqdm
import glob
import argparse
from betrobot.grabbing.intelbet.downloading import intelbet_get
from betrobot.grabbing.intelbet.parsing import handle_date


def _parse_file(file_path):
    m = re.search(r'(\d{4}-\d{2}-\d{2})\.html$', file_path)
    date_str = m.group(1)

    with open(file_path, 'rt', encoding='utf-8') as f:
        data = handle_date(f)

    for item in data:
        (intelbet_home, intelbet_away, url, match_time_str) = item

        intelbet_match_uuid_str = str(uuid.uuid4())

        intelbet_match_header = {
            'uuid': intelbet_match_uuid_str,
            'date': date_str,
            'home': intelbet_home,
            'away': intelbet_away,
            'url': url,
            'time': match_time_str
        }

        print(url)
        match_html = intelbet_get(url, delay=0.5)

        out_dir_path = os.path.join('tmp', 'update', 'intelbet', 'matchesHtml', date_str)
        os.makedirs(out_dir_path, exist_ok=True)

        header_out_file_path = os.path.join(out_dir_path, '%s.json' % (intelbet_match_uuid_str,))
        with open(header_out_file_path, 'wt', encoding='utf-8') as header_f_out:
            json.dump(intelbet_match_header, header_f_out, ensure_ascii=False)

        out_file_path = os.path.join(out_dir_path, '%s.html' % (intelbet_match_uuid_str,))
        with open(out_file_path, 'wt', encoding='utf-8') as f_out:
            f_out.write(match_html)


def _download_intelbet_stage2(glob_path):
    file_paths = glob.glob(glob_path)
    bar = tqdm.tqdm(file_paths)
    for file_path in bar:
        bar.write('Processing file %s...' % (file_path,))
        _parse_file(file_path)


if __name__ == '__main__':
    default_glob_path = os.path.join('tmp', 'update', 'intelbet', 'datesHtml', '*.html')

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('glob_path', nargs='?', default=default_glob_path)
    args = argument_parser.parse_args()

    _download_intelbet_stage2(args.glob_path)
