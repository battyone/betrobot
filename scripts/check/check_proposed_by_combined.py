import os
import json
import glob
import pymongo
import datetime
import argparse
from betrobot.betting.sport_util import get_teams_tournaments_countries_value
from betrobot.betting.bets_checking import check_bet


def _check_bet(bet, proposed_collection):
    whoscored_home = get_teams_tournaments_countries_value('betcityName', bet['home'], 'whoscoredName')
    whoscored_away = get_teams_tournaments_countries_value('betcityName', bet['away'], 'whoscoredName')
    if whoscored_home is None or whoscored_away is None:
        return None

    match_data = matches_collection.find_one({ 'date': date_str, 'home': home_whoscored, 'away': away_whoscored })
    if match_data is None:
        continue
    whoscored_match = match_data['whoscored'][0]

    ground_truth = _check_bet(bet['bet_pattern'], bet['match_special_word'], whoscored_match)
    if ground_truth is not None:
        proposed_collection.update_one({ '_id': bet['_id'] }, { '$set': { 'ground_truth': ground_truth }})


def _check_proposed_by_combined():
    client = pymongo.MongoClient()
    db = client['betrobot']
    proposed_collection = db['proposed']
    matches_collection = db['matches']

    unchecked_bets = proposed_collection.find({ 'ground_truth': None })
    for bet in unchecked_bets:
        date_str = bet['date'].strftime('%Y-%m-%d')
        print('%s - %s vs %s' % (date_str, bet['home'], bet['away']))

        _check_bet(bet, proposed_collection)


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.parse_args()

    _check_proposed_by_combined()
