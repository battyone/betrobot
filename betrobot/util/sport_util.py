import os
import numpy as np
import pandas as pd
import json
from betrobot.util.common_util import count, get_first


def _get_countries():
    with open(os.path.join('data', 'whoscored_countries.json'), 'rt', encoding='utf-8') as f:
        countries = json.load(f)

    return countries

countries = _get_countries()


def _get_tournaments():
    with open(os.path.join('data', 'whoscored_tournaments.json'), 'rt', encoding='utf-8') as f:
        tournaments = json.load(f)

    return tournaments

tournaments = _get_tournaments()


def _get_teams():
  with open(os.path.join('data', 'teams.csv'), 'rt', encoding='utf-8') as f:
    teams = pd.read_csv(f)

  return teams

teams = _get_teams()


def get_country_name(country_id):
    return countries.get(country_id, country_id)


def get_team_info_by(column, value, default=None):
    s = teams.loc[ teams[column] == value ]
    if s.shape[0] > 0:
      return s.iloc[0]
    else:
      return default


def get_whoscored_team_ids_of_betcity_match(betcity_match):
    home_whoscored_id = None
    away_whoscored_id = None

    home_info = get_team_info_by('betcityName', betcity_match['home'])
    if home_info is not None:
        home_whoscored_id = home_info['whoscoredId']
    away_info = get_team_info_by('betcityName', betcity_match['away'])
    if away_info is not None:
        away_whoscored_id = away_info['whoscoredId']

    return (home_whoscored_id, away_whoscored_id)


def get_betcity_teams_of_whoscored_match(whoscored_match):
    home_betcity = None
    away_betcity = None

    home_info = get_team_info_by('whoscoredName', whoscored_match['home'])
    if home_info is not None:
        home_betcity = home_info['betcityName']
    away_info = get_team_info_by('whoscoredName', whoscored_match['away'])
    if away_info is not None:
        away_betcity = away_info['betcityName']

    return (home_betcity, away_betcity)


def get_whoscored_teams_of_betcity_match(betcity_match):
    home_whoscored_id = None
    away_whoscored_id = None

    home_info = get_team_info_by('betcityName', betcity_match['home'])
    if home_info is not None:
        home_whoscored_id = home_info['whoscoredName']
    away_info = get_team_info_by('betcityName', betcity_match['away'])
    if away_info is not None:
        away_whoscored_id = away_info['whoscoredName']

    return (home_whoscored_id, away_whoscored_id)


def get_whoscored_tournament_id_of_betcity_match(betcity_match):
    (home, away) = get_whoscored_team_ids_of_betcity_match(betcity_match)
    if home is None or away is None:
        return None

    home_info = get_team_info_by('whoscoredId', home)
    if home_info is None:
        return None

    tournament_id = home_info['whoscoredTournamentId']

    return tournament_id


def get_tournament_id_of_betcity_match(betcity_match):
    home_info = get_team_info_by('betcityName', betcity_match['home'])
    return home_info['whoscoredTournamentId']


def is_home_or_away_by_betcity_team_name(betcity_team_name, whoscored_match):
    if betcity_team_name == '1':
        return 'H'
    if betcity_team_name == '2':
        return 'A'

    team_info = get_team_info_by('betcityName', betcity_team_name)
    if team_info is None:
        return None
    team_whoscored_name = team_info['whoscoredName']

    if team_whoscored_name == whoscored_match['home']:
        return 'H'
    if team_whoscored_name == whoscored_match['away']:
        return 'A'

    return None


def get_types(event):
    types = set()

    types.add(event['type']['displayName'])

    # types.add(event['outcomeType']['displayName'])

    if event.get('isGoal'):
        types.add('Goal')
    if event.get('isTouch'):
        types.add('Touch')
    if event.get('isShot'):
        types.add('Shot')

    types.update( qualifier['type']['displayName'] for qualifier in event['qualifiers'] if 'value' not in qualifier )

    return types


def is_event_successful(event):
    return event['outcomeType']['displayName'] == 'Successful'


def is_event_unsuccessful(event):
    return event['outcomeType']['displayName'] == 'Unsuccessful'


