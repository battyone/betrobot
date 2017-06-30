import datetime
from betrobot.util.reproduce_util import cartesian_product_of_dict_item, cartesian_product, multiple_cartesian_product_of_dict_item, make_sets_of_object_templates

from betrobot.betting.samplers.whole_sampler import WholeSampler

from betrobot.betting.fitters.statistic_fitters.teams_based_statistic_fitters.corners_statistic_fitters import CornersStatisticFitter, CornersFirstPeriodStatisticFitter, CornersSecondPeriodStatisticFitter
from betrobot.betting.fitters.statistic_fitters.teams_based_statistic_fitters.crosses_statistic_fitters import CrossesStatisticFitter, CrossesFirstPeriodStatisticFitter, CrossesSecondPeriodStatisticFitter
from betrobot.betting.fitters.statistic_fitters.teams_based_statistic_fitters.shots_statistic_fitters import ShotsStatisticFitter, ShotsFirstPeriodStatisticFitter, ShotsSecondPeriodStatisticFitter

from betrobot.betting.refitters.unattainable_matches_filter_refitter_statistic_transformer_refitter import UnattainableMatchesFilterStatisticTransformerRefitter
from betrobot.betting.refitters.tournament_filter_statistic_transformer_refitter import TournamentFilterStatisticTransformerRefitter
from betrobot.betting.refitters.match_eve_statistic_transformer_refitter import MatchEveStatisticTransformerRefitter
from betrobot.betting.refitters.event_counts_refitter import EventCountsRefitter

from betrobot.betting.predictors.corners_results_result_predictors import CornersResultsResultsResultPredictor, CornersViaPassesResultsResultsResultPredictor
from betrobot.betting.predictors.corners_results_result_predictors import CornersResultsResultsResultPredictor, CornersViaPassesResultsResultsResultPredictor

from betrobot.betting.proposers.corners_result_proposers import CornersResults1ResultProposer, CornersResults1XResultProposer, CornersResultsX2ResultProposer, CornersResults2ResultProposer, CornersFirstPeriodResults1ResultProposer, CornersFirstPeriodResults1XResultProposer, CornersFirstPeriodResultsX2ResultProposer, CornersFirstPeriodResults2ResultProposer, CornersSecondPeriodResults1ResultProposer, CornersSecondPeriodResults1XResultProposer, CornersSecondPeriodResultsX2ResultProposer, CornersSecondPeriodResults2ResultProposer, CornersHandicapsHomeResultProposer, CornersHandicapsAwayResultProposer, CornersFirstPeriodHandicapsHomeResultProposer, CornersFirstPeriodHandicapsAwayResultProposer, CornersSecondPeriodHandicapsHomeResultProposer, CornersSecondPeriodHandicapsAwayResultProposer, CornersTotalsGreaterResultProposer, CornersTotalsLesserResultProposer, CornersFirstPeriodTotalsGreaterResultProposer, CornersFirstPeriodTotalsLesserResultProposer, CornersSecondPeriodTotalsGreaterResultProposer, CornersSecondPeriodTotalsLesserResultProposer, CornersIndividualTotalsHomeGreaterResultProposer, CornersIndividualTotalsHomeLesserResultProposer, CornersIndividualTotalsAwayGreaterResultProposer, CornersIndividualTotalsAwayLesserResultProposer, CornersFirstPeriodIndividualTotalsHomeGreaterResultProposer, CornersFirstPeriodIndividualTotalsHomeLesserResultProposer, CornersFirstPeriodIndividualTotalsAwayGreaterResultProposer, CornersFirstPeriodIndividualTotalsAwayLesserResultProposer, CornersSecondPeriodIndividualTotalsHomeGreaterResultProposer, CornersSecondPeriodIndividualTotalsHomeLesserResultProposer, CornersSecondPeriodIndividualTotalsAwayGreaterResultProposer, CornersSecondPeriodIndividualTotalsAwayLesserResultProposer

from betrobot.betting.experiment import Experiment

from betrobot.betting.presenters.table_summary_presenter import TableSummaryPresenter


