import functools

import os
from flask import Flask
from serverai import api


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='namdz',
    )

    # if test_config is None:
    #     app.config.from_pyfile('config_const.py', silent=True)
    # else:
    #     app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World'
    app.register_blueprint(api.bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=1999, debug=True)