"""Personal income and expense categories."""

from app.extensions import db


class Category(db.Model):
    """A user-owned label that defines whether money is income or expense."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(7), nullable=False)
    color = db.Column(db.String(7), nullable=True)
    icon = db.Column(db.String(40), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    __table_args__ = (db.UniqueConstraint("user_id", "name", "type", name="uq_category_user_name_type"),)

    user = db.relationship("User", back_populates="categories")
    transactions = db.relationship("Transaction", back_populates="category")
    budgets = db.relationship("Budget", back_populates="category")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "type": self.type, "color": self.color,
                "icon": self.icon, "isActive": self.is_active}