def is_goal(event):
    return is_event_successful(event) and event.get('isGoal') == True and event['type']['displayName'] == 'Goal'


def is_pass(event):
    return event['type']['displayName'] == 'Pass'


def is_corner(event):
    return is_pass(event) and 'CornerTaken' in get_types(event)


def is_yellow_card(event):
    return is_event_successful(event) and event['type']['displayName'] == 'Card' and event['cardType']['displayName'] == 'Yellow'


def is_cross(event):
    return is_pass(event) and 'Cross' in get_types(event)


def is_shot(event):
    return event.get('isShot') == True


def is_foul(event):
    return is_event_unsuccessful(event) and 'Foul' in get_types(event) and event['type']['displayName'] == 'Foul'


def is_first_period(event):
    return event['period']['displayName'] == 'FirstHalf'


def is_second_period(event):
    return event['period']['displayName'] == 'SecondHalf'


def is_betarch_match_main(betarch_match):
    return betarch_match['specialWord'] is None


def get_betarch_main_match(betarch_data):
    return get_first(is_betarch_match_main, betarch_data)


def is_betarch_match_corner(betarch_match):
    return betarch_match['specialWord'] == 'УГЛ'


def get_betarch_corner_match(betarch_data):
    return get_first(is_betarch_match_corner, betarch_data)


def is_betarch_match_yellow_card(betarch_match):
    return betarch_match['specialWord'] == 'ЖК'


def get_betarch_yellow_card_match(betarch_data):
    return get_first(is_betarch_match_yellow_card, betarch_data)


def get_whoscored_teams(whoscored_match):
    whoscored_home = whoscored_match['matchCentreData']['home']['teamId']
    whoscored_away = whoscored_match['matchCentreData']['away']['teamId']

    return (whoscored_home, whoscored_away)


def get_betarch_teams(betarch_match):
    return (betarch_match['home'], betarch_match['away'])


def count_events(function, whoscored_match):
    return count(function, whoscored_match['matchCentreData']['events'])


def count_events_of_teams(function, whoscored_match):
    (whoscored_home, whoscored_away) = get_whoscored_teams(whoscored_match)

    events_home_count = count_events(
        lambda event: function(event) and event['teamId'] == whoscored_home,
        whoscored_match
    )
    events_away_count = count_events(
        lambda event: function(event) and event['teamId'] == whoscored_away,
        whoscored_match
    )

    return (events_home_count, events_away_count)


def bet_satisfy(condition, bet_or_pattern):
    for i in range(len(condition)):
        # FIXME: Исправлять такие ситуации на этапе парсинга
        if condition[i] != '*' and condition[i] != bet_or_pattern[i] and \
          not ((condition[i] is None and bet_or_pattern[i] == '') or (condition[i] == '' and bet_or_pattern[i] is None)):
            return False

    return True


# TODO: Избавиться в пользу get_bets ?
def get_bet(condition, betarch_match):
    bet = get_first(lambda bet: bet_satisfy(condition, bet), betarch_match['bets'])
    if bet is None or bet[5] is None:
        return None

    return bet


def get_bets(condition, betarch_match):
    bets = [ bet for bet in betarch_match['bets'] if bet[5] is not None and bet_satisfy(condition, bet) ]
    return bets


def collect_events_data(function, sample):
    events_data = pd.DataFrame(columns=['uuid', 'home', 'away', 'events_home_count', 'events_away_count']).set_index('uuid', drop=False)

    for data in sample:
          match_uuid = data['uuid']
          whoscored_match = data['whoscored'][0]

          (whoscored_home, whoscored_away) = get_whoscored_teams(whoscored_match)
          (events_home_count, events_away_count) = count_events_of_teams(function, whoscored_match)

          events_data.loc[match_uuid] = {
             'uuid': match_uuid,
             'home': whoscored_home,
             'away': whoscored_away,
             'events_home_count': events_home_count,
             'events_away_count': events_away_count
          }

    return events_data


