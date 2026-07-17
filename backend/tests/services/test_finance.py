"""Exact financial calculation tests."""

from app.services.finance import overview
from app.extensions import db
from app.models import Category, Transaction, User
from datetime import date


def test_overview_uses_integer_minor_units(app):
    with app.app_context():
        user = User(display_name="A", email="finance@example.test"); user.set_password("safe-password")
        category = Category(user=user, name="Pay", type="income")
        expense = Category(user=user, name="Food", type="expense")
        db.session.add_all([user, category, expense]); db.session.flush()
        db.session.add_all([Transaction(user=user, category=category, amount_minor=2000, type="income", date=date(2026, 1, 1)), Transaction(user=user, category=expense, amount_minor=1250, type="expense", date=date(2026, 1, 2))]); db.session.commit()
        assert overview(user.id, "2026-01")["balanceMinor"] == 750
