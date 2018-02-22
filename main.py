from pprint import pprint
from urllib.parse import urlencode
import requests

# get_token
OAUTH_URI = 'https://oauth.yandex.ru/authorize'
APP_ID = 'd301a9dfef2d476a83b6d134306d2291'
oauth_params = {
    'response_type': 'token',
    'client_id': APP_ID
}
print('?'.join((OAUTH_URI, urlencode(oauth_params))))

# get_counters_data
OAUTH_TOKEN = 'AQAAAAAFyY7jAATTwOKuJsdhXkYzvXQuomNXVlw'
params = {
    'oauth_token': OAUTH_TOKEN
}
headers = {
    'Authorization': 'OAuth {}'.format(OAUTH_TOKEN)
}
response = requests.get('https://api-metrika.yandex.ru/management/v1/counters/', params)
pprint(response.headers)
pprint(response.json())
