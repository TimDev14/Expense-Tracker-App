"""Owned transaction CRUD with month and category filters."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Transaction
from app.schemas.validation import optional_string, positive_integer, validate_date, validate_month
from app.services.finance import month_dates, owned_category, owned_transaction
from app.utils.auth import current_user_id
from app.utils.http import error


transactions_bp = Blueprint("transactions", __name__)


def transaction_payload(data, partial=False):
    """Validate money, dates, type, and category before an owned write."""
    fields = {}
    amount = parsed_date = description = category_id = transaction_type = None
    if not partial or "amountMinor" in data:
        amount, message = positive_integer(data, "amountMinor")
        if message:
            fields["amountMinor"] = message
    if not partial or "date" in data:
        parsed_date, message = validate_date(data.get("date"))
        if message:
            fields["date"] = message
    if not partial or "type" in data:
        transaction_type = data.get("type")
        if transaction_type not in {"income", "expense"}:
            fields["type"] = "type must be income or expense."
    if not partial or "categoryId" in data:
        category_id = data.get("categoryId")
        if isinstance(category_id, bool) or not isinstance(category_id, int):
            fields["categoryId"] = "categoryId must be an integer."
    if not partial or "description" in data:
        description, message = optional_string(data, "description", 280)
        if message:
            fields["description"] = message
    return amount, parsed_date, transaction_type, category_id, description, fields


@transactions_bp.get("")
@jwt_required()
def list_transactions():
    user_id = current_user_id()
    query = Transaction.query.filter_by(user_id=user_id)
    month = request.args.get("month")
    if month:
        month, message = validate_month(month)
        if message:
            return error(message, 422, {"month": message})
        start, end = month_dates(month)
        query = query.filter(Transaction.date.between(start, end))
    if request.args.get("categoryId"):
        query = query.filter_by(category_id=request.args.get("categoryId", type=int))
    if request.args.get("type") in {"income", "expense"}:
        query = query.filter_by(type=request.args["type"])
    return jsonify(transactions=[item.to_dict() for item in query.order_by(Transaction.date.desc(), Transaction.id.desc()).all()])


@transactions_bp.post("")
@jwt_required()
def create_transaction():
    user_id = current_user_id()
    data = request.get_json(silent=True) or {}
    amount, transaction_date, transaction_type, category_id, description, fields = transaction_payload(data)
    category = owned_category(user_id, category_id) if category_id else None
    if category and category.type != transaction_type:
        fields["type"] = "Transaction type must match the category type."
    if not category and category_id:
        fields["categoryId"] = "Choose one of your own categories."
    if fields:
        return error("Validation failed.", 422, fields)
    transaction = Transaction(user_id=user_id, category_id=category.id, amount_minor=amount, type=transaction_type,
                              date=transaction_date, description=description)
    db.session.add(transaction)
    db.session.commit()
    return jsonify(transaction=transaction.to_dict()), 201


@transactions_bp.patch("/<int:transaction_id>")
@jwt_required()
def update_transaction(transaction_id):
    user_id = current_user_id()
    transaction = owned_transaction(user_id, transaction_id)
    if not transaction:
        return error("Transaction not found.", 404)
    data = request.get_json(silent=True) or {}
    amount, transaction_date, transaction_type, category_id, description, fields = transaction_payload(data, partial=True)
    category = owned_category(user_id, category_id) if category_id else transaction.category
    final_type = transaction_type or transaction.type
    if category and category.type != final_type:
        fields["type"] = "Transaction type must match the category type."
    if category_id and not category:
        fields["categoryId"] = "Choose one of your own categories."
    if fields:
        return error("Validation failed.", 422, fields)
    for attribute, value in {"amount_minor": amount, "date": transaction_date, "type": transaction_type,
                             "category_id": category_id, "description": description}.items():
        if value is not None:
            setattr(transaction, attribute, value)
    db.session.commit()
    return jsonify(transaction=transaction.to_dict())


@transactions_bp.delete("/<int:transaction_id>")
@jwt_required()
def delete_transaction(transaction_id):
    transaction = owned_transaction(current_user_id(), transaction_id)
    if not transaction:
        return error("Transaction not found.", 404)
    db.session.delete(transaction)
    db.session.commit()
    return "", 204
