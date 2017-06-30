import os
import pickle
import tqdm
import pandas as pd
from betrobot.betting.fitter import Fitter


class StatisticFitter(Fitter):

    _pick = [ 'statistic', '_statistic_file_path' ]


    def _clean(self):
        super()._clean()

        self.statistic = None
        self._statistic_file_path = None


    def _fit(self, force=False):
        # FIXME: Подумать об именах
        self._statistic_file_path = os.path.join('data', 'statistics', 'statistic-%s-%s.pkl' % (self.__class__.__name__, self.train_sampler.__class__.__name__))

        if not force and os.path.exists(self._statistic_file_path):
            print('Use already saved statistic %s' % (self._statistic_file_path,))
            with open(self._statistic_file_path, 'rb') as f:
                self.statistic = pickle.load(f)

        else:
            print('Evaluating statistic %s...' % (self._statistic_file_path,))
            self.statistic = self._evaluate_statistic()


    def _evaluate_statistic(self):
        statistic = pd.DataFrame(columns=['uuid', 'date', 'tournament_id', 'home', 'away']).set_index('uuid', drop=False)

        for data in tqdm.tqdm(self.sample, total=self.sample.count()):
            whoscored_match = data['whoscored'][0]

            match_statistic = {
                'uuid': data['uuid'],
                'date': data['date'],
                'tournament_id': data['tournamentId'],
                'home': whoscored_match['home'],
                'away': whoscored_match['away'],
            }
            match_statistic_data = self._get_match_statistic_data(whoscored_match)
            match_statistic.update(match_statistic_data)

            match_df = pd.DataFrame(match_statistic, index=[ data['uuid'] ])
            statistic = pd.concat([ statistic, match_df ])

        with open(self._statistic_file_path, 'wb') as f_out:
            pickle.dump(statistic, f_out)

        return statistic


    def _get_match_statistic_data(self, whoscored_match):
        return {}
