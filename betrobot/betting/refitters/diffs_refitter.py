from betrobot.betting.refitter import Refitter
from betrobot.util.sport_util import get_teams_tournaments_countries_data


class DiffsRefitter(Refitter):

    _pick = [ 'home', 'away', 'events_home_diffs', 'events_away_diffs' ]


    def _clean(self):
        super()._clean()

        self.home = None
        self.away = None
        self.events_home_diffs = None
        self.events_away_diffs = None


    def _refit(self, betcity_match):
        statistic = self.previous_fitter.statistic
        if statistic.shape[0] == 0:
            return

        self.home = get_teams_tournaments_countries_data('betcityName', betcity_match['home'], 'whoscoredName')
        self.away = get_teams_tournaments_countries_data('betcityName', betcity_match['away'], 'whoscoredName')
        if self.home is None or self.away is None:
            return

        # Статистика матчей, где betcity_match['home'] тоже была хозяйкой
        home_data = statistic[ statistic['home'] == self.home ].sort_values('date', ascending=False)
        if home_data.shape[0] == 0:
            return
        # Статистика матчей, где betcity_match['away'] тоже была гостьей
        away_data = statistic[ statistic['away'] == self.away ].sort_values('date', ascending=False)
        if away_data.shape[0] == 0:
            return

        self.events_home_diffs = (home_data['events_home_count'] - home_data['events_away_count']).values
        self.events_away_diffs = (away_data['events_home_count'] - away_data['events_away_count']).values
