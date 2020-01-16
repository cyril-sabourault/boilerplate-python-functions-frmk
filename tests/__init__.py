class E2E():
    def __init__(self):
        pass

    def run(self):
        print('Launching tests:')
        self._test_HTTP()
        self._test_Translate()

    def _test_HTTP(self):
        print('- [HTTP]:')
        from services.http import HTTP
        http = HTTP()

        tokeninfo_url = 'https://oauth2.googleapis.com/tokeninfo'
        custom_params = {
            'access_token': http._get_access_token()
        }
        tokeninfo_url = http.ext_call(
            url=tokeninfo_url, custom_params=custom_params)
        print(tokeninfo_url.get('email'))

    def _test_Translate(self):
        print('- [TRANSLATE]:')
        from services.translate import Translate
        translate = Translate()

        fr_data = 'Cette phrase est en francais.'
        en_data = 'This sentence is exclusively written with english words.'
        mixed_fr_en_data = ('J\'ai book un low-cost'
                            'pour le road-trip du week-end.')

        print(
            [translate.detect_language(data) for data in [
                fr_data, en_data, mixed_fr_en_data]])
