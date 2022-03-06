from flask import Flask


def create_app():
    app = Flask(__name__)

    from .test_end_point import test
    app.register_blueprint(test)

    return app