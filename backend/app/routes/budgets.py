"""Monthly expense-budget endpoints."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Budget
from app.schemas.validation import positive_integer, validate_month
from app.services.finance import budget_progress, owned_budget, owned_category
from app.utils.auth import current_user_id
from app.utils.http import error


budgets_bp = Blueprint("budgets", __name__)


@budgets_bp.get("")
@jwt_required()
def list_budgets():
    month, message = validate_month(request.args.get("month"))
    if message:
        return error(message, 422, {"month": message})
    user_id = current_user_id()
    budgets = Budget.query.filter_by(user_id=user_id, month=month).all()
    return jsonify(budgets=[budget_progress(user_id, budget) for budget in budgets])


@budgets_bp.put("")
@jwt_required()
def save_budget():
    """Create or update the one allowed budget for category and month."""
    user_id = current_user_id()
    data = request.get_json(silent=True) or {}
    month, month_error = validate_month(data.get("month"))
    amount, amount_error = positive_integer(data, "amountMinor")
    category_id = data.get("categoryId")
    category = owned_category(user_id, category_id) if isinstance(category_id, int) else None
    fields = {}
    if month_error:
        fields["month"] = month_error
    if amount_error:
        fields["amountMinor"] = amount_error
    if not category or category.type != "expense":
        fields["categoryId"] = "Choose one of your expense categories."
    if fields:
        return error("Validation failed.", 422, fields)
    budget = Budget.query.filter_by(user_id=user_id, category_id=category.id, month=month).first()
    if budget is None:
        budget = Budget(user_id=user_id, category_id=category.id, month=month, amount_minor=amount)
        db.session.add(budget)
    else:
        budget.amount_minor = amount
    db.session.commit()
    return jsonify(budget=budget_progress(user_id, budget)), 201


@budgets_bp.delete("/<int:budget_id>")
@jwt_required()
def delete_budget(budget_id):
    budget = owned_budget(current_user_id(), budget_id)
    if not budget:
        return error("Budget not found.", 404)
    db.session.delete(budget)
    db.session.commit()
    return "", 204
