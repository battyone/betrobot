import os
import numpy as np
import pandas as pd
import datetime
import csv
from collections import Counter
from betrobot.util.database_util import db
from betrobot.util.cache_util import memoize, cache_check, cache_put, cache_get
from betrobot.util.common_util import get_value, wrap, hashize
from betrobot.util.logging_util import get_logger


# TODO: Разделить файл на части




countries_data_file_path = os.path.join('data', 'countries.csv')


with open(countries_data_file_path, 'rt', encoding='utf-8') as f:
    countries_data = pd.read_csv(f, encoding='utf-8').set_index('whoscoredCountryId', drop=False)


tournaments_data_file_path = os.path.join('data', 'tournaments.csv')


with open(tournaments_data_file_path, 'rt', encoding='utf-8') as f:
    tournaments_data = pd.read_csv(f, encoding='utf-8').set_index('whoscoredCountryId', drop=False)


teams_data_file_path = os.path.join('data', 'teams.csv')


with open(teams_data_file_path, 'rt', encoding='utf-8') as f:
    teams_data = pd.read_csv(f, encoding='utf-8').set_index('whoscoredId', drop=False)


players_data_file_path = os.path.join('data', 'players.csv')


with open(players_data_file_path, 'rt', encoding='utf-8') as f:
    players_data = pd.read_csv(f, encoding='utf-8').set_index('whoscoredPlayerId', drop=False)


def save_players_data():
    players_data.sort_values(['whoscoredName', 'whoscoredPlayerName']) \
        .to_csv(players_data_file_path, quoting=csv.QUOTE_NONNUMERIC, index=False)



def get_match_title(match_header, show_uuid=False):
    if show_uuid:
        match_title = '%s - %s vs %s (%s)' % (match_header['date'].strftime('%Y-%m-%d'), match_header['home'], match_header['away'], match_header['uuid'])
    else:
        match_title = '%s - %s vs %s' % (match_header['date'].strftime('%Y-%m-%d'), match_header['home'], match_header['away'])

    return match_title


