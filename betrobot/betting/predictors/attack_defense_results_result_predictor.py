import numpy as np
from betrobot.betting.predictor import Predictor
from betrobot.util.math_util import get_weights_array


class AttackDefenseResultsResultPredictor(Predictor):

    _pick = [ 'home_weights', 'away_weights' ]


    def __init__(self, home_weights=None, away_weights=None):
        super().__init__()

        self.home_weights = home_weights
        self.away_weights = away_weights


    def _predict(self, fitteds, match_header, **kwargs):
        [ events_mean_fitted, matches_data_fitted ] = fitteds

        if events_mean_fitted.events_home_mean == 0 or events_mean_fitted.events_away_mean == 0:
            return None

        whoscored_home = match_header['home']
        whoscored_away = match_header['away']
        if whoscored_home != events_mean_fitted.home or whoscored_away != events_mean_fitted.away:
            return None
        if whoscored_home != matches_data_fitted.home or whoscored_away != matches_data_fitted.away:
            return None

        # Статистика матчей, где match_header['home'] тоже была хозяйкой
        home_data = matches_data_fitted.statistic[ matches_data_fitted.statistic['home'] == whoscored_home ].sort_values('date', ascending=False)
        if home_data.shape[0] == 0:
            return None
        # Статистика матчей, где match_header['away'] тоже была гостьей
        away_data = matches_data_fitted.statistic[ matches_data_fitted.statistic['away'] == whoscored_away ].sort_values('date', ascending=False)
        if away_data.shape[0] == 0:
            return None

        home_weights_full = get_weights_array(home_data['events_home_count'].size, self.home_weights)
        away_weights_full = get_weights_array(away_data['events_away_count'].size, self.away_weights)

        # Во сколько раз превышает среднее по турниру число голов, забитых match_header['home'] в домашних матчах?
        home_attack = np.sum(home_data['events_home_count'].values * home_weights_full) / events_mean_fitted.events_home_mean
        # Во сколько раз превышает среднее по турниру число голов, пропущенных match_header['away'] в гостевых матчах?
        away_defense = np.sum(away_data['events_home_count'].values * away_weights_full) / events_mean_fitted.events_home_mean
        # Во сколько раз превышает среднее по турниру число голов, пропущенных match_header['home'] в домашних матчах?
        home_defense = np.sum(home_data['events_away_count'].values * home_weights_full) / events_mean_fitted.events_away_mean
        # Во сколько раз превышает среднее по турниру число голов, забитых match_header['away'] в гостевых матчах?
        away_attack = np.sum(away_data['events_away_count'].values * away_weights_full) / events_mean_fitted.events_away_mean

        events_home_count_prediction = home_attack * away_defense * events_mean_fitted.events_home_mean
        events_away_count_prediction = away_attack * home_defense * events_mean_fitted.events_away_mean
        prediction = (events_home_count_prediction, events_away_count_prediction)

        return prediction


    def _get_init_strs(self):
        result = []
        if self.home_weights is not None:
            strs.append( 'home_weights=[%s]' % (str(', '.join(map(str, self.home_weights))),) )
        if self.away_weights is not None:
            strs.append( 'away_weights=[%s]' % (str(', '.join(map(str, self.away_weights))),) )
        return result
