"""Shared pytest fixtures will be added here as models and APIs are implemented."""

import pytest

from app import create_app
from app.config import TestConfig
from app.extensions import db


@pytest.fixture()
def app():
    # TODO(Milestones 2-5): add database setup and reusable authenticated-user
    # fixtures once models and protected API endpoints are implemented.
    application = create_app(TestConfig)
    with application.app_context():
        db.create_all()
    yield application
    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
