"""Authentication helpers shared by protected endpoints."""

from flask_jwt_extended import get_jwt_identity


def current_user_id():
    """JWT identities are stored as strings, so convert them at one boundary."""
    return int(get_jwt_identity())
