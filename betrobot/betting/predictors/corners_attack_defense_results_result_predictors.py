import numpy as np
from betrobot.betting.predictor import Predictor
from betrobot.betting.predictors.attack_defense_results_result_predictor import AttackDefenseResultsResultPredictor


class CornersAttackDefenseResultsResultPredictor(Predictor):

    _pick = [ '_corners_attack_defense_results_result_predictor' ]


    def __init__(self, **kwargs):
         super().__init__()

         self._corners_attack_defense_results_result_predictor = AttackDefenseResultsResultPredictor(**kwargs)


    def _predict(self, fitteds, match_header, **kwargs):
        [ corners_events_mean_fitted, corners_matches_data_fitted ] = fitteds

        corners_prediction = self._corners_attack_defense_results_result_predictor.predict([ corners_events_mean_fitted, corners_matches_data_fitted ], match_header, **kwargs)

        return corners_prediction


    def _get_runtime_strs(self):
        return [
            '_corners_attack_defense_results_result_predictor=%s' % (str(self._corners_attack_defense_results_result_predictor),)
        ]


class CornersViaPassesAttackDefenseResultsResultPredictor(Predictor):

    _pick = [ '_crosses_attack_defense_results_result_predictor', '_shots_attack_defense_results_result_predictor' ]


    def __init__(self, **kwargs):
         super().__init__()

         self._crosses_attack_defense_results_result_predictor = AttackDefenseResultsResultPredictor(**kwargs)
         self._shots_attack_defense_results_result_predictor = AttackDefenseResultsResultPredictor(**kwargs)


    def _predict(self, fitteds, match_header, **kwargs):
         [ crosses_events_mean_fitted, crosses_matches_data_fitted, shots_events_mean_fitted, shots_matches_data_fitted ] = fitteds

         crosses_prediction = self._crosses_attack_defense_results_result_predictor._predict([ crosses_events_mean_fitted, crosses_matches_data_fitted ], match_header, **kwargs)
         if crosses_prediction is None:
             return
         (crosses_home_prediction, crosses_away_prediction) = crosses_prediction

         shots_prediction = self._shots_attack_defense_results_result_predictor._predict([ shots_events_mean_fitted, shots_matches_data_fitted ], match_header, **kwargs)
         if shots_prediction is None:
             return
         (shots_home_prediction, shots_away_prediction) = shots_prediction

         # Формула:
         # corners = 0.187*crosses + 0.119*shots - 0.24
         corners_home_prediction = 0.187*crosses_home_prediction + 0.119*shots_home_prediction - 0.24
         corners_away_prediction = 0.187*crosses_away_prediction + 0.119*shots_away_prediction - 0.24
         corners_prediction = (corners_home_prediction, corners_away_prediction)

         return corners_prediction


    def _get_runtime_strs(self):
        return [
            '_crosses_attack_defense_results_result_predictor=%s' % (str(self._crosses_attack_defense_results_result_predictor),),
            '_shots_attack_defense_results_result_predictor=%s' % (str(self._shots_attack_defense_results_result_predictor),)
        ]
