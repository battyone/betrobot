import datetime
import numpy as np
import pandas as pd
from betrobot.betting.fitters.statistic_fitter import StatisticFitter
from betrobot.util.logging_util import get_logger


class LastMatchesFilterStatisticTransformerFitter(StatisticFitter):

    _pick = [ 'n', 'home', 'away', 'statistic' ]


    def __init__(self, n=3, **kwargs):
        super().__init__(**kwargs)

        self.n = n


    def _clean(self):
        super()._clean()

        self.home = None
        self.away = None
        self.statistic = None


    def _fit(self, match_header, **kwargs):
        statistic = self.previous_fitter.statistic.copy()
        if statistic.shape[0] == 0:
            self.statistic = statistic
            return

        self.home = match_header['home']
        self.away = match_header['away']

        last_home_uuids = statistic[ (statistic['home'] == self.home) | (statistic['away'] == self.home) ].index.values[:self.n]
        last_away_uuids = statistic[ (statistic['away'] == self.away) | (statistic['home'] == self.away) ].index.values[:self.n]
        last_uuids = np.unique(np.concatenate([last_home_uuids, last_away_uuids]))

        transformed_statistic = statistic.loc[last_uuids]

        self.statistic = transformed_statistic.copy()
        get_logger('prediction').info('Отобраны последние %u заголовков матчей, где команда %s также была хозяйкой, и последние %u заголовков матчей, где команда %s также была гостей: %u штук',
            self.n, match_header['home'], self.n, match_header['away'], self.statistic.shape[0])


    def _get_init_strs(self):
        return [
            'n=%s' % (str(self.n),)
        ]


    def _get_runtime_strs(self):
        result = []

        if self.is_fitted:
            result += [
                'home=%s' % (self.home,),
                'away=%s' % (self.away,),
                'statistic=<%u matches data>' % (self.statistic.shape[0],)
            ]

        return result