def dateize(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')




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


def _update_current_score(whoscored_match, function):
    if 'matchCentreData' not in whoscored_match:
        return

    whoscored_match_uuid = whoscored_match['uuid']

    home_events_count = 0
    away_events_count = 0
    for event in whoscored_match['matchCentreData']['events']:
        event_id = event['id']

        namespace = hashize(whoscored_match_uuid)
        key = hashize(('current_score', function, event_id))

        current_score = (home_events_count, away_events_count)
        cache_put(key, current_score, namespace=namespace)

        if function(event):
          if is_home(event, whoscored_match=whoscored_match):
              home_events_count += 1
          elif is_away(event, whoscored_match=whoscored_match):
              away_events_count += 1


def get_current_score(event, whoscored_match):
    whoscored_match_uuid = whoscored_match['uuid']
    event_id = event['id']

    namespace = hashize(whoscored_match_uuid)
    key = hashize(('current_score', function, event_id))

    if not cache_check(key, namespace=namespace):
        _update_current_score(whoscored_match, function)

    current_score = cache_get(key, namespace=namespace)
    return current_score


def is_event_successful(event, whoscored_match=None):
    return event['outcomeType']['displayName'] == 'Successful'


def is_event_unsuccessful(event, whoscored_match=None):
    return event['outcomeType']['displayName'] == 'Unsuccessful'


def is_goal(event, whoscored_match=None):
    return event.get('isGoal') == True and event['type']['displayName'] == 'Goal'


def is_pass(event, whoscored_match=None):
    return event['type']['displayName'] == 'Pass'


def is_corner(event, whoscored_match=None):
    return is_pass(event) and 'CornerTaken' in get_types(event)


def is_yellow_card(event, whoscored_match=None):
    return event['type']['displayName'] == 'Card' and event['cardType']['displayName'] == 'Yellow'


def is_red_card(event, whoscored_match=None):
    return event['type']['displayName'] == 'Card' and event['cardType']['displayName'] == 'Red'


def is_cross(event, whoscored_match=None):
    return is_pass(event) and 'Cross' in get_types(event)


def is_shot(event, whoscored_match=None):
    return event.get('isShot') == True


def is_foul(event, whoscored_match=None):
    return 'Foul' in get_types(event) and event['type']['displayName'] == 'Foul'


def is_first_period(event, whoscored_match=None):
    if 'period' not in event:
        return False

    return event['period']['displayName'] == 'FirstHalf'


def is_first_period_main_time(event, whoscored_match=None):
    if 'period' not in event:
        return False

    return event['period']['displayName'] == 'FirstHalf' and event['minute'] < 45


def is_second_period(event, whoscored_match=None):
    if 'period' not in event:
        return False

    return event['period']['displayName'] == 'SecondHalf'


def is_second_period_main_time(event, whoscored_match=None):
    if 'period' not in event:
        return False

    return event['period']['displayName'] == 'SecondHalf' and event['minute'] < 90


def is_home(event, whoscored_match):
    return event['teamId'] == whoscored_match['homeId']


def is_away(event, whoscored_match):
    return event['teamId'] == whoscored_match['awayId']


def is_goals_score_1(event, whoscored_match):
    goals_score = get_current_score(event, whoscored_match, is_goal)
    if goals_score is None:
        return None

    return goals_score[0] > goals_score[1]


def is_goals_score_1X(event, whoscored_match):
    goals_score = get_current_score(event, whoscored_match, is_goal)
    if goals_score is None:
        return None

    return goals_score[0] >= goals_score[1]


def is_goals_score_X2(event, whoscored_match):
    goals_score = get_current_score(event, whoscored_match, is_goal)
    if goals_score is None:
        return None

    return goals_score[0] <= goals_score[1]


def is_goals_score_2(event, whoscored_match):
    goals_score = get_current_score(event, whoscored_match, is_goal)
    if goals_score is None:
        return None

    return goals_score[0] < goals_score[1]


def is_goals_score_12(event, whoscored_match):
    goals_score = get_current_score(event, whoscored_match, is_goal)
    if goals_score is None:
        return None

    return goals_score[0] != goals_score[1]


def is_goals_score_X(event, whoscored_match):
    goals_score = get_current_score(event, whoscored_match, is_goal)
    if goals_score is None:
        return None

    return goals_score[0] == goals_score[1]


def is_player(event, player_name, whoscored_match):
    if 'playerId' not in event or event['playerId'] is None:
        return False

    event_player_id_str = str(event['playerId'])
    if event_player_id_str not in whoscored_match['matchCentreData']['playerIdNameDictionary']:
        return False

    event_player_name = whoscored_match['matchCentreData']['playerIdNameDictionary'][event_player_id_str]

    return player_name == event_player_name


_match_headers = {}


def get_match_headers(sample_condition=None, force=False):
    if sample_condition is None:
        sample_condition = {}

    sample_condition_hash = hashize(sample_condition)

    match_headers_collection = db['match_headers']
    sample = match_headers_collection.find(sample_condition)

    if sample_condition_hash not in _match_headers or force:
        data = []
        for match_header in sample:
            data.append({
                'uuid': match_header['uuid'],
                'region_id': match_header['regionId'],
                'tournament_id': match_header['tournamentId'],
                'date': match_header['date'],
                'home': match_header['home'],
                'away': match_header['away']
            })
        _match_headers[sample_condition_hash] = pd.DataFrame(data, columns=['uuid', 'region_id', 'tournament_id', 'date', 'home', 'away']).set_index('uuid', drop=False)
        _match_headers[sample_condition_hash] = _match_headers[sample_condition_hash].sort_values('date', ascending=False)

    return _match_headers[sample_condition_hash].copy()


def match_exists(match_uuid):
    match_headers_collection = db['match_headers']

    return match_headers_collection.count({ 'uuid': match_uuid }) > 0


def get_match_header(match_uuid):
    match_headers_collection = db['match_headers']

    return match_headers_collection.find_one({ 'uuid': match_uuid })


def get_match_header_by_date_and_teams(date_, home, away):
    match_headers_collection = db['match_headers']

    match_header = match_headers_collection.find_one({ 'date': date_, 'home': home, 'away': away })
    if match_header is None:
        return None

    return match_header['uuid']


def get_additional_info(match_uuid):
    additional_info_collection = db['additional_info']
    return additional_info_collection.find_one({ 'match_uuid': match_uuid })


def get_extended_info(match_uuid):
    matches_collection = db['matches']
    return matches_collection.find_one({ 'match_uuid': match_uuid })


def get_bets_match(match_uuid):
    bets_collection = db['bets']
    return bets_collection.find_one({ 'match_uuid': match_uuid })


def get_match_uuid_by_whoscored_match(whoscored_match):
    date_ = dateize(whoscored_match['date'])
    home = whoscored_match['home']
    away = whoscored_match['away']

    return get_match_header_by_date_and_teams(date_, home, away)


def get_match_uuid_by_betarch_match(betarch_match):
    date_ = dateize(betarch_match['date'])
    home = get_value(teams_data, 'betarchName', betarch_match['home'], 'whoscoredName')
    away = get_value(teams_data, 'betarchName', betarch_match['away'], 'whoscoredName')
    if home is None or away is None:
        return None

    return get_match_header_by_date_and_teams(date_, home, away)


def get_match_uuid_by_betcity_match(betcity_match):
    date_ = dateize(betcity_match['date'])
    home = get_value(teams_data, 'betcityName', betcity_match['home'], 'whoscoredName')
    away = get_value(teams_data, 'betcityName', betcity_match['away'], 'whoscoredName')
    if home is None or away is None:
        return None

    return get_match_header_by_date_and_teams(date_, home, away)


def get_match_uuid_by_intelbet_match(intelbet_match):
    date_ = dateize(intelbet_match['date'])
    home = get_value(teams_data, 'intelbetName', intelbet_match['home'], 'whoscoredName')
    away = get_value(teams_data, 'intelbetName', intelbet_match['away'], 'whoscoredName')
    if home is None or away is None:
        return None

    return get_match_header_by_date_and_teams(date_, home, away)


def filter_events(function, events):
    if function is None:
        return events

    filtered_events = [ event for event in events if function(event) ]

    return filtered_events


def count_events(function, whoscored_match):
    if 'matchCentreData' not in whoscored_match:
        return None

    events = whoscored_match['matchCentreData']['events']

    if function is None:
        return len(events)

    result = 0
    for event in events:
        if function(event, whoscored_match=whoscored_match):
            result += 1

    return result


@memoize(namespace_lambda=lambda function, match_uuid: match_uuid)
def count_events_by_match_uuid(function, match_uuid):
    if not match_exists(match_uuid):
        # WARNING: Выбрасывание исключения предотвращает кеширование
        raise ValueError('match uuid %s is incorrect' % (match_uuid,))

    whoscored_match = get_extended_info(match_uuid)['whoscored']

    return count_events(function, whoscored_match)


def count_events_multiple(functions, whoscored_match):
    if 'matchCentreData' not in whoscored_match:
        return None

    results = [ 0 ] * len(functions)

    for event in whoscored_match['matchCentreData']['events']:
        for i in range(len(functions)):
            if functions[i] is None or functions[i](event, whoscored_match=whoscored_match):
                results[i] += 1

    return tuple(results)


@memoize(namespace_lambda=lambda functions, match_uuid: match_uuid)
def count_events_multiple_by_match_uuid(functions, match_uuid):
    if not match_exists(match_uuid):
        # WARNING: Выбрасывание исключения предотвращает кеширование
        raise ValueError('match uuid %s is incorrect' % (match_uuid,))

    whoscored_match = get_extended_info(match_uuid)['whoscored']

    return count_events(functions, whoscored_match)


def count_events_of_teams(function, whoscored_match):
    if 'matchCentreData' not in whoscored_match:
        return None

    t = whoscored_match['matchCentreData']['playerIdNameDictionary']

    event_team_ids = [ event.get('teamId', "Not-a-Team's") for event in whoscored_match['matchCentreData']['events'] if function(event, whoscored_match=whoscored_match) ]
    event_team_id_freqs = Counter(event_team_ids)

    home_id = whoscored_match['homeId']
    home_count = event_team_id_freqs[home_id]
    away_id = whoscored_match['awayId']
    away_count = event_team_id_freqs[away_id]

    return (home_count, away_count)


@memoize(namespace_lambda=lambda functions, match_uuid: match_uuid)
def count_events_of_teams_by_match_uuid(function, match_uuid):
    if not match_exists(match_uuid):
        return None

    whoscored_match = get_extended_info(match_uuid)['whoscored']

    return count_events_of_teams(function, whoscored_match)


def count_events_of_players(function, whoscored_match):
    if 'matchCentreData' not in whoscored_match:
        return None

    t = whoscored_match['matchCentreData']['playerIdNameDictionary']

    event_player_ids = [ event.get('playerId', "Not-a-Player's") for event in whoscored_match['matchCentreData']['events'] if function(event, whoscored_match=whoscored_match) ]
    event_player_id_freqs = Counter(event_player_ids)
    counts = { t[player_id]: event_player_id_freqs[int(player_id)] for player_id in t }

    return counts


@memoize(namespace_lambda=lambda functions, match_uuid: match_uuid)
def count_events_of_players_by_match_uuid(function, match_uuid):
    if not match_exists(match_uuid):
        return None

    whoscored_match = get_extended_info(match_uuid)['whoscored']

    return count_events_of_players(function, whoscored_match)




# TODO: Внедрить регулярные выражения?
def bet_satisfy(condition, bet):
    for i in range(len(condition)):
        if condition[i] != '*' and condition[i] != bet['pattern'][i]:
            return False

    return True


def filter_bets(bet_patterns, bets):
    filtered_bets = []
    for bet in bets:
        for _bet_pattern in bet_patterns:
            if bet_satisfy(_bet_pattern, bet):
                filtered_bets.append(bet)

    return filtered_bets


def get_substatistic(statistic, notnull=None, by=None, value=None, n=None, min_n=None, sort_by=None, ascending=True, which=None):
    def _log(substatistic, which):
        if which is None:
            get_logger().debug('%s', substatistic.to_string(index=False))
        else:
            log_columns = ['date', 'home', 'away'] + wrap(which)
            get_logger().debug('%s', substatistic[log_columns].to_string(index=False))

    substatistic = statistic

    if by is not None:
        byes = wrap(by)
        values = wrap(value)
        by_condition_list = [ substatistic[byes_item].isin(values) for byes_item in byes ]
        substatistic = substatistic[ np.logical_or.reduce(by_condition_list) ]

    if notnull is not None:
        notnulls = wrap(notnull)
        notnull_condition_list = [ substatistic[notnulls_item].notnull() for notnulls_item in notnulls ]
        substatistic = substatistic[ np.logical_and.reduce(notnull_condition_list) ]

    if min_n is not None and substatistic.shape[0] < min_n:
        _log(substatistic, which)
        return None

    if sort_by is not None:
        substatistic = substatistic.sort_values(sort_by, ascending=ascending)

    if n is not None:
        substatistic = substatistic[:n]

    _log(substatistic, which)
    if which is None:
        return substatistic.copy()
    else:
        # WARNING: Тут необходимо использовать именно `which`, а не `wrap(which)`
        return substatistic[which].values


def get_tournament_season_substatistic(statistic, tournament_id, first_year):
    first_date = datetime.datetime(first_year, 6, 1)
    last_year = first_year + 1
    last_date = datetime.datetime(last_year, 6, 1)

    substatistic = statistic
    substatistic = substatistic[ substatistic['tournament_id'] == tournament_id ]
    substatistic = substatistic[ (substatistic['date'] >= first_date) & (substatistic['date'] < last_date) ]

    return substatistic.copy()


@memoize(namespace_lambda=lambda potential_event_filter, correct_event_filter, match_uuid: match_uuid)
def count_game_situation_durations_by_match_uuid(potential_event_filter, correct_event_filter, match_uuid):
    if not match_exists(match_uuid):
        return None

    whoscored_match = get_extended_info(match_uuid)['whoscored']

    return count_game_situation_durations(potential_event_filter, correct_event_filter, whoscored_match)


def count_game_situation_durations(potential_event_filter, correct_event_filter, whoscored_match):
    def handle_event(event):
        nonlocal home_winning_duration, away_winning_duration, draw_duration, home_count, away_count, last_time_game_situation_changed

        # FIXME: Учитывать дополнительное время
        second = event['minute'] * 60 + event['second']
        current_game_situation_duration = second - last_time_game_situation_changed + 1

        if home_count > away_count:
            home_winning_duration += current_game_situation_duration
        elif home_count < away_count:
            away_winning_duration += current_game_situation_duration
        else:
            draw_duration += current_game_situation_duration

        if is_home(event, whoscored_match=whoscored_match):
            home_count += 1
        elif is_away(event, whoscored_match=whoscored_match):
            away_count += 1

        last_time_game_situation_changed = second

    if 'matchCentreData' not in whoscored_match:
        return None

    events = whoscored_match['matchCentreData']['events']
    potential_events = filter_events(potential_event_filter, events)
    correct_events = filter_events(correct_event_filter, potential_events)

    home_winning_duration = 0
    away_winning_duration = 0
    draw_duration = 0

    home_count = 0
    away_count = 0
    last_time_game_situation_changed = 0
    for event in correct_events:
        handle_event(event)

    last_potential_event = potential_events[-1]
    handle_event(last_potential_event)

    return (home_winning_duration, away_winning_duration, draw_duration)


# TODO: Выводить дисперсию ROI
def get_standard_investigation(bets_data, matches_count=None):
    known_ground_truth_bets_data = bets_data.copy()

    known_ground_truth_bets_data = known_ground_truth_bets_data[ known_ground_truth_bets_data['ground_truth'].notnull() ]

    bets_count = known_ground_truth_bets_data.shape[0]
    if bets_count == 0:
        return None

    used_matches_count = known_ground_truth_bets_data['match_uuid'].nunique()
    matches_frequency = used_matches_count / matches_count if matches_count is not None and matches_count != 0 else np.nan
    bets_successful = known_ground_truth_bets_data[ known_ground_truth_bets_data['ground_truth'] ]
    bets_successful_count = bets_successful.shape[0]
    accuracy = bets_successful_count / bets_count
    roi = bets_successful['value'].sum() / bets_count - 1
    profit = bets_successful['value'].sum() - bets_count

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
        result = result.sort_values(by=sort_by, ascending=sort_ascending)

    return result
