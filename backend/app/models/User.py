"""User model and password helpers."""

from datetime import datetime, timezone

import bcrypt

from app.extensions import db


class User(db.Model):
    """A person who owns every category, transaction, and budget."""

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    default_currency = db.Column(db.String(3), nullable=False, default="USD")
    timezone = db.Column(db.String(64), nullable=False, default="UTC")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    categories = db.relationship("Category", back_populates="user", cascade="all, delete-orphan")
    transactions = db.relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    budgets = db.relationship("Budget", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        """Hash a plaintext password before it is stored."""
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        """Compare a submitted password with its secure stored hash."""
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    def to_dict(self):
        """Return only safe fields that may be sent to the browser."""
        return {
            "id": self.id,
            "displayName": self.display_name,
            "email": self.email,
            "defaultCurrency": self.default_currency,
            "timezone": self.timezone,
        }