def bet_to_string(bet, match_special_word=None):
    if len(bet) == 6:
        (special_word, type_, prefix, name, handicap, bet_value) = bet
    else:
        (special_word, type_, prefix, name, handicap) = bet
        bet_value = None

    bet_str = ''
    if match_special_word is not None:
        bet_str += '(%s) ' % (match_special_word,)
    if type_ is not None and type_ != '':
        bet_str += '%s: ' % (type_,)
    if special_word is not None and special_word != '':
        bet_str += '%s' % (special_word,)
    if prefix is not None and prefix != '':
        bet_str += ' %s' % (prefix,)
    if name is not None and name != '':
        bet_str += ' %s' % (name,)
    if handicap is not None:
        bet_str += ' (%.1f)' % (handicap,)
    if bet_value is not None:
        bet_str += ' (%.2f)' % (bet_value,)

    return bet_str


# TODO: Выводить дисперсию ROI
def get_standard_investigation(bets_data, matches_count=None):
    known_ground_truth_bets_data = bets_data.copy()

    known_ground_truth_bets_data = known_ground_truth_bets_data[ known_ground_truth_bets_data['ground_truth'].notnull() ]

    bets_count = known_ground_truth_bets_data.shape[0]
    if bets_count == 0:
        return None

    used_matches_count = known_ground_truth_bets_data['match_uuid'].nunique()
    matches_frequency = used_matches_count / matches_count if matches_count is not None else np.nan
    bets_successful = known_ground_truth_bets_data[ known_ground_truth_bets_data['ground_truth'] ]
    bets_successful_count = bets_successful.shape[0]
    accuracy = bets_successful_count / bets_count
    roi = bets_successful['bet_value'].sum() / bets_count - 1
    profit = bets_successful['bet_value'].sum() - bets_count

    standard_investigation_line_dict = {
       'matches': matches_count,
       'matches_frequency': matches_frequency,
       'bets': bets_count,
       'win': bets_successful_count,
       'accuracy': accuracy,
       'roi': roi,
       'profit': profit
    }

    return standard_investigation_line_dict


# TODO: Избавиться
def filter_bets_data_by_thresholds(bets_data, value_threshold=None, predicted_threshold=None, ratio_threshold=None, max_value=None):
    filtered_bets_data = bets_data.copy()

    if value_threshold is not None:
        filtered_bets_data = filtered_bets_data[ filtered_bets_data['bet_value'] >= value_threshold ]

    if predicted_threshold is not None:
        try:
            # WARNING: Если selecting пустой, то возникает исключение: ValueError: Cannot index with multidimensional key
            filtered_bets_data = filtered_bets_data.loc[ filtered_bets_data.apply(lambda row: row['data'].get('probability_prediction', None) is None or 1.0/row['data']['probability_prediction'] <= predicted_threshold, axis='columns'), :]
        except ValueError:
            pass

    if ratio_threshold is not None:
        try:
            # WARNING: Если selecting пустой, то возникает исключение: ValueError: Cannot index with multidimensional key
            filtered_bets_data = filtered_bets_data.loc[ filtered_bets_data.apply(lambda row: row['data'].get('probability_prediction', None) is None or row['bet_value'] * row['data']['probability_prediction'] >= ratio_threshold, axis='columns'), :]
        except ValueError:
            pass

    if max_value is not None:
        filtered_bets_data = filtered_bets_data[ filtered_bets_data['bet_value'] <= max_value ]

    return filtered_bets_data


def filter_and_sort_investigation(investigation, min_bets=50, min_matches_frequency=0.00, min_accuracy=None, min_roi=None, sort_by=['roi', 'matches'], sort_ascending=[False, False]):
    result = investigation.copy()

    if min_bets is not None:
        result = result[ result['bets'] >= min_bets ]
    if min_matches_frequency is not None:
        result = result[ result['matches_frequency'] >= min_matches_frequency ]
    if min_accuracy is not None:
        result = result[ result['accuracy'] >= min_accuracy ]
    if min_roi is not None:
        result = result[ result['roi'] >= min_roi ]

    if sort_by is not None:
        result.sort_values(by=sort_by, ascending=sort_ascending, inplace=True)

    return result
