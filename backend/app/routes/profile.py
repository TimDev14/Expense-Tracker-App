"""Current-user profile endpoint."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import User
from app.schemas.validation import optional_string
from app.utils.auth import current_user_id
from app.utils.http import error


profile_bp = Blueprint("profile", __name__)


@profile_bp.patch("")
@jwt_required()
def update_profile():
    """Allow a user to update only their own presentation preferences."""
    data = request.get_json(silent=True) or {}
    user = db.session.get(User, current_user_id())
    display_name, name_error = optional_string(data, "displayName", 80)
    timezone, timezone_error = optional_string(data, "timezone", 64)
    currency, currency_error = optional_string(data, "defaultCurrency", 3)
    fields = {key: value for key, value in {"displayName": name_error, "timezone": timezone_error,
                                             "defaultCurrency": currency_error}.items() if value}
    if fields:
        return error("Validation failed.", 422, fields)
    if display_name is not None:
        user.display_name = display_name
    if timezone is not None:
        user.timezone = timezone
    if currency is not None:
        user.default_currency = currency.upper()
    db.session.commit()
    return jsonify(user=user.to_dict())
