"""Monthly category budget model."""

from app.extensions import db


class Budget(db.Model):
    """An expense limit for one category during one calendar month."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False, index=True)
    month = db.Column(db.String(7), nullable=False)
    amount_minor = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.UniqueConstraint("user_id", "category_id", "month", name="uq_budget_user_category_month"),)

    user = db.relationship("User", back_populates="budgets")
    category = db.relationship("Category", back_populates="budgets")

    def to_dict(self):
        return {"id": self.id, "categoryId": self.category_id, "month": self.month,
                "amountMinor": self.amount_minor, "category": self.category.to_dict() if self.category else None}
