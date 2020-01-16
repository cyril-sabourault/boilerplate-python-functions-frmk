import requests as r
from requests.exceptions import RequestException
from datetime import datetime, timedelta


class HTTP():
    def __init__(self):
        self._access_token_info = None

    def _get_access_token(self):
        now = datetime.now()
        if (self._access_token_info is not None and
                self._access_token_info.get('expires_at') < now):
            return self._access_token_info.get('access_token')

        metadata_access_token_route = 'instance/service-accounts/default/token'
        self._access_token_info = self._metadata_server(
            route=metadata_access_token_route)

        expires_in = self._access_token_info.get('expires_in') - 1
        self._access_token_info['expires_at'] = datetime.now() + timedelta(
            seconds=expires_in)

        return self._access_token_info.get('access_token')

    def _metadata_server(self, route):
        base_url = 'http://metadata/computeMetadata/v1/'
        headers = {
            'Metadata-Flavor': 'Google'
        }
        try:
            result = r.get(base_url + route, headers=headers)
            result.raise_for_status()

            return result.json()
        except RequestException as e:
            return e

    def ext_call(self,
                 url, method='GET', data=None, authz_header=True,
                 custom_headers=None, custom_params=None):
        params = {}
        if custom_params is not None:
            params = {k: custom_params[k] for k in custom_params}

        headers = {}
        if custom_headers is not None:
            headers = {k: custom_headers[k] for k in custom_headers}

        access_token = self._get_access_token()
        if authz_header is True:
            headers['Authorization'] = 'Bearer {}'.format(access_token)

        try:
            if method == 'GET':
                result = r.get(url, headers=headers, params=params)
            if method == 'POST':
                result = r.post(url, data=data, headers=headers, params=params)
            result.raise_for_status()

            return result.json()
        except RequestException as e:
            return e
