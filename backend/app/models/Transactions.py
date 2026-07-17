"""Financial transaction model."""

from datetime import datetime, timezone

from app.extensions import db


class Transaction(db.Model):
    """An income or expense stored in exact minor currency units."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False, index=True)
    amount_minor = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(7), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    description = db.Column(db.String(280), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", back_populates="transactions")
    category = db.relationship("Category", back_populates="transactions")

    def to_dict(self):
        return {"id": self.id, "categoryId": self.category_id, "amountMinor": self.amount_minor,
                "type": self.type, "date": self.date.isoformat(), "description": self.description or "",
                "category": self.category.to_dict() if self.category else None}
