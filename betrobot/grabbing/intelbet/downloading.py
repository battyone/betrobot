from betrobot.util.requests_util import requests_get


def intelbet_get(*args, **kwargs):
    response = requests_get('www.intelbet.ru', *args, **kwargs)
    if response is None:
        return None

    return response.text
