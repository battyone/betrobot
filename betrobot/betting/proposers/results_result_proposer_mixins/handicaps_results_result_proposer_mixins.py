import numpy as np
from betrobot.betting.proposers.results_result_proposer_mixins.results_result_proposer_mixin import ResultsResultProposerMixin
from betrobot.util.sport_util import get_bets


class HandicapsHomeResultsResultProposerMixin(ResultsResultProposerMixin):

    def _handle_bet(self, bet, prediction, betcity_match, whoscored_match=None):
        handicap = bet[4]
        (events_home_count_prediction, events_away_count_prediction) = prediction
        if events_home_count_prediction - events_away_count_prediction + handicap > self.min_diff:
            self.propose(bet, betcity_match, None, whoscored_match=whoscored_match)


class HandicapsAwayResultsResultProposerMixin(ResultsResultProposerMixin):

    def _handle_bet(self, bet, prediction, betcity_match, whoscored_match=None):
        handicap = bet[4]
        (events_home_count_prediction, events_away_count_prediction) = prediction
        if events_home_count_prediction - events_away_count_prediction + handicap < -self.min_diff:
            self.propose(bet, betcity_match, None, whoscored_match=whoscored_match)
