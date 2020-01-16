from flask import jsonify, abort
from services.translate import Translate

translate = Translate()


def entrypoint(request):
    if request.method != 'GET':
        return abort(405)

    request_args = request.args
    if request_args and 'q' in request_args:
        queried_text = request_args['q']
    else:
        return abort(400)

    detected_language = translate.detect_language(queried_text)

    return jsonify({
        queried_text: detected_language
    })


if __name__ == '__main__':
    from tests import E2E
    E2E().run()
