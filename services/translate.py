from services.http import HTTP
from utils import Config


class Translate():
    def __init__(self,
                 http=None):
        self.http = http if http is not None else HTTP()
        self._config = Config(config_path='config.yaml')
        self._api_key = self._config.get('translate.api_key')
        self._translate_url = 'https://translation.googleapis.com/'

    def detect_language(self, data):
        detect_translate_route = 'language/translate/v2/detect'
        custom_params = {
            'key': self._api_key,
            'q': data
        }
        detect = self.http.ext_call(
            url=self._translate_url + detect_translate_route,
            method='POST',
            authz_header=False,
            custom_params=custom_params)

        return detect.get(
            'data', {}).get(
                'detections', [])[0][0].get(
                    'language', '')
