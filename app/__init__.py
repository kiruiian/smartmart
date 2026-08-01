from flask import Flask

from .extensions import db, migrate


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app