"""Owned category CRUD endpoints."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Category
from app.schemas.validation import optional_string, required_string
from app.services.finance import owned_category
from app.utils.auth import current_user_id
from app.utils.http import error


categories_bp = Blueprint("categories", __name__)


def category_payload(data, partial=False):
    """Validate category fields before a write reaches the database."""
    fields = {}
    name = None
    if not partial or "name" in data:
        name, message = required_string(data, "name", maximum=80)
        if message:
            fields["name"] = message
    category_type = data.get("type")
    if not partial or "type" in data:
        if category_type not in {"income", "expense"}:
            fields["type"] = "type must be income or expense."
    color, color_error = optional_string(data, "color", 7)
    icon, icon_error = optional_string(data, "icon", 40)
    if color_error:
        fields["color"] = color_error
    if icon_error:
        fields["icon"] = icon_error
    return name, category_type, color, icon, fields


@categories_bp.get("")
@jwt_required()
def list_categories():
    user_id = current_user_id()
    include_archived = request.args.get("includeArchived") == "true"
    query = Category.query.filter_by(user_id=user_id)
    if not include_archived:
        query = query.filter_by(is_active=True)
    return jsonify(categories=[item.to_dict() for item in query.order_by(Category.name).all()])


@categories_bp.post("")
@jwt_required()
def create_category():
    data = request.get_json(silent=True) or {}
    name, category_type, color, icon, fields = category_payload(data)
    if fields:
        return error("Validation failed.", 422, fields)
    category = Category(user_id=current_user_id(), name=name, type=category_type, color=color, icon=icon)
    db.session.add(category)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return error("A category with that name and type already exists.", 409)
    return jsonify(category=category.to_dict()), 201


@categories_bp.patch("/<int:category_id>")
@jwt_required()
def update_category(category_id):
    category = owned_category(current_user_id(), category_id)
    if not category:
        return error("Category not found.", 404)
    data = request.get_json(silent=True) or {}
    name, category_type, color, icon, fields = category_payload(data, partial=True)
    if fields:
        return error("Validation failed.", 422, fields)
    if name is not None:
        category.name = name
    if category_type is not None:
        category.type = category_type
    if color is not None:
        category.color = color
    if icon is not None:
        category.icon = icon
    if "isActive" in data:
        category.is_active = bool(data["isActive"])
    db.session.commit()
    return jsonify(category=category.to_dict())


@categories_bp.delete("/<int:category_id>")
@jwt_required()
def delete_category(category_id):
    category = owned_category(current_user_id(), category_id)
    if not category:
        return error("Category not found.", 404)
    if category.transactions:
        return error("Archive a category that has transaction history instead of deleting it.", 409)
    db.session.delete(category)
    db.session.commit()
    return "", 204
