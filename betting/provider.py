import pickle


class Provider(object):

    def __init__(self):
        pass


    def prepare(self, **kwargs):
        raise NotImplementedError()


    def handle(self, betcity_match, whoscored_match=None, **kwargs):
        raise NotImplementedError()
