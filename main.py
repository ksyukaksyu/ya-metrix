from pprint import pprint
from urllib.parse import urlencode
import requests


class OAuth:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Authorization': 'OAuth {}'.format(self.token)}


class Manager(OAuth):
    api_url = 'https://api-metrika.yandex.ru/management/v1/counters'
    params = {
        'search_string': 'ksyukaksyu.github.io'
    }

    def get_counters_list(self):
        response = requests.get(
            self.api_url,
            self.params,
            headers = self.get_headers()
        )
        return response.json()['counters']


class Counter(OAuth):
    url = 'https://api-metrika.yandex.ru/stat/v1/data'

    def __init__(self, token, counter_id):
        self.counter_id = counter_id
        super().__init__(token)

    def get_base_metrics(self, metrics):
        params = {
            'id': self.counter_id,
            'metrics': metrics
        }
        response = requests.get(self.url, params, headers = self.get_headers())
        return response.json()['data'][0]['metrics'][0]


def get_oauth_url(oauth_uri, app_id):
    oauth_params = {
        'response_type': 'token',
        'client_id': app_id
    }
    print('Get your token here: {}'.format('?'.join((oauth_uri, urlencode(oauth_params)))))


def main():
    # Get OAuth token:
    get_oauth_url(OAUTH_URI, APP_ID)

    # Do magic:
    ksyukaksyu = Manager(OAUTH_TOKEN)
    counters = ksyukaksyu.get_counters_list()
    for _ in counters:
        c = Counter(OAUTH_TOKEN, _['id'])
        print('Total visits: {}'.format(c.get_base_metrics('ym:s:visits')))
        print('Total page views: {}'.format(c.get_base_metrics('ym:s:pageviews')))
        print('Total users: {}'.format(c.get_base_metrics('ym:s:users')))


OAUTH_URI = 'https://oauth.yandex.ru/authorize'
APP_ID = 'd301a9dfef2d476a83b6d134306d2291'
OAUTH_TOKEN = 'AQAAAAAFyY7jAATTwOKuJsdhXkYzvXQuomNXVlw'

main()
