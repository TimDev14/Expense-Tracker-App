"""Application factory for the Personal Expense Tracker API."""

from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from .config import Config
from .extensions import db, jwt, migrate


def create_app(config_object=Config):
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    CORS(app, resources={r"/api/*": {"origins": app.config["FRONTEND_ORIGIN"]}})
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from .routes.health import health_bp

    app.register_blueprint(health_bp, url_prefix="/api")
    return app
