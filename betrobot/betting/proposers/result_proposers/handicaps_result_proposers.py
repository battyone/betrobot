from betrobot.betting.proposers.result_proposers.result_proposer import ResultProposer


class HandicapsHomeResultProposer(ResultProposer):

    def _handle_bet(self, bet, result_prediction, match_header, **kwargs):
        (events_home_count_prediction, events_away_count_prediction) = result_prediction
        handicap = bet['pattern'][4]

        if (events_home_count_prediction + handicap) - events_away_count_prediction > self.min_margin:
            self.propose(bet, match_header, result_prediction=result_prediction, **kwargs)


class HandicapsAwayResultProposer(ResultProposer):

    def _handle_bet(self, bet, result_prediction, match_header, **kwargs):
        (events_home_count_prediction, events_away_count_prediction) = result_prediction
        handicap = bet['pattern'][4]

        if events_home_count_prediction - (events_away_count_prediction + handicap) < -self.min_margin:
            self.propose(bet, match_header, result_prediction=result_prediction, **kwargs)
