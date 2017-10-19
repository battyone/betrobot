#!/usr/bin/env python3


import re
import json
import glob
import os
import datetime
import uuid
import tqdm
import argparse
from betrobot.grabbing.whoscored.parsing import fix_dirtyjson, extract_dirtyjson_definition, extract_escaped_json_definition


def _parse_file(whoscored_header_file_path):
    with open(whoscored_header_file_path, 'rt', encoding='utf-8') as f:
      whoscored_header = json.load(f)

    match_uuid_str = str(uuid.uuid4())
    match_date_str = '%s' % (whoscored_header['date'],)
    match_data = dict(whoscored_header)

    match_files_glob_path = re.sub(r'\.json$', '*.html', whoscored_header_file_path)
    match_file_paths = glob.glob(match_files_glob_path)
    for match_file_path in match_file_paths:
      with open(match_file_path, 'rt', encoding='utf-8') as f:
          match_html = f.read()

          # WARNING: Предполагается отсутствие символа ';' в репрезентации значении переменной
          extract_dirtyjson_definition(match_html, match_data, r'var matchCentreData = (.+?);', 'matchCentreData')
          # WARNING: В случае подключения других страниц (и необходимости):
          # extract_dirtyjson_definition(match_html, match_data, r'var matchCentreEventType = (.+?);', 'matchCentreEventType')
          # extract_dirtyjson_definition(match_html, match_data, r'var formationIdNameMappings = (.+?);', 'formationIdNameMappings')
          # extract_dirtyjson_definition(match_html, match_data, r'var matchStats = (.+?);', 'matchStats', re.MULTILINE | re.DOTALL)
          # extract_dirtyjson_definition(match_html, match_data, r'var initialMatchDataForScrappers = (.+?);', 'initialMatchDataForScrappers', re.MULTILINE | re.DOTALL)
          # extract_escaped_json_definition(match_html, match_data, r'var matchHeaderJson = JSON.parse\(\'(.+?)\'\);', 'matchHeader', 0)
          # extract_escaped_json_definition(match_html, match_data, r'var homePlayers = JSON.parse\(\'(.+?)\'\);', 'homePlayers', 0)
          # extract_escaped_json_definition(match_html, match_data, r'var awayPlayers = JSON.parse\(\'(.+?)\'\);', 'awayPlayers', 0)

    out_dir_path = os.path.join('tmp', 'update', 'whoscored', 'matchesJson', match_date_str)
    os.makedirs(out_dir_path, exist_ok=True)
    out_file_path = os.path.join(out_dir_path, '%s.json' % (match_uuid_str,))
    with open(out_file_path, 'wt', encoding='utf-8') as f_out:
      json.dump(match_data, f_out, ensure_ascii=False)


def _parse_whoscored_stage3(glob_path):
    file_paths = glob.glob(glob_path)
    bar = tqdm.tqdm(file_paths)
    for file_path in bar:
        bar.write('Processing file %s...' % (file_path,))
        _parse_file(file_path)


if __name__ == '__main__':
    default_glob_path = os.path.join('tmp', 'update', 'whoscored', 'matchesHtml', '*', '*.json')

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('glob_path', nargs='?', default=default_glob_path)
    args = argument_parser.parse_args()

    _parse_whoscored_stage3(args.glob_path)
