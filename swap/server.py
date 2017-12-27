from __future__ import absolute_import, unicode_literals

import logging

import flask

from swap import handlers  # import error_404, error_405, error_500, root
from swap.restutils import Return, return_error

logger = logging.getLogger()

_app = None


def setup_logging(app):
    logging.basicConfig(level=logging.INFO)


def get_app():
    global _app
    if _app is not None:
        return _app

    app = flask.Flask(__name__)
    app.config['SECRET_KEY'] = '+&zul)of3s6o0=_$8hr=+k!ju^g*r7$rvj^e+49caj)otq'
    # setup_logging(app)

    app.register_error_handler(404, handlers.error_404)
    app.register_error_handler(405, handlers.error_405)
    app.register_error_handler(500, handlers.error_500)
    app.register_error_handler(Return, return_error)

    app.config.update(
        PROPAGATE_EXCEPTIONS=True
    )

    app.add_url_rule('/item/', view_func=handlers.item,
                     methods=['POST', 'GET'])
    app.add_url_rule('/swapping/', view_func=handlers.swapping,
                     methods=['POST'])

    _app = app
    return _app


def wsgi(*args, **kwargs):
    app = get_app()
    return app(*args, **kwargs)
