"""Shared pytest fixtures will be added here as models and APIs are implemented."""

import pytest

from app import create_app
from app.config import TestConfig


@pytest.fixture()
def app():
    application = create_app(TestConfig)
    yield application
