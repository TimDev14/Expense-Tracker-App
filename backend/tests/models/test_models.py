"""Model behavior that does not require an HTTP request."""

from app.models import User


def test_user_password_is_hashed_and_can_be_checked(app):
    with app.app_context():
        user = User(display_name="A", email="model@example.test")
        user.set_password("safe-password")
        assert user.password_hash != "safe-password"
        assert user.check_password("safe-password")
        assert not user.check_password("wrong-password")
