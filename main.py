from flask import jsonify, abort, make_response
from services.translate import Translate

translate = Translate()


def entrypoint(request):
    if request.method != 'GET':
        return abort(405)

    request_args = request.args
    if not (request_args and 'q' in request_args and request_args['q'] != ''):
        response = make_response('please specify a \'q\' query param', 400)
        response.mimetype = 'text/plain'
        return response

    queried_text = request_args['q']
    detected_language = translate.detect_language(queried_text)

    return jsonify({
        queried_text: detected_language
    })


if __name__ == '__main__':
    from tests import E2E
    E2E().run()
