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

    # Importing the package registers every SQLAlchemy model before migrations run.
    from . import models  # noqa: F401

    from .routes.health import health_bp
    from .routes.auth import auth_bp
    from .routes.budgets import budgets_bp
    from .routes.categories import categories_bp
    from .routes.profile import profile_bp
    from .routes.reports import reports_bp
    from .routes.transactions import transactions_bp

    # TODO(Milestones 2-5): register auth, profile, category, transaction,
    # budget, and report blueprints here as their endpoints are implemented.
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(transactions_bp, url_prefix="/api/transactions")
    app.register_blueprint(budgets_bp, url_prefix="/api/budgets")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")
    return app
