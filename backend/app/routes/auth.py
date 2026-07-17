"""Registration, sign-in, and current-user endpoints."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required

from app.extensions import db
from app.models import User
from app.schemas.validation import EMAIL_PATTERN, required_string
from app.utils.auth import current_user_id
from app.utils.http import error


auth_bp = Blueprint("auth", __name__)


def credentials(data, registering=False):
    email, email_error = required_string(data, "email", maximum=255)
    password, password_error = required_string(data, "password", minimum=8, maximum=128)
    fields = {}
    if email_error or not EMAIL_PATTERN.fullmatch(email or ""):
        fields["email"] = "Enter a valid email address."
    if password_error:
        fields["password"] = "Password must contain at least 8 characters."
    display_name = None
    if registering:
        display_name, name_error = required_string(data, "displayName", maximum=80)
        if name_error:
            fields["displayName"] = name_error
    return email.lower() if email else None, password, display_name, fields


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email, password, display_name, fields = credentials(data, registering=True)
    if fields:
        return error("Validation failed.", 422, fields)
    if User.query.filter_by(email=email).first():
        return error("An account with that email already exists.", 409, {"email": "Email is already registered."})
    user = User(display_name=display_name, email=email,
                default_currency=data.get("defaultCurrency", "USD"), timezone=data.get("timezone", "UTC"))
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user=user.to_dict(), accessToken=create_access_token(identity=str(user.id))), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email, password, _, fields = credentials(data)
    if fields:
        return error("Validation failed.", 422, fields)
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return error("Email or password is incorrect.", 401)
    return jsonify(user=user.to_dict(), accessToken=create_access_token(identity=str(user.id)))


@auth_bp.get("/me")
@jwt_required()
def me():
    user = db.session.get(User, current_user_id())
    return jsonify(user=user.to_dict())
