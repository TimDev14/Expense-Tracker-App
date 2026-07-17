"""Flask extensions, initialized without binding them to an app yet."""

from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# TODO(Milestone 3): import models before generating migrations so SQLAlchemy
# can discover the User, Category, Transaction, and Budget tables.
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