if __name__ == '__main__':

    db_name = 'betrobot'
    collection_name = 'matches'
    train_sample_condition = { }
    test_sample_condition = {
       'date': { '$gte': datetime.datetime(2017, 1, 1) }
    }


    train_sampler = WholeSampler(db_name, collection_name)


    corners_result_refitters_sets_variants = cartesian_product(
        [ (UnattainableMatchesFilterStatisticTransformerRefitter, (), {}) ],
        [ (TournamentFilterStatisticTransformerRefitter, (), {}) ],
        [ (MatchEveStatisticTransformerRefitter, (), {}) ],
        [ (EventCountsRefitter, (), {}) ]
    )
    corners_result_refitters_sets = cartesian_product([], corners_result_refitters_sets_variants)
    corners_via_passes_result_refitters_sets = cartesian_product([], corners_result_refitters_sets_variants, corners_result_refitters_sets_variants)


    corners_result_proposers = [
        (CornersResults1ResultProposer, (), { 'min_margin': 1, 'value_threshold': 2.0 }),
        (CornersResults1XResultProposer, (), { 'min_margin': 1, 'value_threshold': 1.8 }),
        (CornersResultsX2ResultProposer, (), { 'min_margin': 1, 'value_threshold': 1.8 }),
        (CornersResults2ResultProposer, (), { 'min_margin': 1, 'value_threshold': 1.8 }),
        (CornersHandicapsHomeResultProposer, (), { 'min_margin': 1, 'value_threshold': 1.8 }),
        (CornersHandicapsAwayResultProposer, (), { 'min_margin': 2, 'value_threshold': 2.2 }),
        (CornersTotalsGreaterResultProposer, (), { 'min_margin': 2, 'value_threshold': 2.2 }),
        (CornersTotalsLesserResultProposer, (), { 'min_margin': 1, 'value_threshold': 2.0 }),
        (CornersIndividualTotalsHomeGreaterResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.6 }),
        (CornersIndividualTotalsHomeLesserResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.6 }),
        (CornersIndividualTotalsAwayGreaterResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.6 }),
        (CornersIndividualTotalsAwayLesserResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.8 })
    ]
    corners_first_period_result_proposers = [
        (CornersFirstPeriodResults1ResultProposer, (), { 'min_margin': 0, 'value_threshold': 2.0 }),
        (CornersFirstPeriodResults1XResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.8 }),
        (CornersFirstPeriodResultsX2ResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.8 }),
        (CornersFirstPeriodResults2ResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.8 }),
        (CornersFirstPeriodHandicapsHomeResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.8 }),
        (CornersFirstPeriodHandicapsAwayResultProposer, (), { 'min_margin': 1, 'value_threshold': 2.2 }),
        (CornersFirstPeriodTotalsGreaterResultProposer, (), { 'min_margin': 1, 'value_threshold': 2.2 }),
        (CornersFirstPeriodTotalsLesserResultProposer, (), { 'min_margin': 0, 'value_threshold': 2.0 }),
        (CornersFirstPeriodIndividualTotalsHomeGreaterResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.6 }),
        (CornersFirstPeriodIndividualTotalsHomeLesserResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.6 }),
        (CornersFirstPeriodIndividualTotalsAwayGreaterResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.6 }),
        (CornersFirstPeriodIndividualTotalsAwayLesserResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.8 })
    ]
    corners_second_period_result_proposers = [
        (CornersSecondPeriodResults1ResultProposer, (), { 'min_margin': 0, 'value_threshold': 2.0 }),
        (CornersSecondPeriodResults1XResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.8 }),
        (CornersSecondPeriodResultsX2ResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.8 }),
        (CornersSecondPeriodResults2ResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.8 }),
        (CornersSecondPeriodHandicapsHomeResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.8 }),
        (CornersSecondPeriodHandicapsAwayResultProposer, (), { 'min_margin': 1, 'value_threshold': 2.2 }),
        (CornersSecondPeriodTotalsGreaterResultProposer, (), { 'min_margin': 1, 'value_threshold': 2.2 }),
        (CornersSecondPeriodTotalsLesserResultProposer, (), { 'min_margin': 0, 'value_threshold': 2.0 }),
        (CornersSecondPeriodIndividualTotalsHomeGreaterResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.6 }),
        (CornersSecondPeriodIndividualTotalsHomeLesserResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.6 }),
        (CornersSecondPeriodIndividualTotalsAwayGreaterResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.6 }),
        (CornersSecondPeriodIndividualTotalsAwayLesserResultProposer, (), { 'min_margin': 0, 'value_threshold': 1.8 })
    ]


    corners_result_experiments_data = multiple_cartesian_product_of_dict_item([ {} ], {
        'train_sampler': [ train_sampler ],
        'fitters': [ [ (CornersStatisticFitter, (), {}) ] ] * len(corners_result_refitters_sets),
        'refitters_sets': corners_result_refitters_sets,
        'predictor': [ (CornersResultsResultsResultPredictor, (), {}) ],
        'proposers': [ corners_result_proposers ]
    })

    corners_first_period_result_experiments_data = multiple_cartesian_product_of_dict_item([ {} ], {
        'train_sampler': [ train_sampler ],
        'fitters': [ [ (CornersFirstPeriodStatisticFitter, (), {}) ] ] * len(corners_result_refitters_sets),
        'refitters_sets': corners_result_refitters_sets,
        'predictor': [ (CornersResultsResultsResultPredictor, (), {}) ],
        'proposers': [ corners_first_period_result_proposers ]
    })

    corners_second_period_result_experiments_data = multiple_cartesian_product_of_dict_item([ {} ], {
        'train_sampler': [ train_sampler ],
        'fitters': [ [ (CornersSecondPeriodStatisticFitter, (), {}) ] ] * len(corners_result_refitters_sets),
        'refitters_sets': corners_result_refitters_sets,
        'predictor': [ (CornersResultsResultsResultPredictor, (), {}) ],
        'proposers': [ corners_second_period_result_proposers ]
    })

    corners_via_passes_result_experiments_data = multiple_cartesian_product_of_dict_item([ {} ], {
        'train_sampler': [ train_sampler ],
        'fitters': [ [ (CrossesStatisticFitter, (), {}), (ShotsStatisticFitter, (), {}) ] ] * len(corners_via_passes_result_refitters_sets),
        'refitters_sets': corners_via_passes_result_refitters_sets,
        'predictor': [ (CornersViaPassesResultsResultsResultPredictor, (), {}) ],
        'proposers': [ corners_result_proposers ]
    })

    corners_via_passes_first_period_result_experiments_data = multiple_cartesian_product_of_dict_item([ {} ], {
        'train_sampler': [ train_sampler ],
        'fitters': [ [ (CrossesFirstPeriodStatisticFitter, (), {}), (ShotsFirstPeriodStatisticFitter, (), {}) ] ] * len(corners_via_passes_result_refitters_sets),
        'refitters_sets': corners_via_passes_result_refitters_sets,
        'predictor': [ (CornersViaPassesResultsResultsResultPredictor, (), {}) ],
        'proposers': [ corners_first_period_result_proposers ]
    })

    corners_via_passes_second_period_result_experiments_data = multiple_cartesian_product_of_dict_item([ {} ], {
        'train_sampler': [ train_sampler ],
        'fitters': [ [ (CrossesSecondPeriodStatisticFitter, (), {}), (ShotsSecondPeriodStatisticFitter, (), {}) ] ] * len(corners_via_passes_result_refitters_sets),
        'refitters_sets': corners_via_passes_result_refitters_sets,
        'predictor': [ (CornersViaPassesResultsResultsResultPredictor, (), {}) ],
        'proposers': [ corners_second_period_result_proposers ]
    })


    presenter = TableSummaryPresenter()
    presenters = [ presenter ]


    experiments_data = \
        corners_result_experiments_data + \
        corners_via_passes_result_experiments_data + \
        corners_first_period_result_experiments_data + \
        corners_via_passes_first_period_result_experiments_data + \
        corners_second_period_result_experiments_data + \
        corners_via_passes_second_period_result_experiments_data

    experiment = Experiment(experiments_data, presenters, db_name=db_name, collection_name=collection_name, train_sample_condition=train_sample_condition, test_sample_condition=test_sample_condition)
    experiment.test()

    representation = experiment.get_representation()
    print(representation)
