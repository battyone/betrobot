import sys
import os
import json
import glob2
from betrobot.util.sport_util import get_types


def clean_data(data, need_events):
  del data['whoscored'][0]['matchCentreEventType']
  del data['whoscored'][0]['formationIdNameMappings']
  del data['whoscored'][0]['matchCentreData']['commonEvents']
  del data['whoscored'][0]['matchCentreData']['home']['stats']
  del data['whoscored'][0]['matchCentreData']['home']['shotZones']
  del data['whoscored'][0]['matchCentreData']['home']['players']
  del data['whoscored'][0]['matchCentreData']['home']['formations']
  del data['whoscored'][0]['matchCentreData']['home']['incidentEvents']
  del data['whoscored'][0]['matchCentreData']['away']['stats']
  del data['whoscored'][0]['matchCentreData']['away']['shotZones']
  del data['whoscored'][0]['matchCentreData']['away']['players']
  del data['whoscored'][0]['matchCentreData']['away']['formations']
  del data['whoscored'][0]['matchCentreData']['away']['incidentEvents']
  data['whoscored'][0]['matchCentreData']['events'] = [ event for event in data['whoscored'][0]['matchCentreData']['events'] if not get_types(event).isdisjoint(need_events) ]


need_events = sys.argv[1:]
print(need_events)

glob_path = os.path.join('data', 'combined', 'matchesJson', '**', '*.json')
for file_path, (path, filename) in glob2.iglob(glob_path, with_matches=True):
  print(file_path)

  with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

  clean_data(data, need_events)

  out_dir_path = os.path.join('data', 'combined', 'matchesJson-cleaned', path)
  os.makedirs(out_dir_path, exist_ok=True)
  out_file_path = os.path.join(out_dir_path, '%s.json' % (filename,))
  with open(out_file_path, 'w', encoding='utf-8') as f_out:
    json.dump(data, f_out, ensure_ascii=False)
