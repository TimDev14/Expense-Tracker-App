"""Configuration objects for development, test, and deployed environments."""

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    # TODO(Milestone 6): require environment-provided secrets outside local
    # development instead of relying on these development-only fallbacks.
    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-secret-change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "development-jwt-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'expense_tracker.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")


class TestConfig(Config):
    # TODO(Milestones 2-5): add test-specific settings as protected endpoints
    # and database-backed features are introduced.
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    JWT_SECRET_KEY = "test-jwt-secret-that-is-long-enough-for-hmac-sha256"
