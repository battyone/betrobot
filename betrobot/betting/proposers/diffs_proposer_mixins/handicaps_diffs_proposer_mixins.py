import numpy as np
from betrobot.betting.proposers.diffs_proposer_mixins.diffs_proposer_mixin import DiffsProposerMixin
from betrobot.util.sport_util import get_bets


class HandicapsHomeDiffsProposerMixin(DiffsProposerMixin):

    def _handle_bet(self, bet, prediction, betcity_match, whoscored_match=None):
        handicap = bet[4]
        if prediction + handicap > self.min_diff:
            self.propose(bet, betcity_match, None, whoscored_match=whoscored_match)


class HandicapsAwayDiffsProposerMixin(DiffsProposerMixin):

    def _handle_bet(self, bet, prediction, betcity_match, whoscored_match=None):
        handicap = bet[4]
        if prediction + handicap < -self.min_diff:
            self.propose(bet, betcity_match, None, whoscored_match=whoscored_match)
