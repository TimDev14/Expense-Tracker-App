"""Monthly overview and category-breakdown endpoints."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.schemas.validation import validate_month
from app.services.finance import month_transactions, overview
from app.utils.auth import current_user_id
from app.utils.http import error


reports_bp = Blueprint("reports", __name__)


def requested_month():
    month, message = validate_month(request.args.get("month"))
    return month, error(message, 422, {"month": message}) if message else None


@reports_bp.get("/overview")
@jwt_required()
def monthly_overview():
    month, problem = requested_month()
    if problem:
        return problem
    return jsonify(overview=overview(current_user_id(), month))


@reports_bp.get("/category-breakdown")
@jwt_required()
def category_breakdown():
    month, problem = requested_month()
    if problem:
        return problem
    user_id = current_user_id()
    totals = {}
    for transaction in month_transactions(user_id, month).filter_by(type="expense").all():
        category = transaction.category
        totals.setdefault(category.id, {"categoryId": category.id, "name": category.name,
                                       "color": category.color, "amountMinor": 0})
        totals[category.id]["amountMinor"] += transaction.amount_minor
    return jsonify(month=month, categories=sorted(totals.values(), key=lambda item: item["amountMinor"], reverse=True))
