from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import toml

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_file("config.toml", load=toml.load)
    db.init_app(app)

    from .endpoints import test
    app.register_blueprint(test)

    with app.app_context():
        from .models import message
        db.drop_all()
        db.create_all()

    return app
