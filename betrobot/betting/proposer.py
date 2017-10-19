from abc import ABCMeta, abstractmethod
import datetime
import pickle
import numpy as np
import pandas as pd
from betrobot.betting.sport_util import get_bets_match, filter_bets
from betrobot.betting.bets_checking import check_bet
from betrobot.util.pickable_mixin import PickableMixin
from betrobot.util.printable_mixin import PrintableMixin


class Proposer(PickableMixin, PrintableMixin, metaclass=ABCMeta):

    _pick = [ 'value_threshold', 'bets_data', 'attempts_count' ]


    def __init__(self, value_threshold=None):
        super().__init__()

        self.value_threshold = value_threshold

        self.clean()


    def clean(self):
        self.bets_data = pd.DataFrame(columns=['match_uuid', 'pattern', 'value', 'ground_truth', 'prediction_info_uuid'])
        self.attempts_count = 0


    def propose(self, bet, match_header, prediction_info, **kwargs):
        self.attempts_count += 1

        if self.value_threshold is not None and bet['value'] < self.value_threshold:
            return

        bet_data = {
            'match_uuid': match_header['uuid'],
            'pattern': bet['pattern'],
            'value': bet['value'],
            'ground_truth': bet['ground_truth'],
            'prediction_info_uuid': prediction_info['uuid']
        }

        self.bets_data = self.bets_data.append(pd.Series(bet_data), ignore_index=True)


    def _get_candidate_bets(self, match_header):
        bets_match = get_bets_match(match_header['uuid'])
        bets = bets_match['bets']

        candidate_bets = filter_bets(self._candidate_bet_patterns, bets)

        return candidate_bets


    def handle(self, match_header, prediction_info, **kwargs):
        prediction = prediction_info['prediction']
        if prediction is None:
            return

        bets_match = get_bets_match(match_header['uuid'])
        if bets_match is None:
            return

        bets = bets_match['bets']
        self._handle_bets(bets, match_header, prediction_info, **kwargs)


    def _handle_bets(self, bets, match_header, prediction_info, **kwargs):
        prediction = prediction_info['prediction']
        if prediction is None:
            return

        candidate_bets = self._get_candidate_bets(match_header)
        for bet in candidate_bets:
            self._handle_bet(bet, prediction, match_header, prediction_info=prediction_info, **kwargs)


    def flush(self, collection):
        for (i, bet_data) in self.bets_data.iterrows():
            collection.replace_one({ 'match_uuid': bet_data['match_uuid'], 'pattern': bet_data['pattern'] }, bet_data.to_dict(), upsert=True)


    def _get_init_strs(self):
        result = []

        if self.value_threshold is not None:
            result.append( 'value_threshold=%.2f' % (self.value_threshold,) )

        return result
