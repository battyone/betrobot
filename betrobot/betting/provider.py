import uuid
import os
import pickle
from betrobot.util.pickable import Pickable
from betrobot.util.printable import Printable
from betrobot.util.common_util import list_wrap


class Provider(Pickable, Printable):

    _pick = [ 'uuid', 'description', 'fitters', 'refitters_sets', 'predictor', 'proposers', 'attempt_matches' ]


    def __init__(self, fitters, refitters_sets, predictor, proposers, description=None):
        if refitters_sets is not None and len(fitters) != len(refitters_sets):
            raise ValueError('fitters and refitters_sets should have the same length')

        super().__init__()

        self.description = description
        self.fitters = list_wrap(fitters)
        self.refitters_sets = list_wrap(refitters_sets) if refitters_sets is not None else None
        self.predictor = predictor
        self.proposers = proposers

        self.uuid = str(uuid.uuid4())
        self.attempt_matches = set()


    def handle(self, betcity_match, whoscored_match=None, predict_kwargs=None, handle_kwargs=None):
        if predict_kwargs is None:
            predict_kwargs = {}
        if handle_kwargs is None:
            handle_kwargs = {}

        fitters_or_refitters_for_predictor = [ None ] * len(self.fitters)
        for i in range(len(self.fitters)):
            current_fitter = self.fitters[i]
            current_fitter_refitters = self.refitters_sets[i] if self.refitters_sets is not None else None

            if current_fitter_refitters is None or len(current_fitter_refitters) == 0:
                fitters_or_refitters_for_predictor[i] = current_fitter
            else:
                current_fitter_refitters[0].refit(current_fitter, betcity_match=betcity_match)
                for j in range(1, len(current_fitter_refitters)):
                    current_fitter_refitters[j].refit(current_fitter_refitters[j-1], betcity_match=betcity_match)
                fitters_or_refitters_for_predictor[i] = current_fitter_refitters[-1]

        prediction = self.predictor.predict(fitters_or_refitters_for_predictor, betcity_match, **predict_kwargs)

        for proposer in self.proposers:
            proposer.handle(betcity_match, prediction, whoscored_match=whoscored_match, **handle_kwargs)

        match_tuple = (betcity_match['date'], betcity_match['home'], betcity_match['away'])
        self.attempt_matches.add(match_tuple)


    @property
    def matches_count(self):
        return len(self.attempt_matches)


    # TODO: load


    def save(self):
        file_name = 'provider-%s.pkl' % (self.uuid,)
        file_path = os.path.join('data', 'providers', file_name)
        with open(file_path, 'wb') as f_out:
            pickle.dump(self, f_out)


    def clear_proposers(self):
        for proposer in self.proposers:
            proposer.clear()


    def _get_init_strs(self):
        return [
            'uuid=%s' % (self.uuid,),
            'fitters=[%s]' % (str(', '.join(map(str, self.fitters))),),
            'refitters_sets=[%s]' % (', '.join([ ', '.join(map(str, refitters_set)) for refitters_set in self.refitters_sets ]),),
            'predictor=%s' % (str(self.predictor),),
            'proposers=[%s]' % (str(', '.join(map(str, self.proposers))),)
        ]

    def __str__(self):
        return 'refitters_sets=[%s], predictor=%s, proposers=%s)' % (', '.join([ ', '.join(map(str, refitters_set)) for refitters_set in self.refitters_sets ]), str(self.predictor), str(', '.join(map(str, self.proposers))))
