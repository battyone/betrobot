import numpy as np
from betrobot.betting.proposers.match_proposers import MainMatchProposer
from betrobot.util.sport_util import get_bets


class GoalsFirstPeriodTotalsGreaterProposer(MainMatchProposer):

    def _handle(self, betcity_match, probabilities, whoscored_match=None):
        (m, n) = probabilities.shape
        for total in np.arange(0, 20.5, 0.5):
            bet_pattern = (None, 'Исходы по таймам (1-й тайм)', '', 'Бол', '*')

            correct_results = [(i,j) for i in range(m) for j in range(max(int(np.ceil(total))-i+1,0), n)]
            predicted_probability = probabilities[tuple(zip(*correct_results))].sum()

            self.propose(bet_pattern, betcity_match, 1/predicted_probability, whoscored_match=whoscored_match)


class GoalsFirstPeriodTotalsLesserProposer(MainMatchProposer):

    def _handle(self, betcity_match, probabilities, whoscored_match=None):
        (m, n) = probabilities.shape
        for total in np.arange(0, 20.5, 0.5):
            bet_pattern = (None, 'Исходы по таймам (1-й тайм)', '', 'Мен', '*')

            correct_results = [(i,j) for i in range(m) for j in range(0, min(int(np.floor(total))-i,n))]
            predicted_probability = probabilities[tuple(zip(*correct_results))].sum()

            self.propose(bet_pattern, betcity_match, 1/predicted_probability, whoscored_match=whoscored_match)


class GoalsSecondPeriodTotalsGreaterProposer(MainMatchProposer):

    def _handle(self, betcity_match, probabilities, whoscored_match=None):
        (m, n) = probabilities.shape
        for total in np.arange(0, 20.5, 0.5):
            bet_pattern = (None, 'Исходы по таймам (2-й тайм)', '', 'Бол', '*')

            correct_results = [(i,j) for i in range(m) for j in range(max(int(np.ceil(total))-i+1,0), n)]
            predicted_probability = probabilities[tuple(zip(*correct_results))].sum()

            self.propose(bet_pattern, betcity_match, 1/predicted_probability, whoscored_match=whoscored_match)


class GoalsSecondPeriodTotalsLesserProposer(MainMatchProposer):

    def _handle(self, betcity_match, probabilities, whoscored_match=None):
        (m, n) = probabilities.shape
        for total in np.arange(0, 20.5, 0.5):
            bet_pattern = (None, 'Исходы по таймам (2-й тайм)', '', 'Мен', '*')

            correct_results = [(i,j) for i in range(m) for j in range(0, min(int(np.floor(total))-i,n))]
            predicted_probability = probabilities[tuple(zip(*correct_results))].sum()

            self.propose(bet_pattern, betcity_match, 1/predicted_probability, whoscored_match=whoscored_match)