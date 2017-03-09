import pandas as pd
from betting.fitter import Fitter
from util.sport_util import tournaments, collect_events_data


class TeamsPairAndTournamentBasedFitter(Fitter):

    _pick = [ '_events_condition' ]


    def __init__(self, events_condition, **kwargs):
       Fitter.__init__(self, **kwargs)

       self._events_condition = events_condition


    def fit(self, train_sampler):
        tournaments_fitted_data = {}

        for tournament_id in tournaments:
            tournament_id = int(tournament_id)
            print(tournament_id)

            tournament_sample_condition = { 'tournamentId': tournament_id }
            sample = train_sampler.sample(tournament_sample_condition)

            tournaments_fitted_data[tournament_id] = self._fit_on_sample(sample)

        return tournaments_fitted_data


    def _fit_on_sample(self, sample):
        events_data = collect_events_data(self._events_condition, sample)
        events_home_mean = events_data['events_home_count'].mean()
        events_away_mean = events_data['events_away_count'].mean()

        teams_attack_defense = pd.DataFrame(columns=['team', 'home_attack', 'home_defense', 'away_attack', 'away_defense']).set_index('team')

        home_teams = set(events_data['home'])
        for team in home_teams:
            team_home_data = events_data[ events_data['home'] == team ]
            teams_attack_defense.loc[team, 'home_attack'] = team_home_data['events_home_count'].mean() / events_home_mean
            teams_attack_defense.loc[team, 'home_defense'] = team_home_data['events_away_count'].mean() / events_away_mean

        away_teams = set(events_data['away'])
        for team in away_teams:
            team_away_data = events_data[ events_data['away'] == team ]
            teams_attack_defense.loc[team, 'away_attack'] = team_away_data['events_away_count'].mean() / events_away_mean
            teams_attack_defense.loc[team, 'away_defense'] = team_away_data['events_home_count'].mean() / events_home_mean

        fitted_data = {
            'teams_attack_defense': teams_attack_defense,
            'events_home_mean': events_home_mean,
            'events_away_mean': events_away_mean
        }

        return fitted_data
