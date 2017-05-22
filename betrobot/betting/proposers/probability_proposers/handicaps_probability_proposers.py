import numpy as np
from betrobot.betting.proposers.probability_proposers.probability_proposer import ProbabilityProposer


class HandicapsHomeProbabilityProposer(ProbabilityProposer):

    def _handle_bet(self, bet, betcity_match, probabilities, **kwargs):
        handicap = bet[4]

        probability_prediction = np.tril(probabilities, k=np.ceil(handicap)-1).sum()

        self.propose(bet, betcity_match, probability_prediction=probability_prediction, **kwargs)


class HandicapsAwayProbabilityProposer(ProbabilityProposer):

    def _handle_bet(self, bet, betcity_match, probabilities, **kwargs):
        handicap = bet[4]

        probability_prediction = np.triu(probabilities, k=-(np.ceil(handicap)-1)).sum()

        self.propose(bet, betcity_match, probability_prediction=probability_prediction, **kwargs)
