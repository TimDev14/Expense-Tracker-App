"""Owned-record lookups and exact monthly financial calculations."""

from calendar import monthrange
from datetime import date

from app.models import Budget, Category, Transaction


def month_dates(month):
    """Translate a YYYY-MM filter into inclusive start and end dates."""
    year, month_number = map(int, month.split("-"))
    return date(year, month_number, 1), date(year, month_number, monthrange(year, month_number)[1])


def owned_category(user_id, category_id):
    return Category.query.filter_by(id=category_id, user_id=user_id).first()


def owned_transaction(user_id, transaction_id):
    return Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()


def owned_budget(user_id, budget_id):
    return Budget.query.filter_by(id=budget_id, user_id=user_id).first()


def month_transactions(user_id, month):
    start, end = month_dates(month)
    return Transaction.query.filter(
        Transaction.user_id == user_id, Transaction.date.between(start, end)
    )


def overview(user_id, month):
    """Calculate server-trusted totals from the user's owned transaction rows."""
    records = month_transactions(user_id, month).order_by(Transaction.date.desc(), Transaction.id.desc()).all()
    income = sum(item.amount_minor for item in records if item.type == "income")
    expenses = sum(item.amount_minor for item in records if item.type == "expense")
    return {"month": month, "incomeMinor": income, "expenseMinor": expenses,
            "balanceMinor": income - expenses, "recentTransactions": [item.to_dict() for item in records[:5]]}


def budget_progress(user_id, budget):
    """Derive progress from matching expense transactions, never browser totals."""
    spent = sum(item.amount_minor for item in month_transactions(user_id, budget.month).filter_by(
        category_id=budget.category_id, type="expense"
    ).all())
    remaining = budget.amount_minor - spent
    status = "over" if remaining < 0 else "at_limit" if remaining == 0 else "on_track"
    return {**budget.to_dict(), "spentMinor": spent, "remainingMinor": remaining, "status": status}
